#!/bin/bash

wait_for_database_to_be_reachable() {
    echo "Waiting for database to be reachable..."
    failure_count=0
    DATABASE_READINESS_TIMEOUT=${DATABASE_READINESS_TIMEOUT:-30}

    # Loop until the database is reachable or the timeout is reached
    until python manage.py check_db "SELECT 1;" > /dev/null 2>&1; do
        echo -n "."
        failure_count=$((failure_count + 1))
        sleep 1

        if [ $failure_count -ge "$DATABASE_READINESS_TIMEOUT" ]; then
            echo "Database not reachable within timeout (${DATABASE_READINESS_TIMEOUT} seconds). Exiting."
            exit 1
        fi
    done

    echo "Database is reachable!"
}


wait_for_database_to_be_reachable