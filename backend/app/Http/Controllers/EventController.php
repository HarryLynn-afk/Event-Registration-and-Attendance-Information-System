<?php

namespace App\Http\Controllers;

use App\Models\Event;
use Illuminate\Http\JsonResponse;

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
}
