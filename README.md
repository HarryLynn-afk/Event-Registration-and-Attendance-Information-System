# Event Registration & Attendance Information System

Simple campus event registration with QR check-in and attendance dashboard.

## Features
- Student event list + registration (ID, name, email)
- QR generation after registration
- Staff check-in with verification (name + ID before approval)
- Attendance dashboard (registered vs checked-in counts)
- Role landing page (Student / Staff with PIN)

## Quick Start

### Backend (Laravel API)
```bash
cd backend
composer install
touch database/database.sqlite
php artisan migrate
php artisan db:seed --class=EventSeeder
php artisan serve --host=127.0.0.1 --port=8000
```

### Frontend (Static)
```bash
cd frontend
php -S 127.0.0.1:8001
```

Open:
- Frontend: `http://127.0.0.1:8001`
- API: `http://127.0.0.1:8000/api`

## Docs
- Integration guide: `INTEGRATION_GUIDE.md`
- Test checklist: `TEST_CHECKLIST.md`
