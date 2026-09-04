$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "=== Castle Cards Repair ===" -ForegroundColor Cyan
Write-Host "Project: $projectRoot"
Write-Host ""
Write-Host "IMPORTANT: Godot should be closed while this repair runs." -ForegroundColor Yellow
Write-Host ""

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

# Force regeneration of the locally generated art library after a repair.
$assetStamp = Join-Path $projectRoot ".assets-generated"
if (Test-Path $assetStamp) {
    Remove-Item $assetStamp -Force
}

Write-Host ""
Write-Host "Running the normal updater to regenerate art and rebuild C#..." -ForegroundColor Yellow
& (Join-Path $PSScriptRoot "Update-Project.ps1")
if ($LASTEXITCODE -ne 0) {
    throw "Update-Project.ps1 failed during repair."
}

Write-Host ""
Write-Host "Repair completed successfully." -ForegroundColor Green
Write-Host "The detailed art library was regenerated and C# was rebuilt." -ForegroundColor Green
Write-Host "Open the project in Godot again now." -ForegroundColor Green
