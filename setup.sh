#!/bin/bash

# Create directory structure
mkdir -p api
mkdir -p public/css
mkdir -p public/uploads/images
mkdir -p public/uploads/audio
mkdir -p public/uploads/video
mkdir -p public/uploads/pdf
mkdir -p templates
mkdir -p netlify/functions

# Create .gitkeep files to preserve empty directories
touch public/uploads/images/.gitkeep
touch public/uploads/audio/.gitkeep
touch public/uploads/video/.gitkeep
touch public/uploads/pdf/.gitkeep

# Set permissions
chmod -R 755 public/uploads

echo "Directory structure created successfully!"
echo "Remember to:"
echo "1. Set up your virtual environment"
echo "2. Install dependencies: pip install -r requirements.txt"
echo "3. Configure your .env file with required API keys"
echo "4. Run the application: python api/app.py"
