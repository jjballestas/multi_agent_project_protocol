#!/usr/bin/env python3
from __future__ import annotations

import json
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sweep_cron_zombies as sweep


ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTER = "Co" + "dex"
REVIEWER = "Ana" + "lista"
CHECKER = "Arqui" + "tecto"
HARNESS_PATH = ROOT / "scripts/harness/peer_mailbox_cron.ps1"


FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-HARNESS-PREEXEC-DEFER-STARVATION",
        "negative": "Mixed healthy pre-exec causes cannot exhaust the exec retry budget, while one stable over-time cause remains terminal.",
        "mutation": "source.replace(stable_counter, shared_counter).replace(wall_clock_terminal, count_terminal)",
        "boundaries": (
            'assert healthy["mixed"]["exhausted"] is False',
            'assert healthy["stable"]["exhausted"] is True',
            'assert mutant["mixed"]["exhausted"] is True',
        ),
        "exercised_by": "test_preexec_defer_budget_kills_shared_counter_mutant",
    },
)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def base_lease(**overrides: object) -> dict:
    data = {
        "owner": IMPLEMENTER,
        "task_or_msg_id": "MSG-test",
        "pid": 999999,
        "process_start_time_utc": "2000-01-01T00:00:00Z",
        "cmdline_hash": sweep.hash_cmdline("agent exec"),
        "cmdline": "agent exec",
        "started_at": "2000-01-01T00:00:00Z",
        "deadline": (datetime.now(timezone.utc) - timedelta(seconds=10)).isoformat(),
        "heartbeat_monotonic": 1,
        "shutdown_policy": "stop_after_current_turn",
    }
    data.update(overrides)
    return data


def scratch_parent() -> Path | None:
    if os.name != "nt":
        return None
    base = Path("D:/Aegis_Scratch/multi_agent_project_protocol/task0319-tests")
    base.mkdir(parents=True, exist_ok=True)
    return base


def make_tempdir(prefix: str) -> tempfile.TemporaryDirectory[str]:
    return tempfile.TemporaryDirectory(prefix=prefix, dir=scratch_parent())


def make_root() -> tempfile.TemporaryDirectory[str]:
    tmp = make_tempdir("exec-lease-")
    root = Path(tmp.name)
    (root / "Area_comun/state").mkdir(parents=True)
    write_json(root / "Area_comun/state/CLAIMS.json", {"claims": [], "schema_version": "1.0"})
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    return tmp


def test_dead_process_cleans_only() -> None:
    with make_root() as tmp:
        root = Path(tmp)
        lease_path = root / ".protocol-tmp/codex_mailbox_cron/codex_mailbox_cron.exec-lease.json"
        write_json(lease_path, base_lease())
        decision = sweep.decision_for_lease(root, lease_path, IMPLEMENTER, CHECKER)
        assert decision["action"] == "cleanup_only"
        assert decision["reason"] == "process_dead"


def test_kill_mode_cleanup_only_removes_lock_and_lease() -> None:
    with make_root() as tmp:
        root = Path(tmp)
        lease_path = root / ".protocol-tmp/codex_mailbox_cron/codex_mailbox_cron.exec-lease.json"
        lock_path = root / ".protocol-tmp/codex_mailbox_cron/codex_mailbox_cron.lock"
        write_json(lease_path, base_lease())
        lock_path.write_text("locked\n", encoding="ascii")
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/sweep_cron_zombies.py"),
                "--root",
                str(root),
                "--owner",
                IMPLEMENTER,
                "--kill",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr + proc.stdout
        output = json.loads(proc.stdout)
        assert output["decisions"][0]["action"] == "cleanup_only"
        assert not lock_path.exists()
        assert not lease_path.exists()


def test_owner_and_checker_exclusions() -> None:
    with make_root() as tmp:
        root = Path(tmp)
        lease_path = root / ".protocol-tmp/analista_mailbox_cron/analista_mailbox_cron.exec-lease.json"
        write_json(lease_path, base_lease(owner=REVIEWER))
        assert sweep.decision_for_lease(root, lease_path, IMPLEMENTER, CHECKER)["reason"] == "owner_not_target"
        assert sweep.decision_for_lease(root, lease_path, REVIEWER, REVIEWER)["reason"] == "checker_owner_excluded"


