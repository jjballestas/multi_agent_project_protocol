#!/usr/bin/env python3
"""End-to-end regression for bounded retry and post-confirmation seen marking."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "harness" / "peer_mailbox_cron.ps1"
LEDGER_HEAD = ROOT / "scripts" / "ledger_head.py"


def run_outcome_parser_cases(sandbox: Path) -> None:
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    match = re.search(
        r"(?ms)^function Get-ExecOutcomeClass \{.*?^\}\r?\n\r?\nfunction Get-MessageSignature",
        runner_text,
    )
    if not match:
        raise AssertionError("Get-ExecOutcomeClass function not found")
    function_text = match.group(0).rsplit("\nfunction Get-MessageSignature", 1)[0]
    probe = sandbox / "outcome-parser-probe.ps1"
    # The first two response/diagnostic pairs are reduced verbatim from the real
    # 2026-07-20 Codex field transcripts. The diagnostics contain the CLI epilogue
    # and echoed prompt vocabulary that previously forced a false definitive.
    cases = [
        {
            "name": "real_doneflip_codex_epilogue",
            "response": "Further ledger action is blocked because the mandatory preflight validator fails.\n\nOUTCOME: transient\n",
            "diagnostic": "prompt intake: out_of_scope FUERA de alcance\nOUTCOME: transient\ntokens used\n34.968\n",
            "expected": "transient",
        },
        {
            "name": "real_task0277_codex_epilogue",
            "response": "status: blocked\nrisks: Starting now would violate the mandatory cold-start gate.\n\nOUTCOME: transient\n",
            "diagnostic": "prompt intake: out_of_scope FUERA de alcance\nOUTCOME: transient\ntokens used\n42.041\n",
            "expected": "transient",
        },
        {
            "name": "checker_diagnostic_epilogue_ignored",
            "response": "Review could not start.\nOUTCOME: transient\n",
            "diagnostic": "Total cost: 0.42 USD\nTurns: 3\nOUTCOME: definitive\n",
            "expected": "transient",
        },
        {
            "name": "prompt_lexicon_cannot_make_definitive",
            "response": "No structured outcome was emitted.\n",
            "diagnostic": "NO-GO change_required out_of_scope FUERA de alcance\nOUTCOME: definitive\n",
            "expected": "unconfirmed",
        },
        {
            "name": "response_free_text_cannot_make_definitive",
            "response": "NO-GO because this is out_of_scope and fuera de alcance.\n",
            "diagnostic": "",
            "expected": "unconfirmed",
        },
    ]
    rendered = [function_text, "$ErrorActionPreference = 'Stop'", "$results = @()"]
    for case in cases:
        response = case["response"].replace("'", "''")
        diagnostic = case["diagnostic"].replace("'", "''")
        rendered.append(f"$response = @'\n{response}'@")
        rendered.append(f"$diagnostic = @'\n{diagnostic}'@")
        rendered.append(
            "$results += [pscustomobject]@{ name = '"
            + case["name"]
            + "'; outcome = (Get-ExecOutcomeClass -ExitCode 0 -AgentResponse $response -InvokerDiagnostics $diagnostic -OwnEvidence $false) }"
        )
    rendered.append("$results | ConvertTo-Json -Compress")
    probe.write_text("\n".join(rendered) + "\n", encoding="utf-8")
    parsed = json.loads(run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(probe), cwd=sandbox).stdout)
    actual = {item["name"]: item["outcome"] for item in parsed}
    for case in cases:
        assert actual[case["name"]] == case["expected"], (case["name"], actual[case["name"]])


def run_torn_tail_case(sandbox: Path) -> None:
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    head_fn = re.search(r"(?ms)^function Get-LedgerHead \{.*?^\}", runner_text)
    restore_fn = re.search(r"(?ms)^function Restore-TransientExecResidue \{.*?^\}", runner_text)
    if not head_fn or not restore_fn:
        raise AssertionError("rollback helper functions not found")
    events = sandbox / "runtime/state/events.jsonl"
    events.write_bytes(b'{"seq":1}\n{"seq":')
    probe = sandbox / "torn-tail-probe.ps1"
    probe.write_text(
        "$Root=(Get-Location).Path\n$RunsDir=$Root\n$log=@()\n"
        "function Write-Log { param([string]$Message) $script:log += $Message }\n"
        + head_fn.group(0) + "\n" + restore_fn.group(0) + "\n"
        "$before=[pscustomobject]@{readable=$true;seq=1;hash='before';torn_tail=$false}\n"
        "$head=git rev-parse HEAD\n"
        "Restore-TransientExecResidue -HeadBefore $head -IndexPatch '' -WorktreePatch '' -UntrackedBefore @() -LedgerHeadBefore $before\n"
        "$log | ConvertTo-Json -Compress\n",
        encoding="ascii",
    )
    output = run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(probe), cwd=sandbox).stdout
    assert "ROLLBACK_DEFER reason=ledger_torn_tail" in output, output
    assert events.read_bytes().endswith(b'{"seq":'), "torn-tail deferral mutated the queue"


def run(*args: str, cwd: Path, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=True)


def run_unreadable_head_case(sandbox: Path, prompt: Path, fake: Path) -> None:
    """A valid old own event must not confirm work when the head helper fails."""
    helper = sandbox / "scripts/ledger_head.py"
    helper.write_text("raise SystemExit(23)\n", encoding="ascii")
    events = sandbox / "runtime/state/events.jsonl"
    events.write_text(
        '{"seq":1,"actor":"TestPeer","actor_auth":{"method":"ed25519",'
        '"keyid":"testpeer:v1","sig":"old-signature"}}\n',
        encoding="ascii",
    )
    runtime = sandbox / ".protocol-tmp/testpeer_mailbox_cron"
    command = [
        "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER),
        "-PeerId", "TestPeer", "-Root", str(sandbox), "-PromptFile", str(prompt),
        "-AgentExe", str(fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
        "-MaxNoCoordinatorRounds", "6", "-ExecTimeoutSeconds", "20",
        "-MaxTransientRetries", "5", "-RetryBackoffSeconds", "0", "-AbortedResidueMinutes", "0",
    ]
    process = subprocess.Popen(command, cwd=sandbox, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log_path = runtime / "testpeer_mailbox_cron.log"
    deadline = time.monotonic() + 15
    log = ""
    while time.monotonic() < deadline:
        if log_path.exists():
            log = log_path.read_text(encoding="utf-8")
            if "RETRY_DEFER reason=ledger_unreadable_before_exec" in log:
                break
        time.sleep(0.1)
    else:
        process.kill()
        stdout, stderr = process.communicate()
        raise AssertionError(f"unreadable-head deferral missing:\n{log}\n{stdout}\n{stderr}")
    (runtime / "testpeer_mailbox_cron.stop").write_text("stop\n", encoding="ascii")
    process.communicate(timeout=10)
    assert process.returncode == 0, log
    assert not (sandbox / ".protocol-tmp/fake-count.txt").exists(), "agent ran with an unreadable ledger head"
    seen_path = runtime / "testpeer_mailbox_cron.seen.json"
    seen = json.loads(seen_path.read_text(encoding="utf-8")) if seen_path.exists() else {}
    assert "MSG-retry.md" not in seen, "old own evidence consumed the message"
    assert "outcome=confirmed" not in log, log
    shutil.rmtree(sandbox / ".protocol-tmp")
    shutil.copy2(LEDGER_HEAD, helper)


def main() -> int:
    sandbox = Path(tempfile.mkdtemp(prefix="mailbox-retry-"))
    try:
        (sandbox / "Area_comun/mailbox/open").mkdir(parents=True)
        (sandbox / "runtime/state").mkdir(parents=True)
        (sandbox / "runtime/protocol_replay.py").write_text(
            "import json\nfrom pathlib import Path\n"
            "def protocol_state_drift(root: Path):\n"
            "    lines = [line for line in (root / 'runtime/state/events.jsonl').read_text().splitlines() if line.strip()]\n"
            "    event_seq = json.loads(lines[-1])['seq'] if lines else 0\n"
            "    derived_seq = json.loads((root / 'Area_comun/state/CLAIMS.json').read_text())['seq']\n"
            "    return {'has_drift': event_seq != derived_seq}\n",
            encoding="ascii",
        )
        (sandbox / "scripts/harness/prompts").mkdir(parents=True)
        shutil.copy2(RUNNER, sandbox / "scripts/harness/peer_mailbox_cron.ps1")
        shutil.copy2(LEDGER_HEAD, sandbox / "scripts/ledger_head.py")
        (sandbox / "protocol.config.json").write_text("{}\n", encoding="utf-8")
        (sandbox / "runtime/state/events.jsonl").write_text("", encoding="ascii")
        (sandbox / "Area_comun/state").mkdir(parents=True)
        (sandbox / "Area_comun/state/CLAIMS.json").write_text('{"seq":0}\n', encoding="ascii")
        (sandbox / ".gitignore").write_text(".protocol-tmp/\n", encoding="ascii")
        (sandbox / "predirty.txt").write_text("baseline\n", encoding="ascii")
        (sandbox / "Area_comun/tasks").mkdir(parents=True)
        (sandbox / "Area_comun/decisions").mkdir(parents=True)
        (sandbox / "Area_comun/tasks/TASK-fixture.md").write_text("baseline-task\n", encoding="ascii")
        message = sandbox / "Area_comun/mailbox/open/MSG-retry.md"
        message.write_text(
            "---\nfrom: Arquitecto\nto: TestPeer\ntype: ACTION\nstatus: open\n"
            "requires_response: true\nresponse_owner: TestPeer\nrequested_action: test\n---\n",
            encoding="ascii",
        )
        governed_message = sandbox / "Area_comun/mailbox/open/MSG-gov.md"
        governed_message.write_text("governed-message\n", encoding="ascii")
        predirty_message = sandbox / "Area_comun/mailbox/archived/MSG-predirty.md"
        predirty_message.parent.mkdir(parents=True)
        predirty_message.write_text("baseline-msg\n", encoding="ascii")
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
            "if($count -eq 3){\n"
            "  Set-Content -Path (Join-Path $root 'Area_comun/tasks/TASK-residue.md') -Value residue -Encoding ASCII\n"
            "  git add Area_comun/tasks/TASK-residue.md\n"
            "  $source=Join-Path $root 'Area_comun/mailbox/open/MSG-gov.md'\n"
            "  $target=Join-Path $root 'Area_comun/mailbox/archived/MSG-gov.md'\n"
            "  Move-Item -LiteralPath $source -Destination $target\n"
            "  git add -- Area_comun/mailbox/open/MSG-gov.md Area_comun/mailbox/archived/MSG-gov.md\n"
            "  Set-Content -Path (Join-Path $root 'Area_comun/state/TASK_INDEX_ARCHIVE.json') -Value '{\"tasks\":[{\"id\":\"TASK-pruned\"}]}' -Encoding ASCII\n"
            "  Set-Content -Path (Join-Path $root 'Area_comun/decisions/DECISION-test.md') -Value 'signed decision' -Encoding ASCII\n"
            "  git add Area_comun/state/TASK_INDEX_ARCHIVE.json Area_comun/decisions/DECISION-test.md\n"
            "  $events=@(\n"
            "    '{\"seq\":1,\"actor\":\"TestPeer\",\"actor_auth\":{\"method\":\"ed25519\",\"keyid\":\"testpeer:v1\",\"sig\":\"fixture-signature\"},\"payload\":{\"intent_type\":\"mailbox_archive\",\"message_id\":\"MSG-gov\",\"transitions\":{\"mailbox_archive\":{\"message_id\":\"MSG-gov\",\"from\":\"open\",\"to\":\"archived\"}}}}',\n"
            "    '{\"seq\":2,\"actor\":\"TestPeer\",\"actor_auth\":{\"method\":\"ed25519\",\"keyid\":\"testpeer:v1\",\"sig\":\"fixture-signature\"},\"payload\":{\"intent_type\":\"protocol_prune\",\"transitions\":{\"protocol_prune\":{\"task_ids\":[\"TASK-pruned\"]}}}}',\n"
            "    '{\"seq\":3,\"actor\":\"TestPeer\",\"actor_auth\":{\"method\":\"ed25519\",\"keyid\":\"testpeer:v1\",\"sig\":\"fixture-signature\"},\"payload\":{\"intent_type\":\"decision\",\"decision_id\":\"DECISION-test\"}}'\n"
            "  )\n"
            "  Add-Content -Path (Join-Path $root 'runtime/state/events.jsonl') -Value $events -Encoding ASCII\n"
            "  Set-Content -Path (Join-Path $root 'Area_comun/state/CLAIMS.json') -Value '{\"seq\":3}' -Encoding ASCII\n"
            "  Write-Output 'status: blocked claim ajeno active claim pre-gate rojo'\n"
            "  Write-Output 'OUTCOME: transient'\n"
            "  exit 0\n"
            "}\n"
            "if($count -eq 4){\n"
            "  Set-Content -Path (Join-Path $root 'ambiguous-residue.txt') -Value residue -Encoding ASCII\n"
            "  git add ambiguous-residue.txt\n"
            "  $eventPath=Join-Path $root 'runtime/state/events.jsonl'\n"
            "  $lines=@(Get-Content -LiteralPath $eventPath)\n"
            "  Set-Content -LiteralPath $eventPath -Value @($lines[0],'{not-json',$lines[1],$lines[2]) -Encoding ASCII\n"
            "  Copy-Item -LiteralPath $eventPath -Destination (Join-Path $root '.protocol-tmp/ambiguous-events-proof.txt')\n"
            "  $repair=Join-Path $root '.protocol-tmp/repair-events.ps1'\n"
            "  Set-Content -LiteralPath $repair -Value \"Start-Sleep -Milliseconds 500`nSet-Content -LiteralPath '$eventPath' -Value @('$($lines[0])','$($lines[1])','$($lines[2])') -Encoding ASCII\" -Encoding ASCII\n"
            "  Start-Process powershell.exe -WindowStyle Hidden -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',$repair) | Out-Null\n"
            "  Write-Output 'OUTCOME: transient'\n"
            "  exit 0\n"
            "}\n"
            "$response=Join-Path $root 'Area_comun/mailbox/open/MSG-response.md'\n"
            "Set-Content -Path $response -Value 'response confirmed' -Encoding ASCII\n"
            "git add $response; git commit -m 'test confirmed response' | Out-Null\n"
            "Write-Output 'status: in_review'\n"
            "Write-Output 'OUTCOME: confirmed'\n",
            encoding="ascii",
        )
        fake = sandbox / "fake-agent.cmd"
        fake.write_text("@powershell.exe -NoProfile -ExecutionPolicy Bypass -File \"%~dp0fake-agent-core.ps1\"\n", encoding="ascii")
        run("git", "init", cwd=sandbox)
        run("git", "config", "user.email", "retry@example.invalid", cwd=sandbox)
        run("git", "config", "user.name", "TestPeer", cwd=sandbox)
        run("git", "add", ".", cwd=sandbox)
        run("git", "commit", "-m", "fixture", cwd=sandbox)
        run_outcome_parser_cases(sandbox)
        run_torn_tail_case(sandbox)
        run_unreadable_head_case(sandbox, prompt, fake)
        (sandbox / "runtime/state/events.jsonl").write_text("", encoding="ascii")
        (sandbox / "predirty.txt").write_text("peer-content\n", encoding="ascii")
        governed_predirty = {
            "Area_comun/tasks/TASK-fixture.md": "peer-task-edit\n",
            "Area_comun/mailbox/archived/MSG-predirty.md": "peer-msg-edit\n",
            "Area_comun/state/CLAIMS.json": '{"seq":0,"peer":"edit"}\n',
            "runtime/state/events.jsonl": "",
        }
        for relative, content in governed_predirty.items():
            (sandbox / relative).write_text(content, encoding="ascii")
        try:
            result = run(
                "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER),
                "-PeerId", "TestPeer", "-Root", str(sandbox), "-PromptFile", str(prompt),
                "-AgentExe", str(fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
                "-MaxNoCoordinatorRounds", "6", "-ExecTimeoutSeconds", "20",
                "-MaxTransientRetries", "5", "-RetryBackoffSeconds", "0", "-AbortedResidueMinutes", "0",
                cwd=sandbox,
            )
        except subprocess.TimeoutExpired as exc:
            log_path = sandbox / ".protocol-tmp/testpeer_mailbox_cron/testpeer_mailbox_cron.log"
            details = log_path.read_text(encoding="utf-8") if log_path.exists() else "log missing"
            raise AssertionError(f"runner timed out:\n{details}") from exc
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
        assert not (sandbox / "residue.txt").exists(), f"aborted exec residue survived rollback; log={log}"
        assert (sandbox / "Area_comun/tasks/TASK-residue.md").exists(), "ambiguous residue beside signed events was destroyed"
        events = (sandbox / "runtime/state/events.jsonl").read_text(encoding="ascii").splitlines()
        ambiguous_proof = (sandbox / ".protocol-tmp/ambiguous-events-proof.txt").read_text(encoding="ascii").splitlines()
        assert ambiguous_proof[1] == "{not-json", f"ambiguous ledger fixture was not produced: {ambiguous_proof!r}"
        assert json.loads(events[-1])["seq"] == 3, f"signed ledger events did not survive: {events!r}; log={log}"
        assert json.loads((sandbox / "Area_comun/state/CLAIMS.json").read_text(encoding="ascii"))["seq"] == 3
        assert not governed_message.exists(), "signed mailbox archive deletion was rolled back"
        assert (sandbox / "Area_comun/mailbox/archived/MSG-gov.md").exists(), "signed mailbox archive addition was rolled back"
        assert (sandbox / "Area_comun/state/TASK_INDEX_ARCHIVE.json").exists(), "signed prune archive was destroyed"
        assert (sandbox / "Area_comun/decisions/DECISION-test.md").exists(), "signed decision document was destroyed"
        assert (sandbox / "ambiguous-residue.txt").exists(), "mid-log ambiguity was rolled back"
        assert (sandbox / "predirty.txt").read_text(encoding="ascii") == "peer-content\n"
        assert (sandbox / "Area_comun/tasks/TASK-fixture.md").read_text(encoding="ascii") == "peer-task-edit\n"
        predirty_status = run("git", "status", "--porcelain", "--", "predirty.txt", cwd=sandbox).stdout
        assert predirty_status.startswith(" M "), f"pre-dirty index/worktree state was not restored: {predirty_status!r}"
        assert "outcome=unconfirmed" in log and "RETRY_SCHEDULED attempt=1" in log
        assert "outcome=transient" in log and "RETRY_SCHEDULED attempt=2" in log
        assert "RETRY_SCHEDULED attempt=3" in log
        assert "ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=3 proof=disk" in log
        assert ("ROLLBACK_DEFER reason=ledger_unreadable_after_exec" in log or
                "ROLLBACK_DEFER reason=rollback_probe_failed" in log)
        assert "LOOP_ERROR" not in log
        assert "ROLLBACK_LEDGER_DRIFT" not in log
        assert "outcome=confirmed" in log
        assert int((sandbox / ".protocol-tmp/fake-count.txt").read_text()) == 5
        print("mailbox retry cases: PASS (proof-only rollback -> conservative signed/ambiguous preservation)")
        return 0
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
