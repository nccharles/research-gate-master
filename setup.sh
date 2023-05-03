#!/bin/bash

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
# Install requirements
pip install -r requirements.txt

# Create folders if not exists
if [ ! -d "migrations" ]; then
    alembic init migrations
fi

if [ ! -d "migrations/versions" ]; then
    mkdir -p migrations/versions
fi

if [ ! -d "src/documents/temp" ]; then
    mkdir -p src/documents/temp
fi

if [ ! -d "src/storage/db" ]; then
    mkdir -p src/storage/db
fi

# Create tables
alembic revision --autogenerate -m "Create tables"
alembic upgrade head
