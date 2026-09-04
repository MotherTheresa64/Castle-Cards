$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "=== Castle Cards Update ===" -ForegroundColor Cyan
Write-Host "Project: $projectRoot"
Write-Host ""

if (-not (git diff --quiet -- project.godot)) {
    Write-Host "Restoring local project.godot to repository version..." -ForegroundColor Yellow
    git restore -- project.godot
    if ($LASTEXITCODE -ne 0) { throw "Failed to restore project.godot." }
}

Write-Host "Pulling latest repository changes..." -ForegroundColor Yellow
git pull --ff-only
if ($LASTEXITCODE -ne 0) {
    throw "git pull failed. Resolve any remaining local Git changes before continuing."
}

$assetScripts = @(
    (Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_assets.py"),
    (Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_detail_assets.py"),
    (Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_gameplay_assets.py"),
    (Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_hero_assets.py"),
    (Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_hero_tabletop.py"),
    (Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_reference_pass.py")
)

$assetStamp = Join-Path $projectRoot ".assets-generated"

$expectedAssets = @(
    "Models\Castles\Medieval\castle_gatehouse.glb",
    "Models\Castles\Medieval\castle_tower.glb",
    "Models\Castles\Medieval\castle_wall.glb",
    "Models\Castles\Medieval\castle_keep.glb",
    "Models\Terrain\Medieval\oak_tree.glb",
    "Models\Terrain\Medieval\pine_tree.glb",
    "Models\Terrain\Medieval\bush_cluster.glb",
    "Models\Terrain\Medieval\rock_cluster.glb",
    "Models\Terrain\Medieval\fence_section.glb",
    "Models\Terrain\Medieval\ruin_wall.glb",
    "Models\Terrain\Medieval\tent.glb",
    "Models\Terrain\Medieval\campfire.glb",
    "Models\Terrain\Medieval\watchtower.glb",
    "Models\Terrain\Medieval\bridge_detail.glb",
    "Models\Units\Human\spearman.glb",
    "Models\Units\Human\swordsman.glb",
    "Models\Units\Human\archer.glb",
    "Models\Units\Human\knight.glb",
    "Models\Units\Human\king.glb",
    "Models\Units\Human\royal_guard.glb",
    "Models\Units\Human\wizard.glb",
    "Models\Units\Human\assassin.glb",
    "Models\Units\Monsters\ogre.glb",
    "Models\Siege\Medieval\catapult.glb",
    "Models\Siege\Medieval\ballista.glb",
    "Models\Siege\Medieval\trebuchet.glb",
    "Models\Props\Containers\barrel.glb",
    "Models\Props\Containers\crate.glb",
    "Models\Props\Decor\mug.glb",
    "Models\Props\Decor\bottle_cluster.glb",
    "Models\Props\Decor\candle_cluster.glb",
    "Models\Props\Decor\weapon_rack.glb",
    "Models\Props\Decor\shield_decor.glb",
    "Models\Props\Decor\book_stack.glb",
    "Models\Props\Decor\skull.glb",
    "Models\Props\Decor\dice_cluster.glb",
    "Models\Props\Gameplay\reinforcement_cart.glb",
    "Models\Props\Gameplay\reinforcement_outpost.glb",
    "Models\Props\Gameplay\trap_spikes.glb",
    "Models\Props\Gameplay\castle_brazier.glb",
    "Models\Props\Gameplay\throne.glb",
    "Models\Props\Gameplay\spellbook_open.glb",
    "Models\Props\Gameplay\mana_crystals.glb",
    "Models\Props\Gameplay\suspicion_dial.glb",
    "Models\Props\Gameplay\karma_medallion.glb",
    "Models\Props\Gameplay\cheat_stash.glb",
    "Models\Props\Gameplay\fireball_scorch.glb",
    "Models\Props\Gameplay\healing_rune.glb",
    "Models\Props\Gameplay\upgrade_totem.glb",
    "Models\Tavern\Furniture\shelf.glb",
    "Models\Tavern\Furniture\chair.glb",
    "Models\Tavern\Furniture\bench.glb",
    "Models\Tavern\Furniture\small_table.glb",
    "Models\Tavern\Lighting\chandelier.glb",
    "Models\Tavern\Lighting\brazier.glb",
    "Models\Opponent\seated_opponent.glb",
    "Models\Hero\tavern_room_hero.glb",
    "Models\Hero\battlefield_terrain_hero.glb",
    "Models\Hero\castle_hero.glb",
    "Models\Hero\opponent_hero.glb",
    "Models\Hero\war_table_hero.glb",
    "Models\Hero\spearman_hero.glb",
    "Models\Hero\archer_hero.glb",
    "Models\Hero\swordsman_hero.glb"
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

if (-not $needsAssets -and (Test-Path $assetStamp)) {
    foreach ($script in $assetScripts) {
        if ((Test-Path $script) -and ((Get-Item $script).LastWriteTime -gt (Get-Item $assetStamp).LastWriteTime)) {
            $needsAssets = $true
            break
        }
    }
}

if ($needsAssets) {
    Write-Host ""
    Write-Host "Generating/updating Blender assets..." -ForegroundColor Yellow

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

    foreach ($script in $assetScripts) {
        if (-not (Test-Path $script)) { throw "Missing Blender generator: $script" }
        Write-Host "Running $(Split-Path $script -Leaf)..." -ForegroundColor DarkGray
        & $blender --background --python $script
        if ($LASTEXITCODE -ne 0) { throw "Blender asset generation failed while running $script" }
    }

    foreach ($asset in $expectedAssets) {
        if (-not (Test-Path (Join-Path $projectRoot $asset))) { throw "Expected generated asset is missing: $asset" }
    }

    New-Item -Path $assetStamp -ItemType File -Force | Out-Null
    (Get-Item $assetStamp).LastWriteTime = Get-Date
    Write-Host "Asset generation succeeded: $($expectedAssets.Count) verified GLB assets." -ForegroundColor Green
}
else {
    Write-Host "Generated assets are already current." -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "Building CastleCards.csproj..." -ForegroundColor Yellow
dotnet build .\CastleCards.csproj
if ($LASTEXITCODE -ne 0) { throw "dotnet build failed." }

Write-Host ""
Write-Host "Castle Cards is up to date." -ForegroundColor Green
Write-Host "C# build succeeded and the reference-quality art pass is current." -ForegroundColor Green
Write-Host "If Godot is open, let it import the GLB files and accept Reload from disk if prompted." -ForegroundColor Green
