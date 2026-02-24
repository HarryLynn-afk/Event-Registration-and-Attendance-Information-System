#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Event Registration System - Integration${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if backend is running
echo -e "${YELLOW}1. Checking Backend...${NC}"
if curl -s http://localhost:8000/api/events > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is running at http://localhost:8000${NC}"
else
    echo -e "${RED}✗ Backend is not running${NC}"
    echo -e "${YELLOW}   Start it with: cd backend && php artisan serve${NC}"
fi

# Check if frontend is running
echo ""
echo -e "${YELLOW}2. Checking Frontend...${NC}"
if curl -s http://localhost:8001 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend is running at http://localhost:8001${NC}"
else
    echo -e "${RED}✗ Frontend is not running${NC}"
    echo -e "${YELLOW}   Start it with: cd frontend && php -S localhost:8001${NC}"
    echo -e "${YELLOW}   OR: cd frontend && python3 -m http.server 8001${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}System URLs${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Frontend:${NC}  http://localhost:8001"
echo -e "${GREEN}Backend API:${NC}  http://localhost:8000/api"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}API Endpoints${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "GET    /api/events        - Get all events"
echo -e "POST   /api/register      - Register a student"
echo -e "POST   /api/checkin       - Check in attendance"
echo -e "GET    /api/attendance    - Get attendance records"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Quick Commands${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Backend Setup:"
echo -e "  cd backend"
echo -e "  composer install"
echo -e "  php artisan migrate"
echo -e "  php artisan db:seed --class=EventSeeder"
echo -e "  php artisan serve"
echo ""
echo -e "Frontend Setup:"
echo -e "  cd frontend"
echo -e "  php -S localhost:8001"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Integration Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
