param([string]$Name)

if (-not $Name) {
    Write-Host "Usage: ./scripts/save.ps1 <name>  (e.g. swe, ds, google-intern)"
    exit 1
}

$root = Split-Path $PSScriptRoot -Parent
$savedDir = Join-Path $root "saved"
$buildDir = Join-Path $savedDir "build"
$draftPath = Join-Path $root "draft.tex"

if (-not (Test-Path $draftPath)) {
    Write-Host "Error: draft.tex not found at $draftPath"
    exit 1
}

# Auto-detect next number prefix
$existing = Get-ChildItem $savedDir -Filter "*.tex" |
    Where-Object { $_.Name -match '^\((\d+)\)' } |
    ForEach-Object { [int]($_.Name -replace '^\((\d+)\).*', '$1') }

$nextNum = if ($existing) { ($existing | Measure-Object -Maximum).Maximum + 1 } else { 1 }

$destName = "($nextNum)$Name.tex"
$destPath = Join-Path $savedDir $destName

# Copy draft to saved
Copy-Item -LiteralPath $draftPath -Destination $destPath
Write-Host "Saved draft as: saved/$destName"

# Compile
Write-Host "Compiling..."
& pdflatex -interaction=nonstopmode -output-directory $buildDir $destPath | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Compile failed. Check saved/build/ for logs."
    exit 1
}
Write-Host "Compiled successfully."

# Rename PDF
& "$PSScriptRoot\rename-pdf.ps1" -DocPath $destPath
Write-Host "Done. PDF saved to saved/build/"
