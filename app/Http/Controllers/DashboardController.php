<?php

namespace App\Http\Controllers;

use App\Models\Camera;
use App\Models\Incident;
use Illuminate\Http\JsonResponse;
use Illuminate\View\View;

class DashboardController extends Controller
{
    public function index(): View
    {
        $incidents = Incident::query()
            ->with('camera')
            ->latest('detected_at')
            ->latest()
            ->take(20)
            ->get();

        return view('dashboard.index', [
            'cameras' => Camera::query()->orderBy('name')->get(),
            'incidents' => $incidents,
            'stats' => [
                'critical' => Incident::query()->where('alert_level', 'critical')->count(),
                'high' => Incident::query()->where('alert_level', 'high')->count(),
                'today' => Incident::query()->whereDate('created_at', now()->toDateString())->count(),
                'cameras' => Camera::query()->count(),
            ],
        ]);
    }

    public function latestIncidents(): JsonResponse
    {
        return response()->json([
            'incidents' => Incident::query()
                ->with('camera')
                ->latest('detected_at')
                ->latest()
                ->take(10)
                ->get(),
        ]);
    }
}
