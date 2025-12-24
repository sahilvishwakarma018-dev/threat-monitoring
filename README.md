## Overview
Threat monitoring backend built using Django & DRF.

## Features
- JWT Authentication
- Role-based access
- Event ingestion
- Auto alert generation

## Setup
1. Clone repo
2. Create venv
3. Install requirements
4. Run migrations
5. Create admin & analyst users

## API Endpoints
POST /api/events/
GET /api/alerts/
PATCH /api/alerts/{id}/

## Assumptions
- Only high/critical events generate alerts
- Admin manages alerts

# Threat Monitoring & Alert Management Backend

## Overview
A backend API system built using Django and Django REST Framework for ingesting security events and managing alerts. Designed with a security-first approach and role-based access control.

## Features
- JWT Authentication
- Role-based access (Admin / Analyst)
- Event ingestion API
- Automatic alert generation for high/critical threats
- Alert filtering by severity and status
- Rate limiting and logging
- Swagger API documentation
- Dockerized setup

## Tech Stack
- Python, Django, DRF
- PostgreSQL
- JWT (SimpleJWT)
- Docker & Docker Compose

## Setup (Local)
```bash
git clone <repo_url>
cd threat_monitoring
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
