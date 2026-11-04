#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

# Load environment variables (SECRET_KEY, DB_*, ...) from .env if present
if [ -f ".env" ]; then
  set -a
  source .env
  set +a
fi

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
