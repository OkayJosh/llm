#!/usr/bin/env bash

# Apply database migrations
python manage.py migrate --noinput

# Start Celery worker
celery -A llm beat --loglevel=info
