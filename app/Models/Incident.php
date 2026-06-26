<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Str;

class Incident extends Model
{
    use HasFactory;

    protected $fillable = [
        'camera_id',
        'external_camera_id',
        'district',
        'event_type',
        'confidence',
        'violence_score',
        'weapon_detected',
        'alert_level',
        'detected_at',
        'snapshot_url',
        'clip_path',
        'metadata',
    ];

    protected $appends = [
        'snapshot_src',
        'clip_src',
    ];

    protected function casts(): array
    {
        return [
            'confidence' => 'float',
            'violence_score' => 'float',
            'weapon_detected' => 'boolean',
            'detected_at' => 'datetime',
            'metadata' => 'array',
        ];
    }

    public function getSnapshotSrcAttribute(): ?string
    {
        return $this->publicEvidenceUrl($this->snapshot_url);
    }

    public function getClipSrcAttribute(): ?string
    {
        return $this->publicEvidenceUrl($this->clip_path);
    }

    public function camera(): BelongsTo
    {
        return $this->belongsTo(Camera::class);
    }

    private function publicEvidenceUrl(?string $path): ?string
    {
        if (! $path) {
            return null;
        }

        $path = str_replace('\\', '/', trim($path));

        if (Str::startsWith($path, ['http://', 'https://'])) {
            return $path;
        }

        if (Str::startsWith($path, '/storage/')) {
            return asset(ltrim($path, '/'));
        }

        $path = preg_replace('#^.*storage/app/public/#', '', $path);
        $path = preg_replace('#^public/storage/#', '', $path);
        $path = ltrim($path, '/');

        if (Str::startsWith($path, 'storage/')) {
            return asset($path);
        }

        return asset('storage/'.$path);
    }
}
