#! /usr/bin/env sh

# Let the DB Start
python /app/mort_server/pre_start.py

# Run Migrations
alembic upgrade head