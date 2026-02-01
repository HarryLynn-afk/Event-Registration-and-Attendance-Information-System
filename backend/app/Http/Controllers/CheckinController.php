<?php

namespace App\Http\Controllers;

use App\Models\Registration;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class CheckinController extends Controller
{
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
            ]);
        }

        // Update checked_in_at
        $registration->checked_in_at = now();
        $registration->save();

        return response()->json([
            'status' => 'success',
            'checked_in_at' => $registration->checked_in_at->toIso8601String(),
        ]);
    }
}
