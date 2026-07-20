#!/usr/bin/env python3
"""End-to-end regression for bounded retry and post-confirmation seen marking."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "harness" / "peer_mailbox_cron.ps1"


def run(*args: str, cwd: Path, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=True)


def main() -> int:
    sandbox = Path(tempfile.mkdtemp(prefix="mailbox-retry-"))
    try:
        (sandbox / "Area_comun/mailbox/open").mkdir(parents=True)
        (sandbox / "runtime/state").mkdir(parents=True)
        (sandbox / "scripts/harness/prompts").mkdir(parents=True)
        shutil.copy2(RUNNER, sandbox / "scripts/harness/peer_mailbox_cron.ps1")
        (sandbox / "protocol.config.json").write_text("{}\n", encoding="utf-8")
        (sandbox / "runtime/state/events.jsonl").write_text("", encoding="ascii")
        (sandbox / ".gitignore").write_text(".protocol-tmp/\n", encoding="ascii")
        (sandbox / "predirty.txt").write_text("baseline\n", encoding="ascii")
        message = sandbox / "Area_comun/mailbox/open/MSG-retry.md"
        message.write_text(
            "---\nfrom: Arquitecto\nto: TestPeer\ntype: ACTION\nstatus: open\n"
            "requires_response: true\nresponse_owner: TestPeer\nrequested_action: test\n---\n",
            encoding="ascii",
        )
        prompt = sandbox / "scripts/harness/prompts/test.prompt.md"
        prompt.write_text("Process @@MESSAGE_PATH@@ under @@ROOT@@.\n", encoding="ascii")
        fake_core = sandbox / "fake-agent-core.ps1"
        fake_core.write_text(
            "$root=(Get-Location).Path\n"
            "$countPath=Join-Path $root '.protocol-tmp/fake-count.txt'\n"
            "$count=if(Test-Path $countPath){[int](Get-Content $countPath)}else{0}\n"
            "$count++; Set-Content -Path $countPath -Value $count -Encoding ASCII\n"
            "if($count -eq 1){\n"
            "  Set-Content -Path (Join-Path $root 'peer.txt') -Value peer -Encoding ASCII\n"
            "  git add peer.txt\n"
            "  git commit -m 'uniform-author concurrent commit' | Out-Null\n"
            "  Write-Output 'no work was applied'\n"
            "  exit 0\n"
            "}\n"
            "if($count -eq 2){\n"
            "  Set-Content -Path (Join-Path $root 'residue.txt') -Value residue -Encoding ASCII\n"
            "  git add residue.txt\n"
            "  Set-Content -Path (Join-Path $root 'predirty.txt') -Value exec-content -Encoding ASCII\n"
            "  git add predirty.txt\n"
            "  Write-Output 'status: blocked claim ajeno active claim pre-gate rojo'\n"
            "  Write-Output 'OUTCOME: transient'\n"
            "  exit 0\n"
            "}\n"
            "$response=Join-Path $root 'Area_comun/mailbox/open/MSG-response.md'\n"
            "Set-Content -Path $response -Value 'response confirmed' -Encoding ASCII\n"
            "git add $response; git commit -m 'test confirmed response' | Out-Null\n"
            "$event='{\"seq\":1,\"actor\":\"TestPeer\",\"actor_auth\":{\"method\":\"ed25519\",\"keyid\":\"testpeer:v1\",\"sig\":\"fixture-signature\"}}'\n"
            "Add-Content -Path (Join-Path $root 'runtime/state/events.jsonl') -Value $event -Encoding ASCII\n"
            "Write-Output 'status: in_review'\n",
            encoding="ascii",
        )
        fake = sandbox / "fake-agent.cmd"
        fake.write_text("@powershell.exe -NoProfile -ExecutionPolicy Bypass -File \"%~dp0fake-agent-core.ps1\"\n", encoding="ascii")
        run("git", "init", cwd=sandbox)
        run("git", "config", "user.email", "retry@example.invalid", cwd=sandbox)
        run("git", "config", "user.name", "TestPeer", cwd=sandbox)
        run("git", "add", ".", cwd=sandbox)
        run("git", "commit", "-m", "fixture", cwd=sandbox)
        (sandbox / "predirty.txt").write_text("peer-content\n", encoding="ascii")
        result = run(
            "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER),
            "-PeerId", "TestPeer", "-Root", str(sandbox), "-PromptFile", str(prompt),
            "-AgentExe", str(fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
            "-MaxNoCoordinatorRounds", "5", "-ExecTimeoutSeconds", "20",
            "-MaxTransientRetries", "3", "-RetryBackoffSeconds", "0", "-AbortedResidueMinutes", "0",
            cwd=sandbox,
        )
        runtime = sandbox / ".protocol-tmp/testpeer_mailbox_cron"
        if not (runtime / "testpeer_mailbox_cron.seen.json").exists():
            log_path = runtime / "testpeer_mailbox_cron.log"
            details = log_path.read_text(encoding="utf-8") if log_path.exists() else result.stdout + result.stderr
            raise AssertionError(f"seen state missing; runner evidence:\n{details}")
        seen = json.loads((runtime / "testpeer_mailbox_cron.seen.json").read_text(encoding="utf-8"))
        log = (runtime / "testpeer_mailbox_cron.log").read_text(encoding="utf-8")
        retry_path = runtime / "testpeer_mailbox_cron.retry.json"
        if not retry_path.exists():
            raise AssertionError(f"retry state missing; runner evidence:\n{log}")
        retry = json.loads(retry_path.read_text(encoding="utf-8"))
        assert message.name in seen, "confirmed second exec was not marked seen"
        assert message.name not in retry, "retry state was not cleared after confirmation"
        assert not (sandbox / "residue.txt").exists(), "aborted exec residue survived rollback"
        assert (sandbox / "predirty.txt").read_text(encoding="ascii") == "peer-content\n"
        predirty_status = run("git", "status", "--porcelain", "--", "predirty.txt", cwd=sandbox).stdout
        assert predirty_status.startswith(" M "), f"pre-dirty index/worktree state was not restored: {predirty_status!r}"
        assert "outcome=unconfirmed" in log and "RETRY_SCHEDULED attempt=1" in log
        assert "outcome=transient" in log and "RETRY_SCHEDULED attempt=2" in log
        assert "outcome=confirmed" in log
        assert int((sandbox / ".protocol-tmp/fake-count.txt").read_text()) == 3
        print("mailbox retry cases: PASS (uniform author rejected -> rollback -> signed-ledger confirmation)")
        return 0
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
