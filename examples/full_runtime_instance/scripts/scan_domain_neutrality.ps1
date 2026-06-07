param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Convert-GlobToRegex {
    param([string]$Pattern)

    $normalized = ($Pattern -replace "\\", "/").Trim("/")
    $builder = New-Object System.Text.StringBuilder
    [void]$builder.Append("^")
    $i = 0
    while ($i -lt $normalized.Length) {
        $char = $normalized[$i]
        if ($char -eq "*") {
            if (($i + 1) -lt $normalized.Length -and $normalized[$i + 1] -eq "*") {
                [void]$builder.Append(".*")
                $i += 2
            } else {
                [void]$builder.Append("[^/]*")
                $i += 1
            }
        } elseif ($char -eq "?") {
            [void]$builder.Append("[^/]")
            $i += 1
        } else {
            [void]$builder.Append([regex]::Escape([string]$char))
            $i += 1
        }
    }
    [void]$builder.Append("$")
    return $builder.ToString()
}

function Test-AnyGlob {
    param(
        [string]$RelativePath,
        [array]$Patterns
    )

    foreach ($pattern in $Patterns) {
        if ($RelativePath -match (Convert-GlobToRegex -Pattern $pattern)) {
            return $true
        }
    }
    return $false
}

function Get-RelativePath {
    param(
        [string]$RootPath,
        [string]$FullPath
    )

    $rootUri = [System.Uri]((Resolve-Path $RootPath).Path.TrimEnd("\", "/") + [System.IO.Path]::DirectorySeparatorChar)
    $fileUri = [System.Uri](Resolve-Path $FullPath).Path
    return $rootUri.MakeRelativeUri($fileUri).ToString()
}

$resolvedRoot = (Resolve-Path $Root).Path
$configPath = Join-Path $resolvedRoot "protocol.config.json"
if (-not (Test-Path $configPath)) {
    exit 0
}

$config = Get-Content -Raw $configPath -Encoding UTF8 | ConvertFrom-Json
$neutrality = $config.domain_neutrality
if (-not $neutrality -or $neutrality.enabled -eq $false) {
    exit 0
}

$denylist = @($neutrality.denylist)
$scanGlobs = @($neutrality.scan_globs)
$exemptGlobs = @($neutrality.exempt_globs)

if ($denylist.Count -eq 0 -or $scanGlobs.Count -eq 0) {
    exit 0
}

$findings = New-Object System.Collections.Generic.List[string]
$files = Get-ChildItem -Path $resolvedRoot -Recurse -File -Force | ForEach-Object {
    $relativePath = Get-RelativePath -RootPath $resolvedRoot -FullPath $_.FullName
    if ((Test-AnyGlob -RelativePath $relativePath -Patterns $scanGlobs) -and -not (Test-AnyGlob -RelativePath $relativePath -Patterns $exemptGlobs)) {
        [pscustomobject]@{ Path = $_.FullName; RelativePath = $relativePath }
    }
} | Sort-Object RelativePath

foreach ($file in $files) {
    $lines = Get-Content -Path $file.Path -Encoding UTF8
    for ($lineIndex = 0; $lineIndex -lt $lines.Count; $lineIndex++) {
        foreach ($term in $denylist) {
            $cleanTerm = ([string]$term).Trim()
            if (-not $cleanTerm) {
                continue
            }
            $pattern = "(?i)(?<!\w)$([regex]::Escape($cleanTerm))(?!\w)"
            if ($lines[$lineIndex] -match $pattern) {
                $findings.Add("$($file.RelativePath):$($lineIndex + 1): $cleanTerm")
            }
        }
    }
}

foreach ($finding in $findings) {
    Write-Host $finding
}

if ($findings.Count -gt 0) {
    exit 1
}

exit 0
