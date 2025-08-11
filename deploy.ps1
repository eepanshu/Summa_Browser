Set-Location "c:\Users\deepanshu.b\Downloads\Summa_Browser-main\Summa_Browser-main\SummaBrowse"
git config user.email "user@example.com"
git config user.name "User"
git add requirements.txt
git add app-web.py
git commit -m "Remove Pillow dependency and make PIL optional"
git push origin main
Write-Host "Deployment script completed"
