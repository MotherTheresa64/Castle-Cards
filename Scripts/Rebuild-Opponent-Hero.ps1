$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "=== Castle Cards Opponent Hero V3 ===" -ForegroundColor Cyan
Write-Host "Rebuilding only the seated opponent and opening the editable Blender source..." -ForegroundColor Yellow

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

$generator = Join-Path $projectRoot "ArtSource\Blender\Scripts\generate_opponent_hero_v3.py"
$sourceBlend = Join-Path $projectRoot "ArtSource\Blender\HeroSources\opponent_hero_v3.blend"
$heroGlb = Join-Path $projectRoot "Models\Hero\opponent_hero.glb"
$fallbackGlb = Join-Path $projectRoot "Models\Opponent\seated_opponent.glb"

if (-not (Test-Path $generator)) { throw "Missing opponent generator: $generator" }

Write-Host "Blender: $blender" -ForegroundColor DarkGray
Write-Host "Running generate_opponent_hero_v3.py..." -ForegroundColor DarkGray
& $blender --background --python $generator
if ($LASTEXITCODE -ne 0) { throw "Opponent hero V3 generation failed." }

foreach ($path in @($sourceBlend, $heroGlb, $fallbackGlb)) {
    if (-not (Test-Path $path)) { throw "Expected opponent output was not created: $path" }
}

Write-Host ""
Write-Host "Opponent V3 generated successfully." -ForegroundColor Green
Write-Host "Runtime hero: Models\Hero\opponent_hero.glb" -ForegroundColor Green
Write-Host "Review fallback: Models\Opponent\seated_opponent.glb" -ForegroundColor Green
Write-Host "Editable source: ArtSource\Blender\HeroSources\opponent_hero_v3.blend" -ForegroundColor Green
Write-Host "Opening the editable V3 source in Blender..." -ForegroundColor Green
Start-Process -FilePath $blender -ArgumentList @($sourceBlend)
