<x-layouts.app title="Cameras">
    <header class="page-header">
        <div>
            <span class="eyebrow">Camera registry</span>
            <h1>Cameras</h1>
            <p class="page-subtitle">Sources discovered from incoming AI incidents.</p>
        </div>
        <div class="header-actions">
            <a class="secondary-button" href="{{ route('stream') }}">Open live stream</a>
            <button class="theme-icon-button" type="button" data-theme-toggle aria-label="Switch to dark mode">
                <svg class="theme-icon theme-icon-dark" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 14.5A8.5 8.5 0 0 1 9.5 3 7 7 0 1 0 21 14.5Z" /></svg>
                <svg class="theme-icon theme-icon-light" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4V2m0 20v-2m8-8h2M2 12h2m13.66-5.66 1.41-1.41M4.93 19.07l1.41-1.41m0-11.32L4.93 4.93m14.14 14.14-1.41-1.41" /><circle cx="12" cy="12" r="4" /></svg>
            </button>
        </div>
    </header>

    <section class="camera-card-grid">
        @forelse($cameras as $camera)
            <article class="panel camera-summary-card">
                <div class="panel-header">
                    <div>
                        <h2>{{ $camera->name ?? $camera->camera_id }}</h2>
                        <p>{{ $camera->district ?? 'No district assigned' }}</p>
                    </div>
                    <span class="status-pill online">{{ $camera->status ?? 'online' }}</span>
                </div>
                <div class="detail-list">
                    <div><span>Camera ID</span><strong>{{ $camera->camera_id }}</strong></div>
                    <div><span>Incidents</span><strong>{{ $camera->incidents_count }}</strong></div>
                    <div><span>Stream URL</span><strong>{{ $camera->stream_url ?? 'Not registered' }}</strong></div>
                </div>
            </article>
        @empty
            <article class="panel">
                <p class="empty-state">No cameras have been registered yet.</p>
            </article>
        @endforelse
    </section>

    <div class="pagination-wrap">
        {{ $cameras->links() }}
    </div>
</x-layouts.app>
