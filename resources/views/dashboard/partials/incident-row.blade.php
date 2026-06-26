<tr>
    <td><span class="alert-badge {{ $incident->alert_level }}">{{ ucfirst($incident->alert_level) }}</span></td>
    <td>
        <strong>{{ $incident->event_type }}</strong>
        <small>{{ $incident->weapon_detected ? 'Weapon detected' : 'No weapon flag' }}</small>
    </td>
    <td>
        <strong>{{ $incident->external_camera_id ?? $incident->camera?->camera_id ?? 'Unknown' }}</strong>
        <small>{{ $incident->district ?? $incident->camera?->district ?? 'No district' }}</small>
    </td>
    <td>{{ $incident->confidence !== null ? number_format($incident->confidence * 100, 1).'%' : 'N/A' }}</td>
    <td>{{ $incident->detected_at?->format('M d, H:i:s') ?? $incident->created_at->format('M d, H:i:s') }}</td>
    <td class="evidence-links">
        @if($incident->snapshot_src)
            <a href="{{ $incident->snapshot_src }}" target="_blank">Snapshot</a>
        @endif
        @if($incident->clip_src)
            <a href="{{ $incident->clip_src }}" target="_blank">Clip</a>
        @endif
        @unless($incident->snapshot_src || $incident->clip_src)
            <span>N/A</span>
        @endunless
    </td>
</tr>
