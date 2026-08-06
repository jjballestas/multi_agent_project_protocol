param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"
$LegacyIdentityLiteralFiles = @(
    "runtime/apply.py",
    "runtime/budget.py",
    "runtime/context.py",
    "runtime/eventlog.py",
    "runtime/ledger_ops.py",
    "runtime/metrics.py",
    "runtime/router.py",
    "scripts/prune_state.py"
)
$GenericIdentityTokens = @("agent", "human", "humano", "owner")
$RequiredScanGlobs = @(
    "scripts/**/*.py",
    "scripts/**/*.ps1",
    "Area_comun/protocol/*.json"
)
$RequiredExemptGlobs = @("runtime/memory/**")

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

function Get-ConfiguredIdentityTerms {
    param([object]$Config)

    $terms = New-Object System.Collections.Generic.HashSet[string] ([System.StringComparer]::OrdinalIgnoreCase)
    if ($Config.agent_registry -and $Config.agent_registry.agents) {
        foreach ($agent in @($Config.agent_registry.agents)) {
            $value = ([string]$agent.id).Trim()
            # Exempt generic identity words (agent/human/owner/...) as agent ids too,
            # consistent with the agent_roles handling below.
            if ($value.Length -ge 3 -and -not ($GenericIdentityTokens -contains $value.ToLowerInvariant())) {
                [void]$terms.Add($value)
            }
        }
    }
    if ($Config.agent_roles) {
        foreach ($property in $Config.agent_roles.PSObject.Properties) {
            $text = ([string]$property.Value).Trim()
            if ($text.Length -ge 3 -and -not ($GenericIdentityTokens -contains $text.ToLowerInvariant())) {
                [void]$terms.Add($text)
            }
            foreach ($token in ($text -split "\s+")) {
                $clean = ([string]$token).Trim()
                if ($clean.Length -ge 4 -and -not ($GenericIdentityTokens -contains $clean.ToLowerInvariant())) {
                    [void]$terms.Add($clean)
                }
            }
        }
    }
    return @($terms) | Sort-Object { $_.ToLowerInvariant() }
}

function Test-IdentityScanPath {
    param([string]$RelativePath)

    return (($RelativePath.StartsWith("runtime/") -and $RelativePath.EndsWith(".py")) -or
        ($RelativePath.StartsWith("scripts/") -and
            (($RelativePath.ToCharArray() | Where-Object { $_ -eq "/" }).Count -eq 1) -and
            ($RelativePath.EndsWith(".py") -or $RelativePath.EndsWith(".ps1"))))
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
foreach ($pattern in $RequiredScanGlobs) {
    if ($scanGlobs -notcontains $pattern) {
        $scanGlobs += $pattern
    }
}
foreach ($pattern in $RequiredExemptGlobs) {
    if ($exemptGlobs -notcontains $pattern) {
        $exemptGlobs += $pattern
    }
}

$scanTerms = @()
foreach ($term in $denylist) {
    $scanTerms += [pscustomobject]@{ Term = $term; Kind = "domain" }
}
foreach ($term in (Get-ConfiguredIdentityTerms -Config $config)) {
    $scanTerms += [pscustomobject]@{ Term = $term; Kind = "identity" }
}

if ($scanTerms.Count -eq 0 -or $scanGlobs.Count -eq 0) {
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
    $lines = @(Get-Content -Path $file.Path -Encoding UTF8)
    for ($lineIndex = 0; $lineIndex -lt $lines.Count; $lineIndex++) {
        foreach ($scanTerm in $scanTerms) {
            if ($scanTerm.Kind -eq "identity") {
                if (-not (Test-IdentityScanPath -RelativePath $file.RelativePath) -or $LegacyIdentityLiteralFiles -contains $file.RelativePath) {
                    continue
                }
            }
            $cleanTerm = ([string]$scanTerm.Term).Trim()
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
