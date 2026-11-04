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
- PostgreSQL 14+
- Virtual environment

## Database setup (PostgreSQL)

Create a database and user before running the app:

```sql
CREATE DATABASE merry_chama;
CREATE USER merry_chama_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE merry_chama TO merry_chama_user;
\c merry_chama
GRANT ALL ON SCHEMA public TO merry_chama_user;
```

Then set the `DB_*` values in your `.env` file (see below).

## Local development

### Option 1: Use the startup script

Run the project with:

```bash
bash start.sh
```

This will:
- create a virtual environment if needed
- load variables from `.env`
- install dependencies
- apply migrations
- start the Django development server at http://0.0.0.0:8000/

### Option 2: Run manually

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
   python manage.py runserver 0.0.0.0:8000
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
DB_ENGINE=django.db.backends.postgresql
DB_NAME=merry_chama
DB_USER=merry_chama_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## Project structure

- `chama/` - main Django app containing models, views, forms, and URLs
- `merry_chama/` - project settings and configuration
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and other static assets
