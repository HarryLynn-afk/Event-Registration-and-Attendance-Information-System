// Configuration
const API_BASE_URL = 'http://localhost:8000/api';

function getStaffHeaders() {
    const headers = {
        'Content-Type': 'application/json',
    };
    const staffPin = sessionStorage.getItem("staffPin");
    if (staffPin) {
        headers['X-Staff-PIN'] = staffPin;
    }
    return headers;
}

// Get all events
async function fetchEvents() {
    try {
        const response = await fetch(`${API_BASE_URL}/events`);
        if (!response.ok) {
            throw new Error('Failed to fetch events');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching events:', error);
        return [];
    }
}

// Create a new event (staff)
async function createEvent(title, date, time, location) {
    try {
        const response = await fetch(`${API_BASE_URL}/events`, {
            method: 'POST',
            headers: getStaffHeaders(),
            body: JSON.stringify({
                title: title,
                date: date,
                time: time,
                location: location,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            return {
                error: data.error || data.message || 'Failed to create event',
            };
        }

        return data;
    } catch (error) {
        console.error('Error creating event:', error);
        return {
            error: error.message || 'Network error. Please try again.',
        };
    }
}

// Register a student for an event
async function registerStudent(eventId, studentId, name, email) {
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                event_id: parseInt(eventId),
                student_id: studentId,
                name: name,
                email: email,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            console.error('Registration error:', data);
            return {
                error: data.error || data.message || 'Failed to register',
                qr_token: null
            };
        }

        return data;
    } catch (error) {
        console.error('Error registering student:', error);
        return {
            error: error.message || 'Network error. Please try again.',
            qr_token: null
        };
    }
}

// Check in a student (staff)
async function checkinStudent(eventId, qrToken) {
    try {
        const response = await fetch(`${API_BASE_URL}/checkin`, {
            method: 'POST',
            headers: getStaffHeaders(),
            body: JSON.stringify({
                event_id: parseInt(eventId),
                qr_token: qrToken,
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to check in');
        }

        return await response.json();
    } catch (error) {
        console.error('Error checking in:', error);
        return null;
    }
}

// Get attendance records (staff)
async function fetchAttendance(eventId) {
    try {
        if (!eventId) {
            return [];
        }
        const response = await fetch(`${API_BASE_URL}/attendance?event_id=${encodeURIComponent(eventId)}`, {
            headers: getStaffHeaders(),
        });
        if (!response.ok) {
            throw new Error('Failed to fetch attendance');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching attendance:', error);
        return [];
    }
}
