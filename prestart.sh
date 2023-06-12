#! /usr/bin/env bash

# Check if we don't have a TICKETS_API_REPOSITORY_PATH environment variable (i.e running on production)
if [ -z "$TICKETS_API_REPOSITORY_PATH" ]
then
    if [ -f /app/tickets-api/.env ]
    then
        # Remove env file set on build instance
        echo "Removing .env file on this instance"
        rm /app/tickets-api/.env
    fi

    # if [ -f /var/run/secrets/TICKETS_API_DATABASE_ROUTING_CONFIG ]
    # then
    #     # Read the secret value from the file and set it to the same environment variable name
    #     echo "Setting TICKETS_API_DATABASE_ROUTING_CONFIG from secret"
    #     export TICKETS_API_DATABASE_ROUTING_CONFIG=$(cat /var/run/secrets/TICKETS_API_DATABASE_ROUTING_CONFIG)
    # fi
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
