@echo off
echo ============================================
echo    L-mobile Chatbot Backend Server
echo ============================================
echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
python main.py

pause

