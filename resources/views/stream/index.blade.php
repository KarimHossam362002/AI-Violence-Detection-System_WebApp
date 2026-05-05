<x-layouts.app title="Live Stream">
    <div
        id="stream-root"
        data-cameras='@json($cameras, JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP | JSON_HEX_TAG)'
    ></div>
</x-layouts.app>
