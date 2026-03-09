# Database Design — Event Registration & Attendance System

## ER Diagram

```
┌──────────────────┐              ┌──────────────────────────┐
│      events      │              │       registrations       │
├──────────────────┤  1        *  ├──────────────────────────┤
│ id         (PK)  │──────────────│ id           (PK)        │
│ title            │              │ event_id     (FK→events) │
│ date             │              │ student_id               │
│ time             │              │ name                     │
│ location         │              │ email                    │
│ created_at       │              │ qr_token     (unique)    │
│ updated_at       │              │ checked_in_at (nullable) │
└──────────────────┘              │ created_at               │
                                  │ updated_at               │
                                  └──────────────────────────┘

┌──────────────────────┐
│        users         │   (admin / staff accounts)
├──────────────────────┤
│ id              (PK) │
│ name                 │
│ email        (unique)│
│ email_verified_at    │
│ password             │
│ remember_token       │
│ created_at           │
│ updated_at           │
└──────────────────────┘
```

## Relationships

| Relationship | Type | Description |
|---|---|---|
| events → registrations | One-to-Many | One event has many registrations |
| (event_id, student_id) | Unique | A student can only register once per event |
| qr_token | Unique | Each registration has a unique QR code for check-in |

## Table Descriptions

### `events`
Stores event information such as title, date, time, and location.

### `registrations`
Links students to events. Tracks whether a student has checked in via `checked_in_at` (null = not yet checked in). The `qr_token` is used for QR code-based attendance tracking.

### `users`
System accounts for staff/administrators who manage events and attendance.

---

## Laravel Framework Tables (supporting infrastructure)

| Table | Purpose |
|---|---|
| `password_reset_tokens` | Password reset flow |
| `sessions` | User session storage |
| `cache` / `cache_locks` | Application caching |
| `jobs` / `job_batches` / `failed_jobs` | Queue job processing |