def test_dry_run_is_default() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/sweep_cron_zombies.py"), "--root", str(ROOT), "--owner", IMPLEMENTER],
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["mode"] == "dry-run"


HARNESS_RELS = (
    f"personal/{IMPLEMENTER}/codex_mailbox_cron.ps1",
    f"personal/{REVIEWER}/analista_mailbox_cron.ps1",
    f"personal/{CHECKER}/arquitecto_cron.ps1",
)


def harness_contract_text(rel: str) -> str:
    text = (ROOT / rel).read_text(encoding="utf-8")
    if "scripts\\harness\\peer_mailbox_cron.ps1" in text:
        text += "\n" + (ROOT / "scripts/harness/peer_mailbox_cron.ps1").read_text(encoding="utf-8")
    return text


def test_harnesses_contain_required_exec_lease_contract() -> None:
    for rel in HARNESS_RELS:
        text = harness_contract_text(rel)
        assert "exec-lease.json" in text
        assert "process_start_time_utc" in text
        assert "cmdline_hash" in text
        assert "heartbeat_monotonic" in text
        assert "Clear-StaleCronLockIfSafe" in text
        if "arquitecto_cron" not in rel:
            assert "Stop marker detected; waiting for current exec" in text
        assert "Stop-ExpiredLeaseProcess" in text or "Stop-LeaseProcessTree" in text
        assert "finally" in text


def test_self_heal_does_not_wait_for_deadline_before_dead_pid_cleanup() -> None:
    for rel in HARNESS_RELS:
        text = harness_contract_text(rel)
        start = text.index("function Clear-StaleCronLockIfSafe")
        next_function = "function Stop-ExpiredLeaseProcess" if "function Stop-ExpiredLeaseProcess" in text[start:] else "function Get-ExecProgressState"
        end = text.index(next_function, start)
        body = text[start:end]
        assert body.index("Test-LeaseProcessMatches") < body.index("[DateTime]::Parse")
        assert "pre_deadline" in body


def test_harnesses_use_per_exec_prompt_files() -> None:
    for rel in HARNESS_RELS:
        text = harness_contract_text(rel)
        assert '.prompt.txt"' not in text.split("function Invoke-", 1)[0].replace("arquitecto_cron.prompt.txt", "")
        assert "Join-Path $RunsDir" in text and ".prompt.txt" in text
        assert "-RedirectStandardInput $prompt" in text


def test_harnesses_use_tree_kill_and_single_instance_guard() -> None:
    for rel in HARNESS_RELS:
        text = harness_contract_text(rel)
        assert "taskkill.exe" in text
        assert '"/T"' in text
        assert '"/F"' in text
        assert "Test-ExistingCronInstance" in text
        assert "Write-CronPid" in text
        assert "INSTANCE_ALREADY_RUNNING" in text


def test_stop_order_requires_exact_line_not_contains() -> None:
    for rel in HARNESS_RELS:
        text = harness_contract_text(rel)
        assert '-cmatch "\\bSTOP_JOB\\b"' not in text
        assert "-match \"(?i)\\b(detener" not in text
        assert '-ceq "STOP_JOB"' in text


def powershell_executable() -> str:
    executable = shutil.which("pwsh") or shutil.which("powershell")
    if not executable:
        raise AssertionError("PowerShell is required for the generic harness contract")
    return executable


