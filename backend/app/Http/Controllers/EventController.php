<?php

namespace App\Http\Controllers;

use App\Models\Event;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class EventController extends Controller
{
    public function index(): JsonResponse
    {
        $events = Event::all()->map(function ($event) {
            // Time is stored as string in format "H:i:s", extract "H:i"
            $time = substr($event->time, 0, 5);
            
            return [
                'id' => $event->id,
                'title' => $event->title,
                'date' => $event->date->format('Y-m-d'),
                'time' => $time,
                'location' => $event->location,
            ];
        });

        return response()->json($events);
    }

    public function showRegistrations(int $eventId): JsonResponse
    {
        $event = Event::find($eventId);
        
        if (!$event) {
            return response()->json(['error' => 'Event not found'], 404);
        }

        $registrations = $event->registrations()->get()->map(function ($reg) {
            return [
                'id' => $reg->id,
                'student_id' => $reg->student_id,
                'name' => $reg->name,
                'email' => $reg->email,
                'qr_token' => $reg->qr_token,
                'checked_in_at' => $reg->checked_in_at,
            ];
        });

        return response()->json($registrations);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'date' => 'required|date',
            'time' => 'required|date_format:H:i',
            'location' => 'required|string|max:255',
        ]);

        $event = Event::create($validated);

        return response()->json([
            'id' => $event->id,
            'title' => $event->title,
            'date' => $event->date->format('Y-m-d'),
            'time' => substr($event->time, 0, 5),
            'location' => $event->location,
        ], 201);
    }
}
