$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "=== Castle Cards Reference Quality V4 ===" -ForegroundColor Cyan
Write-Host "Rebuilding hero assets, then replacing the seated opponent with the dedicated V4 hero model..." -ForegroundColor Yellow

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
Write-Host "Blender: $blender" -ForegroundColor DarkGray

$heroPass = Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_reference_quality_v2.py"
$opponentPass = Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_opponent_hero_v4.py"
$materialPass = Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_cinematic_material_pass.py"

foreach ($script in @($heroPass, $opponentPass, $materialPass)) {
    if (-not (Test-Path $script)) { throw "Missing reference-quality generator: $script" }
    Write-Host "Running $(Split-Path $script -Leaf)..." -ForegroundColor DarkGray
    & $blender --background --python $script
    if ($LASTEXITCODE -ne 0) { throw "Blender reference-quality pass failed while running $script" }
}

$required = @(
    "Models\Hero\battlefield_terrain_hero.glb",
    "Models\Hero\castle_blue_hero.glb",
    "Models\Hero\castle_red_hero.glb",
    "Models\Hero\opponent_hero.glb",
    "Models\Opponent\seated_opponent.glb",
    "Models\Hero\spearman_hero.glb",
    "Models\Hero\archer_hero.glb",
    "Models\Hero\swordsman_hero.glb"
)

foreach ($asset in $required) {
    if (-not (Test-Path (Join-Path $projectRoot $asset))) {
        throw "Reference-quality asset is missing after generation: $asset"
    }
}

$assetStamp = Join-Path $projectRoot ".assets-generated"
if (-not (Test-Path $assetStamp)) { New-Item -Path $assetStamp -ItemType File -Force | Out-Null }
(Get-Item $assetStamp).LastWriteTime = Get-Date

Write-Host "Reference-quality V4 pass complete." -ForegroundColor Green
Write-Host "Hero castles and terrain were rebuilt, the seated opponent was replaced by the dedicated V4 character, and the PBR material pass was reapplied." -ForegroundColor Green
