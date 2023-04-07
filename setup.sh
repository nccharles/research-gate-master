#!/bin/bash

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Create folders if not exists
if [ ! -d "migrations" ]; then
    mkdir -p migrations
fi

if [ ! -d "migrations/versions" ]; then
    mkdir -p migrations/versions
fi

if [ ! -d "src/documents" ]; then
    mkdir -p src/documents
fi

if [ ! -d "src/storage/db" ]; then
    mkdir -p src/storage/db
fi

# Create tables
alembic init migrations
alembic revision --autogenerate -m "Create tables"
alembic upgrade head
