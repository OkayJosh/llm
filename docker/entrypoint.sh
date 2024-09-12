#!/usr/bin/env bash

# Make the database check script executable
chmod +x ./reach_database.sh

# Navigate to the project directory
PROJECT_DIR="$HOME/llm"
PROJECT_DIR="$HOME/lycon/llm"
echo "Changing to project directory: ${PROJECT_DIR}..."
cd "${PROJECT_DIR}" || {
    echo "Failed to change to project directory. Exiting." >&2
    exit 1
}

# Log start of script
echo "Starting Django application setup..."

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

 Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || { echo "Failed to collect static files. Exiting."; exit 1; }
echo "Static files collected."

# Apply database migrations for multiple databases
echo "Running database migrations for database..."
if ! python manage.py migrate; then
    echo "Database migrations failed. Exiting." >&2
    exit 1
fi

# Start Gunicorn server
echo "Starting Gunicorn server..."
gunicorn llm.wsgi:application \
    --bind ":${GUNICORN_PORT:-8000}" \
    --workers "${GUNICORN_WORKERS:-3}" \
    --log-level "${GUNICORN_LOG_LEVEL:-info}" \
    --access-logfile '-' \
    --error-logfile '-' \
    --timeout "${GUNICORN_TIMEOUT:-30}"

# Log successful start
echo "Gunicorn server started on port ${GUNICORN_PORT:-8000}."
