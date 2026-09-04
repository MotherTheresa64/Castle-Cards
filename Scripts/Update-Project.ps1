$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "=== Castle Cards Update ===" -ForegroundColor Cyan
Write-Host "Project: $projectRoot"
Write-Host ""

# Godot may modify project.godot locally. GitHub is the source of truth for this project,
# so discard only that local config change before pulling. Other local edits are preserved.
if (-not (git diff --quiet -- project.godot)) {
    Write-Host "Restoring local project.godot to repository version..." -ForegroundColor Yellow
    git restore -- project.godot
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to restore project.godot."
    }
}

Write-Host "Pulling latest repository changes..." -ForegroundColor Yellow
git pull --ff-only

if ($LASTEXITCODE -ne 0) {
    throw "git pull failed. Resolve any remaining local Git changes before continuing."
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
