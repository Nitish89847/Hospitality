# Hospitality — Insurance-Aware Hospital & Care Navigation

A full-stack platform that helps patients and caregivers navigate hospital admission using their insurance coverage as a guiding constraint — mapping policy details to eligible hospitals, room categories, and real-time out-of-pocket cost estimates.

**Live demo:** https://hospitality-fawn.vercel.app

**API:** https://hospitality-backend-ojog.onrender.com


## Problem

During hospital admissions, patients and caregivers often can't get timely answers to basic questions: which hospitals accept my insurance, what room category is covered, and what will I actually owe out of pocket. This app consolidates policy rules, hospital data, and a real coverage-calculation engine into one place.

## Tech Stack

- **Frontend:** Next.js (App Router), React, TypeScript, Tailwind CSS
- **Backend:** Django, Django REST Framework, JWT authentication
- **Database:** PostgreSQL
- **Deployment:** Render (backend + Postgres), Vercel (frontend)

## Key Features

- Insurance policy ingestion with structured room eligibility, co-pay, and exclusions
- Hospital matching via private insurer networks or government scheme empanelment
- Room-level eligibility engine calculating coverage, cap-excess cost, co-pay, and ICU-specific handling
- Care journey tracking (admission → investigation → procedure → recovery → discharge)
- JWT authentication with refresh token handling

## ICU coverage with different logic

Regular room categories form a natural tier ladder — a policy covering "up to semi-private" also covers everything below it. ICU doesn't fit this ladder: it's a different kind of care with its own cap and coverage rules. The eligibility engine routes ICU and non-ICU categories through two separate coverage functions, a decision that I came out of manually verifying edge cases during development.

## Testing

python manage.py test hospitals

## Running Locally

**Backend:**

cd backend

python -m venv env

env\Scripts\activate

pip install -r requirements.txt

create .env with DATABASE_URL, SECRET_KEY, DEBUG, ALLOWED_HOSTS

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver


**Frontend:**

cd frontend

npm install

npm run dev