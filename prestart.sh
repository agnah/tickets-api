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
fi

if [ -z "$TICKETS_API_REPOSITORY_PATH" ]
then
    echo "Sleeping 15 seconds"
    sleep 15
fi

echo "Running migration"
PYTHONPATH=. alembic upgrade head

if [ -z "$TICKETS_API_REPOSITORY_PATH" ]
then
    echo "Sleeping 15 seconds"
    sleep 15
fi
