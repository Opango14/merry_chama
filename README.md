# Merry Chama

Merry Chama is a Django web application for managing chama groups, contributions, and member interactions.

## Features

- User registration and login
- Create and join chama groups
- Track contributions and payouts
- Dashboard for group management
- Responsive web interface

## Requirements

- Python 3.11+
- Django 6.0
- Virtual environment

## Local development

1. Create and activate a virtual environment
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations
   ```bash
   python manage.py migrate
   ```

4. Run the development server
   ```bash
   python manage.py runserver
   ```

5. Open http://127.0.0.1:8000/

## Environment variables

Copy the example file and update values as needed:

```bash
cp .env.example .env
```

Example variables:

```env
SECRET_KEY=change-me
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1,https://your-domain.com
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

## Project structure

- `chama/` - main Django app containing models, views, forms, and URLs
- `merry_chama/` - project settings and configuration
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and other static assets
