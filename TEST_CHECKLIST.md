# End-to-End QR Integration Test Checklist

## Prerequisites
- ✅ Backend running: `php artisan serve` (http://localhost:8000)
- ✅ Frontend running: `php -S localhost:8001` (http://localhost:8001)
- ✅ Database migrated: `php artisan migrate`
- ✅ Sample data seeded: `php artisan db:seed --class=EventSeeder`
- ✅ Browser DevTools open to monitor network requests

---

## Test Flow: Registration → QR → Check-in → Dashboard

### **STEP 1: Verify Backend API is Ready**

#### Command:
```bash
curl -X GET http://localhost:8000/api/events
```

#### Expected Output:
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
    },
    ...
]
```

**UI Check**: Open browser DevTools → Network tab (keep it open)

---

### **STEP 2: Test Registration Flow (UI)**

**Navigation**: Open http://localhost:8001

#### Page: index.html (Events List)
**Expected UI Elements**:
- ✅ Header: "Campus Events" + "Upcoming Events"
- ✅ Dashboard button (📊) in top right
- ✅ Event cards displayed dynamically from API
- ✅ Each card shows: Title, Date, Time, Location, Register button
- ✅ Cards arranged in responsive grid

**Network Check** (DevTools):
- Request: `GET http://localhost:8000/api/events`
- Status: 200
- Response: Array of events

**User Action**: Click "Register" on **Event 1** (Tech Talk: Introduction to AI)

**Navigation**: → register.html

---

### **STEP 3: Verify Registration Page**

#### Page: register.html
**Expected UI Elements**:
- ✅ Header: "Campus Events"
- ✅ Form title: "Event Registration"
- ✅ Input fields:
  - Student ID
  - Full Name
  - Email Address
- ✅ Submit button (blue)
- ✅ Error message box (hidden initially)

**Storage Check** (DevTools → Application → LocalStorage):
```
selectedEventId: "1"
selectedEvent: "Tech Talk: Introduction to AI"
```

**Test Registration Data**:
- Student ID: `STU001`
- Full Name: `John Doe`
- Email: `john.doe@university.edu`

**User Action**: Fill form and click "Submit"

---

### **STEP 4: Test API Registration (Backend)**

#### Command (Manual API Test):
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "student_id": "STU002",
    "name": "Jane Smith",
    "email": "jane.smith@university.edu"
  }'
```

#### Expected Output:
```json
{
    "registration_id": 1,
    "event_id": 1,
    "student_id": "STU002",
    "name": "Jane Smith",
    "email": "jane.smith@university.edu",
    "qr_token": "EV1-ABC12345"
}
```

**Status**: 201 Created

---

### **STEP 5: Verify Registration Success & Redirect**

**Network Check** (DevTools):
- Request: `POST http://localhost:8000/api/register`
- Status: 201
- Response: Contains `qr_token`
- No error in Console tab

**UI Behavior**:
- ✅ Submit button shows "Submitting..." and is disabled
- ✅ No error message shown
- ✅ Page redirects to qr.html within 1-2 seconds

---

### **STEP 6: Verify QR Code Page**

#### Page: qr.html
**Expected UI Elements**:
- ✅ Header: "Campus Events"
- ✅ Title: "Your QR Code" (or similar)
- ✅ **QR Code Image** (must be visible and scannable)
- ✅ Student Name: "John Doe"
- ✅ Event Name: "Tech Talk: Introduction to AI"
- ✅ Token displayed: "EV1-ABC12345"
- ✅ Back button

**Storage Check** (DevTools → Application → LocalStorage):
```
qr_token: "EV1-ABC12345"
event_id: "1"
student_name: "John Doe"
event_title: "Tech Talk: Introduction to AI"
```

**QR Code Verification**:
- Right-click QR code → Open in new tab
- Should show canvas-generated image
- Scan with phone camera or QR reader
- Should decode to: `{"event_id":1,"qr_token":"EV1-ABC12345"}`

---

### **STEP 7: Test Check-In Success**

#### Option A: Via Check-In Page (Manual)

**Navigation**: Click Back → Dashboard → "📱 Staff Check-In"

#### Page: checkin.html
**Expected UI Elements**:
- ✅ Header and title
- ✅ Camera section with Start/Stop buttons
- ✅ Manual entry fields (Event ID, QR Token)
- ✅ Check In button

**Test Method 1 - Manual Entry**:
- Event ID: `1`
- QR Token: `EV1-ABC12345`
- Click "Check In"

