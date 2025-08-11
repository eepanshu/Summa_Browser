# SummaBrowser Deployment Script
# This script pushes the Pillow dependency fixes to GitHub

Write-Host "=== SummaBrowser Video Integration Deployment ===" -ForegroundColor Cyan
Write-Host "Timestamp: $(Get-Date)" -ForegroundColor Gray

# Change to project directory
$ProjectPath = "c:\Users\deepanshu.b\Downloads\Summa_Browser-main\Summa_Browser-main\SummaBrowse"
Set-Location $ProjectPath
Write-Host "Working in: $ProjectPath" -ForegroundColor Green

# Configure Git
Write-Host "`nConfiguring Git..." -ForegroundColor Yellow
git config user.email "summabrowser@deploy.com"
git config user.name "SummaBrowser Deploy"

# Show current status
Write-Host "`nCurrent Git Status:" -ForegroundColor Yellow
git status

# Add the critical files
Write-Host "`nAdding modified files..." -ForegroundColor Yellow
git add requirements.txt
git add app-web.py
git add deployment_status.py

# Show what's staged
Write-Host "`nStaged changes:" -ForegroundColor Yellow
git diff --cached --name-only

# Commit the changes
Write-Host "`nCommitting changes..." -ForegroundColor Yellow
$CommitMessage = @"
Fix: Remove Pillow dependency for Python 3.13 compatibility

Critical fixes for deployment:
- ❌ REMOVED: Pillow from requirements.txt (was causing build failures)
- ✅ FIXED: Made PIL import optional in app-web.py with try/except
- ✅ PRESERVED: All video processing functionality intact
- ✅ ENHANCED: Image processing now gracefully handles missing dependencies
- 🚀 READY: For production deployment without build errors

Video features included:
- YouTube transcript extraction
- Video URL processing and validation
- AI-powered video summarization
- Enhanced web UI with video input support
- Multiple fallback options for video processing

This resolves the Python 3.13 + Pillow compatibility issue blocking deployment.
"@

git commit -m $CommitMessage

# Push to GitHub
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host "`n=== Deployment Push Completed! ===" -ForegroundColor Green
Write-Host "✅ Changes pushed to GitHub" -ForegroundColor Green
Write-Host "🔄 Render will automatically deploy the new version" -ForegroundColor Cyan
Write-Host "⏱️ Deployment typically takes 10-15 minutes" -ForegroundColor Cyan
Write-Host "`n🌐 Monitor deployment at: https://dashboard.render.com" -ForegroundColor Blue
Write-Host "🧪 Test deployment with: python test_video_deployment.py" -ForegroundColor Blue

Write-Host "`n🎥 Once deployed, your video features will include:" -ForegroundColor Magenta
Write-Host "   • YouTube video URL processing" -ForegroundColor White
Write-Host "   • Automatic transcript extraction" -ForegroundColor White  
Write-Host "   • AI-powered video summarization" -ForegroundColor White
Write-Host "   • Enhanced web UI with video support" -ForegroundColor White
