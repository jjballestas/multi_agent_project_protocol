param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"
$IdentityLiteralExemptions = @{
    "runtime/apply.py" = @{
        Reason = "Compatibility fixture output preserves the historical implementer owner."
        Lines = @{
            440 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
        }
    }
    "runtime/budget.py" = @{
        Reason = "Historical hardening annotations identify the independent review pass."
        Lines = @{
            68 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e")
            104 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e")
        }
    }
    "runtime/context.py" = @{
        Reason = "Legacy fallback roles preserve the pre-registry compatibility contract."
        Lines = @{
            16 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            17 = @("e257b110509437aaceddbd342bc63d05e74221d6bac056ed279d752ff8d3afcb", "9775f123593b08a132c7cf8f54927592c171e05134bae46a8c0ed7b40579b178")
        }
    }
    "runtime/eventlog.py" = @{
        Reason = "Legacy key fallbacks and historical review annotations are compatibility evidence."
        Lines = @{
            316 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e", "fcfd3ebc250c5fa0477f28cfa8c36c8910231a6836f973267d4a4ebc730d1ab7", "57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            468 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e")
            1176 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e")
        }
    }
    "runtime/ledger_ops.py" = @{
        Reason = "The legacy command description names the compatibility loop it builds for."
        Lines = @{
            319 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
        }
    }
    "runtime/metrics.py" = @{
        Reason = "A historical hardening annotation identifies the independent review pass."
        Lines = @{
            196 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e")
        }
    }
    "runtime/router.py" = @{
        Reason = "Legacy fallback envelopes preserve the pre-registry human-owner contract."
        Lines = @{
            120 = @("e257b110509437aaceddbd342bc63d05e74221d6bac056ed279d752ff8d3afcb", "9775f123593b08a132c7cf8f54927592c171e05134bae46a8c0ed7b40579b178")
            130 = @("e257b110509437aaceddbd342bc63d05e74221d6bac056ed279d752ff8d3afcb", "9775f123593b08a132c7cf8f54927592c171e05134bae46a8c0ed7b40579b178")
        }
    }
    "scripts/harness/peer_mailbox_cron.ps1" = @{
        Reason = "These occurrences identify the third-party provider CLI, executable, or install path."
        Lines = @{
            9 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            420 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            427 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            437 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            446 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            447 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            454 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            470 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1337 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
        }
    }
    "scripts/memory/test_memory_db.py" = @{
        Reason = "Exact fixture lines exercise multi-agent indexing and per-agent memory isolation."
        Lines = @{
            172 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e", "fcfd3ebc250c5fa0477f28cfa8c36c8910231a6836f973267d4a4ebc730d1ab7", "57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            205 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            206 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            273 = @("fcfd3ebc250c5fa0477f28cfa8c36c8910231a6836f973267d4a4ebc730d1ab7", "57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            304 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            313 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            318 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            341 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            355 = @("e257b110509437aaceddbd342bc63d05e74221d6bac056ed279d752ff8d3afcb")
            360 = @("e257b110509437aaceddbd342bc63d05e74221d6bac056ed279d752ff8d3afcb")
            382 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            440 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            444 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            449 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            455 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            461 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            468 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            495 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            520 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            525 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            563 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            879 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            964 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1020 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1062 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1077 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1128 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1182 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1186 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1413 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1726 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1787 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1864 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1882 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1911 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1920 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1943 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1958 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1981 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1991 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2008 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2025 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2030 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2040 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2046 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2064 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2083 = @("fcfd3ebc250c5fa0477f28cfa8c36c8910231a6836f973267d4a4ebc730d1ab7", "57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2090 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2124 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2125 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2140 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2162 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2176 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2185 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2193 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2202 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
        }
    }
    "scripts/prune_state.py" = @{
        Reason = "Legacy state fixtures preserve the historical writer marker."
        Lines = @{
            272 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            409 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            410 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            411 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            412 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
        }
    }
}
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
            ($RelativePath.EndsWith(".py") -or $RelativePath.EndsWith(".ps1"))))
}

function Test-IdentityLiteralExempt {
    param(
        [string]$RelativePath,
        [int]$LineNumber,
        [string]$Term
    )

    if (-not $IdentityLiteralExemptions.ContainsKey($RelativePath)) {
        return $false
    }
    $declaration = $IdentityLiteralExemptions[$RelativePath]
    if (-not $declaration.Lines.ContainsKey($LineNumber)) {
        return $false
    }

    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Term.ToLowerInvariant())
        $digest = -join ($sha256.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") })
    } finally {
        $sha256.Dispose()
    }
    return $declaration.Lines[$LineNumber] -contains $digest
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
                if (-not (Test-IdentityScanPath -RelativePath $file.RelativePath)) {
                    continue
                }
                if (Test-IdentityLiteralExempt -RelativePath $file.RelativePath -LineNumber ($lineIndex + 1) -Term $scanTerm.Term) {
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
