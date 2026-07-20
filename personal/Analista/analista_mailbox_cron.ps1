param(
    [int]$IntervalSeconds = 300,
    [int]$MaxNoArquitectoRounds = 15,
    [string]$AgentExe = "",
    [ValidateSet("Anthropic", "LegacyCodex")][string]$AgentProvider = "Anthropic",
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
& $runner -PeerId Analista -CoordinatorId Arquitecto `
    -AcceptedTypes @("REVIEW", "REQUEST", "ACTION", "QUESTION", "DECISION") `
    -PromptFile $prompt -Root $root -AgentExe $AgentExe -AgentProvider $provider `
    -ReasoningEffort $ReasoningEffort -IntervalSeconds $IntervalSeconds `
    -MaxNoCoordinatorRounds $MaxNoArquitectoRounds -ExecTimeoutSeconds $ExecTimeoutSeconds `
    -MaxTransientRetries $MaxTransientRetries -RetryBackoffSeconds $RetryBackoffSeconds `
    -AbortedResidueMinutes $AbortedResidueMinutes
exit $LASTEXITCODE
