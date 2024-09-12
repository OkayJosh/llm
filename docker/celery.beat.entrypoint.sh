#!/bin/bash

# Make the database check script executable
chmod +x ./reach_database.sh

# Navigate to the project directory
PROJECT_DIR="$HOME/llm" # Should work like this in Docker
PROJECT_DIR="$HOME/lycon/llm"
echo "Changing to project directory: ${PROJECT_DIR}..."
cd "${PROJECT_DIR}" || {
    echo "Failed to change to project directory. Exiting." >&2
    exit 1
}

# Source the .env file and export environment variables
echo "Loading environment variables from .env file..."
if ! export $(grep -v '^#' .env | xargs); then
    echo "Failed to export environment variables from .env file. Exiting." >&2
    exit 1
fi

# Check if the database is reachable
echo "Checking if the database is reachable..."
if ! docker/reach_database.sh; then
    echo "Database is not reachable. Exiting." >&2
    exit 1
fi

# Run Django health check to verify configurations
echo "Performing Django system checks..."
if ! python manage.py check; then
    echo "Django system check failed. Exiting." >&2
    exit 1
fi

# Create the Celery Beat PID directory within the project directory
echo "Setting up Celery Beat directories..."
CELERY_DIR="/var/run/llm"
mkdir -p "${CELERY_DIR}"
if [[ $? -ne 0 ]]; then
    echo "Failed to create directory ${CELERY_DIR}. Exiting." >&2
    exit 1
fi

# Ensure the current user owns the Celery directory
chown "$USER:$USER" "${CELERY_DIR}"

# Start Celery Beat
echo "Starting Celery Beat..."
exec celery --app=llm \
    beat \
    --pidfile="${CELERY_DIR}/celery-beat.pid" \
    --schedule="${CELERY_DIR}/celerybeat-schedule" || {
    echo "Failed to start Celery Beat. Exiting." >&2
    exit 1
}
