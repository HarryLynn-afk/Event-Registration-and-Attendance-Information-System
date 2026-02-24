<?php

namespace App\Http\Controllers;

use App\Models\Registration;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class CheckinController extends Controller
{
    public function verify(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'event_id' => 'required|integer',
            'qr_token' => 'required|string',
        ]);

        $registration = Registration::where('qr_token', $validated['qr_token'])->first();

        if (!$registration) {
            return response()->json(['error' => 'Registration not found'], 404);
        }

        if ($registration->event_id != $validated['event_id']) {
            return response()->json(['error' => 'Wrong event for this token'], 400);
        }

        return response()->json([
            'status' => $registration->checked_in_at ? 'already_checked_in' : 'ready',
            'student_id' => $registration->student_id,
            'name' => $registration->name,
            'checked_in_at' => $registration->checked_in_at?->toIso8601String(),
        ]);
    }

    public function lookup(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'event_id' => 'required|integer',
            'student_id' => 'required|string',
            'name' => 'nullable|string',
        ]);

        $registration = Registration::where('event_id', $validated['event_id'])
            ->where('student_id', $validated['student_id'])
            ->first();

        if (!$registration) {
            return response()->json(['error' => 'Registration not found'], 404);
        }

        if (!empty($validated['name'])) {
            $expected = trim($registration->name);
            $provided = trim($validated['name']);
            if (strcasecmp($expected, $provided) !== 0) {
                return response()->json(['error' => 'Student name does not match'], 400);
            }
        }

        return response()->json([
            'status' => $registration->checked_in_at ? 'already_checked_in' : 'ready',
            'student_id' => $registration->student_id,
            'name' => $registration->name,
            'qr_token' => $registration->qr_token,
            'checked_in_at' => $registration->checked_in_at?->toIso8601String(),
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'event_id' => 'required|integer',
            'qr_token' => 'required|string',
        ]);

        $registration = Registration::where('qr_token', $validated['qr_token'])->first();

        if (!$registration) {
            return response()->json(['error' => 'Registration not found'], 404);
        }

        // Verify event_id matches
        if ($registration->event_id != $validated['event_id']) {
            return response()->json(['error' => 'Wrong event for this token'], 400);
        }

        // Check if already checked in
        if ($registration->checked_in_at) {
            return response()->json([
                'status' => 'already_checked_in',
                'checked_in_at' => $registration->checked_in_at?->toIso8601String(),
                'student_id' => $registration->student_id,
                'name' => $registration->name,
            ]);
        }

        // Update checked_in_at
        $registration->checked_in_at = now();
        $registration->save();

        return response()->json([
            'status' => 'success',
            'checked_in_at' => $registration->checked_in_at->toIso8601String(),
            'student_id' => $registration->student_id,
            'name' => $registration->name,
        ]);
    }
}
