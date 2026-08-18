param([string]$DraftPath)

if (-not (Test-Path $DraftPath)) {
    Write-Host "Error: draft.tex not found at $DraftPath"
    exit 1
}

$lines = Get-Content $DraftPath
$flagged = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '\\resumeItem\{\s*\*') {
        $flagged += "  Line $($i + 1): $($lines[$i].Trim())"
    }
}

if ($flagged.Count -gt 0) {
    Write-Host "Pre-save check failed: unreviewed draft bullet(s) found (leading '*')."
    $flagged | ForEach-Object { Write-Host $_ }
    Write-Host "Per CLAUDE.md, only the user may remove a draft asterisk. Review these bullets, then save again."
    exit 1
}

exit 0
