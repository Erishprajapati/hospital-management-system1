#!/bin/bash

echo "BUILD START"

# Install Python dependencies
pip3 install -r requirements.txt

# Create staticfiles_build directory if it doesn't exist
mkdir -p staticfiles_build/public

# Collect static files
python3 manage.py collectstatic --noinput --clear

# Move static files to the correct directory
cp -r staticfiles_build/static/* staticfiles_build/public/

echo "BUILD END"