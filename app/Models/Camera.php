<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Camera extends Model
{
    use HasFactory;

    protected $fillable = [
        'camera_id',
        'name',
        'district',
        'stream_url',
        'status',
    ];

    public function incidents(): HasMany
    {
        return $this->hasMany(Incident::class);
    }
}
