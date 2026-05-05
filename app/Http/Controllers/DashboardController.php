<?php

namespace App\Http\Controllers;

use App\Models\Camera;
use App\Models\Incident;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Carbon;
use Illuminate\View\View;

class DashboardController extends Controller
{
    public function index(): View
    {
        $recentIncidents = Incident::query()
            ->with('camera')
            ->latest('detected_at')
            ->latest()
            ->take(8)
            ->get();

        return view('dashboard.index', [
            'recentIncidents' => $recentIncidents,
            'stats' => [
                'total' => Incident::query()->count(),
                'critical' => Incident::query()->where('alert_level', 'critical')->count(),
                'high' => Incident::query()->where('alert_level', 'high')->count(),
                'today' => Incident::query()->whereDate('created_at', now()->toDateString())->count(),
                'cameras' => Camera::query()->count(),
                'evidence' => Incident::query()
                    ->where(fn ($query) => $query->whereNotNull('snapshot_url')->orWhereNotNull('clip_path'))
                    ->count(),
            ],
            'alertBreakdown' => $this->alertBreakdown(),
            'eventBreakdown' => $this->eventBreakdown(),
            'dailyTrend' => $this->dailyTrend(),
        ]);
    }

    public function stream(): View
    {
        return view('stream.index', [
            'cameras' => Camera::query()->orderBy('name')->get(),
        ]);
    }

    public function incidents(): View
    {
        return view('incidents.index', [
            'incidents' => $this->incidentPaginator(),
        ]);
    }

    public function showIncident(Incident $incident): View
    {
        return view('incidents.show', [
            'incident' => $incident->load('camera'),
        ]);
    }

    public function cameras(): View
    {
        return view('cameras.index', [
            'cameras' => Camera::query()
                ->withCount('incidents')
                ->orderBy('name')
                ->paginate(12),
        ]);
    }

    public function evidence(): View
    {
        return view('evidence.index', [
            'incidents' => Incident::query()
                ->with('camera')
                ->where(fn ($query) => $query->whereNotNull('snapshot_url')->orWhereNotNull('clip_path'))
                ->latest('detected_at')
                ->latest()
                ->paginate(12),
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

    private function incidentPaginator(): LengthAwarePaginator
    {
        return Incident::query()
            ->with('camera')
            ->latest('detected_at')
            ->latest()
            ->paginate(12);
    }

    private function alertBreakdown(): array
    {
        $counts = Incident::query()
            ->selectRaw('alert_level, count(*) as aggregate')
            ->groupBy('alert_level')
            ->pluck('aggregate', 'alert_level');

        return collect(['critical', 'high', 'medium', 'low'])
            ->map(fn ($level) => [
                'label' => ucfirst($level),
                'count' => (int) ($counts[$level] ?? 0),
                'tone' => $level,
            ])
            ->all();
    }

    private function eventBreakdown(): array
    {
        return Incident::query()
            ->selectRaw('event_type, count(*) as aggregate')
            ->groupBy('event_type')
            ->orderByDesc('aggregate')
            ->take(5)
            ->get()
            ->map(fn (Incident $incident) => [
                'label' => $incident->event_type,
                'count' => (int) $incident->aggregate,
            ])
            ->all();
    }

    private function dailyTrend(): array
    {
        $start = now()->subDays(6)->startOfDay();
        $counts = Incident::query()
            ->where('created_at', '>=', $start)
            ->selectRaw('DATE(created_at) as day, count(*) as aggregate')
            ->groupBy('day')
            ->pluck('aggregate', 'day');

        return collect(range(0, 6))
            ->map(function (int $offset) use ($start, $counts) {
                $day = Carbon::parse($start)->addDays($offset);

                return [
                    'label' => $day->format('D'),
                    'date' => $day->toDateString(),
                    'count' => (int) ($counts[$day->toDateString()] ?? 0),
                ];
            })
            ->all();
    }
}
