from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANALISTA = (ROOT / "personal/Analista/analista_mailbox_cron.ps1").read_text(encoding="utf-8-sig")
GENERIC = (ROOT / "scripts/harness/peer_mailbox_cron.ps1").read_text(encoding="utf-8-sig")


def require(text: str, fragment: str) -> None:
    if fragment not in text:
        raise AssertionError(f"missing contract fragment: {fragment}")


def main() -> None:
    for text in (ANALISTA, GENERIC):
        require(text, '"-p", "--permission-mode", "bypassPermissions", "--output-format", "text"')
        require(text, 'RedirectStandardInput $promptPath')
        require(text, 'Get-MessageSignature -Message')
        require(text, '.Trim() -ceq "STOP_JOB"')
        require(text, 'Write-ExecLease')
        require(text, 'Update-ExecLeaseHeartbeat')
        require(text, 'LOCKED skip')
    require(ANALISTA, '[ValidateSet("Anthropic", "LegacyCodex")]')
    require(ANALISTA, '[string]$AgentProvider = "Anthropic"')
    require(ANALISTA, '"exec", "-s", "danger-full-access"')
    require(GENERIC, '[ValidateSet("Auto", "Anthropic", "Codex")]')
    print("anthropic checker harness contract: PASS")


if __name__ == "__main__":
    main()
