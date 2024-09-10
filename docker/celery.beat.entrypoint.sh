#!/bin/bash

# Source the script to ensure the database is reachable
. docker/reach_database.sh

# Set restrictive file permissions (group write permissions allowed)
umask 0002

# Wait for the database to become reachable
wait_for_database_to_be_reachable || {
    echo "Database is not reachable. Exiting." >&2
    exit 1
}

# Run Django health check to verify configurations
echo "Performing Django system checks..."
python3 manage.py check || {
    echo "Django check failed. Exiting." >&2
    exit 1
}

# Start the Celery Beat scheduler
echo "Starting Celery Beat..."
exec celery --app=llm \
    beat \
    --pidfile=/var/run/llm/celery-beat.pid \
    --schedule=/var/run/llm/celerybeat-schedule &
