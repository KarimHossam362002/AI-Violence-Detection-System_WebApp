<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('incidents', function (Blueprint $table) {
            $table->id();
            $table->foreignId('camera_id')->nullable()->constrained()->nullOnDelete();
            $table->string('external_camera_id')->nullable()->index();
            $table->string('district')->nullable();
            $table->string('event_type');
            $table->decimal('confidence', 5, 4)->nullable();
            $table->decimal('violence_score', 5, 4)->nullable();
            $table->boolean('weapon_detected')->default(false);
            $table->string('alert_level')->default('low');
            $table->timestamp('detected_at')->nullable();
            $table->string('snapshot_url')->nullable();
            $table->string('clip_path')->nullable();
            $table->json('metadata')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('incidents');
    }
};
