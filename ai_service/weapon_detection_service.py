import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from threading import Thread, Lock  # Added for thread-safe frame reading

import cv2
import requests
import torch
from flask import Flask, Response, jsonify

BASE_DIR = Path(__file__).resolve().parents[1]
os.environ.setdefault("YOLO_CONFIG_DIR", str(BASE_DIR / ".ultralytics"))

from ultralytics import YOLO

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL_PATH = Path(
    os.getenv(
        "WEAPON_MODEL_PATH",
        BASE_DIR / "storage" / "app" / "models" / "weapon" / "weapon_detection_yolov11m.pt",
    )
)
VIDEO_OUTPUT_DIR = BASE_DIR / "storage" / "app" / "public" / "incidents" / "videos"
SNAPSHOT_OUTPUT_DIR = BASE_DIR / "storage" / "app" / "public" / "incidents" / "snapshots"

LARAVEL_INCIDENT_API = os.getenv("LARAVEL_INCIDENT_API", "http://127.0.0.1:8000/api/incidents")
INFERENCE_API_TOKEN = os.getenv("INFERENCE_API_TOKEN", "")

CAMERA_ID = os.getenv("CAMERA_ID", "LAPTOP_CAM")
DISTRICT = os.getenv("CAMERA_DISTRICT", "Local Test")

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 20
CONFIDENCE_THRESHOLD = float(os.getenv("WEAPON_CONFIDENCE_THRESHOLD", "0.65"))
DETECTION_HITS_TO_START = int(os.getenv("WEAPON_DETECTION_HITS_TO_START", "2"))
SNAPSHOT_CONFIDENCE_DELTA = float(os.getenv("WEAPON_SNAPSHOT_CONFIDENCE_DELTA", "0.02"))
RECORD_SECONDS_AFTER_LAST_DETECTION = float(os.getenv("WEAPON_RECORD_SECONDS_AFTER_LAST_DETECTION", "2"))

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
app = Flask(__name__)

@app.after_request
def add_local_dashboard_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8000"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

VIDEO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SNAPSHOT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

device = 0 if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
print(f"Loading weapon model: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))
model.fuse()
FIREARM_CLASS_IDS = [
    class_id
    for class_id, name in model.names.items()
    if "firearm" in str(name).lower()
]
print(f"Firearm class ids: {FIREARM_CLASS_IDS}", flush=True)

# ---------------------------------------------------------------------------
# Threaded Camera Reader (Stops buffer accumulation)
# ---------------------------------------------------------------------------
class CameraStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.stream.set(cv2.CAP_PROP_FPS, FPS)
        # Minimize backend buffering
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            return self
        self.started = True
        self.thread = Thread(target=self.update, args=(), daemon=True)
        self.thread.start()
        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            if not grabbed:
                self.started = False
                break
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            frame_to_return = self.frame.copy() if self.frame is not None else None
            grabbed_to_return = self.grabbed
        return grabbed_to_return, frame_to_return

    def stop(self):
        self.started = False
        if self.thread.is_alive():
            self.thread.join()
        self.stream.release()

# Initialize threaded camera
camera = CameraStream(0).start()

tracking_enabled = False
consecutive_firearm_hits = 0
recording = {
    "writer": None,
    "clip_path": None,
    "snapshot_path": None,
    "last_detection_at": 0.0,
    "best_confidence": 0.0,
    "best_label": None,
}

# ---------------------------------------------------------------------------
# Recording helpers
# ---------------------------------------------------------------------------
def public_url_for(path: Path) -> str:
    relative = path.relative_to(BASE_DIR / "storage" / "app" / "public").as_posix()
    return f"/storage/{relative}"


def make_browser_playable_clip(path: Path) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg or not path.exists():
        if not ffmpeg:
            print("ffmpeg was not found; clip was saved with OpenCV's default mp4v codec.", flush=True)
        return path

    converted_path = path.with_name(f"{path.stem}_h264{path.suffix}")
    command = [
        ffmpeg,
        "-y",
        "-i",
        str(path),
        "-vcodec",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-an",
        str(converted_path),
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        converted_path.replace(path)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Could not convert clip to browser-compatible H.264: {exc}", flush=True)

    return path


def build_incident_name() -> str:
    return datetime.now().strftime("weapon_%Y%m%d_%H%M%S")


def save_best_snapshot(frame, confidence: float, label: str) -> None:
    snapshot_path = recording["snapshot_path"]
    if snapshot_path is None:
        return

    previous_best = float(recording["best_confidence"])
    if confidence < previous_best + SNAPSHOT_CONFIDENCE_DELTA:
        return

    cv2.imwrite(str(snapshot_path), frame)
    recording["best_confidence"] = confidence
    recording["best_label"] = label


def start_recording(frame, confidence: float, label: str) -> None:
    incident_name = build_incident_name()
    clip_path = VIDEO_OUTPUT_DIR / f"{incident_name}.mp4"
    snapshot_path = SNAPSHOT_OUTPUT_DIR / f"{incident_name}.jpg"

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(clip_path), fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))

    recording.update(
        {
            "writer": writer,
            "clip_path": clip_path,
            "snapshot_path": snapshot_path,
            "last_detection_at": time.time(),
            "best_confidence": 0.0,
            "best_label": None,
        }
    )
    save_best_snapshot(frame, confidence, label)


