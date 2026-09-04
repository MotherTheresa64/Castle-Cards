$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "=== Castle Cards Repair ===" -ForegroundColor Cyan
Write-Host "Project: $projectRoot"
Write-Host ""
Write-Host "IMPORTANT: Godot should be closed while this repair runs." -ForegroundColor Yellow
Write-Host ""

# Godot may touch project.godot locally when opening/importing the project.
# For this repo, GitHub is the source of truth, so discard only that generated/local change
# before pulling. Other tracked local edits are intentionally left alone.
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

$foldersToRemove = @(
    ".godot",
    "bin",
    "obj",
    ".vs"
)

foreach ($folder in $foldersToRemove) {
    $path = Join-Path $projectRoot $folder
    if (Test-Path $path) {
        Write-Host "Removing $folder cache..." -ForegroundColor Yellow
        Remove-Item $path -Recurse -Force
    }
}

Write-Host ""
Write-Host "Restoring .NET packages..." -ForegroundColor Yellow
dotnet restore .\CastleCards.csproj
if ($LASTEXITCODE -ne 0) {
    throw "dotnet restore failed."
}

Write-Host ""
Write-Host "Building CastleCards.csproj..." -ForegroundColor Yellow
dotnet build .\CastleCards.csproj
if ($LASTEXITCODE -ne 0) {
    throw "dotnet build failed."
}

Write-Host ""
Write-Host "Repair completed successfully." -ForegroundColor Green
Write-Host "Open the project in Godot again now." -ForegroundColor Green
