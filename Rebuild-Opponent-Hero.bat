@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\Rebuild-Opponent-Hero.ps1"
if errorlevel 1 goto :fail
exit /b 0

:fail
echo.
echo Opponent hero rebuild failed. Scroll up for the first error.
pause
exit /b 1
