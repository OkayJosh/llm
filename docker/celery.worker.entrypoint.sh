#!/bin/bash

# Set restrictive file creation permissions
umask 0002

# Source necessary files for environment and database configurations
. /secret-file-loader.sh
. /reach_database.sh

# Apply database migrations without requiring user input
python manage.py migrate --noinput

# Wait for the database to be reachable before starting services
if ! wait_for_database_to_be_reachable; then
    echo "Database is not reachable. Exiting." >&2
    exit 1
fi

# Configure Celery worker parameters based on pool type
if [ "${CELERY_WORKER_POOL_TYPE}" = "prefork" ]; then
    EXTRA_PARAMS=("--autoscale=${CELERY_WORKER_AUTOSCALE_MAX},${CELERY_WORKER_AUTOSCALE_MIN}"
        "--prefetch-multiplier=${CELERY_WORKER_PREFETCH_MULTIPLIER}")
else
    EXTRA_PARAMS=()
fi

# Perform a Django health check to ensure the application is ready
python manage.py check

# Start Celery worker with the appropriate configuration
echo "Starting Celery Worker..."
exec celery --app=llm \
    worker \
    --loglevel="${CELERY_LOG_LEVEL}" \
    --pool="${CELERY_WORKER_POOL_TYPE}" \
    --concurrency="${CELERY_WORKER_CONCURRENCY:-1}" \
    "${EXTRA_PARAMS[@]}"
