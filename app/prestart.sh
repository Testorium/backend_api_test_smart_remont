#!/usr/bin/env bash

set -e

echo "Run apply migrations.."

alembic upgrade head

if [ $? -ne 0 ]; then
    echo "Failed to apply migrations"
    exit 1
fi

echo "Migrations applied!"

exec "$@"