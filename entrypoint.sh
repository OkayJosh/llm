#!/usr/bin/env bash

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

# test
pytest

# Start Gunicorn server
gunicorn -b :8000 llm.wsgi