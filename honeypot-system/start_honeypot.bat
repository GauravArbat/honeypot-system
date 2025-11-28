@echo off
echo ========================================
echo    HONEYPOT SECURITY SYSTEM LAUNCHER
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 14+
    pause
    exit /b 1
)

echo Checking SQLite support...
python -c "import sqlite3; print('SQLite ready')" >nul 2>&1
if errorlevel 1 (
    echo ERROR: SQLite not available
    pause
    exit /b 1
)

echo.
echo Starting Honeypot System...
echo.
echo Services will be available at:
echo - Dashboard: http://localhost:3000
echo - Web Honeypot: http://localhost:8080
echo - SSH Honeypot: localhost:2222
echo - API: http://localhost:5000
echo.
echo Press Ctrl+C to stop all services
echo.

python start_system.py

pause