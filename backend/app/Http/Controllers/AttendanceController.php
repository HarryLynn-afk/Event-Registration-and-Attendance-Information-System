<?php

namespace App\Http\Controllers;

use App\Models\Event;
use App\Models\Registration;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class AttendanceController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'event_id' => 'required|integer',
        ]);

        $eventId = $validated['event_id'];

        $event = Event::find($eventId);
        if (!$event) {
            return response()->json(['error' => 'Event not found'], 404);
        }

        $registrations = Registration::where('event_id', $eventId)
            ->get()
            ->map(function ($registration) {
                return [
                    'student_id' => $registration->student_id,
                    'name' => $registration->name,
                    'email' => $registration->email,
                    'checked_in' => $registration->checked_in,
                    'checked_in_at' => $registration->checked_in_at?->toIso8601String(),
                ];
            });

        return response()->json($registrations);
    }
}
