#!/bin/bash

# Print Python version and path
echo "Python version:"
python --version
echo "Python path:"
python -c "import sys; print('\n'.join(sys.path))"

# Create necessary directories
mkdir -p public/uploads/images
mkdir -p public/uploads/audio
mkdir -p public/uploads/video
mkdir -p public/uploads/pdf

# Set permissions
chmod -R 755 public/uploads

# Verify module structure
echo "Checking module structure..."
python -c "import api.app; print('Module check successful')"

# Start application with gunicorn
echo "Starting application..."
exec gunicorn -c gunicorn_config.py api.app:app
