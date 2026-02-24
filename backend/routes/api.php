<?php

use App\Http\Controllers\AttendanceController;
use App\Http\Controllers\CheckinController;
use App\Http\Controllers\EventController;
use App\Http\Controllers\RegistrationController;
use App\Http\Middleware\StaffPinMiddleware;
use Illuminate\Support\Facades\Route;

Route::get('/events', [EventController::class, 'index']);
Route::post('/register', [RegistrationController::class, 'store']);

Route::middleware(StaffPinMiddleware::class)->group(function () {
    Route::post('/events', [EventController::class, 'store']);
    Route::get('/events/{eventId}/registrations', [EventController::class, 'showRegistrations']);
    Route::post('/checkin/verify', [CheckinController::class, 'verify']);
    Route::post('/checkin/lookup', [CheckinController::class, 'lookup']);
    Route::post('/checkin', [CheckinController::class, 'store']);
    Route::get('/attendance', [AttendanceController::class, 'index']);
});
