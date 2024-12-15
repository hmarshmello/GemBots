#!/bin/bash

# Files to remove
echo "Removing unnecessary files..."
rm -f Dockerfile
rm -f runtime.txt
rm -f .python-version
rm -f build.sh
rm -f setup.sh
rm -f package.json
rm -f Procfile
rm -f gunicorn_config.py
rm -f start.sh
rm -rf netlify
rm -f netlify.toml

# Remove netlify directory and its contents
echo "Removing netlify directory..."
rm -rf netlify/

# Create necessary directories if they don't exist
echo "Creating upload directories..."
mkdir -p public/uploads/images
mkdir -p public/uploads/audio
mkdir -p public/uploads/video
mkdir -p public/uploads/pdf

# Add .gitkeep files
echo "Adding .gitkeep files..."
touch public/uploads/images/.gitkeep
touch public/uploads/audio/.gitkeep
touch public/uploads/video/.gitkeep
touch public/uploads/pdf/.gitkeep

# Set permissions
echo "Setting permissions..."
chmod -R 755 public/uploads

echo "Cleanup complete! Project structure has been organized."
echo "Remember to:"
echo "1. Set up your virtual environment"
echo "2. Install dependencies: pip install -r requirements.txt"
echo "3. Configure your .env file"
echo "4. Deploy to Render.com using render.yaml"
