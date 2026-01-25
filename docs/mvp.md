# MVP Specification (v1)

## Goal
Build a working web app for college events where students register, receive a QR code, staff scan it to check in, and organizers view attendance.

## Pages (MVP)
1) Event List (Student)
- Shows all events (title, date/time, location)
- Button: Register

2) Register (Student)
- Form fields: event_id, student_id, name, email
- Submit → calls POST /api/register
- On success → go to My QR page

3) My QR (Student)
- Displays QR code for qr_token
- Shows event info + student info
- Has a button: Back to Event List

4) Staff Scan (Staff)
- Uses camera to scan QR code → gets qr_token
- Calls POST /api/checkin with event_id + qr_token
- Shows result:
  - Success
  - Already checked in
  - Invalid token
  - Wrong event

5) Dashboard (Admin/Organizer)
- Select event
- Shows counts: Registered / Checked-in
- Attendance table (student_id, name, email, status, time)
- Search by student_id or name
- Export CSV

## Rules (Business Rules)
- One registration per student per event (if same student registers again, return an error OR reuse existing token)
- Each qr_token can be checked-in only once
- Check-in must verify the token belongs to the selected event
- Manual token entry is allowed if scanning fails

## Out of Scope (for MVP)
- Payments/ticketing
- Notifications (email/SMS)
- Native mobile app
- Post-event feedback
- Advanced analytics