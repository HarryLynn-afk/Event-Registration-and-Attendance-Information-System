<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class StaffPinMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        $configuredPin = env('STAFF_PIN');

        if (!$configuredPin) {
            return $next($request);
        }

        $providedPin = $request->header('X-Staff-PIN');

        if ($providedPin !== $configuredPin) {
            return response()->json(['error' => 'Unauthorized'], 403);
        }

        return $next($request);
    }
}
