param([string]$DocPath)

$dir = Split-Path $DocPath -Parent
$name = [System.IO.Path]::GetFileNameWithoutExtension($DocPath)
$buildDir = Join-Path $dir "build"

# Find the source PDF in build dir
$sourcePdf = Join-Path $buildDir "$name.pdf"

if (-not (Test-Path $sourcePdf)) { exit 0 }

# Strip leading (N) prefix like (1)main -> main
$cleanName = $name -replace '^\(\d+\)', ''

# Default: always rename to Alessandro_Felici_Resume.pdf if no match
$destName = "Alessandro_Felici_Resume.pdf"

$destPdf = Join-Path $buildDir $destName
Copy-Item -LiteralPath $sourcePdf -Destination $destPdf -Force
