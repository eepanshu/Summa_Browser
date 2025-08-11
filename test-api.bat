@echo off
echo SummaBrowser API Test Script
echo =============================
echo.
echo This will test your deployed API with a sample request
echo.
pause

REM Test API health first
echo Testing API connection...
curl -X GET "https://summabrowser-api.onrender.com/health"
echo.
echo.

echo To test with your PDF file, use this command:
echo curl -X POST -F "file=@your-pdf-file.pdf" https://summabrowser-api.onrender.com/process
echo.
echo Replace 'your-pdf-file.pdf' with the path to your actual PDF file
echo.
pause
