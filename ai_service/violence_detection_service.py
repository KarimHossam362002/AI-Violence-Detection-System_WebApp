import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from threading import Thread, Lock  # Added for thread safety

import cv2
import numpy as np
import requests
import tensorflow as tf
from flask import Flask, Response, jsonify
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = Path(
    os.getenv(
        "VIOLENCE_MODEL_PATH",
        BASE_DIR / "storage" / "app" / "models" / "violence" / "cctvmodel_advanced.keras",
    )
)
VIDEO_OUTPUT_DIR = BASE_DIR / "storage" / "app" / "public" / "incidents" / "videos"
SNAPSHOT_OUTPUT_DIR = BASE_DIR / "storage" / "app" / "public" / "incidents" / "snapshots"

LARAVEL_INCIDENT_API = os.getenv("LARAVEL_INCIDENT_API", "http://127.0.0.1:8000/api/incidents")
INFERENCE_API_TOKEN = os.getenv("INFERENCE_API_TOKEN", "")

CAMERA_ID = os.getenv("CAMERA_ID", "LAPTOP_CAM")
DISTRICT = os.getenv("CAMERA_DISTRICT", "Local Test")
CAMERA_SOURCE = os.getenv("VIOLENCE_CAMERA_SOURCE", os.getenv("CAMERA_SOURCE", "0"))

IMG_SIZE = 224
CHANNELS = 3
FRAME_COUNT = 20
THRESHOLD = 0.8
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 20
RECORD_SECONDS_AFTER_LAST_DETECTION = 5

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

print("Loading violence detection models...")
print(f"Violence model: {MODEL_PATH}")

extractor = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    input_shape=(IMG_SIZE, IMG_SIZE, CHANNELS),
)
model = tf.keras.models.load_model(MODEL_PATH)

# ---------------------------------------------------------------------------
# Threaded Camera Reader (Fixes Buffer Accumulation)
# ---------------------------------------------------------------------------
class CameraStream:
    def __init__(self, src=0):
        self.src = src
        self.last_error = ""
        self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.stream.set(cv2.CAP_PROP_FPS, FPS)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        (self.grabbed, self.frame) = self.stream.read()
        if not self.stream.isOpened() or not self.grabbed:
            self.last_error = (
                f"Could not read camera source {src}. "
                "Close other camera apps/services or use a different camera source."
            )
            print(self.last_error, flush=True)
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
                self.last_error = f"Camera source {self.src} stopped returning frames."
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
        if hasattr(self, "thread") and self.thread.is_alive():
            self.thread.join()
        self.stream.release()

# Initialize and start threaded camera
def parse_camera_source(value):
    return int(value) if str(value).isdigit() else value


camera = CameraStream(parse_camera_source(CAMERA_SOURCE)).start()

analysis_enabled = False
frame_buffer = []
last_label = ""
last_confidence = 0.0

recording = {
    "writer": None,
    "clip_path": None,
    "snapshot_path": None,
    "last_detection_at": 0.0,
    "best_confidence": 0.0,
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
    return datetime.now().strftime("violence_%Y%m%d_%H%M%S")


def start_recording(frame, confidence: float) -> None:
    incident_name = build_incident_name()
    clip_path = VIDEO_OUTPUT_DIR / f"{incident_name}.mp4"
    snapshot_path = SNAPSHOT_OUTPUT_DIR / f"{incident_name}.jpg"

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(clip_path), fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))

    cv2.imwrite(str(snapshot_path), frame)

    recording.update(
        {
            "writer": writer,
            "clip_path": clip_path,
            "snapshot_path": snapshot_path,
            "last_detection_at": time.time(),
            "best_confidence": confidence,
        }
    )


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
    confidence = round(float(recording["best_confidence"]), 4)

    payload = {
        "camera_id": CAMERA_ID,
        "district": DISTRICT,
        "event_type": "Violence Detected",
        "confidence": confidence,
        "violence_score": confidence,
        "weapon_detected": False,
        "alert_level": "high",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "snapshot_url": public_url_for(snapshot_path),
        "clip_path": public_url_for(clip_path),
    }

    headers = {"Accept": "application/json"}
    if INFERENCE_API_TOKEN:
        headers["X-Inference-Token"] = INFERENCE_API_TOKEN

    try:
        response = requests.post(LARAVEL_INCIDENT_API, json=payload, headers=headers, timeout=5)
        print(f"Violence incident sent to Laravel: {response.status_code}")
    except requests.RequestException as exc:
        print(f"Could not send violence incident to Laravel: {exc}")

    recording.update(
        {
            "writer": None,
            "clip_path": None,
            "snapshot_path": None,
            "last_detection_at": 0.0,
            "best_confidence": 0.0,
        }
    )


