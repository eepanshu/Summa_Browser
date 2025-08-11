#!/bin/bash
# Deployment fix for Pillow dependency issues

echo "=== SummaBrowser Video Integration Deployment Fix ==="
echo "Timestamp: $(date)"

# Set git config
git config user.email "summabrowser@deploy.com"
git config user.name "SummaBrowser Deploy"

# Show current status
echo "Current git status:"
git status

# Add the modified files
echo "Adding modified files..."
git add requirements.txt app-web.py

# Commit changes
echo "Committing changes..."
git commit -m "Fix: Remove Pillow dependency, make image processing optional

- Removed Pillow from requirements.txt to fix Python 3.13 build issues
- Made PIL import optional in app-web.py with graceful fallback
- Video processing functionality preserved and enhanced
- Image processing now works without heavy dependencies"

# Push to deploy
echo "Pushing to trigger deployment..."
git push origin main

echo "=== Deployment fix completed ==="
echo "Monitor deployment at: https://dashboard.render.com"
