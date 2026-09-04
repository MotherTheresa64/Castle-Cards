$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$generator = Join-Path $projectRoot "ArtSource\Blender\Scripts\build_model_review_workspace.py"
$reviewFile = Join-Path $projectRoot "ArtSource\Blender\ModelReview\AllModels_Review.blend"

Write-Host ""
Write-Host "=== Castle Cards Blender Model Review ===" -ForegroundColor Cyan
Write-Host "Project: $projectRoot"
Write-Host ""

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

if (-not $blender) {
    throw "Blender could not be found. Install Blender or add blender.exe to PATH."
}
if (-not (Test-Path $generator)) {
    throw "Missing model review generator: $generator"
}

$modelsRoot = Join-Path $projectRoot "Models"
if (-not (Test-Path $modelsRoot)) {
    throw "The Models folder does not exist yet. Run Update-Project.bat first."
}

Write-Host "Blender: $blender" -ForegroundColor DarkGray
Write-Host "Generating editable individual .blend files and review workspace..." -ForegroundColor Yellow
& $blender --background --python $generator
if ($LASTEXITCODE -ne 0) {
    throw "Blender model review generation failed."
}

if (-not (Test-Path $reviewFile)) {
    throw "Expected review file was not created: $reviewFile"
}

Write-Host ""
Write-Host "Opening all-model review workspace in Blender..." -ForegroundColor Green
Write-Host "Individual editable files are under ArtSource\Blender\IndividualModels." -ForegroundColor Green
Start-Process -FilePath $blender -ArgumentList @($reviewFile)
