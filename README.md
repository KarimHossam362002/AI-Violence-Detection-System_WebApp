# AI Violence Detection System

Laravel + React web dashboard for monitoring local AI camera streams, receiving detection incidents, storing evidence, and reviewing alerts from one operator console.

The web app and the AI models are separate services:

- Laravel handles auth, dashboard pages, database records, users, cameras, and the incident API.
- React/Vite powers the dashboard UI.
- Python/OpenCV services run the weapon and violence models, expose MJPEG streams, save snapshots/clips, and post incident records back to Laravel.

## Services

| Service | Local URL | Container name | Purpose |
| --- | --- | --- | --- |
| Laravel backend | `http://127.0.0.1:8000` | `violence-backend` | Web dashboard and API |
| Vite frontend | `http://127.0.0.1:5173` | `violence-frontend` | Dev asset server |
| MySQL | `127.0.0.1:3306` | `violence-mysql` | App database |
| Weapon AI | `http://127.0.0.1:5000` | `violence-weapon-service` | YOLO weapon stream and detection |
| Violence AI | `http://127.0.0.1:5001` | `violence-violence-service` | Keras violence stream and detection |
| phpMyAdmin | `http://127.0.0.1:8080` | `violence-phpmyadmin` | Optional database UI |

Default admin after seeding:

```text
Email: admin@example.com
Password: admin
```

## Architecture

```text
Camera / CCTV source
        |
        v
Python AI services
OpenCV + YOLO weapon model / Keras violence model
        |
        | MJPEG stream on ports 5000 and 5001
        | saves snapshots and clips
        | POST /api/incidents
        v
Laravel backend + MySQL
        |
        v
React dashboard
```

## Local Setup Without Docker

Install PHP and Node dependencies:

```bash
composer install
npm install
```

Create `.env` and configure MySQL:

```bash
cp .env.example .env
php artisan key:generate
```

Recommended `.env` values:

```env
APP_URL=http://127.0.0.1:8000
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=violence
DB_USERNAME=root
DB_PASSWORD=
FILESYSTEM_DISK=public
INFERENCE_API_TOKEN=
```

Create the database, then run:

```bash
php artisan migrate --seed
php artisan storage:link
```

Start the web app:

```bash
php artisan serve --host=127.0.0.1 --port=8000 --no-reload
npm run dev
```

Open:

```text
http://127.0.0.1:8000/login
```

## Running The AI Services

Install Python requirements in your virtual environment:

```bash
pip install -r ai_service/requirements.txt
```

Place models here:

```text
storage/app/models/weapon/weapon_detection_yolov11m.pt
storage/app/models/violence/cctvmodel_advanced.keras
```

Run weapon detection:

```bash
python ai_service/weapon_detection_service.py
```

Weapon endpoints:

```text
GET  http://127.0.0.1:5000/status
GET  http://127.0.0.1:5000/stream
POST http://127.0.0.1:5000/start
POST http://127.0.0.1:5000/stop
```

Run violence detection:

```bash
python ai_service/violence_detection_service.py
```

Violence endpoints:

```text
GET  http://127.0.0.1:5001/status
GET  http://127.0.0.1:5001/stream
POST http://127.0.0.1:5001/start
POST http://127.0.0.1:5001/stop
```

### Camera Source Note

Both AI services default to camera source `0`. On Windows, one physical webcam usually cannot be opened by two OpenCV processes at the same time. Run one model service at a time, or use separate camera sources.

Environment overrides:

```bash
set CAMERA_SOURCE=0
set VIOLENCE_CAMERA_SOURCE=1
```

If you need both models on the same camera at the same time, the best design is a combined Python service that opens the camera once and sends the same frames through both models.

## Docker Setup

The project includes:

```text
docker-compose.yml
docker/backend/Dockerfile
docker/frontend/Dockerfile
docker/ai/Dockerfile
.env.docker.example
```

Start the web stack:

```bash
docker compose up --build
```

This starts Laravel, Vite, and MySQL.

Start with phpMyAdmin:

```bash
docker compose --profile tools up --build
```

Start the AI services too:

```bash
docker compose --profile ai up --build
```

