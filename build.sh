#!/bin/bash

# SummaBrowser Build Script

echo "🚀 Building SummaBrowser for deployment..."

# Create build directory
mkdir -p build/extension-dev build/extension-prod

# Copy common files
cp -r icons build/extension-dev/
cp -r icons build/extension-prod/
cp styles.css build/extension-dev/
cp styles.css build/extension-prod/
cp popup.html build/extension-dev/
cp popup.html build/extension-prod/
cp background.js build/extension-dev/
cp background.js build/extension-prod/

# Development version (local backend)
cp manifest.json build/extension-dev/
cp popup.js build/extension-dev/

# Production version (deployed backend)
cp manifest-production.json build/extension-prod/manifest.json
cp popup-production.js build/extension-prod/popup.js

# Create ZIP files
cd build
zip -r ../summabrowser-dev.zip extension-dev/
zip -r ../summabrowser-prod.zip extension-prod/

cd ..
echo "✅ Build complete!"
echo "📦 Development version: summabrowser-dev.zip"
echo "🌐 Production version: summabrowser-prod.zip"
