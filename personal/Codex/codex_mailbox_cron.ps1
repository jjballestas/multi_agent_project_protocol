param(
    [int]$IntervalSeconds = 300,
    [int]$MaxNoArquitectoRounds = 15,
    [string]$CodexExe = "",
    [int]$ExecTimeoutSeconds = 3600,
    [int]$PostDeliveryTimeoutSeconds = 300,
    [int]$MaxTransientRetries = 3,
    [int]$RetryBackoffSeconds = 30,
    [int]$AbortedResidueMinutes = 5
)

$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$runner = Join-Path $root "scripts\harness\peer_mailbox_cron.ps1"
$prompt = Join-Path $root "scripts\harness\prompts\implementer.prompt.md"
& $runner -PeerId Codex -CoordinatorId Arquitecto -PromptFile $prompt -Root $root `
    -AgentExe $CodexExe -AgentProvider Codex -ReasoningEffort low `
    -IntervalSeconds $IntervalSeconds -MaxNoCoordinatorRounds $MaxNoArquitectoRounds `
    -ExecTimeoutSeconds $ExecTimeoutSeconds -MaxTransientRetries $MaxTransientRetries `
    -PostDeliveryTimeoutSeconds $PostDeliveryTimeoutSeconds `
    -RetryBackoffSeconds $RetryBackoffSeconds -AbortedResidueMinutes $AbortedResidueMinutes
exit $LASTEXITCODE
