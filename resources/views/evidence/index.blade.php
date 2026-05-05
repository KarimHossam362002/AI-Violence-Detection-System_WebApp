<x-layouts.app title="Evidence">
    <header class="page-header">
        <div>
            <span class="eyebrow">Evidence library</span>
            <h1>Evidence</h1>
            <p class="page-subtitle">Snapshots and clips captured by the AI services.</p>
        </div>
        <div class="header-actions">
            <a class="secondary-button" href="{{ route('incidents.index') }}">All incidents</a>
            <button class="theme-icon-button" type="button" data-theme-toggle aria-label="Switch to dark mode">
                <svg class="theme-icon theme-icon-dark" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 14.5A8.5 8.5 0 0 1 9.5 3 7 7 0 1 0 21 14.5Z" /></svg>
                <svg class="theme-icon theme-icon-light" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4V2m0 20v-2m8-8h2M2 12h2m13.66-5.66 1.41-1.41M4.93 19.07l1.41-1.41m0-11.32L4.93 4.93m14.14 14.14-1.41-1.41" /><circle cx="12" cy="12" r="4" /></svg>
            </button>
        </div>
    </header>

    <section class="evidence-grid">
        @forelse($incidents as $incident)
            <article class="panel evidence-card">
                <div class="evidence-thumb">
                    @if($incident->snapshot_url)
                        <img src="{{ $incident->snapshot_url }}" alt="Incident snapshot">
                    @else
                        <span>No snapshot</span>
                    @endif
                </div>
                <div>
                    <span class="alert-badge {{ $incident->alert_level }}">{{ $incident->alert_level }}</span>
                    <h2>{{ $incident->event_type }}</h2>
                    <p>{{ $incident->external_camera_id ?? $incident->camera?->camera_id ?? 'Unknown camera' }} · {{ optional($incident->detected_at)->format('M d, Y H:i') ?? 'N/A' }}</p>
                </div>
                <div class="evidence-links">
                    <a class="ghost-button compact-button" href="{{ route('incidents.show', $incident) }}">Inspect</a>
                    @if($incident->clip_path)
                        <a class="ghost-button compact-button" href="{{ $incident->clip_path }}" target="_blank" rel="noreferrer">Clip</a>
                    @endif
                </div>
            </article>
        @empty
            <article class="panel">
                <p class="empty-state">No evidence files have been recorded yet.</p>
            </article>
        @endforelse
    </section>

    <div class="pagination-wrap">
        {{ $incidents->links() }}
    </div>
</x-layouts.app>
