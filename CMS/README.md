# CMS

A Django + React content management system project.

## Structure

- frontend/ - Vite React frontend
- backend/ - Django backend
- docs/ - Project documentation

## Development

- Frontend: cd frontend && npm install && npm run dev
- Backend: copy `.env.example` to `.env`, set a unique `SECRET_KEY`, then run `cd backend && python manage.py runserver`.

`DEBUG` is enabled only when `ENVIRONMENT=development`. Production uses `ENVIRONMENT=production`, keeps debug disabled, and permits CORS only for the origins listed in `CORS_ALLOWED_ORIGINS`.

## Frontend configuration

The React frontend reads the backend URL from Vite environment files:

- `frontend/.env.development` is used by `npm run dev`.
- `frontend/.env.production` is used by `npm run build`.
- `frontend/.env.example` shows the required variable.

Set `VITE_API_BASE_URL` to your Django backend URL. Use `.env.local` or `.env.production.local` for private machine-specific overrides; those files are ignored by git.
