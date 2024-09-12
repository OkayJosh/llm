#!/bin/bash

# Make the database check script executable
#chmod +x ./reach_database.sh

# Navigate to the project directory
PROJECT_DIR="$WORKDIR" # should work like this in docker
#PROJECT_DIR="$HOME/lycon/llm"
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

# Apply database migrations for multiple databases
echo "Running database migrations for database..."
if ! python manage.py migrate; then
    echo "Database migrations failed. Exiting." >&2
    exit 1
fi


# Configure Celery worker parameters based on the pool type
EXTRA_PARAMS=()
if [ "${CELERY_WORKER_POOL_TYPE}" = "prefork" ]; then
    echo "Configuring Celery worker for prefork pool type..."
    EXTRA_PARAMS+=(
        "--autoscale=${CELERY_WORKER_AUTOSCALE_MAX},${CELERY_WORKER_AUTOSCALE_MIN}"
        "--prefetch-multiplier=${CELERY_WORKER_PREFETCH_MULTIPLIER}"
    )
fi

# Perform Django system health check
echo "Performing Django system checks..."
if ! python manage.py check; then
    echo "Django system check failed. Exiting." >&2
    exit 1
fi

# Start the Celery Worker with the appropriate configuration
echo "Starting Celery Worker..."
exec celery --app=llm \
    worker \
    --loglevel="${CELERY_LOG_LEVEL}" \
    --pool="${CELERY_WORKER_POOL_TYPE}" \
    --concurrency="${CELERY_WORKER_CONCURRENCY:-1}" \
    "${EXTRA_PARAMS[@]}" || {
    echo "Failed to start Celery Worker. Exiting." >&2
    exit 1
}
