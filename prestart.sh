#! /usr/bin/env bash

# Check if we don't have a TICKETS_API_REPOSITORY_PATH environment variable (i.e running on production)
if [ -z "$TICKETS_API_REPOSITORY_PATH" ]
then
    if [ -f /app/tickets-api/.env ]
    then
        # Remove the .env file that came with the docker image, if it exists
        # (i.e running on production)
        echo "Removing .env file on this instance"
        rm /app/tickets-api/.env
    fi
else
    echo "TICKETS_API_REPOSITORY_PATH is set, not removing .env file"
fi

echo "Sleeping 15 seconds"
sleep 15

echo "Running migration"
PYTHONPATH=. alembic upgrade head

echo "Sleeping 15 seconds"
sleep 15