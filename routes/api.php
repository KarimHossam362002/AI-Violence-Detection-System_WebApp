<?php

use App\Http\Controllers\Api\IncidentController;
use Illuminate\Support\Facades\Route;

Route::get('/incidents', [IncidentController::class, 'index']);
Route::post('/incidents', [IncidentController::class, 'store']);
