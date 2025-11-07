# My Django Project

A modern Django web application with REST API and Tailwind CSS frontend.

## Features

- **Django 5.0** - Latest Python web framework
- **Django REST Framework** - Powerful REST API
- **SQLite Database** - Lightweight, serverless database
- **Tailwind CSS** - Modern utility-first CSS framework
- **Alpine.js** - Lightweight JavaScript framework for interactivity

## Project Structure

```
myDjangoProject/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings file
│   ├── urls.py            # URL configuration
│   └── wsgi.py/asgi.py    # WSGI/ASGI entry points
├── api/                   # REST API app
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   └── urls.py            # API URL routing
├── frontend/              # Frontend app
│   ├── templates/         # HTML templates
│   └── views.py           # Frontend views
├── static/                # Static files
│   └── css/               # CSS files (Tailwind)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── package.json           # Node.js dependencies
└── tailwind.config.js     # Tailwind CSS configuration
```

## Setup Instructions

### Prerequisites

- Python 3.14+ installed
- Node.js and npm installed
- Git (optional)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/cersei/myDjangoProject
   ```

2. **Create and activate a virtual environment** (if not already done):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

5. **Build Tailwind CSS:**
   ```bash
   npm run build
   ```

6. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your secret key and other settings.

7. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

## Running the Project

### Development Mode

1. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

2. **In a separate terminal, watch Tailwind CSS for changes** (optional):
   ```bash
   npm run dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:8000/
   - API Root: http://localhost:8000/api/
   - API Items: http://localhost:8000/api/items/
   - Admin Panel: http://localhost:8000/admin/

## API Endpoints

### Items API

- `GET /api/` - API root
- `GET /api/items/` - List all items
- `POST /api/items/` - Create a new item
- `GET /api/items/{id}/` - Retrieve a specific item
- `PUT /api/items/{id}/` - Update a specific item
- `DELETE /api/items/{id}/` - Delete a specific item

### Example API Request

```bash
# List all items
curl http://localhost:8000/api/items/

# Create a new item
curl -X POST http://localhost:8000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "This is a test"}'
```

## Frontend Features

The frontend includes:
- Responsive design with Tailwind CSS
- Interactive UI with Alpine.js
- Real-time API integration
- CRUD operations for items
- Beautiful card layouts and animations

## Configuration

### Django Settings

Key settings are in `config/settings.py`:
- Database: SQLite (default)
- REST Framework pagination
- CORS headers for API access
- Static files configuration

### Tailwind CSS

Configure Tailwind in `tailwind.config.js`:
- Content paths for template scanning
- Theme customization
- Plugins

## Development

### Adding New Models

1. Create models in `api/models.py`
2. Create serializers in `api/serializers.py`
3. Create views in `api/views.py`
4. Add URLs in `api/urls.py`
5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Styling with Tailwind

1. Edit templates in `frontend/templates/`
2. Use Tailwind utility classes
3. Rebuild CSS with `npm run build` or watch with `npm run dev`

## Useful Commands

```bash
# Create a new Django app
python manage.py startapp appname

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Shell access
python manage.py shell

# Database shell
python manage.py dbshell
```

## Troubleshooting

### Python Dependencies
If you encounter issues with Python packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Tailwind CSS Not Building
If Tailwind isn't generating styles:
```bash
npm install
npm run build
```

### Database Issues
Reset the database:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Production Deployment

Before deploying to production:

1. Set `DEBUG=False` in `.env`
2. Update `SECRET_KEY` with a secure key
3. Configure `ALLOWED_HOSTS` properly
4. Use a production-grade database (PostgreSQL)
5. Set up proper static file serving
6. Use environment variables for sensitive data
7. Enable HTTPS

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please refer to the Django and Django REST Framework documentation:
- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Tailwind CSS: https://tailwindcss.com/docs