# ---------------------------------------------------------------------------
# Detection and streaming
# ---------------------------------------------------------------------------
def predict_violence(frames):
    processed = np.array(
        [
            preprocess_input(cv2.resize(f, (IMG_SIZE, IMG_SIZE)).astype(np.float32))
            for f in frames
        ]
    )
    features = extractor.predict(processed, verbose=0)
    probability = float(model.predict(np.expand_dims(features, axis=0), verbose=0)[0][0])
    return probability


def draw_overlay(frame, label, confidence, collecting_count):
    if label:
        color = (0, 0, 220) if label == "Violence" else (0, 200, 0)
        cv2.putText(frame, label, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3, cv2.LINE_AA)
        cv2.putText(
            frame,
            f"Confidence: {confidence * 100:.1f}%",
            (20, 78),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (230, 230, 230),
            2,
            cv2.LINE_AA,
        )

    if collecting_count:
        cv2.putText(
            frame,
            f"Collecting {collecting_count}/{FRAME_COUNT}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (180, 180, 180),
            2,
            cv2.LINE_AA,
        )


def unavailable_camera_frame(message):
    frame = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
    lines = [
        "Violence stream waiting",
        message or "Camera is not returning frames.",
        "Stop the other model or choose another source.",
    ]
    for index, line in enumerate(lines):
        cv2.putText(
            frame,
            line,
            (20, 70 + index * 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (230, 230, 230),
            2,
            cv2.LINE_AA,
        )
    return frame


def generate_frames():
    global frame_buffer, last_label, last_confidence

    while True:
        success, frame = camera.read()
        if not success or frame is None:
            display_frame = unavailable_camera_frame(camera.last_error)
            time.sleep(0.2)
        else:
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            display_frame = frame.copy()

        if success and frame is not None and analysis_enabled:
            frame_buffer.append(frame.copy())

            if len(frame_buffer) == FRAME_COUNT:
                # Predict on the collected frames
                probability = predict_violence(frame_buffer)
                last_confidence = probability
                last_label = "Violence" if probability >= THRESHOLD else "Normal"
                frame_buffer = []

                if last_label == "Violence":
                    if recording["writer"] is None:
                        start_recording(display_frame, probability)

                    recording["last_detection_at"] = time.time()
                    recording["best_confidence"] = max(recording["best_confidence"], probability)

            draw_overlay(display_frame, last_label, last_confidence, len(frame_buffer))

            if recording["writer"] is not None:
                write_recording_frame(display_frame)

                seconds_since_detection = time.time() - recording["last_detection_at"]
                if seconds_since_detection >= RECORD_SECONDS_AFTER_LAST_DETECTION:
                    stop_recording_and_report()
        else:
            cv2.putText(
                display_frame,
                "Analysis Paused",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

        # Optimization: Lower JPEG quality slightly to 80 to reduce network payload
        ok, buffer = cv2.imencode(".jpg", display_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ok:
            continue

        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"


@app.get("/stream")
def stream():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.post("/start")
def start_analysis():
    global analysis_enabled, frame_buffer, last_label, last_confidence
    analysis_enabled = True
    frame_buffer = []
    last_label = ""
    last_confidence = 0.0
    return jsonify({"tracking": analysis_enabled, "mode": "violence"})


@app.post("/stop")
def stop_analysis():
    global analysis_enabled, frame_buffer, last_label, last_confidence
    analysis_enabled = False
    frame_buffer = []
    last_label = ""
    last_confidence = 0.0
    stop_recording_and_report()
    return jsonify({"tracking": analysis_enabled, "mode": "violence"})


@app.get("/status")
def status():
    return jsonify(
        {
            "camera_id": CAMERA_ID,
            "camera_opened": bool(camera.stream.isOpened() and camera.grabbed),
            "camera_source": CAMERA_SOURCE,
            "camera_error": camera.last_error,
            "district": DISTRICT,
            "tracking": analysis_enabled,
            "recording": recording["writer"] is not None,
            "stream_url": "http://127.0.0.1:5001/stream",
            "mode": "violence",
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, threaded=True)
