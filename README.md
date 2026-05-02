# AI Violence Detection System - Web Dashboard

Laravel + React dashboard for monitoring live camera streams, receiving AI detection events, storing incident metadata, and giving operators a simple interface for reviewing alerts and evidence.

The AI models are not executed inside Laravel. The recommended setup is to keep the Python inference code as a separate service that reads the camera, runs the violence/weapon models, saves clips locally, and sends incident events to this Laravel backend.

## Project Overview

This web app provides:

- Login and registration.
- Admin/user privileges.
- Default seeded admin account.
- React dashboard cards for webcam access, incident archive, camera registry, and system health.
- Browser webcam preview for local testing.
- Python MJPEG stream preview, for example `http://127.0.0.1:5000/stream`.
- API endpoint for Python inference events.
- Database tables for users, cameras, and incidents.
- Local storage paths for snapshots, clips, and model files.

## Architecture

```text
Laptop Camera / CCTV Stream
        |
        v
Python Inference Service
OpenCV + Violence Model + Weapon Model
        |
        | saves clips / snapshots locally
        | sends HTTP POST incident payload
        v
Laravel API
stores cameras + incidents in MySQL
        |
        v
React Dashboard
operator views alerts, evidence, stream, users
```

### Why Python is separate

Laravel should handle the web application layer: authentication, database records, API routes, dashboard views, and user permissions.

Python should handle the AI layer: camera capture, frame processing, model inference, clip generation, and event posting.

This separation keeps the dashboard responsive and prevents long-running model inference from blocking normal web requests.

## Tech Stack

- Backend: Laravel 12
- Frontend: React + Vite
- Database: MySQL
- Auth: Laravel session authentication
- AI integration: Python service via REST API
- Camera preview: browser webcam or Python MJPEG stream

## Important Local URLs

| Service | URL | Purpose |
| --- | --- | --- |
| Laravel app | `http://127.0.0.1:8000` | Web dashboard |
| Login page | `http://127.0.0.1:8000/login` | Operator/admin login |
| Dashboard | `http://127.0.0.1:8000/dashboard` | Main monitoring UI |
| Laravel health check | `http://127.0.0.1:8000/up` | Quick app status |
| Python stream example | `http://127.0.0.1:5000/stream` | MJPEG camera stream |
| Jupyter Lab example | `http://localhost:8888/lab/workspaces/auto-F` | Notebook environment only |

Jupyter is where you run/edit Python code. The dashboard does not load the Jupyter URL. The dashboard loads the stream URL exposed by your Python code, usually something like `http://127.0.0.1:5000/stream`.

## Default Admin Account

After running the database seeder:

```text
Email: admin@example.com
Password: admin
Role: admin
```

The admin can access the user management screen and change user roles.

## Local Setup

### 1. Install PHP dependencies

```bash
composer install
```

### 2. Install frontend dependencies

```bash
npm install
```

### 3. Configure environment

Copy the example environment file if `.env` does not exist:

```bash
cp .env.example .env
```

Generate the Laravel app key:

```bash
php artisan key:generate
```

Set the database values in `.env`:

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=violence
DB_USERNAME=root
DB_PASSWORD=
```

Optional API token for Python-to-Laravel incident posting:

```env
INFERENCE_API_TOKEN=your-local-token
```

If `INFERENCE_API_TOKEN` is empty, the incident API accepts local posts without that header. If it is set, Python must send it as `X-Inference-Token`.

### 4. Create the MySQL database

Create a database named:

```text
violence
```

With Laragon/MySQL, this can be done from a database GUI or the MySQL CLI.

### 5. Run migrations

```bash
php artisan migrate
```

### 6. Seed the default admin

```bash
php artisan db:seed
```

### 7. Build frontend assets

```bash
npm run build
```

If `public/hot` exists but Vite is not running, Laravel may try to load assets from `http://[::1]:5173` and the page can look blank. Delete `public/hot` or run Vite with `npm run dev`.

### 8. Start Laravel

```bash
php artisan serve --host=127.0.0.1 --port=8000
```

Open:

```text
http://127.0.0.1:8000/login
```

## Running The Python Stream

Your Python model code should expose a stream endpoint. A simple Flask MJPEG stream looks like this:

```python
from flask import Flask, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()

        if not success:
            break

        ok, buffer = cv2.imencode(".jpg", frame)

        if not ok:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
        )

@app.route("/stream")
def stream():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

app.run(host="127.0.0.1", port=5000)
```

Then in the dashboard:

1. Go to `http://127.0.0.1:8000/dashboard`.
2. Paste `http://127.0.0.1:5000/stream`.
3. Click `Load stream`.