def write_recording_frame(frame) -> None:
    writer = recording["writer"]
    if writer is not None:
        writer.write(frame)


def stop_recording_and_report() -> None:
    writer = recording["writer"]
    if writer is None:
        return

    writer.release()

    clip_path = recording["clip_path"]
    snapshot_path = recording["snapshot_path"]
    clip_path = make_browser_playable_clip(clip_path)

    payload = {
        "camera_id": CAMERA_ID,
        "district": DISTRICT,
        "event_type": "Weapon Detected",
        "confidence": round(float(recording["best_confidence"]), 4),
        "weapon_detected": True,
        "alert_level": "critical",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "snapshot_url": public_url_for(snapshot_path),
        "clip_path": public_url_for(clip_path),
    }

    headers = {"Accept": "application/json"}
    if INFERENCE_API_TOKEN:
        headers["X-Inference-Token"] = INFERENCE_API_TOKEN

    try:
        response = requests.post(LARAVEL_INCIDENT_API, json=payload, headers=headers, timeout=5)
        print(f"Incident sent to Laravel: {response.status_code}")
    except requests.RequestException as exc:
        print(f"Could not send incident to Laravel: {exc}")

    recording.update(
        {
            "writer": None,
            "clip_path": None,
            "snapshot_path": None,
            "last_detection_at": 0.0,
            "best_confidence": 0.0,
            "best_label": None,
        }
    )


# ---------------------------------------------------------------------------
# Detection and streaming
# ---------------------------------------------------------------------------
def detect_weapon(frame):
    # Pass verbose=False to keep the console clean
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=CONFIDENCE_THRESHOLD,
        classes=FIREARM_CLASS_IDS or None,
        device=device,
        verbose=False,
    )

    result = results[0]
    annotated_frame = result.plot()

    best_confidence = 0.0
    best_label = None
    if (
        result.boxes is not None
        and result.boxes.conf is not None
        and result.boxes.cls is not None
        and len(result.boxes.conf) > 0
    ):
        best_index = int(result.boxes.conf.argmax().item())
        best_confidence = float(result.boxes.conf[best_index].item())
        best_class_id = int(result.boxes.cls[best_index].item())
        best_label = model.names.get(best_class_id, str(best_class_id))

    weapon_detected = best_confidence >= CONFIDENCE_THRESHOLD
    return annotated_frame, weapon_detected, best_confidence, best_label


def generate_frames():
    global tracking_enabled, consecutive_firearm_hits

    while True:
        success, frame = camera.read()
        if not success or frame is None:
            time.sleep(0.01)  # Brief pause if the camera hasn't grabbed a frame yet
            continue

        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        display_frame = frame.copy()

        if tracking_enabled:
            display_frame, weapon_detected, confidence, label = detect_weapon(frame)

            if weapon_detected:
                consecutive_firearm_hits += 1

                if recording["writer"] is None and consecutive_firearm_hits >= DETECTION_HITS_TO_START:
                    start_recording(display_frame, confidence, label or "firearms")

                recording["last_detection_at"] = time.time()
                save_best_snapshot(display_frame, confidence, label or "firearms")
            else:
                consecutive_firearm_hits = 0

            if recording["writer"] is not None:
                write_recording_frame(display_frame)

                seconds_since_detection = time.time() - recording["last_detection_at"]
                if seconds_since_detection >= RECORD_SECONDS_AFTER_LAST_DETECTION:
                    stop_recording_and_report()
        else:
            cv2.putText(
                display_frame,
                "Tracking Paused",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

        ok, buffer = cv2.imencode(".jpg", display_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ok:
            continue

        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"


@app.get("/stream")
def stream():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.post("/start")
def start_tracking():
    global tracking_enabled
    tracking_enabled = True
    return jsonify({"tracking": tracking_enabled})


@app.post("/stop")
def stop_tracking():
    global tracking_enabled, consecutive_firearm_hits
    tracking_enabled = False
    consecutive_firearm_hits = 0
    stop_recording_and_report()
    return jsonify({"tracking": tracking_enabled})


@app.get("/status")
def status():
    return jsonify(
        {
            "camera_id": CAMERA_ID,
            "district": DISTRICT,
            "tracking": tracking_enabled,
            "recording": recording["writer"] is not None,
            "confidence_threshold": CONFIDENCE_THRESHOLD,
            "detection_hits_to_start": DETECTION_HITS_TO_START,
            "record_seconds_after_last_detection": RECORD_SECONDS_AFTER_LAST_DETECTION,
            "firearm_class_ids": FIREARM_CLASS_IDS,
            "best_confidence": recording["best_confidence"],
            "best_label": recording["best_label"],
            "stream_url": "http://127.0.0.1:5000/stream",
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True)
