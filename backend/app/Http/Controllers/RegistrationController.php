<?php

namespace App\Http\Controllers;

use App\Models\Event;
use App\Models\Registration;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

class RegistrationController extends Controller
{
    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'event_id' => 'required|integer',
            'student_id' => 'required|string',
            'name' => 'required|string',
            'email' => 'required|email',
        ]);

        $event = Event::find($validated['event_id']);
        if (!$event) {
            return response()->json(['error' => 'Event not found'], 404);
        }

        // Check for existing registration
        $existingRegistration = Registration::where('event_id', $validated['event_id'])
            ->where('student_id', $validated['student_id'])
            ->first();

        if ($existingRegistration) {
            // Return existing registration with its token
            return response()->json([
                'registration_id' => $existingRegistration->id,
                'event_id' => $existingRegistration->event_id,
                'student_id' => $existingRegistration->student_id,
                'name' => $existingRegistration->name,
                'email' => $existingRegistration->email,
                'qr_token' => $existingRegistration->qr_token,
            ], 201);
        }

        // Generate unique QR token
        $qrToken = $this->generateUniqueQrToken($validated['event_id']);

        $registration = Registration::create([
            'event_id' => $validated['event_id'],
            'student_id' => $validated['student_id'],
            'name' => $validated['name'],
            'email' => $validated['email'],
            'qr_token' => $qrToken,
        ]);

        return response()->json([
            'registration_id' => $registration->id,
            'event_id' => $registration->event_id,
            'student_id' => $registration->student_id,
            'name' => $registration->name,
            'email' => $registration->email,
            'qr_token' => $registration->qr_token,
        ], 201);
    }

    private function generateUniqueQrToken(int $eventId): string
    {
        do {
            $randomPart = strtoupper(Str::random(8));
            $qrToken = "EV{$eventId}-{$randomPart}";
        } while (Registration::where('qr_token', $qrToken)->exists());

        return $qrToken;
    }
}
