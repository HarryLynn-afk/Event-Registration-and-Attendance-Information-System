

Event Registration & Attendance Information System — API Contract (v1)

Base URL (local): http://localhost:8000
Auth: none for Milestone 0–1 (can add staff/admin login later)

⸻

Data rules (shared)
	•	event_id is an integer
	•	student_id is a string (keeps leading zeros)
	•	qr_token is a unique string per registration
	•	A registration can be checked-in only once

⸻

1) List events

GET /api/events

Response 200

[
  {
    "id": 1,
    "title": "Orientation 2026",
    "date": "2026-02-01",
    "time": "10:00",
    "location": "Room 101"
  }
]


⸻

2) Register for an event (generate QR token)

POST /api/register

Request body

{
  "event_id": 1,
  "student_id": "65001234",
  "name": "Kyaw Naing Lin",
  "email": "example@email.com"
}

Response 201

{
  "registration_id": 10,
  "event_id": 1,
  "student_id": "65001234",
  "name": "Kyaw Naing Lin",
  "email": "example@email.com",
  "qr_token": "EV1-AB12CD34"
}

Errors
	•	400 missing/invalid fields
	•	404 event not found

⸻

3) Check-in (scan QR)

POST /api/checkin

Request body

{
  "event_id": 1,
  "qr_token": "EV1-AB12CD34"
}

Response 200 (success)

{
  "status": "success",
  "checked_in_at": "2026-02-01T10:03:20"
}

Response 200 (already checked in)

{
  "status": "already_checked_in"
}

Errors
	•	404 registration not found (invalid token)
	•	400 wrong event for this token (token belongs to another event)

⸻

4) Attendance list (for dashboard)

GET /api/attendance?event_id=1

Response 200

[
  {
    "student_id": "65001234",
    "name": "Kyaw Naing Lin",
    "email": "example@email.com",
    "checked_in": true,
    "checked_in_at": "2026-02-01T10:03:20"
  }
]

Errors
	•	404 event not found

⸻

Notes (frontend pages that use these)
	•	Event List page → GET /api/events
	•	Register page → POST /api/register
	•	My QR page → uses qr_token from register response
	•	Staff Scan page → POST /api/checkin
	•	Dashboard page → GET /api/attendance

⸻