**Network Check**:
- Request: `POST http://localhost:8000/api/checkin`
- Payload:
  ```json
  {
    "event_id": 1,
    "qr_token": "EV1-ABC12345"
  }
  ```
- Status: 200
- Response:
  ```json
  {
    "status": "success",
    "checked_in_at": "2026-02-02T14:30:45.000000Z"
  }
  ```

**UI Behavior**:
- ✅ Button shows "Checking in..." and is disabled
- ✅ Success message appears (blue background):
  ```
  ✓ Check-in successful!
  Checked in at: 2/2/2026, 2:30:45 PM
  ```
- ✅ Fields clear automatically
- ✅ Message scrolls into view
- ✅ Button re-enabled after 1-2 seconds

#### Option B: Via API (Curl)
```bash
curl -X POST http://localhost:8000/api/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "qr_token": "EV1-ABC12345"
  }'
```

Expected Response (201/200):
```json
{
    "status": "success",
    "checked_in_at": "2026-02-02T14:30:45.000000Z"
}
```

---

### **STEP 8: Test Duplicate Check-In Blocked**

**Same Page: checkin.html**

**User Action**: Re-submit same token immediately
- Event ID: `1`
- QR Token: `EV1-ABC12345`
- Click "Check In"

#### Expected API Response:
```json
{
    "status": "already_checked_in"
}
```

**UI Behavior**:
- ✅ Warning message appears (yellow background):
  ```
  ⚠ Already checked in for this event.
  ```
- ✅ Fields not cleared (allowing staff to see what was attempted)
- ✅ No timestamp shown (just the warning)

#### Via Curl:
```bash
curl -X POST http://localhost:8000/api/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "qr_token": "EV1-ABC12345"
  }'
```

Response:
```json
{
    "status": "already_checked_in"
}
```

---

### **STEP 9: Test Invalid Token Error**

**Same Page: checkin.html**

**User Action**: Try with invalid token
- Event ID: `1`
- QR Token: `INVALID-TOKEN-12345`
- Click "Check In"

#### Expected API Response:
```json
{
    "error": "Registration not found"
}
```
Status: 404

**UI Behavior**:
- ✅ Error message appears (red background):
  ```
  Registration not found
  ```
- ✅ Fields remain filled for correction
- ✅ Button re-enabled immediately

#### Via Curl:
```bash
curl -X POST http://localhost:8000/api/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "qr_token": "INVALID-TOKEN"
  }'
```

Response: 404
```json
{
    "error": "Registration not found"
}
```

---

### **STEP 10: Test Wrong Event Error**

**Same Page: checkin.html**

**User Action**: Use token from event 1 but wrong event ID
- Event ID: `2` (different event)
- QR Token: `EV1-ABC12345` (from event 1)
- Click "Check In"

#### Expected API Response:
```json
{
    "error": "Wrong event for this token"
}
```
Status: 400

**UI Behavior**:
- ✅ Error message appears (red background):
  ```
  Wrong event for this token
  ```

#### Via Curl:
```bash
curl -X POST http://localhost:8000/api/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 2,
    "qr_token": "EV1-ABC12345"
  }'
```

---

### **STEP 11: Verify Dashboard Shows Check-In Status**

**Navigation**: Click "Back to Dashboard" or go to dashboard.html

#### Page: dashboard.html
**Expected UI Elements**:
- ✅ Header with "Staff Check-In" button (📱)
- ✅ Event dropdown (populated from API)
- ✅ Summary cards: "Total Registered", "Total Checked-in"
- ✅ Attendance table with columns:
  - Student ID
  - Name
  - Email
  - Check-in Status

**User Action**: Select "Tech Talk: Introduction to AI" from dropdown

**Network Check**:
- Request: `GET http://localhost:8000/api/events/1/registrations`
- Status: 200
- Response: Array of registrations for that event

#### Expected API Response:
```json
[
    {
        "id": 1,
        "student_id": "STU001",
        "name": "John Doe",
        "email": "john.doe@university.edu",
        "qr_token": "EV1-ABC12345",
        "checked_in_at": "2026-02-02T14:30:45.000000Z"
    },
    {
        "id": 2,
        "student_id": "STU002",
        "name": "Jane Smith",
        "email": "jane.smith@university.edu",
        "qr_token": "EV1-ABCDEFG",
        "checked_in_at": null
    }
]
```

**UI Behavior**:
- ✅ Summary cards update:
  - Total Registered: `2`
  - Total Checked-in: `1`
