@echo off
echo === SummaBrowser Deployment Push ===
cd /d "c:\Users\deepanshu.b\Downloads\Summa_Browser-main\Summa_Browser-main\SummaBrowse"

echo Setting git config...
git config user.email "summabrowser@deploy.com"
git config user.name "SummaBrowser Deploy"

echo Current git status:
git status

echo Adding modified files...
git add requirements.txt
git add app-web.py
git add deployment_status.py
git add fix_deployment.sh

echo Committing changes...
git commit -m "Fix: Remove Pillow dependency for Python 3.13 compatibility

- Removed Pillow from requirements.txt (causing build failures)
- Made PIL import optional in app-web.py with graceful fallback
- Video processing functionality preserved and enhanced
- Image processing now works without heavy dependencies
- Ready for production deployment"

echo Pushing to GitHub...
git push origin main

echo === Push completed! ===
echo Monitor deployment at: https://dashboard.render.com
echo Test deployment: python test_video_deployment.py
pause
