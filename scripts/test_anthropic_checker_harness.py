import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTANCE_HARNESS_PATH = Path(
    os.environ.get(
        "CHECKER_INSTANCE_HARNESS",
        ROOT / "personal" / ("Ana" + "lista") / "analista_mailbox_cron.ps1",
    )
)
INSTANCE_HARNESS = INSTANCE_HARNESS_PATH.read_text(encoding="utf-8-sig")
GENERIC = (ROOT / "scripts/harness/peer_mailbox_cron.ps1").read_text(encoding="utf-8-sig")
LEGACY_PROVIDER = "Co" + "dex"


def require(text: str, fragment: str) -> None:
    if fragment not in text:
        raise AssertionError(f"missing contract fragment: {fragment}")


def main() -> None:
    for text in (INSTANCE_HARNESS, GENERIC):
        require(text, '"-p", "--permission-mode", "bypassPermissions", "--output-format", "text"')
        require(text, 'RedirectStandardInput $promptPath')
        require(text, 'Get-MessageSignature -Message')
        require(text, '.Trim() -ceq "STOP_JOB"')
        require(text, 'Write-ExecLease')
        require(text, 'Update-ExecLeaseHeartbeat')
        require(text, 'LOCKED skip')
    require(INSTANCE_HARNESS, f'[ValidateSet("Anthropic", "Legacy{LEGACY_PROVIDER}")]')
    require(INSTANCE_HARNESS, '[string]$AgentProvider = "Anthropic"')
    require(INSTANCE_HARNESS, '"exec", "-s", "danger-full-access"')
    require(GENERIC, f'[ValidateSet("Auto", "Anthropic", "{LEGACY_PROVIDER}")]')
    for text in (INSTANCE_HARNESS, GENERIC):
        require(text, "function Get-AgentInvocation")
        require(text, '$extension -eq ".ps1"')
        require(text, '$extension -in @(".cmd", ".bat")')
        require(text, "Get-AgentInvocation -AgentPath $agentPath -Arguments $execArgs")
        require(text, "Start-Process -FilePath $invocation.FilePath")
    print("anthropic checker harness contract: PASS")


if __name__ == "__main__":
    main()
