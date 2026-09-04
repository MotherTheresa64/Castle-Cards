$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "=== Castle Cards Update ===" -ForegroundColor Cyan
Write-Host "Project: $projectRoot"
Write-Host ""

# Godot may rewrite project.godot locally. GitHub is the source of truth for that file.
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

$assetScript = Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_assets.py"
$assetStamp = Join-Path $projectRoot ".assets-generated"
$expectedAssets = @(
    "Models\Castles\Medieval\castle_gatehouse.glb",
    "Models\Castles\Medieval\castle_tower.glb",
    "Models\Castles\Medieval\castle_wall.glb",
    "Models\Terrain\Medieval\oak_tree.glb",
    "Models\Units\Human\spearman.glb",
    "Models\Units\Human\swordsman.glb",
    "Models\Units\Human\archer.glb",
    "Models\Siege\Medieval\catapult.glb",
    "Models\Props\Containers\barrel.glb",
    "Models\Tavern\Furniture\shelf.glb"
)

$needsAssets = -not (Test-Path $assetStamp)
if (-not $needsAssets) {
    foreach ($asset in $expectedAssets) {
        if (-not (Test-Path (Join-Path $projectRoot $asset))) {
            $needsAssets = $true
            break
        }
    }
}

if (-not $needsAssets -and (Test-Path $assetScript)) {
    $needsAssets = (Get-Item $assetScript).LastWriteTime -gt (Get-Item $assetStamp).LastWriteTime
}

if ($needsAssets) {
    Write-Host ""
    Write-Host "Generating/updating Blender assets..." -ForegroundColor Yellow

    $blender = $null
    $blenderCommand = Get-Command blender.exe -ErrorAction SilentlyContinue
    if ($blenderCommand) {
        $blender = $blenderCommand.Source
    }

    if (-not $blender) {
        $blenderRoot = Join-Path $env:ProgramFiles "Blender Foundation"
        if (Test-Path $blenderRoot) {
            $blender = Get-ChildItem $blenderRoot -Filter blender.exe -File -Recurse -ErrorAction SilentlyContinue |
                Sort-Object FullName -Descending |
                Select-Object -First 1 -ExpandProperty FullName
        }
    }

    if (-not $blender) {
        throw "Blender could not be found. Install Blender or add blender.exe to PATH."
    }

    Write-Host "Blender: $blender" -ForegroundColor DarkGray
    & $blender --background --python $assetScript
    if ($LASTEXITCODE -ne 0) {
        throw "Blender asset generation failed."
    }

    New-Item -Path $assetStamp -ItemType File -Force | Out-Null
    (Get-Item $assetStamp).LastWriteTime = Get-Date
    Write-Host "Asset generation succeeded." -ForegroundColor Green
}
else {
    Write-Host "Generated assets are already current." -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "Building CastleCards.csproj..." -ForegroundColor Yellow
dotnet build .\CastleCards.csproj
if ($LASTEXITCODE -ne 0) {
    throw "dotnet build failed."
}

Write-Host ""
Write-Host "Castle Cards is up to date." -ForegroundColor Green
Write-Host "C# build succeeded and generated art is current." -ForegroundColor Green
Write-Host "If Godot is open, let it import the GLB files and accept Reload from disk if prompted." -ForegroundColor Green
