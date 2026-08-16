param(
    [string]$Root = ".",
    [switch]$DumpIdentityInventory
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
            318 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e", "fcfd3ebc250c5fa0477f28cfa8c36c8910231a6836f973267d4a4ebc730d1ab7", "57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            470 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e")
            1284 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e")
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
            553 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            560 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            570 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            579 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            580 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            587 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            603 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1515 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
        }
    }
    "scripts/memory/test_memory_db.py" = @{
        Reason = "Exact fixture lines exercise multi-agent indexing and per-agent memory isolation."
        Lines = @{
            205 = @("1a05b53aa74c2c562c4ce31e6e8bc5d7e4b954218793b97f95660a88c54d4b2e", "fcfd3ebc250c5fa0477f28cfa8c36c8910231a6836f973267d4a4ebc730d1ab7", "57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            238 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            239 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            306 = @("fcfd3ebc250c5fa0477f28cfa8c36c8910231a6836f973267d4a4ebc730d1ab7", "57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            337 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            346 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            351 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            374 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            388 = @("e257b110509437aaceddbd342bc63d05e74221d6bac056ed279d752ff8d3afcb")
            393 = @("e257b110509437aaceddbd342bc63d05e74221d6bac056ed279d752ff8d3afcb")
            415 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            473 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            477 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            482 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            488 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            494 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            501 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            528 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            553 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            558 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            596 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            912 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            997 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1053 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1095 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1110 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1161 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1215 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1219 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1446 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1759 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1820 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1897 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1915 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1944 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1953 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1976 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            1991 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2014 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2024 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2041 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2058 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2063 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2073 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2079 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2097 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2116 = @("fcfd3ebc250c5fa0477f28cfa8c36c8910231a6836f973267d4a4ebc730d1ab7", "57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2123 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2157 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2158 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2173 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2195 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2209 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2218 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2226 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
            2235 = @("57de4cf40144bdf7d00010f2f5557a7d642c2b9705309bfade167dd313e2ca93")
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

    $resolvedRootPath = (Resolve-Path -LiteralPath $RootPath).Path
    $resolvedFullPath = (Resolve-Path -LiteralPath $FullPath).Path
    $trimChars = [char[]]@([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
    $rootPrefix = $resolvedRootPath.TrimEnd($trimChars) + [System.IO.Path]::DirectorySeparatorChar
    $comparison = if ([System.IO.Path]::DirectorySeparatorChar -eq [char]'\') {
        [System.StringComparison]::OrdinalIgnoreCase
    } else {
        [System.StringComparison]::Ordinal
    }
    if (-not $resolvedFullPath.StartsWith($rootPrefix, $comparison)) {
        throw "Path is outside the scan root: $resolvedFullPath"
    }
    $relativePath = $resolvedFullPath.Substring($rootPrefix.Length)
    return ($relativePath -replace "\\", "/")
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

if ($DumpIdentityInventory) {
    # Emit the effective inventory after the real scan has consumed it. Any top-level
    # declaration that can affect scanning has already run, irrespective of its source form.
    $InventoryOutput = [ordered]@{}
    foreach ($InventoryPath in @($IdentityLiteralExemptions.Keys) | Sort-Object) {
        $InventoryLines = [ordered]@{}
        foreach ($InventoryLine in @($IdentityLiteralExemptions[$InventoryPath].Lines.Keys) | Sort-Object) {
            $InventoryLines[[string]$InventoryLine] = @(
                $IdentityLiteralExemptions[$InventoryPath].Lines[$InventoryLine]
            )
        }
        $InventoryOutput[$InventoryPath] = $InventoryLines
    }
    $InventoryOutput | ConvertTo-Json -Depth 8 -Compress
    exit 0
}

foreach ($finding in $findings) {
    Write-Host $finding
}

if ($findings.Count -gt 0) {
    exit 1
}

exit 0
