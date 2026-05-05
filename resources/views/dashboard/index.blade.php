<x-layouts.app title="Operations Overview">
    @php
        $maxTrend = max(1, collect($dailyTrend)->max('count'));
    @endphp

    <header class="page-header">
        <div>
            <span class="eyebrow">Command overview</span>
            <h1>Operations Report</h1>
            <p class="page-subtitle">Daily detection activity, risk distribution, evidence readiness, and recent priority events.</p>
        </div>
        <div class="header-actions">
            <a class="secondary-button" href="{{ route('stream') }}">Open live stream</a>
            <button class="theme-icon-button" type="button" data-theme-toggle aria-label="Switch to dark mode">
                <svg class="theme-icon theme-icon-dark" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M21 14.5A8.5 8.5 0 0 1 9.5 3 7 7 0 1 0 21 14.5Z" />
                </svg>
                <svg class="theme-icon theme-icon-light" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 4V2m0 20v-2m8-8h2M2 12h2m13.66-5.66 1.41-1.41M4.93 19.07l1.41-1.41m0-11.32L4.93 4.93m14.14 14.14-1.41-1.41" />
                    <circle cx="12" cy="12" r="4" />
                </svg>
            </button>
        </div>
    </header>

    <section class="report-kpi-grid">
        <article class="report-kpi danger">
            <small>Total incidents</small>
            <strong>{{ $stats['total'] }}</strong>
            <span>{{ $stats['critical'] }} critical alerts</span>
        </article>
        <article class="report-kpi warning">
            <small>Today</small>
            <strong>{{ $stats['today'] }}</strong>
            <span>{{ $stats['high'] }} high-priority incidents</span>
        </article>
        <article class="report-kpi">
            <small>Evidence captured</small>
            <strong>{{ $stats['evidence'] }}</strong>
            <span>Snapshots or clips stored</span>
        </article>
        <article class="report-kpi system">
            <small>Cameras</small>
            <strong>{{ $stats['cameras'] }}</strong>
            <span>Registered sources</span>
        </article>
    </section>

    <section class="report-layout" id="reports">
        <article class="panel report-panel">
            <div class="panel-header">
                <div>
                    <h2>7-Day Incident Trend</h2>
                    <p>Volume by creation date.</p>
                </div>
            </div>
            <div class="trend-bars">
                @foreach($dailyTrend as $day)
                    <div class="trend-day">
                        <div class="trend-track">
                            <span style="height: {{ max(8, ($day['count'] / $maxTrend) * 100) }}%"></span>
                        </div>
                        <strong>{{ $day['count'] }}</strong>
                        <small>{{ $day['label'] }}</small>
                    </div>
                @endforeach
            </div>
        </article>

        <article class="panel report-panel">
            <div class="panel-header">
                <div>
                    <h2>Alert Mix</h2>
                    <p>Risk distribution across all incidents.</p>
                </div>
            </div>
            <div class="breakdown-list">
                @foreach($alertBreakdown as $alert)
                    <div class="breakdown-row">
                        <span class="alert-badge {{ strtolower($alert['tone']) }}">{{ $alert['label'] }}</span>
                        <strong>{{ $alert['count'] }}</strong>
                    </div>
                @endforeach
            </div>
        </article>

        <article class="panel report-panel">
            <div class="panel-header">
                <div>
                    <h2>Event Types</h2>
                    <p>Most common detection categories.</p>
                </div>
            </div>
            <div class="breakdown-list">
                @forelse($eventBreakdown as $event)
                    <div class="breakdown-row">
                        <span>{{ $event['label'] }}</span>
                        <strong>{{ $event['count'] }}</strong>
                    </div>
                @empty
                    <p class="empty-state">No incidents recorded yet.</p>
                @endforelse
            </div>
        </article>
    </section>

    <section class="panel incident-panel">
        <div class="panel-header">
            <div>
                <h2>Recent Priority Incidents</h2>
                <p>Latest detections with direct investigation links.</p>
            </div>
            <a class="ghost-button" href="{{ route('incidents.index') }}">View all</a>
        </div>

        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Alert</th>
                        <th>Event</th>
                        <th>Camera</th>
                        <th>Confidence</th>
                        <th>Detected</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    @forelse($recentIncidents as $incident)
                        <tr>
                            <td><span class="alert-badge {{ $incident->alert_level }}">{{ $incident->alert_level }}</span></td>
                            <td>
                                <strong>{{ $incident->event_type }}</strong>
                                <small>{{ $incident->weapon_detected ? 'Weapon flag' : 'No weapon flag' }}</small>
                            </td>
                            <td>
                                <strong>{{ $incident->external_camera_id ?? $incident->camera?->camera_id ?? 'Unknown' }}</strong>
                                <small>{{ $incident->district ?? $incident->camera?->district ?? 'No district' }}</small>
                            </td>
                            <td>{{ is_null($incident->confidence) ? 'N/A' : number_format($incident->confidence * 100, 1).'%' }}</td>
                            <td>{{ optional($incident->detected_at)->format('M d, Y H:i') ?? 'N/A' }}</td>
                            <td><a class="ghost-button compact-button" href="{{ route('incidents.show', $incident) }}">Inspect</a></td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="6" class="empty-state">No incidents recorded yet.</td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
    </section>
</x-layouts.app>
