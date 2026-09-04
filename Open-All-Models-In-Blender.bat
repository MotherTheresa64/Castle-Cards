@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\Open-All-Models-In-Blender.ps1"
if errorlevel 1 goto :fail
exit /b 0

:fail
echo.
echo Blender model review setup failed. Scroll up for the first error.
pause
exit /b 1