Important camera caveat: Docker camera access is easiest on Linux with `/dev/video0`. Docker Desktop on Windows does not reliably pass a laptop webcam into Linux containers. For Windows development, run the Laravel/MySQL/frontend services in Docker and run the Python AI service directly on Windows when you need webcam access.

## Incident API

Endpoint:

```http
POST http://127.0.0.1:8000/api/incidents
```

Payload:

```json
{
  "camera_id": "LAPTOP_CAM",
  "district": "Local Test",
  "event_type": "Weapon Detected",
  "confidence": 0.94,
  "violence_score": 0.87,
  "weapon_detected": true,
  "alert_level": "critical",
  "timestamp": "2026-05-04T00:20:00",
  "snapshot_url": "/storage/incidents/snapshots/example.jpg",
  "clip_path": "/storage/incidents/videos/example.mp4"
}
```

If `INFERENCE_API_TOKEN` is set, include:

```http
X-Inference-Token: your-token
```

List incidents:

```http
GET http://127.0.0.1:8000/api/incidents
```

## Postman

Import this collection directly into Postman:

```text
postman/AI-Violence-Detection-System.postman_collection.json
```

To regenerate it:

```bash
node postman/generate-postman-collection.js
```

Collection variables:

```text
laravel_url=http://127.0.0.1:8000
weapon_service_url=http://127.0.0.1:5000
violence_service_url=http://127.0.0.1:5001
inference_token=
```

## Evidence Clips And Snapshots

The Python services save evidence under:

```text
storage/app/public/incidents/videos/
storage/app/public/incidents/snapshots/
```

Laravel serves them through:

```text
public/storage -> storage/app/public
```

Create that link with:

```bash
php artisan storage:link
```

Saved incident URLs look like:

```text
/storage/incidents/videos/weapon_YYYYMMDD_HHMMSS.mp4
/storage/incidents/snapshots/weapon_YYYYMMDD_HHMMSS.jpg
```

### Clip Does Not Play In Edge/Chrome

If the file exists locally but the browser does not play it, the usual cause is codec compatibility. OpenCV often writes `.mp4` files with the `mp4v` codec, while Edge/Chrome prefer H.264 video with `yuv420p` pixels.

The Python services now try to transcode finished clips with `ffmpeg`:

```text
H.264 + yuv420p + faststart
```

Install `ffmpeg` locally and make sure it is available in `PATH`, or use the Docker AI image, which includes `ffmpeg`.

Quick checks:

```bash
ffmpeg -version
php artisan storage:link
```

Then record a new incident. Existing old clips may still be encoded as `mp4v`; re-record or transcode them manually with:

```bash
ffmpeg -i old.mp4 -vcodec libx264 -pix_fmt yuv420p -movflags +faststart -an fixed.mp4
```

## Common Issues

### Dashboard Is Blank

Make sure Vite is running:

```bash
npm run dev
```

Or build assets and remove stale hot reload state:

```bash
npm run build
del public\hot
```

The Blade layout includes `@viteReactRefresh`, which is required for React Fast Refresh in Laravel.

### Stream Does Not Load

Check the service status:

```text
http://127.0.0.1:5000/status
http://127.0.0.1:5001/status
```

If `camera_opened` is false on the violence service, stop other camera apps or the weapon service, then restart violence detection.

### TensorFlow Startup Logs

Messages about oneDNN, CPU instructions, or no native Windows GPU support are normal TensorFlow startup logs. They are not fatal unless the process exits or `/status` is unreachable.

### MySQL Connection Fails In Docker

Inside Docker, use:

```env
DB_HOST=mysql
DB_USERNAME=violence
DB_PASSWORD=violence
```

From your host machine, use:

```env
DB_HOST=127.0.0.1
```

## Project Structure

```text
app/
  Http/Controllers/
    Admin/
    Api/
    Auth/
  Models/

ai_service/
  weapon_detection_service.py
  violence_detection_service.py
  requirements.txt

docker/
  ai/
  backend/
  frontend/

postman/
  generate-postman-collection.js
  AI-Violence-Detection-System.postman_collection.json

resources/
  js/components/Dashboard.jsx
  views/

routes/
  api.php
  web.php

storage/app/
  models/
  public/incidents/
```
