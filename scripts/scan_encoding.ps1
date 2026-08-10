param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [switch]$DumpPolicy
)

$ErrorActionPreference = "Stop"

$ResolvedRoot = (Resolve-Path $Root).Path
# Match the Python scanner's exact relative-path semantics on every host.
$PathComparison = [System.StringComparison]::Ordinal
$SkipDirs = @(".git", ".venv", "venv", "__pycache__", "node_modules")
$SkipAbsoluteDirs = @((Join-Path $ResolvedRoot "runtime/memory"))
$SkipSuffixes = @(".pyc", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip")
$MojibakeSignatures = @(
    [string][char]0x00c3,
    [string][char]0x00c2,
    "$([char]0x00e2)$([char]0x20ac)",
    "$([char]0x00e2)$([char]0x20ac)$([char]0x2122)",
    "$([char]0x00e2)$([char]0x20ac)$([char]0x0153)",
    "$([char]0x00e2)$([char]0x20ac)$([char]0xfffd)",
    "$([char]0x00e2)$([char]0x20ac)$([char]0x201c)",
    "$([char]0x00e2)$([char]0x20ac)$([char]0x201d)",
    "$([char]0x00e2)$([char]0x20ac)$([char]0x00a6)",
    [string][char]0xfffd
)

$Findings = New-Object System.Collections.Generic.List[string]

function Get-RelativePath {
    param([string]$Path)
    $relative = [System.IO.Path]::GetRelativePath($ResolvedRoot, $Path)
    return ($relative -replace "\\", "/")
}

function Get-SharedSuffix {
    param([string]$Name)
    # Shared rule: only a final dot after at least one basename character starts a suffix.
    $dot = $Name.LastIndexOf([char]'.')
    if ($dot -le 0) { return "" }
    return $Name.Substring($dot).ToLowerInvariant()
}

function Should-Scan {
    param([System.IO.FileInfo]$File)
    if ($SkipSuffixes -ccontains (Get-SharedSuffix $File.Name)) { return $false }
    foreach ($directory in $SkipAbsoluteDirs) {
        # Compare one host-native directory boundary, never a literal slash shape.
        $trimChars = [char[]]@([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
        $directoryPrefix = $directory.TrimEnd($trimChars) + [System.IO.Path]::DirectorySeparatorChar
        if ($File.FullName.Equals($directory, $PathComparison) -or $File.FullName.StartsWith($directoryPrefix, $PathComparison)) { return $false }
    }
    foreach ($part in $File.FullName.Split([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)) {
        if ($SkipDirs -ccontains $part) { return $false }
    }
    return $true
}

function Get-LineForOffset {
    param([byte[]]$Bytes, [int]$Offset)
    $line = 1
    for ($i = 0; $i -lt $Offset; $i++) {
        if ($Bytes[$i] -eq 10) { $line++ }
    }
    return $line
}

function Scan-AsciiPath {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return }
    Get-ChildItem -LiteralPath $Path -Recurse -File -Force | ForEach-Object {
        if (-not (Should-Scan $_)) { return }
        $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
        for ($i = 0; $i -lt $bytes.Length; $i++) {
            if ($bytes[$i] -gt 127) {
                $line = Get-LineForOffset -Bytes $bytes -Offset $i
                $detail = "byte 0x{0:x2}" -f $bytes[$i]
                $Findings.Add("non_ascii_channel: $(Get-RelativePath $_.FullName):$line ($detail)")
                break
            }
        }
    }
}

function Scan-AsciiStateJson {
    $statePath = Join-Path $ResolvedRoot "Area_comun/state"
    if (-not (Test-Path -LiteralPath $statePath)) { return }
    Get-ChildItem -LiteralPath $statePath -Filter "*.json" -File -Force | ForEach-Object {
        if (-not (Should-Scan $_)) { return }
        $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
        for ($i = 0; $i -lt $bytes.Length; $i++) {
            if ($bytes[$i] -gt 127) {
                $line = Get-LineForOffset -Bytes $bytes -Offset $i
                $detail = "byte 0x{0:x2}" -f $bytes[$i]
                $Findings.Add("non_ascii_channel: $(Get-RelativePath $_.FullName):$line ($detail)")
                break
            }
        }
    }
}

function Scan-MojibakeRoot {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return }
    Get-ChildItem -LiteralPath $Path -Recurse -File -Force | ForEach-Object {
        if (-not (Should-Scan $_)) { return }
        $lines = [System.IO.File]::ReadAllLines($_.FullName, [System.Text.Encoding]::UTF8)
        for ($lineIndex = 0; $lineIndex -lt $lines.Count; $lineIndex++) {
            foreach ($signature in $MojibakeSignatures) {
                if ($lines[$lineIndex].Contains($signature)) {
                    $Findings.Add("mojibake: $(Get-RelativePath $_.FullName):$($lineIndex + 1) ($signature)")
                    return
                }
            }
        }
    }
}

if ($DumpPolicy) {
    # Emit the policy after every top-level assignment has run, at the same point where
    # the scanner consumes it. Tests therefore observe values, not source formatting.
    [ordered]@{
        skip_dirs = @($SkipDirs)
        skip_relative_dirs = @($SkipAbsoluteDirs | ForEach-Object { Get-RelativePath $_ })
        skip_suffixes = @($SkipSuffixes)
    } | ConvertTo-Json -Compress
    exit 0
}

Scan-AsciiPath (Join-Path $ResolvedRoot "Area_comun/mailbox")
Scan-AsciiStateJson
Scan-MojibakeRoot (Join-Path $ResolvedRoot "Area_comun")
Scan-MojibakeRoot (Join-Path $ResolvedRoot "runtime")

if ($Findings.Count -gt 0) {
    Write-Output "ENCODING ERRORS:"
    $Findings | ForEach-Object { Write-Output "- $_" }
    exit 1
}

Write-Output "OK: encoding scan is clean."
exit 0
