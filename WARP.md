# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Django 5.1 project with two main apps:
- **api**: Simple REST API with basic Item model (demo/example)
- **club**: Full-featured motorcycle club management system with profiles, rides, and polls

The club app is the primary application and serves as the home page.

## Python Environment

This project uses **uv** for Python package management, not pip. The virtual environment is located at `.venv/`.

Dependencies are managed in:
- `pyproject.toml` (primary source)
- `requirements.txt` (generated/legacy)

## Common Development Commands

### Server & Development
```bash
# Start Django development server
python manage.py runserver

# Watch/rebuild Tailwind CSS (in separate terminal)
npm run dev

# Build Tailwind CSS (production)
npm run build
```

### Database Operations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test api
python manage.py test club
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic
```

## Architecture

### URL Structure
The project uses a nested URL configuration:
- Root URLconf: `config/urls.py`
- Club app (primary): `/club/` and `/` (mapped to home)
- API app: `/api/`
- Frontend app: `/frontend/` (legacy, kept for compatibility)

### Apps

**config/**: Django project settings
- `settings.py`: Loads environment variables from `.env`, configures REST Framework, CORS, static/media files
- Django settings module: `config.settings`

**api/**: Simple REST API demo
- Single `Item` model with basic CRUD operations
- Uses DRF ViewSets and routers
- Endpoints: `/api/items/`

**club/**: Motorcycle club management (primary app)
- **Models**: Profile (user profiles with avatars/bike photos), Ride (motorcycle rides with GPX support), Poll/PollChoice/Vote (voting system)
- **Views**: Mix of function-based views for frontend pages and DRF ViewSets for API
- **Templates**: Located in `club/templates/club/`, uses `base.html` as parent template
- **Frontend endpoints**: Home, rides list/detail, polls, members, profile editing, auth
- **API endpoints**: RESTful API at `/club/api/` for profiles, rides, and polls
- **Custom API actions**: 
  - `/club/api/profiles/me/` - current user's profile
  - `/club/api/rides/upcoming/` - next upcoming ride
  - `/club/api/rides/<id>/join/` and `/club/api/rides/<id>/leave/` - ride participation
  - `/club/api/polls/active/` - current active poll
  - `/club/api/polls/<id>/vote/` - submit vote

**frontend/**: Original frontend app (now secondary, club is primary)

### Frontend Stack
- **CSS**: Tailwind CSS v3.4 (configured to scan all `**/templates/**/*.html`)
- **JavaScript**: Alpine.js for interactivity
- **Templates**: Django templates with Tailwind utility classes

Tailwind input/output:
- Input: `static/css/input.css`
- Output: `static/css/output.css`

### Database
- **Development**: SQLite (`db.sqlite3`)
- **Media files**: Stored in `media/` directory (avatars, bikes, ride_headers, gpx_files)

### Authentication & Permissions
- REST Framework configured with `AllowAny` default permissions (development setting)
- Club app includes login/register/logout views
- Some views require authentication (profile editing)

## Key Model Relationships

**Profile** (club app):
- OneToOne with User
- Stores avatar and up to 3 bike photos
- Auto-created when needed

**Ride** (club app):
- ManyToMany with User (riders participating)
- ForeignKey to User (created_by)
- Supports GPX file uploads with validation
- Has `is_upcoming` property and `completed` flag

**Poll/Vote** (club app):
- Poll has multiple PollChoice objects
- Vote enforces unique constraint: one vote per user per poll
- Changing a vote deletes the old one (atomic operation)

## Development Workflow

1. After changing models: `python manage.py makemigrations` → `python manage.py migrate`
2. After changing templates/HTML: If using Tailwind classes, run `npm run dev` in separate terminal or `npm run build` after changes
3. Media files are served by Django in DEBUG mode (see `config/urls.py`)
4. Admin interface available at `/admin/` for all models

## Environment Variables

Configuration loaded from `.env` file:
- `SECRET_KEY` - Django secret key (required)
- `DEBUG` - Set to 'True' or 'False'
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

## Notes

- This project follows the user's preference for Tailwind CSS v4+ but currently uses v3.4
- The project structure separates settings in `config/` rather than the traditional project name directory
- Both apps use DRF for APIs but serve different purposes (api=demo, club=production feature)
- Media uploads require Pillow for image processing
