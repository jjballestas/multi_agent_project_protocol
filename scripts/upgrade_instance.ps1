<#
.SYNOPSIS
    Reporte de adopcion asistida entre versiones del protocolo (espejo de upgrade_instance.py).

.DESCRIPTION
    Compara el conjunto adoptable de archivos del master contra una instancia y emite un reporte
    de deltas con acciones recomendadas. NO modifica la instancia: solo lee (y, si se pide -Report,
    escribe ese archivo). Ver DECISION-0006 §4 y Area_comun/specs/SPEC-0019-upgrade-asistido.md.

.EXAMPLE
    powershell -NoProfile -File scripts/upgrade_instance.ps1 -Instance <ruta> [-Master <ruta>] [-Report <archivo>]
#>
param(
    [Parameter(Mandatory = $true)][string]$Instance,
    [string]$Master,
    [string]$Report
)

$ErrorActionPreference = "Stop"

# Conjunto adoptable por defecto (DISENO-robustez-operacional.md §1.2). Configurable via master
# protocol.config.json -> upgrade.adoptable_globs.
$DefaultAdoptableGlobs = @(
    "AGENTS.template.md",
    "CLAUDE.template.md",
    "protocol.config.template.json",
    "Area_comun/README.template.md",
    "Area_comun/state/*.template.json",
    "Area_comun/protocol/*.md",
    "Area_comun/specs/*_TEMPLATE.md",
    "profiles/PROFILE_TEMPLATE/**/*",
    "scripts/*.py",
    "scripts/*.ps1"
)

function Read-AllTextNoBom([string]$Path) {
    # ReadAllText detecta y descarta BOM (paridad con utf-8-sig de Python).
    return [System.IO.File]::ReadAllText($Path)
}

function Get-ProtocolVersion([string]$Root) {
    $cfg = Join-Path $Root "protocol.config.json"
    if (-not (Test-Path $cfg -PathType Leaf)) { return "unknown" }
    try {
        $data = Read-AllTextNoBom $cfg | ConvertFrom-Json
        if ($null -ne $data.protocol_version) { return [string]$data.protocol_version }
    } catch { }
    return "unknown"
}

function Get-AdoptableGlobs([string]$MasterRoot) {
    $cfg = Join-Path $MasterRoot "protocol.config.json"
    if (Test-Path $cfg -PathType Leaf) {
        try {
            $data = Read-AllTextNoBom $cfg | ConvertFrom-Json
            $g = $data.upgrade.adoptable_globs
            if ($g) { return @($g) }
        } catch { }
    }
    return $DefaultAdoptableGlobs
}