- ✅ Table displays with rows:
  | Student ID | Name | Email | Status |
  |---|---|---|---|
  | STU001 | John Doe | john.doe@... | ✓ Checked In (blue badge) |
  | STU002 | Jane Smith | jane.smith@... | Not Checked In (gray badge) |

**Verification**:
- ✅ "Checked In" students show blue badge with checkmark
- ✅ "Not Checked In" students show gray badge
- ✅ Data matches API response exactly

---

### **STEP 12: Test Multiple Students End-to-End**

**Repeat Steps 2-11 with different data**:

#### Student 2:
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "student_id": "STU003",
    "name": "Bob Johnson",
    "email": "bob.johnson@university.edu"
  }'
```

Response:
```json
{
    "registration_id": 3,
    "qr_token": "EV1-XYZ98765",
    ...
}
```

**Check-in Student 3**:
```bash
curl -X POST http://localhost:8000/api/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "qr_token": "EV1-XYZ98765"
  }'
```

**Dashboard Verification**:
- Total Registered: `3`
- Total Checked-in: `2`
- Table shows all 3 with correct statuses

---

### **STEP 13: Test Multiple Events**

**Register for Different Event**:
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 2,
    "student_id": "STU001",
    "name": "John Doe",
    "email": "john.doe@university.edu"
  }'
```

**Expected**: Different QR token (format: `EV2-XXXXXX`)
```json
{
    "registration_id": 4,
    "event_id": 2,
    "qr_token": "EV2-DEF45678",
    ...
}
```

**Dashboard - Switch Events**:
- Select "Career Fair 2026" (Event 2)
- Should show only registrations for Event 2
- Summary cards update accordingly

---

### **STEP 14: Verify Database State**

**Check Registrations Table**:
```bash
sqlite3 database/database.sqlite
```

```sql
SELECT id, event_id, student_id, name, qr_token, checked_in_at FROM registrations;
```

**Expected Output** (example):
```
1|1|STU001|John Doe|EV1-ABC12345|2026-02-02 14:30:45
2|1|STU002|Jane Smith|EV1-ABCDEFG|
3|1|STU003|Bob Johnson|EV1-XYZ98765|2026-02-02 14:35:20
4|2|STU001|John Doe|EV2-DEF45678|
```

- ✅ `checked_in_at` populated only for checked-in students
- ✅ QR tokens unique and match UI
- ✅ Event IDs correct for each registration

---

## Summary Checklist

### Registration Flow ✅
- [ ] Events load from API (index.html)
- [ ] Register button stores event_id and event_title
- [ ] Registration form validates all fields
- [ ] API returns registration_id and qr_token

### QR Generation ✅
- [ ] QR code displays on qr.html
- [ ] QR code encodes JSON: `{event_id, qr_token}`
- [ ] localStorage stores all 4 required values
- [ ] QR is scannable by phone camera

### Check-In Success ✅
- [ ] Manual entry works (Event ID + Token)
- [ ] API returns status: "success"
- [ ] UI shows success message with timestamp
- [ ] Form clears for next student

### Duplicate Prevention ✅
- [ ] Second check-in returns status: "already_checked_in"
- [ ] UI shows warning message
- [ ] No timestamp in response

### Error Handling ✅
- [ ] Invalid token → "Registration not found" (404)
- [ ] Wrong event ID → "Wrong event for this token" (400)
- [ ] All error messages display clearly

### Dashboard Verification ✅
- [ ] Event dropdown populated from API
- [ ] Summary cards show correct counts
- [ ] Table shows all registrations with status
- [ ] Status badges color-coded correctly
- [ ] Data updates when event selected

### Database Integrity ✅
- [ ] Registrations stored correctly
- [ ] QR tokens unique per registration
- [ ] checked_in_at timestamp only for checked-in students
- [ ] Event constraints enforced

---

## Cleanup (Optional)

Reset database:
```bash
cd backend
php artisan migrate:refresh --seed
```

This re-creates all tables and re-seeds sample events.

---

## Notes for Testing

1. **Browser Storage**: Clear localStorage between full test cycles
   - DevTools → Application → Storage → Clear Site Data

2. **Network Errors**: Check DevTools Console tab for any JavaScript errors

3. **CORS Issues**: Should not occur - CORS middleware enabled in backend

4. **Timestamp Format**: Times may vary by timezone - just verify format is valid

5. **QR Code Scanning**: 
   - Test with phone camera (Google Lens, native camera app)
   - Or use online QR decoder: https://zxing.org/w/decode.jspx

6. **Stress Test**: Create 10+ registrations and verify dashboard handles pagination (if implemented)

