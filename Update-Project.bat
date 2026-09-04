@echo off
setlocal
cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\Update-Project.ps1"
if errorlevel 1 goto :fail

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Scripts\Apply-Reference-Quality-V2.ps1"
if errorlevel 1 goto :fail

echo.
echo Castle Cards update completed successfully.
pause
exit /b 0

:fail
echo.
echo Castle Cards update failed. Scroll up for the first error.
pause
exit /b 1
