<x-layouts.app title="Incident #{{ $incident->id }}">
    <header class="page-header">
        <div>
            <span class="eyebrow">Investigation record</span>
            <h1>Incident #{{ $incident->id }}</h1>
            <p class="page-subtitle">{{ $incident->event_type }} captured {{ optional($incident->detected_at)->format('M d, Y H:i') ?? 'at an unknown time' }}.</p>
        </div>
        <div class="header-actions">
            <a class="ghost-button" href="{{ route('incidents.index') }}">Back to incidents</a>
            <button class="theme-icon-button" type="button" data-theme-toggle aria-label="Switch to dark mode">
                <svg class="theme-icon theme-icon-dark" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 14.5A8.5 8.5 0 0 1 9.5 3 7 7 0 1 0 21 14.5Z" /></svg>
                <svg class="theme-icon theme-icon-light" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4V2m0 20v-2m8-8h2M2 12h2m13.66-5.66 1.41-1.41M4.93 19.07l1.41-1.41m0-11.32L4.93 4.93m14.14 14.14-1.41-1.41" /><circle cx="12" cy="12" r="4" /></svg>
            </button>
        </div>
    </header>

    <section class="detail-grid">
        <article class="panel">
            <div class="panel-header">
                <div>
                    <h2>Incident Details</h2>
                    <p>Detection metadata and source information.</p>
                </div>
                <span class="alert-badge {{ $incident->alert_level }}">{{ $incident->alert_level }}</span>
            </div>
            <div class="detail-list">
                <div><span>Event</span><strong>{{ $incident->event_type }}</strong></div>
                <div><span>Camera</span><strong>{{ $incident->external_camera_id ?? $incident->camera?->camera_id ?? 'Unknown' }}</strong></div>
                <div><span>District</span><strong>{{ $incident->district ?? $incident->camera?->district ?? 'No district' }}</strong></div>
                <div><span>Confidence</span><strong>{{ is_null($incident->confidence) ? 'N/A' : number_format($incident->confidence * 100, 1).'%' }}</strong></div>
                <div><span>Violence score</span><strong>{{ is_null($incident->violence_score) ? 'N/A' : number_format($incident->violence_score * 100, 1).'%' }}</strong></div>
                <div><span>Weapon flag</span><strong>{{ $incident->weapon_detected ? 'Yes' : 'No' }}</strong></div>
            </div>
        </article>

        <article class="panel evidence-panel">
            <div class="panel-header">
                <div>
                    <h2>Snapshot</h2>
                    <p>Best captured still frame.</p>
                </div>
            </div>
            @if($incident->snapshot_url)
                <a href="{{ $incident->snapshot_url }}" target="_blank" rel="noreferrer">
                    <img class="evidence-image" src="{{ $incident->snapshot_url }}" alt="Incident snapshot">
                </a>
            @else
                <p class="empty-state">No snapshot was saved for this incident.</p>
            @endif
        </article>
    </section>

    <section class="panel evidence-panel">
        <div class="panel-header">
            <div>
                <h2>Video Clip</h2>
                <p>Recorded evidence from the detection window.</p>
            </div>
            @if($incident->clip_path)
                <a class="ghost-button" href="{{ $incident->clip_path }}" target="_blank" rel="noreferrer">Open file</a>
            @endif
        </div>

        @if($incident->clip_path)
            <video class="evidence-video" controls preload="metadata">
                <source src="{{ $incident->clip_path }}" type="video/mp4">
            </video>
        @else
            <p class="empty-state">No clip was saved for this incident.</p>
        @endif
    </section>

    @if($incident->metadata)
        <section class="panel">
            <div class="panel-header">
                <div>
                    <h2>Raw Metadata</h2>
                    <p>Extra payload values sent by the AI service.</p>
                </div>
            </div>
            <pre class="metadata-box">{{ json_encode($incident->metadata, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) }}</pre>
        </section>
    @endif
</x-layouts.app>
