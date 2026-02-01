<?php

use App\Http\Controllers\AttendanceController;
use App\Http\Controllers\CheckinController;
use App\Http\Controllers\EventController;
use App\Http\Controllers\RegistrationController;
use Illuminate\Support\Facades\Route;

Route::get('/events', [EventController::class, 'index']);
Route::post('/register', [RegistrationController::class, 'store']);
Route::post('/checkin', [CheckinController::class, 'store']);
Route::get('/attendance', [AttendanceController::class, 'index']);

