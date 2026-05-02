<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Camera;
use App\Models\Incident;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Arr;

class IncidentController extends Controller
{
    public function index(): JsonResponse
    {
        return response()->json([
            'incidents' => Incident::query()
                ->with('camera')
                ->latest('detected_at')
                ->latest()
                ->paginate(25),
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $token = config('services.inference.token');

        if ($token && ! hash_equals($token, (string) $request->header('X-Inference-Token'))) {
            return response()->json(['message' => 'Invalid inference token.'], 401);
        }

        $validated = $request->validate([
            'camera_id' => ['required', 'string', 'max:255'],
            'district' => ['nullable', 'string', 'max:255'],
            'event_type' => ['nullable', 'string', 'max:255'],
            'confidence' => ['nullable', 'numeric', 'between:0,1'],
            'violence_score' => ['nullable', 'numeric', 'between:0,1'],
            'weapon_detected' => ['nullable', 'boolean'],
            'alert_level' => ['nullable', 'in:low,medium,high,critical'],
            'timestamp' => ['nullable', 'date'],
            'snapshot_url' => ['nullable', 'string', 'max:2048'],
            'clip_path' => ['nullable', 'string', 'max:2048'],
        ]);

        $camera = Camera::query()->firstOrCreate(
            ['camera_id' => $validated['camera_id']],
            [
                'name' => $validated['camera_id'],
                'district' => $validated['district'] ?? null,
                'status' => 'online',
            ],
        );

        $weaponDetected = (bool) ($validated['weapon_detected'] ?? false);
        $violenceScore = $validated['violence_score'] ?? $validated['confidence'] ?? null;

        $incident = Incident::query()->create([
            'camera_id' => $camera->id,
            'external_camera_id' => $validated['camera_id'],
            'district' => $validated['district'] ?? $camera->district,
            'event_type' => $validated['event_type'] ?? ($weaponDetected ? 'Weapon Detected' : 'Violence Detected'),
            'confidence' => $validated['confidence'] ?? null,
            'violence_score' => $violenceScore,
            'weapon_detected' => $weaponDetected,
            'alert_level' => $validated['alert_level'] ?? $this->resolveAlertLevel($weaponDetected, $violenceScore),
            'detected_at' => $validated['timestamp'] ?? now(),
            'snapshot_url' => $validated['snapshot_url'] ?? null,
            'clip_path' => $validated['clip_path'] ?? null,
            'metadata' => Arr::except($request->all(), array_keys($validated)),
        ]);

        return response()->json([
            'message' => 'Incident recorded.',
            'incident' => $incident->load('camera'),
        ], 201);
    }

    private function resolveAlertLevel(bool $weaponDetected, ?float $violenceScore): string
    {
        if ($weaponDetected && ($violenceScore === null || $violenceScore >= 0.5)) {
            return 'critical';
        }

        if ($violenceScore !== null && $violenceScore >= 0.75) {
            return 'high';
        }

        if ($violenceScore !== null && $violenceScore >= 0.5) {
            return 'medium';
        }

        return 'low';
    }
}
