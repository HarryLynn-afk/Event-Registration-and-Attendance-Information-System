<?php

namespace Database\Seeders;

use App\Models\Event;
use Illuminate\Database\Seeder;

class EventSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $events = [
            [
                'title' => 'Tech Talk: Introduction to AI',
                'date' => '2026-02-15',
                'time' => '14:00',
                'location' => 'Engineering Building, Room 101',
            ],
            [
                'title' => 'Career Fair 2026',
                'date' => '2026-02-20',
                'time' => '10:00',
                'location' => 'Student Center',
            ],
            [
                'title' => 'Photography Workshop',
                'date' => '2026-02-22',
                'time' => '13:00',
                'location' => 'Arts Building, Studio B',
            ],
            [
                'title' => 'Hackathon Kickoff',
                'date' => '2026-03-01',
                'time' => '09:00',
                'location' => 'Library, Floor 2',
            ],
            [
                'title' => 'Guest Lecture: Entrepreneurship',
                'date' => '2026-03-05',
                'time' => '17:00',
                'location' => 'Business School Auditorium',
            ],
            [
                'title' => 'Student Art Exhibition',
                'date' => '2026-03-10',
                'time' => '11:00',
                'location' => 'Gallery Hall',
            ],
        ];

        foreach ($events as $event) {
            Event::create($event);
        }
    }
}
