$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "=== Castle Cards Update ===" -ForegroundColor Cyan
Write-Host "Project: $projectRoot"
Write-Host ""

Write-Host "Pulling latest repository changes..." -ForegroundColor Yellow
git pull --ff-only

if ($LASTEXITCODE -ne 0) {
    throw "git pull failed. Resolve the Git error before continuing."
}

Write-Host ""
Write-Host "Building CastleCards.csproj..." -ForegroundColor Yellow

dotnet build .\CastleCards.csproj

if ($LASTEXITCODE -ne 0) {
    throw "dotnet build failed."
}

Write-Host ""
Write-Host "Castle Cards is up to date and the C# build succeeded." -ForegroundColor Green
Write-Host "If Godot is already open, accept Reload from disk when prompted." -ForegroundColor Green
