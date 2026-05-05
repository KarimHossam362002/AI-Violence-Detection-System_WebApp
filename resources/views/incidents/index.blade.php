<x-layouts.app title="Incidents">
    <header class="page-header">
        <div>
            <span class="eyebrow">Incident center</span>
            <h1>All Incidents</h1>
            <p class="page-subtitle">Paginated detection history with direct access to each investigation record.</p>
        </div>
        <div class="header-actions">
            <a class="secondary-button" href="{{ route('stream') }}">Open live stream</a>
            <button class="theme-icon-button" type="button" data-theme-toggle aria-label="Switch to dark mode">
                <svg class="theme-icon theme-icon-dark" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 14.5A8.5 8.5 0 0 1 9.5 3 7 7 0 1 0 21 14.5Z" /></svg>
                <svg class="theme-icon theme-icon-light" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4V2m0 20v-2m8-8h2M2 12h2m13.66-5.66 1.41-1.41M4.93 19.07l1.41-1.41m0-11.32L4.93 4.93m14.14 14.14-1.41-1.41" /><circle cx="12" cy="12" r="4" /></svg>
            </button>
        </div>
    </header>

    <section class="panel incident-panel">
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Alert</th>
                        <th>Event</th>
                        <th>Camera</th>
                        <th>Confidence</th>
                        <th>Detected</th>
                        <th>Evidence</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    @forelse($incidents as $incident)
                        <tr>
                            <td><span class="alert-badge {{ $incident->alert_level }}">{{ $incident->alert_level }}</span></td>
                            <td>
                                <strong>{{ $incident->event_type }}</strong>
                                <small>{{ $incident->weapon_detected ? 'Weapon detected' : 'No weapon flag' }}</small>
                            </td>
                            <td>
                                <strong>{{ $incident->external_camera_id ?? $incident->camera?->camera_id ?? 'Unknown' }}</strong>
                                <small>{{ $incident->district ?? $incident->camera?->district ?? 'No district' }}</small>
                            </td>
                            <td>{{ is_null($incident->confidence) ? 'N/A' : number_format($incident->confidence * 100, 1).'%' }}</td>
                            <td>{{ optional($incident->detected_at)->format('M d, Y H:i') ?? 'N/A' }}</td>
                            <td>
                                <div class="evidence-links">
                                    @if($incident->snapshot_url)<span>Snapshot</span>@endif
                                    @if($incident->clip_path)<span>Clip</span>@endif
                                    @if(! $incident->snapshot_url && ! $incident->clip_path)<span>N/A</span>@endif
                                </div>
                            </td>
                            <td><a class="ghost-button compact-button" href="{{ route('incidents.show', $incident) }}">Details</a></td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="7" class="empty-state">No incidents recorded yet.</td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>

        <div class="pagination-wrap">
            {{ $incidents->links() }}
        </div>
    </section>
</x-layouts.app>