function Get-RelPosix([string]$RootFull, [string]$FileFull) {
    $rel = $FileFull.Substring($RootFull.Length).TrimStart([char]'\', [char]'/')
    return ($rel -replace '\\', '/')
}

function Get-AdoptableRelFiles([string]$RootFull, [string[]]$Globs) {
    $set = New-Object System.Collections.Generic.List[string]
    $seen = @{}
    foreach ($g in $Globs) {
        $matched = @()
        if ($g.Contains("**")) {
            $base = ($g -split '\*\*')[0].TrimEnd('/')
            $basePath = Join-Path $RootFull ($base -replace '/', [System.IO.Path]::DirectorySeparatorChar)
            if (Test-Path $basePath) {
                $matched = Get-ChildItem -Path $basePath -Recurse -File -ErrorAction SilentlyContinue
            }
        }
        elseif ($g.Contains("*")) {
            $dir = [System.IO.Path]::GetDirectoryName(($g -replace '/', [System.IO.Path]::DirectorySeparatorChar))
            $leaf = [System.IO.Path]::GetFileName($g)
            $dirPath = if ([string]::IsNullOrEmpty($dir)) { $RootFull } else { Join-Path $RootFull $dir }
            if (Test-Path $dirPath) {
                $matched = Get-ChildItem -Path $dirPath -Filter $leaf -File -ErrorAction SilentlyContinue
            }
        }
        else {
            $p = Join-Path $RootFull ($g -replace '/', [System.IO.Path]::DirectorySeparatorChar)
            if (Test-Path $p -PathType Leaf) { $matched = @(Get-Item $p) }
        }
        foreach ($f in $matched) {
            $rel = Get-RelPosix $RootFull $f.FullName
            if (-not $seen.ContainsKey($rel)) { $seen[$rel] = $true; $set.Add($rel) | Out-Null }
        }
    }
    return $set
}

function Get-Normalized([string]$Path) {
    $t = Read-AllTextNoBom $Path
    return ($t -replace "`r`n", "`n" -replace "`r", "`n")
}

# --- Resolucion de rutas ---
$instanceFull = (Resolve-Path -LiteralPath $Instance -ErrorAction SilentlyContinue)
if (-not $instanceFull) { Write-Error "instancia no encontrada: $Instance"; exit 2 }
$instanceFull = $instanceFull.Path
if ($Master) {
    $masterResolved = (Resolve-Path -LiteralPath $Master -ErrorAction SilentlyContinue)
    if (-not $masterResolved) { Write-Error "master no encontrado: $Master"; exit 2 }
    $masterFull = $masterResolved.Path
}
else {
    $masterFull = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

$masterV = Get-ProtocolVersion $masterFull
$instanceV = Get-ProtocolVersion $instanceFull
$globs = Get-AdoptableGlobs $masterFull
$relFiles = Get-AdoptableRelFiles $masterFull $globs

# --- Clasificacion ---
$rows = @()
foreach ($rel in ($relFiles | Sort-Object)) {
    $m = Join-Path $masterFull ($rel -replace '/', [System.IO.Path]::DirectorySeparatorChar)
    $i = Join-Path $instanceFull ($rel -replace '/', [System.IO.Path]::DirectorySeparatorChar)
    if (-not (Test-Path $i)) { $status = "nuevo" }
    elseif ((Get-Normalized $m) -ne (Get-Normalized $i)) { $status = "cambiado" }
    else { $status = "igual" }
    $rows += [pscustomobject]@{ Rel = $rel; Status = $status }
}

# --- Render (identico a render_report de upgrade_instance.py) ---
$nuevo = ($rows | Where-Object { $_.Status -eq "nuevo" }).Count
$cambiado = ($rows | Where-Object { $_.Status -eq "cambiado" }).Count
$igual = ($rows | Where-Object { $_.Status -eq "igual" }).Count
$action = @{
    "nuevo"    = "anadir a la instancia (decision de adopcion)"
    "cambiado" = "revisar delta y decidir adopcion"
    "igual"    = "sin accion"
}
$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# Reporte de adopcion asistida")
$lines.Add("")
$lines.Add("- Version de la instancia: ``$instanceV``")
$lines.Add("- Version del master: ``$masterV``")
$lines.Add("- Conjunto adoptable: $($rows.Count) archivos (nuevo=$nuevo, cambiado=$cambiado, igual=$igual)")
$lines.Add("")
$lines.Add("> La herramienta informa; la instancia adopta por decision (DECISION-0001). No se modifico nada.")
$lines.Add("")
$lines.Add("| Archivo | Estado | Accion recomendada |")
$lines.Add("|---------|--------|--------------------|")
foreach ($r in $rows) {
    if ($r.Status -eq "igual") { continue }
    $lines.Add("| ``$($r.Rel)`` | $($r.Status) | $($action[$r.Status]) |")
}
if ($nuevo -eq 0 -and $cambiado -eq 0) {
    $lines.Add("| (ninguno) | igual | la instancia esta al dia |")
}
$report = ($lines -join "`n") + "`n"

if ($Report) {
    [System.IO.File]::WriteAllText($Report, $report)
    Write-Host "OK: reporte escrito en $Report"
}
else {
    [System.Console]::Out.Write($report)
}
exit 0
