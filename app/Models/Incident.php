<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

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

    public function camera(): BelongsTo
    {
        return $this->belongsTo(Camera::class);
    }
}
