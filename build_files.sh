#!/bin/bash

echo "BUILD START"

# Install Python dependencies
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles_build/public
mkdir -p staticfiles_build/static
mkdir -p staticfiles_build/media

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput --clear

# Copy static files to public directory
if [ -d "staticfiles_build/static" ]; then
    cp -r staticfiles_build/static/* staticfiles_build/public/
fi

# Create a dummy index.html if it doesn't exist
touch staticfiles_build/public/index.html

echo "BUILD END"