def ps_literal(value: Path | str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def run_powershell(script: str, cwd: Path) -> dict:
    script_path = cwd / "probe.ps1"
    script_path.write_text(script, encoding="utf-8", newline="\n")
    proc = subprocess.run(
        [powershell_executable(), "-NoProfile", "-NonInteractive", "-File", str(script_path)],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    return json.loads(proc.stdout)


def function_loader(source: Path, names: tuple[str, ...]) -> str:
    requested = ",".join(f'"{name}"' for name in names)
    return f"""
$sourcePath = {ps_literal(source)}
$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($sourcePath, [ref]$tokens, [ref]$errors)
if ($errors.Count -gt 0) {{ throw ($errors | Out-String) }}
$wanted = @({requested})
foreach ($name in $wanted) {{
    $node = $ast.FindAll({{ param($item) $item -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $item.Name -eq $name }}, $true) | Select-Object -First 1
    if (-not $node) {{ throw "missing function $name" }}
    Invoke-Expression $node.Extent.Text
}}
"""


def defer_probe(source: Path) -> dict:
    with make_tempdir("defer-probe-") as tmp:
        root = Path(tmp)
        message = root / "MSG-test.md"
        message.write_text("message\n", encoding="ascii")
        script = function_loader(source, ("Register-PreExecDefer", "Reset-PreExecDefer")) + f"""
$script:state = @{{}}
$script:logs = @()
function Get-MessageSignature {{ param($Message) return "sig" }}
function Read-RetryState {{ return $script:state }}
function Write-RetryState {{ param($State) $script:state = $State }}
function Write-Log {{ param([string]$Line) $script:logs += $Line }}
$RetryBackoffSeconds = 0
$MaxTransientRetries = 3
$PreExecDeferTimeoutSeconds = 300
$message = Get-Item -LiteralPath {ps_literal(message)}
$script:state[$message.Name] = [pscustomobject]@{{ signature = "sig"; attempts = 2; defers = 2; defer_reason = "active_peer_lease"; defer_started_at = [DateTime]::UtcNow.AddSeconds(-30).ToString("o"); exhausted = $false }}
Register-PreExecDefer -Message $message -Reason "worktree_residue_live" -Detail "paths=owned.txt"
$mixed = $script:state[$message.Name]
$script:state[$message.Name] = [pscustomobject]@{{ signature = "sig"; attempts = 2; defers = 8; defer_reason = "active_peer_lease"; defer_started_at = [DateTime]::UtcNow.AddSeconds(-301).ToString("o"); exhausted = $false }}
Register-PreExecDefer -Message $message -Reason "active_peer_lease" -Detail "peer={REVIEWER}"
$stable = $script:state[$message.Name]
Reset-PreExecDefer -Message $message
$cleared = $script:state[$message.Name]
[ordered]@{{ mixed = $mixed; stable = $stable; cleared = $cleared; logs = $script:logs }} | ConvertTo-Json -Depth 8 -Compress
"""
        return run_powershell(script, root)


def test_preexec_defer_budget_kills_shared_counter_mutant() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-PREEXEC-DEFER-STARVATION"""
    healthy = defer_probe(HARNESS_PATH)
    assert healthy["mixed"]["exhausted"] is False
    assert healthy["mixed"]["defers"] == 1
    assert healthy["mixed"]["attempts"] == 2
    assert healthy["stable"]["exhausted"] is True
    assert healthy["stable"]["outcome"] == "defer_terminal"
    assert healthy["cleared"]["defers"] == 0
    assert healthy["cleared"]["attempts"] == 2

    source = HARNESS_PATH.read_text(encoding="utf-8")
    stable_counter = '$defers = if ($sameReason -and $null -ne $retry[$Message.Name].defers) { [int]$retry[$Message.Name].defers + 1 } else { 1 }'
    shared_counter = '$defers = if ($same -and $null -ne $retry[$Message.Name].defers) { [int]$retry[$Message.Name].defers + 1 } else { 1 }'
    wall_clock_terminal = '$terminal = ($sameReason -and $elapsedSeconds -ge $PreExecDeferTimeoutSeconds)'
    count_terminal = '$terminal = ($defers -ge $MaxTransientRetries)'
    mutant_source = source.replace(stable_counter, shared_counter).replace(wall_clock_terminal, count_terminal)
    assert mutant_source != source
    with make_tempdir("defer-mutant-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = defer_probe(mutant_path)
    assert mutant["mixed"]["exhausted"] is True


def test_residue_excludes_foreign_personal_and_caps_diagnostics() -> None:
    with make_tempdir("residue-probe-") as tmp:
        root = Path(tmp)
        own_paths = [f"personal/{IMPLEMENTER}/owned-{index}.txt" for index in range(12)]
        foreign_path = f"personal/{REVIEWER}/foreign.txt"
        for relative in [foreign_path, *own_paths]:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("dirty\n", encoding="ascii")
        entries = [f"?? {foreign_path}", *(f"?? {path}" for path in own_paths)]
        raw = "`0".join(entries) + "`0"
        script = function_loader(HARNESS_PATH, ("Get-StagedResidueState",)) + f"""
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$ResiduePath = Join-Path $Root "residue.json"
$AbortedResidueMinutes = 5
$ResidueDiagnosticPathLimit = 10
$script:LastResiduePaths = @()
$script:statusRaw = "{raw}"
function Get-GitStatusPorcelainUtf8 {{ return [pscustomobject]@{{ ok = $true; raw = $script:statusRaw }} }}
function Write-Utf8NoBom {{ param($Path, $Content) [IO.File]::WriteAllText($Path, $Content, [Text.UTF8Encoding]::new($false)) }}
$live = Get-StagedResidueState
$livePaths = @($script:LastResiduePaths)
$script:statusRaw = "?? {foreign_path}`0"
$foreignOnly = Get-StagedResidueState
[ordered]@{{ live = $live; live_paths = $livePaths; foreign_only = $foreignOnly; foreign_paths = @($script:LastResiduePaths) }} | ConvertTo-Json -Depth 6 -Compress
"""
        result = run_powershell(script, root)
    assert result["live"] == "live"
    assert len(result["live_paths"]) == 10
    assert all(path.startswith(f"personal/{IMPLEMENTER}/") for path in result["live_paths"])
    assert result["foreign_only"] == "none"
    assert result["foreign_paths"] == []


def test_active_peer_lease_reports_owner_and_claim_veto_survives() -> None:
    with make_tempdir("lease-detail-") as tmp:
        root = Path(tmp)
        claims_path = root / "Area_comun/state/CLAIMS.json"
        lease_path = root / ".protocol-tmp/reviewer/reviewer.exec-lease.json"
        write_json(claims_path, {"claims": []})
        write_json(lease_path, {"owner": REVIEWER, "pid": 1})
        own_lease = root / ".protocol-tmp/implementer/implementer.exec-lease.json"
        script = function_loader(HARNESS_PATH, ("Get-AdditionalWorkSignal",)) + f"""
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$LeasePath = {ps_literal(own_lease)}
$script:LastAdditionalSignalDetail = ""
function Read-JsonWithDeadline {{ param($Path) return [pscustomobject]@{{ ok = $true; value = (Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json) }} }}
function Test-LeaseProcessMatches {{ param($Lease) return $true }}
$leaseSignal = Get-AdditionalWorkSignal
$leaseDetail = $script:LastAdditionalSignalDetail
[IO.File]::WriteAllText({ps_literal(claims_path)}, '{{"claims":[{{"owner":"{CHECKER}","status":"active","expires_at":"2099-01-01T00:00:00Z"}}]}}')
$claimSignal = Get-AdditionalWorkSignal
[ordered]@{{ lease_signal = $leaseSignal; lease_detail = $leaseDetail; claim_signal = $claimSignal }} | ConvertTo-Json -Compress
"""
        result = run_powershell(script, root)
    assert result["lease_signal"] == "active_peer_lease"
    assert result["lease_detail"] == f"peer={REVIEWER}"
    assert result["claim_signal"] == "active_external_claim"


def test_new_instance_exports_identical_harness() -> None:
    spec = importlib.util.spec_from_file_location("new_instance_task0319", ROOT / "scripts/new_instance.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with make_tempdir("export-probe-") as tmp:
        target = Path(tmp) / "instance"
        target.mkdir()
        module.copy_peer_harness(ROOT, target)
        exported = target / "scripts/harness/peer_mailbox_cron.ps1"
        assert exported.read_bytes() == HARNESS_PATH.read_bytes()


def main() -> int:
    tests = [
        test_dead_process_cleans_only,
        test_kill_mode_cleanup_only_removes_lock_and_lease,
        test_owner_and_checker_exclusions,
        test_dry_run_is_default,
        test_harnesses_contain_required_exec_lease_contract,
        test_self_heal_does_not_wait_for_deadline_before_dead_pid_cleanup,
        test_harnesses_use_per_exec_prompt_files,
        test_harnesses_use_tree_kill_and_single_instance_guard,
        test_stop_order_requires_exact_line_not_contains,
        test_preexec_defer_budget_kills_shared_counter_mutant,
        test_residue_excludes_foreign_personal_and_caps_diagnostics,
        test_active_peer_lease_reports_owner_and_claim_veto_survives,
        test_new_instance_exports_identical_harness,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
