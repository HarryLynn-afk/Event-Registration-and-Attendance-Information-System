# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
No authentication required for MVP (can be added later for admin/staff endpoints).

---

## Endpoints

### 1. List Events

Get all available events.

**Endpoint:** `GET /api/events`

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Tech Talk: Introduction to AI",
    "date": "2026-02-15",
    "time": "14:00",
    "location": "Engineering Building, Room 101"
  },
  {
    "id": 2,
    "title": "Career Fair 2026",
    "date": "2026-02-20",
    "time": "10:00",
    "location": "Student Center"
  }
]
```

**Example:**
```bash
curl http://localhost:8000/api/events
```

---

### 2. Register for Event

Register a student for an event. Returns a unique QR token for check-in.

**Endpoint:** `POST /api/register`

**Request Body:**
```json
{
  "event_id": 1,
  "student_id": "65001234",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response:** `201 Created`

```json
{
  "registration_id": 10,
  "event_id": 1,
  "student_id": "65001234",
  "name": "John Doe",
  "email": "john@example.com",
  "qr_token": "EV1-AB12CD34"
}
```

**Error Responses:**
- `400 Bad Request` - Missing or invalid fields
- `404 Not Found` - Event not found

**Business Rules:**
- One registration per student per event
- If student already registered, returns existing registration with same QR token
- QR token format: `EV{event_id}-{8 character alphanumeric}`

**Example:**
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "student_id": "65001234",
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

---

### 3. Check-In (Scan QR)

Check in a registered student using their QR token.

**Endpoint:** `POST /api/checkin`

**Request Body:**
```json
{
  "event_id": 1,
  "qr_token": "EV1-AB12CD34"
}
```

**Response:** `200 OK` (Success)

```json
{
  "status": "success",
  "checked_in_at": "2026-02-01T10:03:20+00:00"
}
```

**Response:** `200 OK` (Already Checked In)

```json
{
  "status": "already_checked_in"
}
```

**Error Responses:**
- `400 Bad Request` - Wrong event for this token (token belongs to another event)
- `404 Not Found` - Registration not found (invalid token)

**Business Rules:**
- Each QR token can only be checked in once
- Event ID must match the event the token was issued for
- Check-in timestamp is recorded when first checked in

**Example:**
```bash
curl -X POST http://localhost:8000/api/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "qr_token": "EV1-AB12CD34"
  }'
```

---

### 4. Get Attendance List

Get attendance list for a specific event.

**Endpoint:** `GET /api/attendance?event_id=1`

**Query Parameters:**
- `event_id` (required, integer) - The event ID

**Response:** `200 OK`

```json
[
  {
    "student_id": "65001234",
    "name": "John Doe",
    "email": "john@example.com",
    "checked_in": true,
    "checked_in_at": "2026-02-01T10:03:20+00:00"
  },
  {
    "student_id": "65001235",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "checked_in": false,
    "checked_in_at": null
  }
]
```

**Error Responses:**
- `400 Bad Request` - Missing or invalid event_id
- `404 Not Found` - Event not found

**Example:**
```bash
curl http://localhost:8000/api/attendance?event_id=1
```

---

## Data Models

### Event
- `id` (integer) - Unique event identifier
- `title` (string) - Event name
- `date` (date, format: YYYY-MM-DD) - Event date
- `time` (time, format: HH:MM) - Event time
- `location` (string) - Event location

### Registration
- `id` (integer) - Registration ID
- `event_id` (integer) - Foreign key to events table
- `student_id` (string) - Student identifier (preserves leading zeros)
- `name` (string) - Student full name
- `email` (string) - Student email address
- `qr_token` (string, unique) - QR code token for check-in
- `checked_in_at` (timestamp, nullable) - Check-in timestamp
- `created_at` (timestamp) - Registration timestamp
- `updated_at` (timestamp) - Last update timestamp

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid input or business rule violation
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors (Laravel default)

Error response format:
```json
{
  "error": "Error message description"
}
```

---

## Frontend Integration

### Event List Page (`index.html`)
- Uses: `GET /api/events`
- Fetches and displays all events

### Registration Page (`register.html`)
- Uses: `POST /api/register`
- Submits registration form
- Receives QR token in response
- Stores token in localStorage for QR page

### QR Code Page (`qr.html`)
- Uses: QR token from registration response
- Displays QR code (frontend generates from token)

### Dashboard Page (`dashboard.html`)
- Uses: `GET /api/attendance?event_id=X`
- Fetches attendance list for selected event
- Displays registered count, checked-in count, and attendance table

### Staff Scan Page (to be implemented)
- Uses: `POST /api/checkin`
- Scans QR code and submits check-in request

---

## Testing

### Using cURL

**List Events:**
```bash
curl http://localhost:8000/api/events
```

**Register:**
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"event_id":1,"student_id":"12345","name":"Test User","email":"test@example.com"}'
```

**Check-In:**
```bash
curl -X POST http://localhost:8000/api/checkin \
  -H "Content-Type: application/json" \
  -d '{"event_id":1,"qr_token":"EV1-AB12CD34"}'
```

**Get Attendance:**
```bash
curl http://localhost:8000/api/attendance?event_id=1
```

### Using Postman or Similar Tools

1. Set base URL: `http://localhost:8000/api`
2. For POST requests, set `Content-Type: application/json`
3. Include JSON body for POST requests
4. Use query parameters for GET requests

---

## Database Schema

### events table
```sql
id (primary key)
title (string)
date (date)
time (time)
location (string)
created_at (timestamp)
updated_at (timestamp)
```

### registrations table
```sql
id (primary key)
event_id (foreign key -> events.id)
student_id (string)
name (string)
email (string)
qr_token (string, unique, indexed)
checked_in_at (timestamp, nullable)
created_at (timestamp)
updated_at (timestamp)

Unique constraint: (event_id, student_id)
```

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- Student IDs are stored as strings to preserve leading zeros
- QR tokens are unique across all registrations
- One registration per student per event (enforced by unique constraint)
- Check-in can only happen once per registration
- Event ID validation ensures QR tokens are only used for correct events

---

## Future Enhancements

- Authentication for admin/staff endpoints
- Email notifications
- QR code generation on backend
- Export attendance to CSV
- Search and filter functionality
- Event capacity limits
- Waitlist functionality

