#!/usr/bin/env bash

# Exit immediately if any command fails
set -e

# Log start of script
echo "Starting Django application setup..."

# Source necessary files for environment and database configurations
#. /reach_database.sh
. docker/reach_database.sh

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || { echo "Failed to collect static files. Exiting."; exit 1; }
echo "Static files collected."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput || { echo "Database migration failed. Exiting."; exit 1; }
echo "Database migrations applied."

# Wait for the database to be reachable before starting services
wait_for_database_to_be_reachable || {
    echo "Database is not reachable. Exiting." >&2
    exit 1
}

# Start Gunicorn server
echo "Starting Gunicorn server..."
gunicorn llm.wsgi:application \
    --bind ":8000" \
    --workers "${GUNICORN_WORKERS:-3}" \
    --log-level "${GUNICORN_LOG_LEVEL:-info}" \
    --access-logfile '-' \
    --error-logfile '-' \
    --timeout "${GUNICORN_TIMEOUT:-30}"

# Log successful start
echo "Gunicorn server started on port 8000."
