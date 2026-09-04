$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$cacheRoot = Join-Path $projectRoot ".asset-cache\kaykit"
New-Item -ItemType Directory -Path $cacheRoot -Force | Out-Null

function Ensure-PinnedRepo {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][string]$Commit
    )

    $target = Join-Path $cacheRoot $Name
    $gitDir = Join-Path $target ".git"

    if (-not (Test-Path $gitDir)) {
        if (Test-Path $target) {
            Remove-Item -Recurse -Force $target
        }
        New-Item -ItemType Directory -Path $target -Force | Out-Null
        Write-Host "Preparing art source cache: $Name" -ForegroundColor DarkGray
        git -C $target init --quiet
        if ($LASTEXITCODE -ne 0) { throw "Failed to initialize asset cache for $Name." }
        git -C $target remote add origin $Url
        if ($LASTEXITCODE -ne 0) { throw "Failed to configure asset source for $Name." }
    }

    $current = $null
    try {
        $current = (git -C $target rev-parse HEAD 2>$null).Trim()
    } catch {
        $current = $null
    }

    if ($current -ne $Commit) {
        Write-Host "Acquiring pinned CC0 art source: $Name" -ForegroundColor DarkGray
        git -C $target fetch --quiet --depth 1 origin $Commit
        if ($LASTEXITCODE -ne 0) { throw "Failed to download pinned art source $Name." }
        git -C $target checkout --quiet --detach FETCH_HEAD
        if ($LASTEXITCODE -ne 0) { throw "Failed to checkout pinned art source $Name." }
        git -C $target reset --quiet --hard $Commit
        if ($LASTEXITCODE -ne 0) { throw "Failed to reset pinned art source $Name." }
    }
}

# Both packs are CC0. Exact commits are pinned so a future upstream update cannot silently alter
# Castle Cards' visual build.
Ensure-PinnedRepo `
    -Name "medieval" `
    -Url "https://github.com/KayKit-Game-Assets/KayKit-Medieval-Hexagon-Pack-1.0.git" `
    -Commit "84fa4e91af6a88989be7c99e0891cede11f2ca38"

Ensure-PinnedRepo `
    -Name "adventurers" `
    -Url "https://github.com/KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0.git" `
    -Commit "672074b73ba276876a19e8816ecdc5241817ab47"

$required = @(
    ".asset-cache\kaykit\medieval\addons\kaykit_medieval_hexagon_pack\Assets\gltf\buildings\blue\building_castle_blue.gltf",
    ".asset-cache\kaykit\medieval\addons\kaykit_medieval_hexagon_pack\Assets\gltf\buildings\red\building_castle_red.gltf",
    ".asset-cache\kaykit\medieval\addons\kaykit_medieval_hexagon_pack\Assets\gltf\buildings\neutral\wall_straight.gltf",
    ".asset-cache\kaykit\medieval\addons\kaykit_medieval_hexagon_pack\Assets\gltf\decoration\nature\tree_single_A.gltf",
    ".asset-cache\kaykit\adventurers\addons\kaykit_character_pack_adventures\Characters\gltf\Barbarian.glb"
)

foreach ($relative in $required) {
    $full = Join-Path $projectRoot $relative
    if (-not (Test-Path $full)) {
        throw "Pinned quality asset source is incomplete: $relative"
    }
}

Write-Host "Pinned CC0 quality art sources are ready." -ForegroundColor DarkGray
