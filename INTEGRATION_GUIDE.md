# Frontend-Backend Integration Setup

## Overview
The Event Registration and Attendance Information System now has full frontend-backend integration. The frontend fetches events from the backend API, registers students, and generates QR codes for attendance tracking.

## Architecture

### Backend (Laravel API)
- **Base URL**: `http://localhost:8000/api`
- **CORS Enabled**: Allows frontend requests from any origin
- **Endpoints**:
  - `GET /events` - Retrieve all events
  - `POST /register` - Register a student for an event
  - `POST /checkin` - Check in a student (attendance)
  - `GET /attendance` - Retrieve attendance records

### Frontend (Static HTML/JS)
- Dynamic event loading from backend
- Registration form that posts to backend
- QR code generation using qrcode.js library
- LocalStorage for temporary session data

## Setup Instructions

### 1. Backend Setup

#### Prerequisites
- PHP 8.2+
- Composer
- SQLite (configured in .env)

#### Steps
1. Navigate to backend directory:
   ```bash
   cd /Users/kyawnainglin/Desktop/Event-Registration-and-Attendance-Information-System/project/backend
   ```

2. Install dependencies:
   ```bash
   composer install
   ```

3. Create database (if not exists):
   ```bash
   touch database/database.sqlite
   ```

4. Run migrations:
   ```bash
   php artisan migrate
   ```

5. Seed sample data (optional):
   ```bash
   php artisan db:seed --class=EventSeeder
   ```

6. Start the development server:
   ```bash
   php artisan serve
   ```
   The API will be available at: `http://localhost:8000`

### 2. Frontend Setup

#### Prerequisites
- A modern web browser
- HTTP server (for proper CORS handling)

#### Option A: Using PHP Built-in Server
1. Navigate to frontend directory:
   ```bash
   cd /Users/kyawnainglin/Desktop/Event-Registration-and-Attendance-Information-System/project/frontend
   ```

2. Start the development server:
   ```bash
   php -S localhost:8001
   ```
   The frontend will be available at: `http://localhost:8001`

#### Option B: Using Python HTTP Server
1. Navigate to frontend directory:
   ```bash
   cd /Users/kyawnainglin/Desktop/Event-Registration-and-Attendance-Information-System/project/frontend
   ```

2. Start the development server:
   ```bash
   python3 -m http.server 8001
   ```
   The frontend will be available at: `http://localhost:8001`

### 3. Verification

#### Check Backend is Running
- Visit `http://localhost:8000/api/events` in your browser
- You should see a JSON array of events (may be empty initially)

#### Check Frontend is Running
- Visit `http://localhost:8001` in your browser
- You should see the Campus Events page with event cards loaded from the backend

## API Endpoints Documentation

### GET /api/events
**Description**: Retrieve all events

**Response (200 OK)**:
```json
[
    {
        "id": 1,
        "title": "Tech Talk: Introduction to AI",
        "date": "2026-02-15",
        "time": "14:00",
        "location": "Engineering Building, Room 101"
    },
    ...
]
```

### POST /api/register
**Description**: Register a student for an event

**Request Body**:
```json
{
    "event_id": 1,
    "student_id": "STU001",
    "name": "John Doe",
    "email": "john@example.com"
}
```

**Response (201 Created)**:
```json
{
    "registration_id": 1,
    "event_id": 1,
    "student_id": "STU001",
    "name": "John Doe",
    "email": "john@example.com",
    "qr_token": "EV1-ABC12345"
}
```

### POST /api/checkin
**Description**: Check in a student (mark attendance)

**Request Body**:
```json
{
    "registration_id": 1
}
```

**Response (200 OK)**:
```json
{
    "id": 1,
    "registration_id": 1,
    "checked_in_at": "2026-02-15T14:30:00Z"
}
```

### GET /api/attendance
**Description**: Retrieve all attendance records

**Response (200 OK)**:
```json
[
    {
        "id": 1,
        "registration_id": 1,
        "checked_in_at": "2026-02-15T14:30:00Z"
    },
    ...
]
```

## Frontend Files Overview

### api.js
Central API utility file containing functions for:
- `fetchEvents()` - Get all events
- `registerStudent()` - Register for an event
- `checkinStudent()` - Check in to an event
- `fetchAttendance()` - Get attendance records

### index.html
- Dynamically loads events from backend API
- Displays event cards in a responsive grid
- Routes to registration page when "Register" is clicked

### register.html
- Collects student information (ID, name, email)
- Posts registration data to backend API
- Receives and stores QR token from backend
- Redirects to QR code display page

### qr.html
- Generates QR code from the registration token
- Uses qrcode.js library for QR generation
- Displays student name and event information
- QR code contains the token needed for check-in

## Frontend Usage Flow

1. **Home Page** (`index.html`)
   - User sees list of events fetched from backend
   - Click "Register" on any event

2. **Registration Page** (`register.html`)
   - User enters: Student ID, Name, Email
   - Click "Submit"
   - Data is sent to backend API
   - Backend validates and creates registration
   - Backend generates unique QR token

3. **QR Code Page** (`qr.html`)
   - User sees generated QR code with their token
   - Token can be scanned for check-in/attendance

## Troubleshooting

### Issue: Events not loading on frontend
**Solution**:
1. Check that backend is running: `php artisan serve`
2. Check browser console for CORS errors (F12)
3. Verify database has events: Run `php artisan db:seed --class=EventSeeder`
4. Check backend API directly: Visit `http://localhost:8000/api/events`

### Issue: Registration fails
**Solution**:
1. Ensure all form fields are filled
2. Check browser console for error messages
3. Verify backend API is responding: `curl http://localhost:8000/api/events`
4. Check Laravel logs: `tail -f storage/logs/laravel.log`

### Issue: CORS errors in browser console
**Solution**:
1. Backend must have CORS middleware enabled (already done)
2. Frontend must use correct API base URL in api.js
3. Ensure backend server is running

### Issue: QR code not generating
**Solution**:
1. Check that qrcode.js library loaded: Open DevTools → Network tab
2. Verify localStorage contains qrToken
3. Check browser console for JavaScript errors

## Database Schema

### Events Table
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    date DATE,
    time TIME,
    location VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Registrations Table
```sql
CREATE TABLE registrations (
    id INTEGER PRIMARY KEY,
    event_id INTEGER,
    student_id VARCHAR(255),
    name VARCHAR(255),
    email VARCHAR(255),
    qr_token VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Attendance Table
```sql
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY,
    registration_id INTEGER,
    checked_in_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## Next Steps (Optional Enhancements)

1. Add authentication (Login/Logout)
2. Add dashboard for attendance tracking
3. Deploy to production server
4. Add email notifications on registration
5. Implement QR scanning for attendance
6. Add event management admin panel
7. Add student dashboard to view registrations
