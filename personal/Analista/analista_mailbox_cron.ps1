param(
    [int]$IntervalSeconds = 300,
    [int]$MaxNoArquitectoRounds = 15,
    [string]$AgentExe = "",
    [ValidateSet("Anthropic", "LegacyCodex")][string]$AgentProvider = "Anthropic",
    # Modelo del checker. Vive AQUI a proposito: el 2026-07-20 el modelo por defecto del CLI
    # se quedo sin creditos y el checker cayo; la reparacion se hizo pasando --model en la
    # linea de lanzamiento, que se pierde en silencio en cuanto alguien relanza por la via
    # normal. Cadena vacia = usar el modelo por defecto del CLI.
    [string]$AgentModel = "opus",
    [string]$ReasoningEffort = "medium",
    [int]$ExecTimeoutSeconds = 3600,
    [int]$MaxTransientRetries = 3,
    [int]$RetryBackoffSeconds = 30,
    [int]$AbortedResidueMinutes = 5
)

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$runner = Join-Path $root "scripts\harness\peer_mailbox_cron.ps1"
$prompt = Join-Path $root "scripts\harness\prompts\reviewer.prompt.md"
$provider = if ($AgentProvider -eq "LegacyCodex") { "Codex" } else { "Anthropic" }

# Solo se fija cuando hay modelo Y proveedor Anthropic: para LegacyCodex los argumentos por
# defecto del runner son otros y no admiten --model.
$agentArgs = @()
if ($provider -eq "Anthropic" -and $AgentModel) {
    $agentArgs = @("-p", "--permission-mode", "bypassPermissions", "--output-format", "text", "--model", $AgentModel)
}

& $runner -PeerId Analista -CoordinatorId Arquitecto `
    -AcceptedTypes @("REVIEW", "REQUEST", "ACTION", "QUESTION", "DECISION") `
    -PromptFile $prompt -Root $root -AgentExe $AgentExe -AgentProvider $provider `
    -AgentArgs $agentArgs `
    -ReasoningEffort $ReasoningEffort -IntervalSeconds $IntervalSeconds `
    -MaxNoCoordinatorRounds $MaxNoArquitectoRounds -ExecTimeoutSeconds $ExecTimeoutSeconds `
    -MaxTransientRetries $MaxTransientRetries -RetryBackoffSeconds $RetryBackoffSeconds `
    -AbortedResidueMinutes $AbortedResidueMinutes
exit $LASTEXITCODE
