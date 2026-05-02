<x-layouts.app title="Dashboard">
    <div
        id="dashboard-root"
        data-cameras='@json($cameras, JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP | JSON_HEX_TAG)'
        data-incidents='@json($incidents, JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP | JSON_HEX_TAG)'
        data-stats='@json($stats, JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP | JSON_HEX_TAG)'
        data-latest-url='@json(route('dashboard.incidents.latest'), JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP | JSON_HEX_TAG)'
    ></div>
</x-layouts.app>
