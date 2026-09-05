$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "=== Castle Cards Opponent Art Reboot ===" -ForegroundColor Cyan
Write-Host "Discarding the primitive-built character workflow and preparing a real CC0 human base in Blender..." -ForegroundColor Yellow

$blender = $null
$blenderCommand = Get-Command blender.exe -ErrorAction SilentlyContinue
if ($blenderCommand) { $blender = $blenderCommand.Source }

if (-not $blender) {
    $blenderRoot = Join-Path $env:ProgramFiles "Blender Foundation"
    if (Test-Path $blenderRoot) {
        $blender = Get-ChildItem $blenderRoot -Filter blender.exe -File -Recurse -ErrorAction SilentlyContinue |
            Sort-Object FullName -Descending |
            Select-Object -First 1 -ExpandProperty FullName
    }
}

if (-not $blender) { throw "Blender could not be found. Install Blender or add blender.exe to PATH." }

$acquire = Join-Path $projectRoot "Scripts\Acquire-Quality-Assets.ps1"
$prepare = Join-Path $projectRoot "ArtSource\Blender\Scripts\prepare_opponent_real_base.py"
$sourceBlend = Join-Path $projectRoot "ArtSource\Blender\HeroSources\opponent_real_base.blend"

if (-not (Test-Path $acquire)) { throw "Missing art-source acquisition script: $acquire" }
if (-not (Test-Path $prepare)) { throw "Missing realistic opponent preparation script: $prepare" }

Write-Host "Acquiring/validating CC0 source art..." -ForegroundColor DarkGray
& $acquire
if ($LASTEXITCODE -ne 0) { throw "CC0 source-art acquisition failed." }

Write-Host "Blender: $blender" -ForegroundColor DarkGray
Write-Host "Preparing Blender Studio realistic male base mesh..." -ForegroundColor DarkGray
& $blender --background --python $prepare
if ($LASTEXITCODE -ne 0) { throw "Realistic opponent base preparation failed." }

if (-not (Test-Path $sourceBlend)) {
    throw "Expected realistic opponent source was not created: $sourceBlend"
}

Write-Host ""
Write-Host "Opponent art reboot base prepared successfully." -ForegroundColor Green
Write-Host "Editable source: ArtSource\Blender\HeroSources\opponent_real_base.blend" -ForegroundColor Green
Write-Host "This file comes from Blender Studio's CC0 Human Base Meshes, not the old primitive generators." -ForegroundColor Green
Write-Host "Opening the clean realistic base in Blender..." -ForegroundColor Green
Start-Process -FilePath $blender -ArgumentList @($sourceBlend)