## Incident API

Python should send a POST request when violence or weapon detection happens.

Endpoint:

```http
POST http://127.0.0.1:8000/api/incidents
```

Example payload:

```json
{
  "camera_id": "CAM_042",
  "district": "Downtown",
  "event_type": "Weapon Detected",
  "confidence": 0.94,
  "violence_score": 0.87,
  "weapon_detected": true,
  "alert_level": "critical",
  "timestamp": "2026-05-02T14:32:10",
  "snapshot_url": "/storage/incidents/snapshots/042.jpg",
  "clip_path": "/storage/incidents/videos/incident_042.mp4"
}
```

If `INFERENCE_API_TOKEN` is set in `.env`, include:

```http
X-Inference-Token: your-local-token
```

Python example:

```python
import requests

payload = {
    "camera_id": "CAM_042",
    "district": "Downtown",
    "event_type": "Violence Detected",
    "confidence": 0.91,
    "violence_score": 0.91,
    "weapon_detected": False,
    "alert_level": "high",
    "clip_path": "/storage/incidents/videos/incident_042.mp4",
}

requests.post(
    "http://127.0.0.1:8000/api/incidents",
    json=payload,
    headers={
        "Accept": "application/json",
        "X-Inference-Token": "your-local-token",
    },
    timeout=5,
)
```

## Model File Locations

Place model files here:

```text
storage/app/models/violence/
storage/app/models/weapon/
```

Recommended naming:

```text
storage/app/models/violence/violence_model.pt
storage/app/models/weapon/weapon_model.pt
```

The Laravel app does not load these files directly yet. They are reserved for local organization and future service integration.

## Evidence Storage

Recommended local evidence paths:

```text
storage/app/public/incidents/videos/
storage/app/public/incidents/snapshots/
```

Public URLs should look like:

```text
/storage/incidents/videos/incident_001.mp4
/storage/incidents/snapshots/incident_001.jpg
```

If public storage links are not working, run:

```bash
php artisan storage:link
```

## Dashboard Cards

The React dashboard contains:

- Live Webcam: starts the browser webcam or loads a Python stream URL.
- Incident Archive: jumps to the incidents table.
- Camera Registry: shows cameras discovered from incoming incidents.
- System Health: links to Laravel `/up`.

The incidents table refreshes every five seconds using:

```text
/dashboard/incidents/latest
```

## Roles And Privileges

| Role | Permissions |
| --- | --- |
| admin | Access dashboard, manage users, change roles |
| user | Access dashboard and view incidents |

The first manually registered user is also created as admin, but the recommended local account is the seeded admin.

## Common Issues

### Dashboard looks blank

Check whether `public/hot` exists.

If Vite is not running:

```bash
del public\hot
npm run build
```

Or start Vite:

```bash
npm run dev
```

### Unknown database `violence`

Create the MySQL database first, then run:

```bash
php artisan migrate
```

### Login fails after fresh setup

Run:

```bash
php artisan db:seed
```

Then use:

```text
admin@example.com / admin
```

### Stream does not load

Make sure your Python service is running at the stream URL, for example:

```text
http://127.0.0.1:5000/stream
```

Do not paste the Jupyter Lab URL into the dashboard stream box.

## Suggested Development Flow

1. Start MySQL/Laragon.
2. Start Laravel on port `8000`.
3. Start Python/Jupyter.
4. Run the Python stream server on port `5000`.
5. Open the Laravel dashboard.
6. Paste the Python stream URL into the dashboard.
7. Let Python POST incidents to `/api/incidents`.
8. Review alerts and clips in the dashboard.

## Project Structure Notes

```text
app/
  Http/Controllers/
    Auth/              # Login and registration
    Admin/             # User role management
    Api/               # Python incident ingestion API
  Models/
    Camera.php
    Incident.php
    User.php

database/
  factories/
    UserFactory.php
  migrations/
  seeders/
    DatabaseSeeder.php

resources/
  js/
    components/
      Dashboard.jsx    # React dashboard UI
  views/
    auth/
    admin/
    dashboard/

routes/
  web.php              # Auth, dashboard, admin pages
  api.php              # Incident API

storage/
  app/models/          # Local AI model drop-zone
  app/public/incidents # Suggested evidence storage
```

## Current Status

This project currently supports the full local demo loop:

```text
Python camera stream -> Laravel dashboard preview
Python detection event -> Laravel API -> MySQL incident record -> React incident table
```

Next improvements can include WebSocket alerts, clip upload endpoints, camera management screens, and separate pages for incident details.
