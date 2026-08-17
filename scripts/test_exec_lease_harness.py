#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
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
        "id": "NEG-HARNESS-RETRY-EXHAUSTED-DURABLE-ALERT",
        "negative": "A terminal retry must create a durable cold-start alert, and the stalled-task control must honor its persistence threshold.",
        "mutation": "source.replace(retry_alert_call, dead_retry_alert_call, 1)",
        "boundaries": (
            'assert healthy["retry_alert_count"] == 1',
            'assert healthy["fresh_stalled_count"] == 0',
            'assert healthy["old_stalled_count"] == 1',
            'assert mutant["retry_alert_count"] == 0',
        ),
        "exercised_by": "test_retry_exhaustion_alert_and_stalled_task_threshold_kill_mutant",
    },
    {
        "id": "NEG-HARNESS-PREEXEC-DEFER-STARVATION",
        "negative": "Mixed healthy pre-exec causes cannot exhaust the exec retry budget, while one stable over-time cause remains terminal.",
        "mutation": "source.replace(stable_counter, shared_counter).replace(wall_clock_terminal, count_terminal)",
        "boundaries": (
            'assert healthy["mixed"]["exhausted"] is False',
            'assert healthy["stable"]["exhausted"] is True',
            'assert mutant["mixed"]["exhausted"] is True',
            'assert rename["state"] == "none"',
            'assert rename["paths"] == []',
        ),
        "exercised_by": "test_preexec_defer_budget_kills_shared_counter_mutant",
    },
    {
        "id": "NEG-HARNESS-WORKTREE-DISK-PROOF-RENAME-PAIRING",
        "negative": "Worktree disk proof must preserve both real paths in a porcelain v1 -z rename pair and fail closed on a missing source record.",
        "mutation": "source.replace(paired_source, stripped_source, 1)",
        "boundaries": (
            'assert healthy["paths"] == [new_path, old_path]',
            'assert healthy["exists"] == [True, False]',
            'assert mutant["paths"] != healthy["paths"]',
            'assert malformed is None',
        ),
        "exercised_by": "test_worktree_disk_proof_pairs_real_git_rename_records",
    },
    {
        "id": "NEG-CRON-ZOMBIE-SWEEPER-PORCELAIN-Z-PATHS",
        "negative": "The zombie sweeper must preserve exact quoted and renamed paths from real Git porcelain output.",
        "mutation": "source.replace(nul_command, line_command, 1)",
        "boundaries": (
            "assert expected <= healthy",
            "assert expected <= set(runtime_parser(real_z_raw))",
            "assert expected <= set(mirror_parser(real_z_raw))",
            "assert not expected <= legacy",
            "assert mutant_failed_closed is True",
            "assert b\" -> \" in legacy_raw",
            "assert b'\"' in legacy_raw",
        ),
        "exercised_by": "test_zombie_sweeper_parses_real_git_quoted_rename_paths",
    },
    {
        "id": "NEG-CRON-STATUS-UNTRACKED-FILE-CONVERGENCE",
        "negative": "Both Git status readers must enumerate individual files inside untracked directories so file-scoped claims remain visible without broadening unrelated-owner vetoes.",
        "mutation": 'source.replace(untracked_option, "", 1)',
        "boundaries": (
            "assert collapsed_paths == {untracked_dir}",
            "assert healthy_paths == {untracked_path}",
            "assert powershell_paths == [f\"?? {untracked_path}\"]",
            'assert sweep.dirty_claimed_route(root, IMPLEMENTER) is True',
            'assert mutant.dirty_claimed_route(root, IMPLEMENTER) is False',
            'assert sweep.dirty_claimed_route(root, REVIEWER) is False',
        ),
        "exercised_by": "test_git_status_readers_enumerate_untracked_files_without_overbroad_veto",
    },
    {
        "id": "NEG-CRON-STATUS-EMBEDDED-REPOSITORY-DIRTY-CLAIM",
        "negative": "The destructive claim-veto readers must query embedded repositories at arbitrary physical depth so a file-scoped dirty claim vetoes termination; disabling discovery must reproduce the destructive false negative.",
        "mutation": "source.replace(discovery",
        "boundaries": (
            "assert live_path not in parent_variants[0]",
            "assert live_path not in parent_variants[1]",
            "assert live_path not in parent_variants[2]",
            "assert live_path in sweep.dirty_paths(root)",
            "assert sweep.dirty_claimed_route(root, IMPLEMENTER) is True",
            "assert live_path in powershell_paths",
            "assert mutant.dirty_claimed_route(root, IMPLEMENTER) is False",
            "assert live_path not in powershell_mutant_paths",
            "assert python_discovery_failed_closed is True",
            "assert powershell_discovery_failure[\"ok\"] is False",
        ),
        "exercised_by": "test_embedded_repository_dirty_claim_is_fail_closed_and_mutation_proven",
    },
    {
        "id": "NEG-HARNESS-PARENT-IGNORE-BOUNDARY",
        "negative": "Embedded-repository expansion remains enabled for destructive claim vetoes but must not make residue or disk-proof readers block on a path ignored by the parent repository.",
        "mutation": "source.replace(blocking_status_call, expanded_status_call)",
        "boundaries": (
            'assert healthy["parent_paths"] == []',
            'assert ignored_path in healthy["expanded_paths"]',
            'assert healthy["residue"] == "none"',
            'assert ignored_path not in healthy["proof"]',
            'assert sweep.dirty_claimed_route(root, IMPLEMENTER) is True',
            'assert mutant["residue"] == "live"',
            'assert ignored_path in mutant["proof"]',
        ),
        "exercised_by": "test_parent_ignore_boundary_separates_claim_veto_from_blocking_readers",
    },
    {
        "id": "NEG-HARNESS-POST-DELIVERY-PROGRESS-DEADLINE",
        "negative": "The post-delivery window must inherit a later main progress deadline without exceeding its own hard deadline.",
        "mutation": "dead_wiring_source = source.replace(live_guard, dead_guard, 1)",
        "boundaries": (
            'assert healthy["after_second_progress"] == "2026-08-07T02:44:41.0000000Z"',
            'assert healthy["alive_at_original_timeout"] is True',
            'assert healthy["no_progress_times_out"] is True',
            'assert healthy["clamped_deadline"] == "2026-08-07T02:59:00.0000000Z"',
            'assert healthy["hard_cap_times_out"] is True',
            'assert mutant["alive_at_original_timeout"] is False',
            'assert live["post_delivery_timeout_fired"] is False',
            'assert live["inherited_deadline_observed"] is True',
            'assert dead_wiring["post_delivery_timeout_fired"] is True',
        ),
        "exercised_by": "test_post_delivery_window_honors_main_progress_extensions",
    },
    {
        "id": "NEG-HARNESS-WORK-DERIVED-EXEC-LIVENESS",
        "negative": "The real supervision loop must keep a silent CPU-working exec alive at its first deadline and kill it when the production CPU-sampling block is unreachable.",
        "mutation": "sign_changed_source = source.replace(live_sampling_seed, sign_changed_seed, 1)",
        "boundaries": (
            'assert healthy_outcome["exec_progressing"] is True',
            'assert healthy_outcome["exec_hung"] is False',
            'assert mutant_outcome["exec_progressing"] is False',
            'assert mutant_outcome["exec_hung"] is True',
            'assert max_deadline_outcome["exec_progressing"] is False',
            'assert max_deadline_outcome["exec_hung"] is True',
            'assert sign_changed_outcome["exec_progressing"] is False',
            'assert sign_changed_outcome["exec_hung"] is True',
        ),
        "exercised_by": "test_silent_process_tree_cpu_is_work_derived_and_mutation_proven",
    },
    {
        "id": "NEG-HARNESS-PROCESS-IDENTITY-CPU-SAMPLE",
        "negative": "A live process reusing a numeric PID must contribute CPU independently from an inflated sample belonging to the old process identity.",
        "mutation": "source.replace(identity_key, pid_only_key, 1)",
        "boundaries": (
            'assert healthy["progressing"] is True',
            'assert healthy["after"] > healthy["before"]',
            'assert mutant["progressing"] is False',
            'assert mutant["live_process_ticks"] > 0',
        ),
        "exercised_by": "test_process_tree_cpu_sample_distinguishes_recycled_pid",
    },
    {
        "id": "NEG-HARNESS-SCOPE-AWARE-EXTERNAL-CLAIM",
        "negative": "An external claim must veto intersecting material routes without vetoing disjoint work, and malformed claim scope remains fail-closed.",
        "mutation": "source.replace(claim_intersection",
        "boundaries": (
            'assert healthy["disjoint"] == "none"',
            'assert healthy["intersecting"] == "active_external_claim"',
            'assert healthy["malformed"] == [',
            'assert allow_mutant["intersecting"] == "none"',
            'assert veto_mutant["disjoint"] == "active_external_claim"',
        ),
        "exercised_by": "test_scope_aware_claim_veto_kills_both_direction_mutants",
    },
    {
        "id": "NEG-HARNESS-SCOPE-AWARE-PEER-LEASE",
        "negative": "A live peer lease must veto intersecting declared work without vetoing disjoint work, while ambiguous lease scope remains fail-closed.",
        "mutation": "source.replace(lease_intersection",
        "boundaries": (
            'assert healthy["disjoint"] == "none"',
            'assert healthy["intersecting"] == "active_peer_lease"',
            'assert healthy["ambiguous"] == "active_peer_lease"',
            'assert allow_mutant["intersecting"] == "none"',
            'assert veto_mutant["disjoint"] == "active_peer_lease"',
        ),
        "exercised_by": "test_scope_aware_lease_veto_kills_both_direction_mutants",
    },
    {
        "id": "NEG-HARNESS-ATOMIC-EXEC-ADMISSION",
        "negative": "Simultaneous overlapping peer probes must serialize an atomic check-and-reserve critical section before either exec starts.",
        "mutation": "source.replace(shared_admission_path, peer_specific_admission_path, 1)",
        "boundaries": (
            'assert healthy["admitted"] == 1',
            'assert mutant["admitted"] == 2',
            'assert healthy["lease_count"] == 1',
            'assert mutant["lease_count"] == 2',
        ),
        "exercised_by": "test_atomic_exec_admission_kills_peer_specific_lock_mutant",
    },
    {
        "id": "NEG-HARNESS-RESERVED-LEASE-SELF-HEAL",
        "negative": "Startup self-heal must remove unreadable leases only with proven-dead owner evidence; an identityless no-lock reservation must be preserved behind an explicit recovery marker.",
        "mutation": "source.replace(lock_liveness_promotion, dead_evidence_ignored, 1)",
        "boundaries": (
            'assert set(healthy) == expected_states',
            'assert all(row["lock_exists"] and row["lease_exists"] for row in unknown_rounds)',
            'assert "liveness=unknown action=preserve" in healthy["reserved_without_lock"]["logs"][0]',
            'assert all(not row["lock_exists"] and not row["lease_exists"] for row in healthy_rounds)',
            'assert all(row["lease_exists"] for row in mutant["truncated_with_lock"]["rounds"])',
            'assert all(len(result["rounds"]) == 3 for result in healthy.values())',
        ),
        "exercised_by": "test_orphan_lease_self_heal_matrix_requires_dead_owner_evidence",
    },
    {
        "id": "NEG-HARNESS-LIVE-UNREADABLE-LEASE-PRESERVED",
        "negative": "Startup self-heal must preserve a live owner's unreadable lease and distinguish it from a proven orphan; reserved leases must use reservation_deadline.",
        "mutation": "source.replace(reservation_deadline_selector, running_deadline_selector, 1)",
        "boundaries": (
            'assert all(row["lock_exists"] and row["lease_exists"] for row in healthy.values())',
            'assert healthy["reserved_live"]["logs"] == []',
            'assert "liveness=live action=preserve" in healthy["truncated_live"]["logs"][0]',
            'assert "liveness=live action=preserve" in mutant["reserved_live"]["logs"][0]',
        ),
        "exercised_by": "test_live_unreadable_lease_is_preserved_and_deadline_mutant_dies",
    },
    {
        "id": "NEG-HARNESS-LEASE-OWNER-LOCK-STATE-TABLE",
        "negative": "The 24 lease-owner-lock cells must share one tri-state decision: remove only proven-dead owners, preserve and visibly lock unknown owners, and keep malformed peer leases fail-closed.",
        "mutation": "source.replace(unknown_default, dead_default, 1)",
        "boundaries": (
            "assert len(healthy) == 24",
            "assert process_states == expected_process_states",
            "assert nullish == {\"empty\": \"peer_lease_unreadable\", \"whitespace\": \"peer_lease_unreadable\"}",
            "assert row[\"lease_exists\"] is should_preserve",
            "assert row[\"before\"] == expected_before",
            "assert row[\"after\"] == expected_after",
            "assert row[\"lock_exists\"] is True",
            "assert collapsed_unknown[unknown_absent][\"lease_exists\"] is False",
            "assert ignored_lock[dead_with_lock][\"lease_exists\"] is True",
            "assert open_guard[identityless_unknown][\"before\"] == \"none\"",
            "assert no_marker[unknown_absent][\"lock_exists\"] is False",
            "assert start_time_mutant[\"start_time_error\"] == \"dead\"",
            "assert get_process_mutant[\"get_process_error\"] == \"dead\"",
            "assert pid_reuse_mutant[\"pid_reused\"] == \"live\"",
        ),
        "exercised_by": "test_lease_owner_lock_state_table_is_complete_and_mutation_proven",
    },
    {
        "id": "NEG-HARNESS-ADMISSION-LIVENESS-PRODUCTION-PATH",
        "negative": "Every producer or consumer on the exec-admission liveness path must be observed in its production position; collapsing any one to a constant must change a required behavior.",
        "mutation": "inject_function_return(source, function_name, constant_return)",
        "boundaries": (
            "assert healthy == expected",
            "assert mutant != expected",
            'assert mutant["dead_signal"] == "active_peer_lease"',
            'assert mutant["live_signal"] == "none"',
        ),
        "exercised_by": "test_admission_liveness_path_uses_production_functions_and_kills_constant_mutants",
    },
    {
        "id": "NEG-HARNESS-ARCHIVED-TASK-WORK-RESOLUTION",
        "negative": "Message work resolution must consult the cold task archive when the task is absent from the pruned hot index.",
        "mutation": "source.replace(archive_index, hot_index, 1)",
        "boundaries": (
            'assert healthy["task_id"] == "TASK-1001"',
            'assert "src/target" in healthy["work_scope"]',
            'assert mutant is None',
        ),
        "exercised_by": "test_archived_task_work_resolution_kills_hot_only_mutant",
    },
    {
        "id": "NEG-HARNESS-GLOB-SCOPE-FAILS-CLOSED",
        "negative": "Claim routes containing glob metacharacters are ambiguous material scope and must veto instead of being compared as literals.",
        "mutation": "source.replace(glob_guard, dead_glob_guard, 1)",
        "boundaries": (
            'assert healthy == ["active_external_claim", "active_external_claim"]',
            'assert mutant == ["none", "none"]',
        ),
        "exercised_by": "test_glob_claim_scope_fails_closed_and_kills_guard_mutant",
    },
    {
        "id": "NEG-HARNESS-DIRTY-VETO-PRECEDES-SCOPE-ADMISSION",
        "negative": "Live dirty-tree residue must behaviorally stop execution before scope admission, including when the guard text remains present but is made unreachable.",
        "mutation": "source.replace(live_residue_guard, dead_wiring + live_residue_guard, 1)",
        "boundaries": (
            'assert healthy["admission_calls"] == 0',
            'assert healthy["defer_reasons"] == ["worktree_residue_live"]',
            'assert mutant["admission_calls"] == 1',
        ),
        "exercised_by": "test_dirty_tree_veto_still_precedes_scope_admission",
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
        liveness_check = "Get-LeaseProcessState" if "Get-LeaseProcessState" in body else "Test-LeaseProcessMatches"
        assert body.index(liveness_check) < body.index("[DateTime]::Parse")
        assert "liveness" in body or "pre_deadline" in body


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


SCOPE_FUNCTIONS = (
    "Get-Field",
    "Read-JsonWithDeadline",
    "Get-TaskRowById",
    "ConvertTo-ComparableRoute",
    "ConvertTo-ComparableScope",
    "Test-ScopeIntersection",
    "Get-MessageWorkDescriptor",
    "Get-LeaseWorkScope",
    "Get-AdditionalWorkSignal",
)


def write_scope_fixture(root: Path) -> Path:
    task_rel = "Area_comun/tasks/TASK-1001-scope-probe.md"
    task_path = root / task_rel
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(
        """---
task_id: TASK-1001
file: Area_comun/tasks/TASK-1001-scope-probe.md
status: ready
intake:
  scope_routes:
    - src/target
---
""",
        encoding="ascii",
    )
    write_json(
        root / "Area_comun/state/TASK_INDEX.json",
        {"tasks": [{"id": "TASK-1001", "file": task_rel, "status": "ready"}]},
    )
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"tasks": []})
    message = root / "Area_comun/mailbox/open/MSG-scope-TASK-1001.md"
    message.parent.mkdir(parents=True, exist_ok=True)
    message.write_text("task_id: TASK-1001\n", encoding="ascii")
    return message


def orphan_lease_self_heal_matrix_probe(source: Path) -> dict:
    cases = {
        "reserved_without_lock": {
            "lock": False,
            "content": json.dumps(
                {
                    "owner": IMPLEMENTER,
                    "task_or_msg_id": "MSG-probe-TASK-1001.md",
                    "task_id": "TASK-1001",
                    "state": "reserved",
                    "reserved_at": "2026-08-07T22:00:00Z",
                    "reservation_deadline": "2099-01-01T00:00:00Z",
                }
            ),
        },
        "truncated_with_lock": {"lock": True, "content": "{"},
        "empty_with_lock": {"lock": True, "content": ""},
        "reserved_missing_deadline_with_lock": {
            "lock": True,
            "content": json.dumps(
                {
                    "owner": IMPLEMENTER,
                    "task_or_msg_id": "MSG-probe-TASK-1001.md",
                    "task_id": "TASK-1001",
                    "state": "reserved",
                    "reserved_at": "2026-08-07T22:00:00Z",
                }
            ),
        },
    }
    results = {}
    for name, case in cases.items():
        with make_tempdir(f"orphan-self-heal-{name}-") as tmp:
            root = Path(tmp)
            lock_path = root / "peer.lock"
            lease_path = root / "peer.exec-lease.json"
            if case["lock"]:
                lock_path.write_text(
                    json.dumps(
                        {
                            "owner": IMPLEMENTER,
                            "task_or_msg_id": "MSG-probe-TASK-1001.md",
                            "pid": 999999,
                            "process_start_time_utc": "2000-01-01T00:00:00Z",
                        }
                    ),
                    encoding="ascii",
                )
            lease_path.write_text(case["content"], encoding="ascii")
            script = function_loader(source, ("Get-LeaseProcessState", "Test-LeaseProcessMatches", "Clear-StaleCronLockIfSafe")) + f"""
$LockPath = {ps_literal(lock_path)}
$LeasePath = {ps_literal(lease_path)}
$PeerId = "{IMPLEMENTER}"
$script:logs = @()
$script:rounds = @()
function Stop-LeaseProcessTree {{ param($Lease, $Reason) return $false }}
function Write-Log {{ param([string]$Line) $script:logs += $Line }}
1..3 | ForEach-Object {{
    Clear-StaleCronLockIfSafe
    $script:rounds += [ordered]@{{ lock_exists=(Test-Path -LiteralPath $LockPath); lease_exists=(Test-Path -LiteralPath $LeasePath) }}
}}
[ordered]@{{ rounds=@($script:rounds); logs=@($script:logs) }} | ConvertTo-Json -Depth 6 -Compress
"""
            results[name] = run_powershell(script, root)
    return results


def live_lease_self_heal_probe(source: Path) -> dict:
    results = {}
    for mode in ("reserved_live", "truncated_live", "empty_live", "reserved_missing_deadline_live"):
        with make_tempdir(f"live-self-heal-{mode}-") as tmp:
            root = Path(tmp)
            lock_path = root / "peer.lock"
            lease_path = root / "peer.exec-lease.json"
            script = function_loader(source, ("Get-LeaseProcessState", "Test-LeaseProcessMatches", "Clear-StaleCronLockIfSafe")) + f'''
$LockPath = {ps_literal(lock_path)}
$LeasePath = {ps_literal(lease_path)}
$PeerId = "{IMPLEMENTER}"
$script:logs = @()
function Stop-LeaseProcessTree {{ param($Lease, $Reason) return $false }}
function Write-Log {{ param([string]$Line) $script:logs += $Line }}
$engine = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$child = Start-Process -FilePath $engine -ArgumentList @("-NoProfile", "-Command", "Start-Sleep -Seconds 30") -PassThru -WindowStyle Hidden
try {{
    $null = $child.Handle
    $started = $child.StartTime.ToUniversalTime().ToString("o")
    $evidence = [ordered]@{{ owner="{IMPLEMENTER}"; task_or_msg_id="MSG-live"; pid=$child.Id; process_start_time_utc=$started }}
    [System.IO.File]::WriteAllText($LockPath, (($evidence | ConvertTo-Json -Compress) + "`n"))
    $lease = [ordered]@{{ owner="{IMPLEMENTER}"; task_or_msg_id="MSG-live"; task_id="TASK-1001"; state="reserved"; pid=$child.Id; process_start_time_utc=$started; reservation_deadline="2099-01-01T00:00:00Z" }}
    if ("{mode}" -eq "truncated_live") {{
        [System.IO.File]::WriteAllText($LeasePath, "{{")
    }} elseif ("{mode}" -eq "empty_live") {{
        [System.IO.File]::WriteAllText($LeasePath, "")
    }} else {{
        if ("{mode}" -eq "reserved_missing_deadline_live") {{ $lease.Remove("reservation_deadline") }}
        [System.IO.File]::WriteAllText($LeasePath, (($lease | ConvertTo-Json -Compress) + "`n"))
    }}
    Clear-StaleCronLockIfSafe
    [ordered]@{{ lock_exists=(Test-Path -LiteralPath $LockPath); lease_exists=(Test-Path -LiteralPath $LeasePath); logs=@($script:logs) }} | ConvertTo-Json -Depth 5 -Compress
}} finally {{
    if (-not $child.HasExited) {{ Stop-Process -Id $child.Id -Force -ErrorAction SilentlyContinue }}
}}
'''
            results[mode] = run_powershell(script, root)
    return results


def lease_process_state_probe(source: Path) -> dict[str, str]:
    script = function_loader(source, ("Get-LeaseProcessState",)) + '''
$engine = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$child = Start-Process -FilePath $engine -ArgumentList @("-NoProfile", "-Command", "Start-Sleep -Seconds 30") -PassThru -WindowStyle Hidden
$deadChild = Start-Process -FilePath $engine -ArgumentList @("-NoProfile", "-Command", "Start-Sleep -Seconds 30") -PassThru -WindowStyle Hidden
$script:ProcessProbeMode = "real"
function Get-Process {
    param([int]$Id, $ErrorAction)
    if ($script:ProcessProbeMode -eq "get_process_error") { throw "forced Get-Process failure" }
    if ($script:ProcessProbeMode -eq "start_time_error") {
        $broken = [pscustomobject]@{}
        return ($broken | Add-Member -MemberType ScriptProperty -Name StartTime -Value { throw "forced StartTime failure" } -PassThru)
    }
    return Microsoft.PowerShell.Management\\Get-Process -Id $Id -ErrorAction SilentlyContinue
}
try {
    $null = $child.Handle
    $null = $deadChild.Handle
    $live = [pscustomobject]@{ pid=$child.Id; process_start_time_utc=$child.StartTime.ToUniversalTime().ToString("o") }
    $pidReused = [pscustomobject]@{ pid=$child.Id; process_start_time_utc=$child.StartTime.ToUniversalTime().AddSeconds(-7).ToString("o") }
    $dead = [pscustomobject]@{ pid=$deadChild.Id; process_start_time_utc=$deadChild.StartTime.ToUniversalTime().ToString("o") }
    Stop-Process -Id $deadChild.Id -Force -ErrorAction Stop
    $deadChild.WaitForExit()
    $unknown = [pscustomobject]@{ pid=$child.Id; process_start_time_utc="" }
    $result = [ordered]@{
        live=(Get-LeaseProcessState -Lease $live)
        dead=(Get-LeaseProcessState -Lease $dead)
        unknown=(Get-LeaseProcessState -Lease $unknown)
        pid_reused=(Get-LeaseProcessState -Lease $pidReused)
    }
    $script:ProcessProbeMode = "get_process_error"
    $result.get_process_error = Get-LeaseProcessState -Lease $live
    $script:ProcessProbeMode = "start_time_error"
    $result.start_time_error = Get-LeaseProcessState -Lease $live
    $result | ConvertTo-Json -Compress
} finally {
    if (-not $child.HasExited) { Stop-Process -Id $child.Id -Force -ErrorAction SilentlyContinue }
    if (-not $deadChild.HasExited) { Stop-Process -Id $deadChild.Id -Force -ErrorAction SilentlyContinue }
}
'''
    with make_tempdir("lease-process-state-") as tmp:
        return run_powershell(script, Path(tmp))


def admission_liveness_path_probe(source: Path) -> dict[str, object]:
    with make_tempdir("admission-liveness-") as tmp:
        root = Path(tmp)
        message = write_scope_fixture(root)
        write_json(root / "Area_comun/state/CLAIMS.json", {"claims": []})
        lease = root / ".protocol-tmp/reviewer/reviewer.exec-lease.json"
        own_lease = root / ".protocol-tmp/implementer/implementer.exec-lease.json"
        functions = SCOPE_FUNCTIONS + ("Get-LeaseProcessState", "Test-LeaseProcessMatches")
        script = function_loader(source, functions) + f'''
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$LeasePath = {ps_literal(own_lease)}
$Message = Get-Item -LiteralPath {ps_literal(message)}
$PeerLeasePath = {ps_literal(lease)}
$script:LastAdditionalSignalDetail = ""
$current = Get-Process -Id $PID -ErrorAction Stop
$started = $current.StartTime.ToUniversalTime()
function Set-ProbeLease {{
    param([int]$PidValue, [string]$StartedValue)
    $value = [ordered]@{{
        owner = "{REVIEWER}"
        state = "running"
        pid = $PidValue
        process_start_time_utc = $StartedValue
        work_scope = @("src/target")
    }}
    [IO.Directory]::CreateDirectory((Split-Path -Parent $PeerLeasePath)) | Out-Null
    [IO.File]::WriteAllText($PeerLeasePath, (($value | ConvertTo-Json -Depth 5) + "`n"))
    return [pscustomobject]$value
}}
$deadLease = Set-ProbeLease -PidValue 2147483647 -StartedValue "2000-01-01T00:00:00Z"
$deadState = Get-LeaseProcessState -Lease $deadLease
$deadMatches = Test-LeaseProcessMatches -Lease $deadLease
$deadSignal = Get-AdditionalWorkSignal -Message $Message
$liveLease = Set-ProbeLease -PidValue $PID -StartedValue $started.ToString("o")
$liveState = Get-LeaseProcessState -Lease $liveLease
$liveMatches = Test-LeaseProcessMatches -Lease $liveLease
$liveSignal = Get-AdditionalWorkSignal -Message $Message
$reusedLease = Set-ProbeLease -PidValue $PID -StartedValue $started.AddSeconds(-7).ToString("o")
$reusedState = Get-LeaseProcessState -Lease $reusedLease
$reusedMatches = Test-LeaseProcessMatches -Lease $reusedLease
$reusedSignal = Get-AdditionalWorkSignal -Message $Message
[ordered]@{{
    dead_state=$deadState
    dead_matches=$deadMatches
    dead_signal=$deadSignal
    live_state=$liveState
    live_matches=$liveMatches
    live_signal=$liveSignal
    reused_state=$reusedState
    reused_matches=$reusedMatches
    reused_signal=$reusedSignal
}} | ConvertTo-Json -Compress
'''
        return run_powershell(script, root)


def inject_function_return(source: str, function_name: str, constant_return: str) -> str:
    marker = f"function {function_name} {{\n    param("
    assert source.count(marker) == 1
    start = source.index(marker)
    param_end = source.index("\n", start + len(marker))
    return source[: param_end + 1] + f"    return {constant_return}\n" + source[param_end + 1 :]


def lease_owner_lock_state_table_probe(source: Path, selected: set[str] | None = None) -> dict:
    forms = ("readable", "unreadable", "empty", "identityless")
    owners = ("live", "dead", "unknown")
    lock_states = ("present", "absent")
    results = {}
    probe_source = source.read_text(encoding="utf-8").replace(
        "[int]$TimeoutMilliseconds = 2000",
        "[int]$TimeoutMilliseconds = 50",
        1,
    )
    with make_tempdir("lease-state-table-source-") as source_tmp:
        probe_path = Path(source_tmp) / "peer_mailbox_cron.ps1"
        probe_path.write_text(probe_source, encoding="utf-8", newline="\n")
        for form in forms:
            for owner in owners:
                for lock_state in lock_states:
                    cell = f"{form}|{owner}|{lock_state}"
                    if selected is not None and cell not in selected:
                        continue
                    with make_tempdir(f"lease-state-{form}-{owner}-{lock_state}-") as tmp:
                        root = Path(tmp)
                        message = write_scope_fixture(root)
                        write_json(root / "Area_comun/state/CLAIMS.json", {"claims": []})
                        peer_dir = root / ".protocol-tmp/reviewer"
                        peer_dir.mkdir(parents=True, exist_ok=True)
                        lease = peer_dir / "reviewer.exec-lease.json"
                        lock = peer_dir / "reviewer.lock"
                        own_lease = root / ".protocol-tmp/implementer/implementer.exec-lease.json"
                        if form == "readable":
                            lease_content = json.dumps(
                                {
                                    "owner": REVIEWER,
                                    "state": "running",
                                    "deadline": "2099-01-01T00:00:00Z",
                                    "work_scope": ["src/target"],
                                    "probe_liveness": owner,
                                }
                            )
                        elif form == "identityless":
                            lease_content = json.dumps(
                                {
                                    "owner": REVIEWER,
                                    "state": "running",
                                    "deadline": "2099-01-01T00:00:00Z",
                                    "work_scope": ["src/target"],
                                }
                            )
                        elif form == "unreadable":
                            lease_content = "{"
                        else:
                            lease_content = ""
                        lease.write_text(lease_content, encoding="ascii")
                        if lock_state == "present":
                            write_json(lock, {"owner": REVIEWER, "probe_liveness": owner})
                        script = function_loader(
                            probe_path,
                            SCOPE_FUNCTIONS + ("Clear-StaleCronLockIfSafe",),
                        ) + f'''
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$Message = Get-Item -LiteralPath {ps_literal(message)}
$PeerLeasePath = {ps_literal(lease)}
$PeerLockPath = {ps_literal(lock)}
$OwnLeasePath = {ps_literal(own_lease)}
$LeasePath = $OwnLeasePath
$LockPath = $PeerLockPath
$script:logs = @()
$script:LastAdditionalSignalDetail = ""
function Get-LeaseProcessState {{
    param($Lease)
    if ($null -ne $Lease -and $Lease.PSObject.Properties['probe_liveness']) {{ return [string]$Lease.probe_liveness }}
    return "unknown"
}}
function Test-LeaseProcessMatches {{ param($Lease) return ((Get-LeaseProcessState -Lease $Lease) -ceq "live") }}
function Stop-LeaseProcessTree {{ param($Lease, $Reason) return $false }}
function Write-Log {{ param([string]$Line) $script:logs += $Line }}
$before = Get-AdditionalWorkSignal -Message $Message
$LeasePath = $PeerLeasePath
Clear-StaleCronLockIfSafe
$leaseExists = Test-Path -LiteralPath $PeerLeasePath
$lockExists = Test-Path -LiteralPath $PeerLockPath
$LeasePath = $OwnLeasePath
$script:LastAdditionalSignalDetail = ""
$after = Get-AdditionalWorkSignal -Message $Message
[ordered]@{{ before=$before; after=$after; lease_exists=$leaseExists; lock_exists=$lockExists; logs=@($script:logs) }} | ConvertTo-Json -Depth 5 -Compress
'''
                        results[cell] = run_powershell(script, root)
    return results


def nullish_peer_lease_guard_probe(source: Path) -> dict[str, str]:
    results = {}
    probe_source = source.read_text(encoding="utf-8").replace(
        "[int]$TimeoutMilliseconds = 2000",
        "[int]$TimeoutMilliseconds = 50",
        1,
    )
    with make_tempdir("nullish-peer-source-") as source_tmp:
        probe_path = Path(source_tmp) / "peer_mailbox_cron.ps1"
        probe_path.write_text(probe_source, encoding="utf-8", newline="\n")
        for name, content in (("empty", ""), ("whitespace", " \r\n\t")):
            with make_tempdir(f"nullish-peer-{name}-") as tmp:
                root = Path(tmp)
                message = write_scope_fixture(root)
                write_json(root / "Area_comun/state/CLAIMS.json", {"claims": []})
                lease = root / ".protocol-tmp/reviewer/reviewer.exec-lease.json"
                lease.parent.mkdir(parents=True, exist_ok=True)
                lease.write_text(content, encoding="ascii")
                own_lease = root / ".protocol-tmp/implementer/implementer.exec-lease.json"
                script = function_loader(probe_path, SCOPE_FUNCTIONS) + f'''
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$Message = Get-Item -LiteralPath {ps_literal(message)}
$LeasePath = {ps_literal(own_lease)}
$script:LastAdditionalSignalDetail = ""
function Get-LeaseProcessState {{ param($Lease) return "unknown" }}
function Test-LeaseProcessMatches {{ param($Lease) return $false }}
(Get-AdditionalWorkSignal -Message $Message) | ConvertTo-Json -Compress
'''
                results[name] = run_powershell(script, root)
    return results


def archived_task_descriptor_probe(source: Path) -> dict | None:
    with make_tempdir("archived-task-scope-") as tmp:
        root = Path(tmp)
        message = write_scope_fixture(root)
        hot = root / "Area_comun/state/TASK_INDEX.json"
        archive = root / "Area_comun/state/TASK_INDEX_ARCHIVE.json"
        archived_row = json.loads(hot.read_text(encoding="utf-8"))["tasks"][0]
        write_json(hot, {"tasks": []})
        write_json(archive, {"tasks": [archived_row]})
        script = function_loader(source, SCOPE_FUNCTIONS) + f"""
$Root = {ps_literal(root)}
$Message = Get-Item -LiteralPath {ps_literal(message)}
$result = Get-MessageWorkDescriptor -Message $Message
if ($null -eq $result) {{ "null" }} else {{ $result | ConvertTo-Json -Depth 4 -Compress }}
"""
        result = run_powershell(script, root)
        return None if result == "null" else result


def glob_claim_probe(source: Path) -> list[str]:
    with make_tempdir("glob-claim-scope-") as tmp:
        root = Path(tmp)
        message = write_scope_fixture(root)
        claims = root / "Area_comun/state/CLAIMS.json"
        own_lease = root / ".protocol-tmp/implementer/implementer.exec-lease.json"
        script = function_loader(source, SCOPE_FUNCTIONS) + f"""
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$LeasePath = {ps_literal(own_lease)}
$Message = Get-Item -LiteralPath {ps_literal(message)}
$script:LastAdditionalSignalDetail = ""
function Test-LeaseProcessMatches {{ param($Lease) return $true }}
function Set-Claims {{ param([string]$Scope) [IO.Directory]::CreateDirectory((Split-Path -Parent {ps_literal(claims)})) | Out-Null; [IO.File]::WriteAllText({ps_literal(claims)}, ('{{"claims":[{{"owner":"{REVIEWER}","status":"active","expires_at":"2099-01-01T00:00:00Z","scope":["' + $Scope + '"]}}]}}')) }}
Set-Claims "*"
$star = Get-AdditionalWorkSignal -Message $Message
Set-Claims "src/**"
$recursive = Get-AdditionalWorkSignal -Message $Message
@($star, $recursive) | ConvertTo-Json -Compress
"""
        return run_powershell(script, root)


def dirty_veto_probe(source: Path) -> dict:
    with make_tempdir("dirty-veto-") as tmp:
        root = Path(tmp)
        message = root / "Area_comun/mailbox/open/MSG-probe-TASK-1001.md"
        message.parent.mkdir(parents=True, exist_ok=True)
        message.write_text("task_id: TASK-1001\n", encoding="ascii")
        script = function_loader(source, ("Invoke-PeerForMessage",)) + f"""
$Root = {ps_literal(root)}
$LockPath = Join-Path $Root "peer.lock"
$RunsDir = Join-Path $Root "runs"
$ResolvedAgentPath = "agent"
$PromptTemplate = "@@MESSAGE_PATH@@ @@ROOT@@ @@PEER_ID@@ @@COORDINATOR_ID@@"
$PeerId = "{IMPLEMENTER}"
$CoordinatorId = "{CHECKER}"
$AbortedResidueMinutes = 5
$script:LastResiduePaths = @("dirty.txt")
$script:deferReasons = @()
$script:admissionCalls = 0
function Clear-StaleCronLockIfSafe {{}}
function Get-StagedResidueState {{ return "live" }}
function Register-PreExecDefer {{ param($Message, [string]$Reason, [string]$Detail) $script:deferReasons += $Reason }}
function Write-Log {{ param([string]$Line) }}
function Get-AgentArguments {{ return @() }}
function Get-AgentInvocation {{ param($AgentPath, $Arguments) return [pscustomobject]@{{ FilePath=$AgentPath; Arguments=@() }} }}
function Write-Utf8NoBom {{ param($Path, $Content) [IO.Directory]::CreateDirectory((Split-Path -Parent $Path)) | Out-Null; [IO.File]::WriteAllText($Path, $Content) }}
function Acquire-ExecReservation {{ param($Message) $script:admissionCalls += 1; return [pscustomobject]@{{ ok=$false; reason="probe_stop"; detail="" }} }}
$Message = Get-Item -LiteralPath {ps_literal(message)}
Invoke-PeerForMessage -Message $Message
[ordered]@{{ admission_calls=$script:admissionCalls; defer_reasons=@($script:deferReasons) }} | ConvertTo-Json -Depth 4 -Compress
"""
        return run_powershell(script, root)


def claim_scope_probe(source: Path) -> dict:
    with make_tempdir("claim-scope-") as tmp:
        root = Path(tmp)
        message = write_scope_fixture(root)
        claims = root / "Area_comun/state/CLAIMS.json"
        own_lease = root / ".protocol-tmp/implementer/implementer.exec-lease.json"
        script = function_loader(source, SCOPE_FUNCTIONS) + f"""
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$LeasePath = {ps_literal(own_lease)}
$Message = Get-Item -LiteralPath {ps_literal(message)}
$script:LastAdditionalSignalDetail = ""
function Test-LeaseProcessMatches {{ param($Lease) return $true }}
function Set-Claims {{ param([string]$Json) [IO.Directory]::CreateDirectory((Split-Path -Parent {ps_literal(claims)})) | Out-Null; [IO.File]::WriteAllText({ps_literal(claims)}, $Json) }}
$base = '{{"claims":[{{"owner":"{REVIEWER}","status":"active","expires_at":"2099-01-01T00:00:00Z","scope":REPLACE}}]}}'
Set-Claims ($base.Replace('REPLACE', '["src/other/file.py"]'))
$disjoint = Get-AdditionalWorkSignal -Message $Message
Set-Claims ($base.Replace('REPLACE', '["src/target/file.py"]'))
$intersecting = Get-AdditionalWorkSignal -Message $Message
Set-Claims ($base.Replace(',"scope":REPLACE', ''))
$missing = Get-AdditionalWorkSignal -Message $Message
Set-Claims ($base.Replace('REPLACE', '[]'))
$empty = Get-AdditionalWorkSignal -Message $Message
Set-Claims ($base.Replace('REPLACE', '"src/target"'))
$nonArray = Get-AdditionalWorkSignal -Message $Message
Set-Claims '{{not-json'
$unreadable = Get-AdditionalWorkSignal -Message $Message
[ordered]@{{ disjoint=$disjoint; intersecting=$intersecting; malformed=@($missing,$empty,$nonArray,$unreadable) }} | ConvertTo-Json -Compress
"""
        return run_powershell(script, root)


def lease_scope_probe(source: Path) -> dict:
    with make_tempdir("lease-scope-") as tmp:
        root = Path(tmp)
        message = write_scope_fixture(root)
        write_json(root / "Area_comun/state/CLAIMS.json", {"claims": []})
        lease = root / ".protocol-tmp/reviewer/reviewer.exec-lease.json"
        own_lease = root / ".protocol-tmp/implementer/implementer.exec-lease.json"
        script = function_loader(source, SCOPE_FUNCTIONS) + f"""
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$LeasePath = {ps_literal(own_lease)}
$Message = Get-Item -LiteralPath {ps_literal(message)}
$script:LastAdditionalSignalDetail = ""
function Test-LeaseProcessMatches {{ param($Lease) return $true }}
function Set-Lease {{ param([string]$Json) [IO.Directory]::CreateDirectory((Split-Path -Parent {ps_literal(lease)})) | Out-Null; [IO.File]::WriteAllText({ps_literal(lease)}, $Json) }}
$base = '{{"owner":"{REVIEWER}","pid":1,"state":"running","work_scope":REPLACE}}'
Set-Lease ($base.Replace('REPLACE', '["src/other/file.py"]'))
$disjoint = Get-AdditionalWorkSignal -Message $Message
Set-Lease ($base.Replace('REPLACE', '["src/target/file.py"]'))
$intersecting = Get-AdditionalWorkSignal -Message $Message
Set-Lease '{{"owner":"{REVIEWER}","pid":1,"state":"running","task_or_msg_id":"unknown"}}'
$ambiguous = Get-AdditionalWorkSignal -Message $Message
[ordered]@{{ disjoint=$disjoint; intersecting=$intersecting; ambiguous=$ambiguous }} | ConvertTo-Json -Compress
"""
        return run_powershell(script, root)


def atomic_admission_probe(source: Path) -> dict:
    with make_tempdir("atomic-admission-") as tmp:
        root = Path(tmp)
        message_a = write_scope_fixture(root)
        message_b = message_a.with_name("MSG-scope-2-TASK-1001.md")
        message_b.write_text(message_a.read_text(encoding="ascii"), encoding="ascii")
        write_json(root / "Area_comun/state/CLAIMS.json", {"claims": []})
        (root / ".protocol-tmp").mkdir(parents=True, exist_ok=True)
        gate = root / "start.gate"
        function_names = SCOPE_FUNCTIONS + ("Acquire-ExecReservation",)
        processes: list[subprocess.Popen[str]] = []
        for peer, message in ((IMPLEMENTER, message_a), (REVIEWER, message_b)):
            peer_lower = peer.lower()
            lease = root / f".protocol-tmp/{peer_lower}/{peer_lower}.exec-lease.json"
            lease.parent.mkdir(parents=True, exist_ok=True)
            script = function_loader(source, function_names) + f"""
$Root = {ps_literal(root)}
$PeerId = "{peer}"
$LeasePath = {ps_literal(lease)}
$ExecAdmissionPath = Join-Path $Root ".protocol-tmp/peer-exec-admission.lock"
$Message = Get-Item -LiteralPath {ps_literal(message)}
$script:LastAdditionalSignalDetail = ""
function Test-LeaseProcessMatches {{ param($Lease) return $true }}
while (-not (Test-Path -LiteralPath {ps_literal(gate)})) {{ Start-Sleep -Milliseconds 5 }}
$result = Acquire-ExecReservation -Message $Message
[ordered]@{{ ok=[bool]$result.ok; reason=[string]$result.reason }} | ConvertTo-Json -Compress
"""
            script_path = root / f"probe-{peer_lower}.ps1"
            script_path.write_text(script, encoding="utf-8", newline="\n")
            processes.append(
                subprocess.Popen(
                    [powershell_executable(), "-NoProfile", "-NonInteractive", "-File", str(script_path)],
                    cwd=root,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            )
        gate.write_text("go\n", encoding="ascii")
        results = []
        for process in processes:
            stdout, stderr = process.communicate(timeout=30)
            assert process.returncode == 0, stderr + stdout
            results.append(json.loads(stdout))
        lease_count = len(list((root / ".protocol-tmp").glob("*/*.exec-lease.json")))
        return {"admitted": sum(1 for result in results if result["ok"]), "lease_count": lease_count, "results": results}


def post_delivery_deadline_probe(source: Path) -> dict:
    with make_tempdir("post-delivery-deadline-") as tmp:
        root = Path(tmp)
        script = function_loader(source, ("Get-PostDeliveryDeadlineAfterProgress",)) + """
$base = [DateTime]::Parse("2026-08-07T02:44:00Z").ToUniversalTime()
$hard = [DateTime]::Parse("2026-08-07T02:59:00Z").ToUniversalTime()
$afterFirst = Get-PostDeliveryDeadlineAfterProgress -CurrentDeadlineUtc $base -HardDeadlineUtc $hard -ExecDeadlineUtc ([DateTime]::Parse("2026-08-07T02:43:41Z").ToUniversalTime())
$afterSecond = Get-PostDeliveryDeadlineAfterProgress -CurrentDeadlineUtc $afterFirst -HardDeadlineUtc $hard -ExecDeadlineUtc ([DateTime]::Parse("2026-08-07T02:44:41Z").ToUniversalTime())
$atOriginalTimeout = [DateTime]::Parse("2026-08-07T02:44:01Z").ToUniversalTime()
$afterOvershoot = Get-PostDeliveryDeadlineAfterProgress -CurrentDeadlineUtc $afterSecond -HardDeadlineUtc $hard -ExecDeadlineUtc ([DateTime]::Parse("2026-08-07T03:00:00Z").ToUniversalTime())
$afterHardCap = [DateTime]::Parse("2026-08-07T02:59:01Z").ToUniversalTime()
[ordered]@{
    after_first_progress = $afterFirst.ToString("o")
    after_second_progress = $afterSecond.ToString("o")
    alive_at_original_timeout = ($atOriginalTimeout -le $afterSecond)
    no_progress_times_out = ($atOriginalTimeout -gt $base)
    clamped_deadline = $afterOvershoot.ToString("o")
    hard_cap_times_out = ($afterHardCap -gt $afterOvershoot)
} | ConvertTo-Json -Compress
"""
        return run_powershell(script, root)


def post_delivery_live_loop_probe(source: Path) -> dict:
    with make_tempdir("post-delivery-live-loop-") as tmp:
        root = Path(tmp)
        stdout_path = root / "stdout.log"
        stderr_path = root / "stderr.log"
        events_path = root / "events.jsonl"
        lease_path = root / "lease.json"
        script = function_loader(source, ("Get-PostDeliveryDeadlineAfterProgress",)) + f"""
$whileNode = $ast.FindAll({{ param($item)
    $item -is [System.Management.Automation.Language.WhileStatementAst] -and
    $item.Extent.Text.Contains("POST_DELIVERY_WINDOW_START")
}}, $true) | Select-Object -First 1
if (-not $whileNode) {{ throw "missing live supervision loop" }}
$script:logs = @()
$script:progressCalls = 0
$script:stopped = $false
$script:ticks = 0
function Write-Log {{ param([string]$Line) $script:logs += $Line }}
function Update-ExecLeaseHeartbeat {{}}
function Get-OwnDeliveryEvidence {{ return $true }}
function Stop-LeaseProcessTree {{ $script:stopped = $true; return $true }}
function Get-ExecTreeCpuSample {{ return [pscustomobject]@{{ total_ticks = 0L; cpu_by_pid = @{{}} }} }}
function Get-ExecProgressState {{
    $script:progressCalls += 1
    if ($script:progressCalls -eq 1) {{
        return [pscustomobject]@{{ progressing = $true; output_bytes = 1L; ledger_bytes = 0L; process_cpu_ticks = 0L; process_cpu_sample = [pscustomobject]@{{ total_ticks = 0L; cpu_by_pid = @{{}} }}; reasons = "probe_progress" }}
    }}
    return [pscustomobject]@{{ progressing = $false; output_bytes = 1L; ledger_bytes = 0L; process_cpu_ticks = 0L; process_cpu_sample = [pscustomobject]@{{ total_ticks = 0L; cpu_by_pid = @{{}} }}; reasons = "none" }}
}}
$process = [pscustomobject]@{{ Id = 4242 }}
$process | Add-Member ScriptMethod WaitForExit {{
    param([int]$Milliseconds)
    $script:ticks += 1
    Start-Sleep -Milliseconds 100
    return ($script:ticks -ge 80)
}}
$Message = [pscustomobject]@{{ Name = "MSG-probe.md" }}
$Root = {ps_literal(root)}
$stdoutPath = {ps_literal(stdout_path)}
$stderrPath = {ps_literal(stderr_path)}
$eventsPath = {ps_literal(events_path)}
$LeasePath = {ps_literal(lease_path)}
$StopPath = Join-Path $Root "STOP"
[IO.File]::WriteAllText($stdoutPath, "")
[IO.File]::WriteAllText($stderrPath, "")
[IO.File]::WriteAllText($eventsPath, "")
[IO.File]::WriteAllText($LeasePath, '{{}}')
$HeartbeatSeconds = 0
$nextHeartbeatSeconds = 0
$execStopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$PostDeliveryTimeoutSeconds = 5
$ProgressHardCapSeconds = 30
$ProgressExtensionSeconds = 10
$ProgressFreshSeconds = 1
$ledgerBytesBefore = 0L
$ledgerPrefixSha256Before = "probe"
$progressOutputBytes = 0L
$progressLedgerBytes = 0L
$progressProcessCpuSample = [pscustomobject]@{{ total_ticks = 0L; cpu_by_pid = @{{}} }}
$progressSampleSeconds = 1
$nextProgressCpuSampleUtc = [DateTime]::UtcNow.AddSeconds(10)
$postDeliveryDeadlineUtc = $null
$postDeliveryHardDeadlineUtc = $null
$deadlineUtc = [DateTime]::UtcNow.AddSeconds(1)
$execHardDeadlineUtc = $deadlineUtc.AddSeconds($ProgressHardCapSeconds)
Invoke-Expression $whileNode.Extent.Text
[ordered]@{{
    post_delivery_timeout_fired = [bool]($script:logs -match '^POST_DELIVERY_TIMEOUT ')
    inherited_deadline_observed = [bool]($script:logs -match 'post_delivery_deadline=(?!none)')
    stopped = $script:stopped
    ticks = $script:ticks
}} | ConvertTo-Json -Compress
"""
        return run_powershell(script, root)


def test_post_delivery_window_honors_main_progress_extensions() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-POST-DELIVERY-PROGRESS-DEADLINE"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    wiring = (
        "$postDeliveryDeadlineUtc = Get-PostDeliveryDeadlineAfterProgress "
        "-CurrentDeadlineUtc $postDeliveryDeadlineUtc -HardDeadlineUtc "
        "$postDeliveryHardDeadlineUtc -ExecDeadlineUtc $deadlineUtc"
    )
    assert wiring in source
    healthy = post_delivery_deadline_probe(HARNESS_PATH)
    assert healthy["after_first_progress"] == "2026-08-07T02:44:00.0000000Z"
    assert healthy["after_second_progress"] == "2026-08-07T02:44:41.0000000Z"
    assert healthy["alive_at_original_timeout"] is True
    assert healthy["no_progress_times_out"] is True
    assert healthy["clamped_deadline"] == "2026-08-07T02:59:00.0000000Z"
    assert healthy["hard_cap_times_out"] is True

    progress_sync = "if ($ExecDeadlineUtc -gt $nextDeadlineUtc) { $nextDeadlineUtc = $ExecDeadlineUtc }"
    ignore_progress = "if ($ExecDeadlineUtc -gt $nextDeadlineUtc) { $nextDeadlineUtc = $CurrentDeadlineUtc }"
    mutant_source = source.replace(progress_sync, ignore_progress, 1)
    assert mutant_source != source
    with make_tempdir("post-delivery-mutant-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = post_delivery_deadline_probe(mutant_path)
    assert mutant["alive_at_original_timeout"] is False

    live = post_delivery_live_loop_probe(HARNESS_PATH)
    assert live["post_delivery_timeout_fired"] is False
    assert live["inherited_deadline_observed"] is True

    live_guard = "if ($null -ne $postDeliveryDeadlineUtc) {"
    dead_guard = "if ($false -and $null -ne $postDeliveryDeadlineUtc) {"
    dead_wiring_source = source.replace(live_guard, dead_guard, 1)
    assert dead_wiring_source != source
    with make_tempdir("post-delivery-dead-wiring-") as tmp:
        dead_wiring_path = Path(tmp) / "peer_mailbox_cron.ps1"
        dead_wiring_path.write_text(dead_wiring_source, encoding="utf-8", newline="\n")
        dead_wiring = post_delivery_live_loop_probe(dead_wiring_path)
    assert dead_wiring["post_delivery_timeout_fired"] is True


def process_tree_cpu_probe(source: Path, mode: str) -> dict:
    assert mode in {"busy", "blocked", "retiring_child"}
    with make_tempdir(f"process-tree-cpu-{mode}-") as tmp:
        root = Path(tmp)
        stdout_path = root / "stdout.log"
        stderr_path = root / "stderr.log"
        events_path = root / "events.jsonl"
        for path in (stdout_path, stderr_path, events_path):
            path.write_text("", encoding="ascii")
        workload_path = root / "workload.ps1"
        heavy_path = root / "heavy-child.ps1"
        heavy_path.write_text(
            "$until=[DateTime]::UtcNow.AddMilliseconds(3500); "
            "while([DateTime]::UtcNow -lt $until){[void][Math]::Sqrt(12345.6789)}\n",
            encoding="ascii",
        )
        workloads = {
            "busy": (
                "param([int]$LifetimeMilliseconds); "
                "$until=[DateTime]::UtcNow.AddMilliseconds($LifetimeMilliseconds); "
                "while([DateTime]::UtcNow -lt $until){[void][Math]::Sqrt(12345.6789)}\n"
            ),
            "blocked": (
                "param([int]$LifetimeMilliseconds); "
                "$gate=New-Object System.Threading.ManualResetEvent($false); "
                "[void]$gate.WaitOne($LifetimeMilliseconds)\n"
            ),
            "retiring_child": (
                "param([int]$LifetimeMilliseconds); "
                "$until=[DateTime]::UtcNow.AddMilliseconds($LifetimeMilliseconds); "
                f"$worker=Start-Process -FilePath {ps_literal(powershell_executable())} "
                f"-ArgumentList @('-NoProfile','-NonInteractive','-File',{ps_literal(heavy_path)}) "
                "-WindowStyle Hidden -PassThru; $worker.WaitForExit(); "
                "while([DateTime]::UtcNow -lt $until){[void][Math]::Sqrt(12345.6789)}\n"
            ),
        }
        workload_path.write_text(workloads[mode], encoding="ascii")
        script = function_loader(
            source,
            ("Get-LeaseProcessState", "Test-LeaseProcessMatches", "Get-ExecTreeCpuSample", "Get-ExecProgressState"),
        ) + f"""
$selfProcess = Get-Process -Id $PID
$measurementLease = [pscustomobject]@{{ pid = $PID; process_start_time_utc = $selfProcess.StartTime.ToUniversalTime().ToString('o') }}
$null = Get-ExecTreeCpuSample -Lease $measurementLease
$instrumentSamplesMs = @()
foreach ($measurement in 1..2) {{
    $timer = [System.Diagnostics.Stopwatch]::StartNew()
    $sample = Get-ExecTreeCpuSample -Lease $measurementLease
    $timer.Stop()
    if ($null -eq $sample) {{ throw "process-tree CPU instrument measurement returned null" }}
    $instrumentSamplesMs += [double]$timer.Elapsed.TotalMilliseconds
}}
$instrumentCostMs = [Math]::Max($instrumentSamplesMs[0], $instrumentSamplesMs[1])
$fixedProbeDelayMs = 4500
$instrumentTraversals = 2
$safetyMarginMs = [Math]::Max(5000, [Math]::Ceiling($instrumentCostMs * 2))
$workloadLifetimeMs = [int][Math]::Ceiling($fixedProbeDelayMs + ($instrumentTraversals * $instrumentCostMs) + $safetyMarginMs)
$child = Start-Process -FilePath {ps_literal(powershell_executable())} -ArgumentList @('-NoProfile','-NonInteractive','-File',{ps_literal(workload_path)},$workloadLifetimeMs) -WindowStyle Hidden -PassThru
$null = $child.Handle
try {{
    Start-Sleep -Milliseconds 1500
    $lease = [pscustomobject]@{{ pid = $child.Id; process_start_time_utc = $child.StartTime.ToUniversalTime().ToString('o') }}
    $before = Get-ExecTreeCpuSample -Lease $lease
    Start-Sleep -Milliseconds 3000
    $result = Get-ExecProgressState -Lease $lease -StdoutPath {ps_literal(stdout_path)} -StderrPath {ps_literal(stderr_path)} -EventsPath {ps_literal(events_path)} -PreviousOutputBytes 0L -PreviousLedgerBytes 0L -PreviousProcessCpuSample $before -FreshSeconds 1
    $childAliveAtSecondSample = -not $child.HasExited
    [ordered]@{{
        progressing = [bool]$result.progressing
        before = $before.total_ticks
        after = $result.process_cpu_ticks
        child_alive_at_second_sample = $childAliveAtSecondSample
        instrument_cost_ms = [int][Math]::Ceiling($instrumentCostMs)
        workload_lifetime_ms = $workloadLifetimeMs
        safety_margin_ms = [int]$safetyMarginMs
    }} | ConvertTo-Json -Compress
}} finally {{
    if (-not $child.HasExited) {{ Stop-Process -Id $child.Id -Force -ErrorAction SilentlyContinue }}
}}
"""
        return run_powershell(script, root)


def supervision_loop_outcome_probe(source: Path) -> dict:
    with make_tempdir("supervision-loop-outcome-") as tmp:
        root = Path(tmp)
        stdout_path = root / "stdout.log"
        stderr_path = root / "stderr.log"
        events_path = root / "events.jsonl"
        lease_path = root / "lease.json"
        workload_path = root / "silent-busy.ps1"
        for path in (stdout_path, stderr_path, events_path):
            path.write_text("", encoding="ascii")
        workload_path.write_text(
            "param([int]$LifetimeMilliseconds); "
            "$until=[DateTime]::UtcNow.AddMilliseconds($LifetimeMilliseconds); "
            "while([DateTime]::UtcNow -lt $until){[void][Math]::Sqrt(12345.6789)}\n",
            encoding="ascii",
        )
        script = function_loader(
            source,
            ("Get-LeaseProcessState", "Test-LeaseProcessMatches", "Get-ExecTreeCpuSample", "Get-ExecProgressState"),
        ) + f"""
$whileNode = $ast.FindAll({{ param($item)
    $item -is [System.Management.Automation.Language.WhileStatementAst] -and
    $item.Extent.Text.Contains("POST_DELIVERY_WINDOW_START")
}}, $true) | Select-Object -First 1
if (-not $whileNode) {{ throw "missing live supervision loop" }}
$selfProcess = Get-Process -Id $PID
$measurementLease = [pscustomobject]@{{ pid = $PID; process_start_time_utc = $selfProcess.StartTime.ToUniversalTime().ToString('o') }}
$null = Get-ExecTreeCpuSample -Lease $measurementLease
$instrumentTimer = [System.Diagnostics.Stopwatch]::StartNew()
$instrumentSample = Get-ExecTreeCpuSample -Lease $measurementLease
$instrumentTimer.Stop()
if ($null -eq $instrumentSample) {{ throw "process-tree CPU instrument measurement returned null" }}
$instrumentCostMs = [Math]::Max(1, [int][Math]::Ceiling($instrumentTimer.Elapsed.TotalMilliseconds))
$ProgressFreshSeconds = [Math]::Max(2, [int][Math]::Ceiling(($instrumentCostMs + 1000) / 1000.0))
$ExecTimeoutSeconds = $ProgressFreshSeconds + [Math]::Max(3, [int][Math]::Ceiling(($instrumentCostMs + 2000) / 1000.0))
$workloadLifetimeMs = [int](($ExecTimeoutSeconds * 1000) + (3 * $instrumentCostMs) + 10000)
$process = Start-Process -FilePath {ps_literal(powershell_executable())} -ArgumentList @('-NoProfile','-NonInteractive','-File',{ps_literal(workload_path)},$workloadLifetimeMs) -WindowStyle Hidden -PassThru
$null = $process.Handle
$lease = [ordered]@{{ pid = $process.Id; process_start_time_utc = $process.StartTime.ToUniversalTime().ToString('o') }}
$lease | ConvertTo-Json -Compress | Set-Content -LiteralPath {ps_literal(lease_path)} -Encoding UTF8
$script:logs = @()
$script:stopCalls = 0
function Write-Log {{
    param([string]$Line)
    $script:logs += $Line
    if ($Line -match '^EXEC_PROGRESSING ' -and -not $process.HasExited) {{
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    }}
}}
function Update-ExecLeaseHeartbeat {{}}
function Get-OwnDeliveryEvidence {{ return $false }}
function Stop-LeaseProcessTree {{
    param($Lease, [string]$Reason)
    $script:stopCalls += 1
    Stop-Process -Id ([int]$Lease.pid) -Force -ErrorAction SilentlyContinue
    return $true
}}
$Message = [pscustomobject]@{{ Name = "MSG-real-loop-probe.md" }}
$Root = {ps_literal(root)}
$stdoutPath = {ps_literal(stdout_path)}
$stderrPath = {ps_literal(stderr_path)}
$eventsPath = {ps_literal(events_path)}
$LeasePath = {ps_literal(lease_path)}
$StopPath = Join-Path $Root "STOP"
$HeartbeatSeconds = 0
$nextHeartbeatSeconds = 0
$execStopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$PostDeliveryTimeoutSeconds = 0
$ProgressHardCapSeconds = $ExecTimeoutSeconds
$ProgressExtensionSeconds = $ExecTimeoutSeconds
$ledgerBytesBefore = 0L
$ledgerPrefixSha256Before = "probe"
$deadlineUtc = [DateTime]::UtcNow.AddSeconds($ExecTimeoutSeconds)
$postDeliveryDeadlineUtc = $null
$postDeliveryHardDeadlineUtc = $null
$execHardDeadlineUtc = $deadlineUtc.AddSeconds($ProgressHardCapSeconds)
$progressOutputBytes = 0L
$progressLedgerBytes = 0L
try {{
    $srcText = [System.IO.File]::ReadAllText($sourcePath)
    $seedIdx = $srcText.IndexOf('$progressSampleSeconds = [Math]::Max(1, $ProgressFreshSeconds)')
    if ($seedIdx -lt 0) {{ throw "missing production seed" }}
    Invoke-Expression $srcText.Substring($seedIdx, $whileNode.Extent.EndOffset - $seedIdx)
}} finally {{
    if (-not $process.HasExited) {{ Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue }}
    $process.WaitForExit()
}}
[ordered]@{{
    exec_progressing = [bool]($script:logs -match '^EXEC_PROGRESSING ')
    exec_hung = [bool]($script:logs -match '^EXEC_HUNG ')
    stop_calls = $script:stopCalls
    instrument_cost_ms = $instrumentCostMs
    exec_timeout_seconds = $ExecTimeoutSeconds
    workload_lifetime_ms = $workloadLifetimeMs
    logs = @($script:logs)
}} | ConvertTo-Json -Depth 5 -Compress
"""
        return run_powershell(script, root)


def test_silent_process_tree_cpu_is_work_derived_and_mutation_proven() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-WORK-DERIVED-EXEC-LIVENESS"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    healthy_outcome = supervision_loop_outcome_probe(HARNESS_PATH)
    assert healthy_outcome["exec_progressing"] is True
    assert healthy_outcome["exec_hung"] is False
    assert healthy_outcome["stop_calls"] == 0

    live_sampling_guard = "if ([DateTime]::UtcNow -ge $nextProgressCpuSampleUtc) {"
    unreachable_sampling_guard = "if ($false) {"
    live_sampling_seed = "$nextProgressCpuSampleUtc = $deadlineUtc.AddSeconds(-$progressSampleSeconds)"
    max_deadline_seed = "$nextProgressCpuSampleUtc = [DateTime]::MaxValue"
    sign_changed_seed = "$nextProgressCpuSampleUtc = $deadlineUtc.AddSeconds($progressSampleSeconds)"
    assert source.count(live_sampling_guard) == 1
    assert source.count(live_sampling_seed) == 2
    mutant_source = source.replace(live_sampling_guard, unreachable_sampling_guard, 1)
    assert mutant_source != source
    with make_tempdir("supervision-loop-unreachable-sampling-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant_outcome = supervision_loop_outcome_probe(mutant_path)
    assert mutant_outcome["exec_progressing"] is False
    assert mutant_outcome["exec_hung"] is True
    assert mutant_outcome["stop_calls"] == 1

    max_deadline_source = source.replace(live_sampling_seed, max_deadline_seed, 1)
    assert max_deadline_source != source
    with make_tempdir("supervision-loop-max-deadline-seed-") as tmp:
        max_deadline_path = Path(tmp) / "peer_mailbox_cron.ps1"
        max_deadline_path.write_text(max_deadline_source, encoding="utf-8", newline="\n")
        max_deadline_outcome = supervision_loop_outcome_probe(max_deadline_path)
    assert max_deadline_outcome["exec_progressing"] is False
    assert max_deadline_outcome["exec_hung"] is True
    assert max_deadline_outcome["stop_calls"] == 1

    sign_changed_source = source.replace(live_sampling_seed, sign_changed_seed, 1)
    assert sign_changed_source != source
    with make_tempdir("supervision-loop-sign-changed-seed-") as tmp:
        sign_changed_path = Path(tmp) / "peer_mailbox_cron.ps1"
        sign_changed_path.write_text(sign_changed_source, encoding="utf-8", newline="\n")
        sign_changed_outcome = supervision_loop_outcome_probe(sign_changed_path)
    assert sign_changed_outcome["exec_progressing"] is False
    assert sign_changed_outcome["exec_hung"] is True
    assert sign_changed_outcome["stop_calls"] == 1


def recycled_pid_cpu_probe(source: Path) -> dict:
    with make_tempdir("recycled-pid-cpu-") as tmp:
        root = Path(tmp)
        stdout_path = root / "stdout.log"
        stderr_path = root / "stderr.log"
        events_path = root / "events.jsonl"
        workload_path = root / "busy.ps1"
        for path in (stdout_path, stderr_path, events_path):
            path.write_text("", encoding="ascii")
        workload_path.write_text(
            "$until=[DateTime]::UtcNow.AddSeconds(20); "
            "while([DateTime]::UtcNow -lt $until){[void][Math]::Sqrt(12345.6789)}\n",
            encoding="ascii",
        )
        script = function_loader(
            source,
            ("Get-LeaseProcessState", "Test-LeaseProcessMatches", "Get-ExecTreeCpuSample", "Get-ExecProgressState"),
        ) + f"""
$child = Start-Process -FilePath {ps_literal(powershell_executable())} -ArgumentList @('-NoProfile','-NonInteractive','-File',{ps_literal(workload_path)}) -WindowStyle Hidden -PassThru
$null = $child.Handle
try {{
    Start-Sleep -Milliseconds 1500
    $start = $child.StartTime.ToUniversalTime().ToString('o')
    $lease = [pscustomobject]@{{ pid = $child.Id; process_start_time_utc = $start }}
    $inflated = 6000000000L
    $oldIdentity = "{{0}}|1900-01-01T00:00:00.0000000Z" -f $child.Id
    $previousMap = @{{ ([string]$child.Id) = $inflated; $oldIdentity = $inflated }}
    $before = [pscustomobject]@{{ total_ticks = (2L * $inflated); cpu_by_pid = $previousMap }}
    Start-Sleep -Milliseconds 1500
    $result = Get-ExecProgressState -Lease $lease -StdoutPath {ps_literal(stdout_path)} -StderrPath {ps_literal(stderr_path)} -EventsPath {ps_literal(events_path)} -PreviousOutputBytes 0L -PreviousLedgerBytes 0L -PreviousProcessCpuSample $before -FreshSeconds 1
    $liveProcessTicks = [long](Get-Process -Id $child.Id -ErrorAction Stop).TotalProcessorTime.Ticks
    [ordered]@{{
        progressing = [bool]$result.progressing
        before = [long]$before.total_ticks
        after = [long]$result.process_cpu_ticks
        live_process_ticks = $liveProcessTicks
    }} | ConvertTo-Json -Compress
}} finally {{
    if (-not $child.HasExited) {{ Stop-Process -Id $child.Id -Force -ErrorAction SilentlyContinue }}
}}
"""
        return run_powershell(script, root)


def test_process_tree_cpu_sample_distinguishes_recycled_pid() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-PROCESS-IDENTITY-CPU-SAMPLE"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    healthy = recycled_pid_cpu_probe(HARNESS_PATH)
    assert healthy["progressing"] is True
    assert healthy["after"] > healthy["before"]

    identity_key = '$processKey = "{0}|{1}" -f $processId, $processStartTimeUtc'
    pid_only_key = "$processKey = [string]$processId"
    assert source.count(identity_key) == 1
    mutant_source = source.replace(identity_key, pid_only_key, 1)
    with make_tempdir("recycled-pid-mutant-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = recycled_pid_cpu_probe(mutant_path)
    assert mutant["progressing"] is False
    assert mutant["live_process_ticks"] > 0


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


def obligation_alert_probe(source: Path) -> dict:
    with make_tempdir("obligation-alert-") as tmp:
        root = Path(tmp)
        task_path = root / "Area_comun/tasks/TASK-test.md"
        task_path.parent.mkdir(parents=True)
        task_path.write_text("---\nstatus: in_progress\n---\n", encoding="ascii")
        state = root / "Area_comun/state"
        state.mkdir(parents=True)
        (state / "TASK_INDEX.json").write_text(json.dumps({"tasks": [{"id": "TASK-test", "status": "in_progress", "owner": IMPLEMENTER, "reviewer": REVIEWER, "file": "Area_comun/tasks/TASK-test.md"}]}), encoding="ascii")
        (state / "CLAIMS.json").write_text('{"claims": []}', encoding="ascii")
        message = root / "MSG-test.md"
        message.write_text("task_id: TASK-test\n", encoding="ascii")
        script = function_loader(source, ("Write-CoordinationAlert", "Register-RetryExhausted", "Test-StalledTaskObligations")) + f"""
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$RuntimeDir = Join-Path $Root ".protocol-tmp\\probe"
New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null
$AlertPath = Join-Path $RuntimeDir "alerts.json"
$LeasePath = Join-Path $RuntimeDir "lease.json"
$StalledTaskMinutes = 30
function Get-Field {{ param($Content, $Name) if ($Content -match '(?m)^task_id:\\s*(.+)$') {{ return $Matches[1].Trim() }} return "" }}
function Write-AtomicUtf8NoBom {{ param($Path, $Content) [IO.File]::WriteAllText($Path, $Content, [Text.UTF8Encoding]::new($false)) }}
function Write-Log {{ param($Line) }}
$message = Get-Item -LiteralPath {ps_literal(message)}
Register-RetryExhausted -Message $message -Attempts 3 -Outcome "transient"
$retryCount = if (Test-Path $AlertPath) {{ (Get-Content -LiteralPath $AlertPath -Raw | ConvertFrom-Json).alerts.psobject.Properties.Count }} else {{ 0 }}
Remove-Item -LiteralPath $AlertPath
Test-StalledTaskObligations
$freshCount = if (Test-Path $AlertPath) {{ (Get-Content -LiteralPath $AlertPath -Raw | ConvertFrom-Json).alerts.psobject.Properties.Count }} else {{ 0 }}
(Get-Item -LiteralPath {ps_literal(task_path)}).LastWriteTimeUtc = [DateTime]::UtcNow.AddMinutes(-31)
Test-StalledTaskObligations
$oldCount = (Get-Content -LiteralPath $AlertPath -Raw | ConvertFrom-Json).alerts.psobject.Properties.Count
[ordered]@{{ retry_alert_count = $retryCount; fresh_stalled_count = $freshCount; old_stalled_count = $oldCount }} | ConvertTo-Json -Compress
"""
        return run_powershell(script, root)


def real_foreign_personal_rename_probe() -> dict:
    with make_tempdir("residue-rename-") as tmp:
        root = Path(tmp)
        old_path = f"personal/{REVIEWER}/draft-old.md"
        new_path = f"personal/{REVIEWER}/draft-new.md"
        source = root / old_path
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("draft\n", encoding="ascii")
        (root / ".gitignore").write_text("probe.ps1\n", encoding="ascii")
        for command in (
            ("git", "init"),
            ("git", "config", "user.name", "Fixture"),
            ("git", "config", "user.email", "fixture@example.invalid"),
            ("git", "add", ".gitignore", old_path),
            ("git", "commit", "-m", "fixture"),
            ("git", "mv", old_path, new_path),
        ):
            subprocess.run(command, cwd=root, check=True, capture_output=True)
        script = function_loader(
            HARNESS_PATH,
            (
                "Invoke-GitStatusPorcelainUtf8",
                "Get-EmbeddedRepositoryRoots",
                "Get-GitStatusPorcelainUtf8",
                "Get-StagedResidueState",
            ),
        ) + f"""
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$ResiduePath = Join-Path $Root "residue.json"
$AbortedResidueMinutes = 5
$ResidueDiagnosticPathLimit = 10
$script:LastResiduePaths = @()
function Write-Utf8NoBom {{ param($Path, $Content) [IO.File]::WriteAllText($Path, $Content, [Text.UTF8Encoding]::new($false)) }}
$statusResult = Get-GitStatusPorcelainUtf8
$records = @([string]$statusResult.raw -split [char]0 | Where-Object {{ $_ }})
$state = Get-StagedResidueState
[ordered]@{{ records = $records; state = $state; paths = @($script:LastResiduePaths) }} | ConvertTo-Json -Depth 6 -Compress
"""
        return run_powershell(script, root)


def real_worktree_disk_proof_rename_probe(source_path: Path = HARNESS_PATH) -> dict:
    with make_tempdir("disk-proof-rename-") as tmp:
        root = Path(tmp)
        old_path = f"personal/{REVIEWER}/disk-old.md"
        new_path = f"personal/{REVIEWER}/disk-new.md"
        source = root / old_path
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("proof\n", encoding="ascii")
        (root / ".gitignore").write_text("probe.ps1\n", encoding="ascii")
        for command in (
            ("git", "init"),
            ("git", "config", "user.name", "Fixture"),
            ("git", "config", "user.email", "fixture@example.invalid"),
            ("git", "add", ".gitignore", old_path),
            ("git", "commit", "-m", "fixture"),
            ("git", "mv", old_path, new_path),
        ):
            subprocess.run(command, cwd=root, check=True, capture_output=True)
        script = function_loader(
            source_path,
            (
                "Invoke-GitStatusPorcelainUtf8",
                "Get-EmbeddedRepositoryRoots",
                "Get-GitStatusPorcelainUtf8",
                "Get-WorktreeDiskProof",
            ),
        ) + f"""
$Root = {ps_literal(root)}
$statusResult = Get-GitStatusPorcelainUtf8
$records = @([string]$statusResult.raw -split [char]0 | Where-Object {{ $_ }})
$proof = Get-WorktreeDiskProof
[ordered]@{{ records = $records; proof = $proof }} | ConvertTo-Json -Depth 6 -Compress
"""
        result = run_powershell(script, root)
    result["proof"] = json.loads(result["proof"]) if result["proof"] is not None else None
    result["paths"] = [row["path"] for row in result["proof"]] if result["proof"] is not None else None
    result["exists"] = [row["exists"] for row in result["proof"]] if result["proof"] is not None else None
    return result


def test_worktree_disk_proof_pairs_real_git_rename_records() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-WORKTREE-DISK-PROOF-RENAME-PAIRING"""
    old_path = f"personal/{REVIEWER}/disk-old.md"
    new_path = f"personal/{REVIEWER}/disk-new.md"
    healthy = real_worktree_disk_proof_rename_probe()
    assert healthy["records"] == [f"R  {new_path}", old_path]
    assert healthy["paths"] == [new_path, old_path]
    assert healthy["exists"] == [True, False]

    source = HARNESS_PATH.read_text(encoding="utf-8")
    paired_source = '$source = $records[$index + 1].Replace("\\", "/")'
    stripped_source = '$source = $records[$index + 1].Substring(3).Replace("\\", "/")'
    mutant_source = source.replace(paired_source, stripped_source, 1)
    assert mutant_source != source
    with make_tempdir("disk-proof-mutant-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = real_worktree_disk_proof_rename_probe(mutant_path)
    assert mutant["paths"] != healthy["paths"]

    with make_tempdir("disk-proof-malformed-") as tmp:
        root = Path(tmp)
        script = function_loader(HARNESS_PATH, ("Get-WorktreeDiskProof",)) + f"""
$Root = {ps_literal(root)}
function Get-GitStatusPorcelainUtf8 {{ return [pscustomobject]@{{ ok = $true; raw = "R  moved.md`0" }} }}
$proof = Get-WorktreeDiskProof
[ordered]@{{ proof = $proof }} | ConvertTo-Json -Compress
"""
        malformed = run_powershell(script, root)["proof"]
    assert malformed is None


def load_sweeper_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_python_function(path: Path, name: str):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)
    namespace: dict[str, object] = {}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), "exec"), namespace)
    return namespace[name]


def test_zombie_sweeper_parses_real_git_quoted_rename_paths() -> None:
    """PERMANENT_NEGATIVE: NEG-CRON-ZOMBIE-SWEEPER-PORCELAIN-Z-PATHS"""
    with make_tempdir("zombie-porcelain-") as tmp:
        root = Path(tmp)
        old_path = "tracked-old.md"
        new_path = "tracked-new.md"
        quoted_path = "untracked cafe\N{LATIN SMALL LETTER E WITH ACUTE} path.md"
        (root / old_path).write_text("tracked\n", encoding="ascii")
        for command in (
            ("git", "init"),
            ("git", "config", "user.name", "Fixture"),
            ("git", "config", "user.email", "fixture@example.invalid"),
            ("git", "add", old_path),
            ("git", "commit", "-m", "fixture"),
            ("git", "mv", old_path, new_path),
        ):
            subprocess.run(command, cwd=root, check=True, capture_output=True)
        (root / quoted_path).write_text("untracked\n", encoding="ascii")

        legacy_raw = subprocess.run(
            ["git", "status", "--porcelain=v1"], cwd=root, check=True, capture_output=True
        ).stdout
        assert b" -> " in legacy_raw
        assert b'"' in legacy_raw
        legacy: set[str] = set()
        for line in legacy_raw.decode("ascii").splitlines():
            path = line[3:].strip()
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            legacy.add(path.replace("\\", "/"))

        expected = {old_path, new_path, quoted_path}
        healthy = sweep.dirty_paths(root)
        assert expected <= healthy
        real_z_raw = subprocess.run(
            ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
            cwd=root,
            check=True,
            capture_output=True,
        ).stdout
        runtime_parser = load_python_function(ROOT / "runtime/orchestrator.py", "parse_porcelain_v1_z")
        mirror_parser = load_python_function(
            ROOT / "examples/full_runtime_instance/runtime/orchestrator.py", "parse_porcelain_v1_z"
        )
        assert expected <= set(runtime_parser(real_z_raw))
        assert expected <= set(mirror_parser(real_z_raw))
        assert not expected <= legacy

        source_path = ROOT / "scripts/sweep_cron_zombies.py"
        source = source_path.read_text(encoding="utf-8")
        nul_command = '["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"]'
        line_command = '["git", "status", "--porcelain=v1", "--untracked-files=all"]'
        mutant_source = source.replace(nul_command, line_command, 1)
        assert mutant_source != source
        mutant_path = root / "sweep_cron_zombies_mutant.py"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = load_sweeper_module(mutant_path, "sweep_cron_zombies_task0323_mutant")
        try:
            mutant.dirty_paths(root)
        except ValueError:
            mutant_failed_closed = True
        else:
            mutant_failed_closed = False
        assert mutant_failed_closed is True


def test_git_status_readers_enumerate_untracked_files_without_overbroad_veto() -> None:
    """PERMANENT_NEGATIVE: NEG-CRON-STATUS-UNTRACKED-FILE-CONVERGENCE"""
    with make_tempdir("status-untracked-files-") as tmp:
        root = Path(tmp)
        claims_path = root / "Area_comun/state/CLAIMS.json"
        claims_path.parent.mkdir(parents=True)
        claims_path.write_text('{"claims": []}\n', encoding="ascii")
        (root / ".gitignore").write_text("probe.ps1\n", encoding="ascii")
        for command in (
            ("git", "init"),
            ("git", "config", "user.name", "Fixture"),
            ("git", "config", "user.email", "fixture@example.invalid"),
            ("git", "add", ".gitignore", "Area_comun/state/CLAIMS.json"),
            ("git", "commit", "-m", "fixture"),
        ):
            subprocess.run(command, cwd=root, check=True, capture_output=True)

        untracked_dir = "work/"
        untracked_path = "work/nested/item.txt"
        nested = root / untracked_path
        nested.parent.mkdir(parents=True)
        nested.write_text("dirty\n", encoding="ascii")
        claims_path.write_text(
            json.dumps(
                {
                    "claims": [
                        {
                            "owner": IMPLEMENTER,
                            "status": "active",
                            "scope": [untracked_path],
                        }
                    ]
                }
            )
            + "\n",
            encoding="ascii",
        )
        subprocess.run(
            ("git", "add", "Area_comun/state/CLAIMS.json"),
            cwd=root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ("git", "commit", "-m", "claim fixture"),
            cwd=root,
            check=True,
            capture_output=True,
        )

        collapsed_raw = subprocess.run(
            ("git", "status", "--porcelain=v1", "-z"),
            cwd=root,
            check=True,
            capture_output=True,
        ).stdout
        collapsed_paths = sweep.parse_porcelain_v1_z(collapsed_raw)
        healthy_paths = sweep.dirty_paths(root)

        script = function_loader(
            HARNESS_PATH,
            ("Invoke-GitStatusPorcelainUtf8", "Get-EmbeddedRepositoryRoots", "Get-GitStatusPorcelainUtf8"),
        ) + f"""
$Root = {ps_literal(root)}
$statusResult = Get-GitStatusPorcelainUtf8
$records = @([string]$statusResult.raw -split [char]0 | Where-Object {{ $_ }})
[ordered]@{{ ok = $statusResult.ok; records = $records }} | ConvertTo-Json -Compress
"""
        powershell = run_powershell(script, root)
        powershell_paths = powershell["records"]

        source = (ROOT / "scripts/sweep_cron_zombies.py").read_text(encoding="utf-8")
        untracked_option = ', "--untracked-files=all"'
        mutant_source = source.replace(untracked_option, "", 1)
        assert mutant_source != source
        mutant_path = root / "sweep_cron_zombies_untracked_mutant.py"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = load_sweeper_module(mutant_path, "sweep_cron_zombies_task0326_mutant")

        assert collapsed_paths == {untracked_dir}
        assert healthy_paths == {untracked_path}
        assert powershell["ok"] is True
        assert powershell_paths == [f"?? {untracked_path}"]
        assert sweep.dirty_claimed_route(root, IMPLEMENTER) is True
        assert mutant.dirty_claimed_route(root, IMPLEMENTER) is False
        assert sweep.dirty_claimed_route(root, REVIEWER) is False


def test_embedded_repository_dirty_claim_is_fail_closed_and_mutation_proven() -> None:
    """PERMANENT_NEGATIVE: NEG-CRON-STATUS-EMBEDDED-REPOSITORY-DIRTY-CLAIM"""
    with make_tempdir("embedded-repository-") as tmp:
        root = Path(tmp)
        claims_path = root / "Area_comun/state/CLAIMS.json"
        claims_path.parent.mkdir(parents=True)
        claims_path.write_text('{"claims": []}\n', encoding="ascii")
        for command in (
            ("git", "init"),
            ("git", "config", "user.name", "Fixture"),
            ("git", "config", "user.email", "fixture@example.invalid"),
            ("git", "add", "Area_comun/state/CLAIMS.json"),
            ("git", "commit", "-m", "outer fixture"),
        ):
            subprocess.run(command, cwd=root, check=True, capture_output=True)

        embedded = root / "work/level/inner"
        embedded.mkdir(parents=True)
        for command in (
            ("git", "init"),
            ("git", "config", "user.name", "Fixture"),
            ("git", "config", "user.email", "fixture@example.invalid"),
        ):
            subprocess.run(command, cwd=embedded, check=True, capture_output=True)
        live_path = "work/level/inner/live_work.md"
        (root / live_path).write_text("live\n", encoding="ascii")
        claims_path.write_text(
            json.dumps(
                {
                    "claims": [
                        {"owner": IMPLEMENTER, "status": "active", "scope": [live_path]}
                    ]
                }
            )
            + "\n",
            encoding="ascii",
        )
        subprocess.run(("git", "add", "Area_comun/state/CLAIMS.json"), cwd=root, check=True)
        subprocess.run(("git", "commit", "-m", "claim fixture"), cwd=root, check=True, capture_output=True)

        parent_variants = []
        for options in ((), ("--untracked-files=all",), ("--untracked-files=all", "--ignored")):
            raw = subprocess.run(
                ("git", "status", "--porcelain=v1", "-z", *options),
                cwd=root,
                check=True,
                capture_output=True,
            ).stdout
            parent_variants.append(sweep.parse_porcelain_v1_z(raw))

        loader = function_loader(
            HARNESS_PATH,
            ("Invoke-GitStatusPorcelainUtf8", "Get-EmbeddedRepositoryRoots", "Get-GitStatusPorcelainUtf8"),
        )
        script = loader + f"""
$Root = {ps_literal(root)}
$result = Get-GitStatusPorcelainUtf8 -IncludeEmbeddedRepositories
$records = @([string]$result.raw -split [char]0 | Where-Object {{ $_ }})
[ordered]@{{ ok = $result.ok; paths = @($records | ForEach-Object {{ if ($_.Length -ge 4) {{ $_.Substring(3).Replace("\\", "/") }} }}) }} | ConvertTo-Json -Compress
"""
        powershell = run_powershell(script, root)
        powershell_paths = set(powershell["paths"])

        source_path = ROOT / "scripts/sweep_cron_zombies.py"
        source = source_path.read_text(encoding="utf-8")
        discovery = "for repository_root in repository_roots(root):"
        mutant_source = source.replace(discovery, "for repository_root in [root]:", 1)
        assert mutant_source != source
        mutant_path = root / "sweep_cron_zombies_embedded_mutant.py"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = load_sweeper_module(mutant_path, "sweep_cron_zombies_task0334_mutant")

        harness_source = HARNESS_PATH.read_text(encoding="utf-8")
        ps_discovery = "if ($IncludeEmbeddedRepositories) {"
        ps_mutant_source = harness_source.replace(ps_discovery, "if ($false) {", 1)
        assert ps_mutant_source != harness_source
        ps_mutant_path = root / "peer_mailbox_cron_embedded_mutant.ps1"
        ps_mutant_path.write_text(ps_mutant_source, encoding="utf-8", newline="\n")
        mutant_loader = function_loader(
            ps_mutant_path,
            ("Invoke-GitStatusPorcelainUtf8", "Get-EmbeddedRepositoryRoots", "Get-GitStatusPorcelainUtf8"),
        )
        mutant_script = mutant_loader + f"""
$Root = {ps_literal(root)}
$result = Get-GitStatusPorcelainUtf8 -IncludeEmbeddedRepositories
$records = @([string]$result.raw -split [char]0 | Where-Object {{ $_ }})
[ordered]@{{ ok = $result.ok; paths = @($records | ForEach-Object {{ if ($_.Length -ge 4) {{ $_.Substring(3).Replace("\\", "/") }} }}) }} | ConvertTo-Json -Compress
"""
        powershell_mutant = run_powershell(mutant_script, root)
        powershell_mutant_paths = set(powershell_mutant["paths"])

        original_discovery = sweep.repository_roots
        try:
            def fail_discovery(_root: Path) -> list[Path]:
                raise OSError("fixture discovery failure")

            sweep.repository_roots = fail_discovery
            try:
                sweep.dirty_claimed_route(root, IMPLEMENTER)
            except OSError:
                python_discovery_failed_closed = True
            else:
                python_discovery_failed_closed = False
        finally:
            sweep.repository_roots = original_discovery

        failure_script = loader + f"""
$Root = {ps_literal(root)}
function Get-EmbeddedRepositoryRoots {{ throw "fixture discovery failure" }}
$result = Get-GitStatusPorcelainUtf8 -IncludeEmbeddedRepositories
[ordered]@{{ ok = $result.ok; reason = $result.reason }} | ConvertTo-Json -Compress
"""
        powershell_discovery_failure = run_powershell(failure_script, root)

        assert live_path not in parent_variants[0]
        assert live_path not in parent_variants[1]
        assert live_path not in parent_variants[2]
        assert live_path in sweep.dirty_paths(root)
        assert sweep.dirty_claimed_route(root, IMPLEMENTER) is True
        assert powershell["ok"] is True
        assert live_path in powershell_paths, sorted(powershell_paths)
        assert mutant.dirty_claimed_route(root, IMPLEMENTER) is False
        assert powershell_mutant["ok"] is True
        assert live_path not in powershell_mutant_paths
        assert python_discovery_failed_closed is True
        assert powershell_discovery_failure["ok"] is False


def test_parent_ignore_boundary_separates_claim_veto_from_blocking_readers() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-PARENT-IGNORE-BOUNDARY"""
    with make_tempdir("parent-ignore-boundary-") as tmp:
        root = Path(tmp)
        claims_path = root / "Area_comun/state/CLAIMS.json"
        claims_path.parent.mkdir(parents=True)
        ignored_path = ".protocol-tmp/zc/note.md"
        claims_path.write_text(
            json.dumps(
                {
                    "claims": [
                        {"owner": IMPLEMENTER, "status": "active", "scope": [ignored_path]}
                    ]
                }
            )
            + "\n",
            encoding="ascii",
        )
        (root / ".gitignore").write_text(
            ".protocol-tmp/\nprobe.ps1\nresidue.json\n", encoding="ascii"
        )
        for command in (
            ("git", "init"),
            ("git", "config", "user.name", "Fixture"),
            ("git", "config", "user.email", "fixture@example.invalid"),
            ("git", "add", ".gitignore", "Area_comun/state/CLAIMS.json"),
            ("git", "commit", "-m", "outer fixture"),
        ):
            subprocess.run(command, cwd=root, check=True, capture_output=True)

        embedded = root / ".protocol-tmp/zc"
        embedded.mkdir(parents=True)
        for command in (
            ("git", "init"),
            ("git", "config", "user.name", "Fixture"),
            ("git", "config", "user.email", "fixture@example.invalid"),
        ):
            subprocess.run(command, cwd=embedded, check=True, capture_output=True)
        (root / ignored_path).write_text("live\n", encoding="ascii")

        functions = (
            "Write-Utf8NoBom",
            "Invoke-GitStatusPorcelainUtf8",
            "Get-EmbeddedRepositoryRoots",
            "Get-GitStatusPorcelainUtf8",
            "Get-WorktreeDiskProof",
            "Get-StagedResidueState",
        )

        def probe(harness_path: Path) -> dict[str, object]:
            loader = function_loader(harness_path, functions)
            script = loader + f"""
$Root = {ps_literal(root)}
$PeerId = "{IMPLEMENTER}"
$ResiduePath = Join-Path $Root "residue.json"
$AbortedResidueMinutes = 5
$ResidueDiagnosticPathLimit = 10
$script:LastResiduePaths = @()
$parent = Get-GitStatusPorcelainUtf8
$expanded = Get-GitStatusPorcelainUtf8 -IncludeEmbeddedRepositories
$parentRecords = @([string]$parent.raw -split [char]0 | Where-Object {{ $_ }})
$expandedRecords = @([string]$expanded.raw -split [char]0 | Where-Object {{ $_ }})
$residue = Get-StagedResidueState
$proofValue = Get-WorktreeDiskProof
$proof = if ($null -eq $proofValue) {{ "" }} else {{ [string]$proofValue }}
[ordered]@{{
    parent_paths = @($parentRecords | ForEach-Object {{ if ($_.Length -ge 4) {{ $_.Substring(3) }} }})
    expanded_paths = @($expandedRecords | ForEach-Object {{ if ($_.Length -ge 4) {{ $_.Substring(3) }} }})
    residue = $residue
    proof = $proof
}} | ConvertTo-Json -Depth 6 -Compress
"""
            return run_powershell(script, root)

        healthy = probe(HARNESS_PATH)
        source = HARNESS_PATH.read_text(encoding="utf-8")
        blocking_status_call = "$statusResult = Get-GitStatusPorcelainUtf8"
        expanded_status_call = "$statusResult = Get-GitStatusPorcelainUtf8 -IncludeEmbeddedRepositories"
        assert source.count(blocking_status_call) == 2
        mutant_source = source.replace(blocking_status_call, expanded_status_call)
        with make_tempdir("parent-ignore-boundary-mutant-") as mutant_tmp:
            mutant_path = Path(mutant_tmp) / "peer_mailbox_cron.ps1"
            mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
            mutant = probe(mutant_path)

        assert healthy["parent_paths"] == []
        assert ignored_path in healthy["expanded_paths"], healthy
        assert healthy["residue"] == "none"
        assert ignored_path not in healthy["proof"]
        assert sweep.dirty_claimed_route(root, IMPLEMENTER) is True
        assert mutant["residue"] == "live"
        assert ignored_path in mutant["proof"]


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
    rename = real_foreign_personal_rename_probe()
    assert rename["records"] == [
        f"R  personal/{REVIEWER}/draft-new.md",
        f"personal/{REVIEWER}/draft-old.md",
    ]
    assert rename["state"] == "none"
    assert rename["paths"] == []


def test_retry_exhaustion_alert_and_stalled_task_threshold_kill_mutant() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-RETRY-EXHAUSTED-DURABLE-ALERT"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    retry_alert_call = 'Write-CoordinationAlert -Kind "retry_exhausted" -Message $Message -Detail "outcome=$Outcome attempts=$Attempts"'
    dead_retry_alert_call = '# retry alert disabled by mutant'
    assert source.count(retry_alert_call) == 1
    healthy = obligation_alert_probe(HARNESS_PATH)
    assert healthy["retry_alert_count"] == 1
    assert healthy["fresh_stalled_count"] == 0
    assert healthy["old_stalled_count"] == 1
    with make_tempdir("retry-alert-mutant-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(source.replace(retry_alert_call, dead_retry_alert_call, 1), encoding="utf-8", newline="\n")
        mutant = obligation_alert_probe(mutant_path)
    assert mutant["retry_alert_count"] == 0


def test_residue_excludes_foreign_personal_and_caps_diagnostics() -> None:
    with make_tempdir("residue-probe-") as tmp:
        root = Path(tmp)
        own_paths = [f"personal/{IMPLEMENTER}/owned-{index}.txt" for index in range(12)]
        foreign_path = f"personal/{REVIEWER}/foreign.txt"
        for relative in [foreign_path, *own_paths]:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("dirty\n", encoding="ascii")
        subprocess.run(("git", "init"), cwd=root, check=True, capture_output=True)
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


def test_scope_aware_claim_veto_kills_both_direction_mutants() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-SCOPE-AWARE-EXTERNAL-CLAIM"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    claim_intersection = "if (Test-ScopeIntersection -Left $messageWork.work_scope -Right $claimScope) { return \"active_external_claim\" }"
    assert source.count(claim_intersection) == 1
    healthy = claim_scope_probe(HARNESS_PATH)
    with make_tempdir("claim-allow-mutant-") as tmp:
        allow_path = Path(tmp) / "peer_mailbox_cron.ps1"
        allow_path.write_text(source.replace(claim_intersection, 'if ($false) { return "active_external_claim" }', 1), encoding="utf-8", newline="\n")
        allow_mutant = claim_scope_probe(allow_path)
    with make_tempdir("claim-veto-mutant-") as tmp:
        veto_path = Path(tmp) / "peer_mailbox_cron.ps1"
        veto_path.write_text(source.replace(claim_intersection, 'if ($true) { return "active_external_claim" }', 1), encoding="utf-8", newline="\n")
        veto_mutant = claim_scope_probe(veto_path)
    assert healthy["disjoint"] == "none"
    assert healthy["intersecting"] == "active_external_claim"
    assert healthy["malformed"] == [
        "active_external_claim",
        "active_external_claim",
        "active_external_claim",
        "claims_unreadable",
    ]
    assert allow_mutant["intersecting"] == "none"
    assert veto_mutant["disjoint"] == "active_external_claim"


def test_scope_aware_lease_veto_kills_both_direction_mutants() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-SCOPE-AWARE-PEER-LEASE"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    lease_intersection = "if (Test-ScopeIntersection -Left $messageWork.work_scope -Right $leaseScope) { return \"active_peer_lease\" }"
    assert source.count(lease_intersection) == 1
    healthy = lease_scope_probe(HARNESS_PATH)
    with make_tempdir("lease-allow-mutant-") as tmp:
        allow_path = Path(tmp) / "peer_mailbox_cron.ps1"
        allow_path.write_text(source.replace(lease_intersection, 'if ($false) { return "active_peer_lease" }', 1), encoding="utf-8", newline="\n")
        allow_mutant = lease_scope_probe(allow_path)
    with make_tempdir("lease-veto-mutant-") as tmp:
        veto_path = Path(tmp) / "peer_mailbox_cron.ps1"
        veto_path.write_text(source.replace(lease_intersection, 'if ($true) { return "active_peer_lease" }', 1), encoding="utf-8", newline="\n")
        veto_mutant = lease_scope_probe(veto_path)
    assert healthy["disjoint"] == "none"
    assert healthy["intersecting"] == "active_peer_lease"
    assert healthy["ambiguous"] == "active_peer_lease"
    assert allow_mutant["intersecting"] == "none"
    assert veto_mutant["disjoint"] == "active_peer_lease"


def test_atomic_exec_admission_kills_peer_specific_lock_mutant() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-ATOMIC-EXEC-ADMISSION"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    signal_line = "$signal = Get-AdditionalWorkSignal -Message $Message"
    delayed_source = source.replace(signal_line, signal_line + "\n        Start-Sleep -Milliseconds 250", 1)
    assert delayed_source != source
    shared_admission_path = "            $ExecAdmissionPath,"
    peer_specific_admission_path = '            ($ExecAdmissionPath + "." + $PeerId),'
    assert delayed_source.count(shared_admission_path) == 1
    mutant_source = delayed_source.replace(shared_admission_path, peer_specific_admission_path, 1)
    with make_tempdir("atomic-healthy-source-") as tmp:
        healthy_path = Path(tmp) / "peer_mailbox_cron.ps1"
        healthy_path.write_text(delayed_source, encoding="utf-8", newline="\n")
        healthy = atomic_admission_probe(healthy_path)
    with make_tempdir("atomic-mutant-source-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = atomic_admission_probe(mutant_path)
    assert healthy["admitted"] == 1
    assert healthy["lease_count"] == 1
    assert mutant["admitted"] == 2
    assert mutant["lease_count"] == 2


def test_orphan_lease_self_heal_matrix_requires_dead_owner_evidence() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-RESERVED-LEASE-SELF-HEAL"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    lock_liveness_promotion = '                if ($lockLiveness -ne "unknown") { $liveness = $lockLiveness }'
    dead_evidence_ignored = '                if ($false) { $liveness = $lockLiveness }'
    assert source.count(lock_liveness_promotion) == 1
    mutant_source = source.replace(lock_liveness_promotion, dead_evidence_ignored, 1)
    with make_tempdir("orphan-self-heal-mutant-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = orphan_lease_self_heal_matrix_probe(mutant_path)
    healthy = orphan_lease_self_heal_matrix_probe(HARNESS_PATH)
    expected_states = {
        "reserved_without_lock",
        "truncated_with_lock",
        "empty_with_lock",
        "reserved_missing_deadline_with_lock",
    }
    assert set(healthy) == expected_states
    assert all(len(result["rounds"]) == 3 for result in healthy.values())
    unknown_rounds = healthy["reserved_without_lock"]["rounds"]
    assert all(row["lock_exists"] and row["lease_exists"] for row in unknown_rounds)
    assert "liveness=unknown action=preserve" in healthy["reserved_without_lock"]["logs"][0]
    for state in expected_states - {"reserved_without_lock"}:
        healthy_rounds = healthy[state]["rounds"]
        assert all(not row["lock_exists"] and not row["lease_exists"] for row in healthy_rounds)
    assert all(row["lease_exists"] for row in mutant["truncated_with_lock"]["rounds"])
    assert all(row["lease_exists"] for row in mutant["empty_with_lock"]["rounds"])


def test_live_unreadable_lease_is_preserved_and_deadline_mutant_dies() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-LIVE-UNREADABLE-LEASE-PRESERVED"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    reservation_deadline_selector = "[string]$lease.reservation_deadline"
    running_deadline_selector = "[string]$lease.deadline"
    assert source.count(reservation_deadline_selector) == 2
    mutant_source = source.replace(reservation_deadline_selector, running_deadline_selector, 1)
    with make_tempdir("live-unreadable-mutant-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = live_lease_self_heal_probe(mutant_path)
    healthy = live_lease_self_heal_probe(HARNESS_PATH)
    expected_states = {
        "reserved_live",
        "truncated_live",
        "empty_live",
        "reserved_missing_deadline_live",
    }
    assert set(healthy) == expected_states
    assert all(row["lock_exists"] and row["lease_exists"] for row in healthy.values())
    assert healthy["reserved_live"]["logs"] == []
    assert "liveness=live action=preserve" in healthy["truncated_live"]["logs"][0]
    for state in expected_states - {"reserved_live"}:
        assert healthy[state]["logs"]
        assert "liveness=live action=preserve" in healthy[state]["logs"][0]
    assert mutant["reserved_live"]["lock_exists"] is True
    assert mutant["reserved_live"]["lease_exists"] is True
    assert mutant["reserved_live"]["logs"]
    assert "liveness=live action=preserve" in mutant["reserved_live"]["logs"][0]


def test_lease_owner_lock_state_table_is_complete_and_mutation_proven() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-LEASE-OWNER-LOCK-STATE-TABLE"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    process_states = lease_process_state_probe(HARNESS_PATH)
    expected_process_states = {
        "live": "live",
        "dead": "dead",
        "unknown": "unknown",
        "pid_reused": "dead",
        "get_process_error": "unknown",
        "start_time_error": "unknown",
    }
    assert process_states == expected_process_states
    nullish = nullish_peer_lease_guard_probe(HARNESS_PATH)
    assert nullish == {"empty": "peer_lease_unreadable", "whitespace": "peer_lease_unreadable"}

    healthy = lease_owner_lock_state_table_probe(HARNESS_PATH)
    assert len(healthy) == 24
    for cell, row in healthy.items():
        form, owner, lock_state = cell.split("|")
        effective = owner if form == "readable" or lock_state == "present" else "unknown"
        should_preserve = effective != "dead"
        if form == "readable":
            expected_before = {"live": "active_peer_lease", "dead": "none", "unknown": "peer_lease_unreadable"}[owner]
        else:
            expected_before = "peer_lease_unreadable"
        expected_after = expected_before if should_preserve else "none"
        assert row["lease_exists"] is should_preserve
        assert row["before"] == expected_before
        assert row["after"] == expected_after
        if effective == "unknown" and lock_state == "absent":
            assert row["lock_exists"] is True
            assert any("SELF_HEAL_MANUAL_RECOVERY_REQUIRED" in line for line in row["logs"])
        if effective == "dead":
            assert row["lock_exists"] is False
            assert any("liveness=dead action=remove" in line for line in row["logs"])

    unknown_default = '$liveness = if ($leaseReadable) { Get-LeaseProcessState -Lease $lease } else { "unknown" }'
    dead_default = '$liveness = if ($leaseReadable) { Get-LeaseProcessState -Lease $lease } else { "dead" }'
    lock_liveness_promotion = '                if ($lockLiveness -ne "unknown") { $liveness = $lockLiveness }'
    dead_evidence_ignored = '                if ($false) { $liveness = $lockLiveness }'
    unknown_guard = '        if ($leaseLiveness -ceq "unknown") { return "peer_lease_unreadable" }'
    open_unknown_guard = '        if ($false) { return "peer_lease_unreadable" }'
    marker_guard = '        if (-not (Test-Path -LiteralPath $LockPath)) {'
    no_marker_guard = '        if ($false) {'
    for original in (unknown_default, lock_liveness_promotion, unknown_guard, marker_guard):
        assert source.count(original) == 1

    unknown_absent = "unreadable|dead|absent"
    dead_with_lock = "unreadable|dead|present"
    identityless_unknown = "identityless|unknown|present"
    with make_tempdir("lease-state-collapse-unknown-") as tmp:
        path = Path(tmp) / "peer_mailbox_cron.ps1"
        path.write_text(source.replace(unknown_default, dead_default, 1), encoding="utf-8", newline="\n")
        collapsed_unknown = lease_owner_lock_state_table_probe(path, {unknown_absent})
    with make_tempdir("lease-state-ignore-lock-") as tmp:
        path = Path(tmp) / "peer_mailbox_cron.ps1"
        path.write_text(source.replace(lock_liveness_promotion, dead_evidence_ignored, 1), encoding="utf-8", newline="\n")
        ignored_lock = lease_owner_lock_state_table_probe(path, {dead_with_lock})
    with make_tempdir("lease-state-open-guard-") as tmp:
        path = Path(tmp) / "peer_mailbox_cron.ps1"
        path.write_text(source.replace(unknown_guard, open_unknown_guard, 1), encoding="utf-8", newline="\n")
        open_guard = lease_owner_lock_state_table_probe(path, {identityless_unknown})
    with make_tempdir("lease-state-no-marker-") as tmp:
        path = Path(tmp) / "peer_mailbox_cron.ps1"
        path.write_text(source.replace(marker_guard, no_marker_guard, 1), encoding="utf-8", newline="\n")
        no_marker = lease_owner_lock_state_table_probe(path, {unknown_absent})
    start = source.index("function Get-LeaseProcessState")
    end = source.index("function Test-LeaseProcessMatches", start)
    process_body = source[start:end]
    get_process_catch = '''    } catch {
        return "unknown"
    }
    try {
        $started = $process.StartTime'''
    get_process_dead = '''    } catch {
        return "dead"
        return "unknown"
    }
    try {
        $started = $process.StartTime'''
    start_time_catch = '''    } catch {
        return "unknown"
    }
}'''
    start_time_dead = '''    } catch {
        return "dead"
        return "unknown"
    }
}'''
    start_compare = '''    try {
        $started = $process.StartTime.ToUniversalTime().ToString("o")'''
    pid_reuse_blind = '''    try {
        if ($true) { return "live" }
        $started = $process.StartTime.ToUniversalTime().ToString("o")'''
    for branch in (get_process_catch, start_time_catch, start_compare):
        assert process_body.count(branch) == 1

    process_mutants = {
        "get_process": process_body.replace(get_process_catch, get_process_dead, 1),
        "start_time": process_body.replace(start_time_catch, start_time_dead, 1),
        "pid_reuse": process_body.replace(start_compare, pid_reuse_blind, 1),
    }
    process_results = {}
    for name, mutant_body in process_mutants.items():
        with make_tempdir(f"lease-state-process-{name}-") as tmp:
            path = Path(tmp) / "peer_mailbox_cron.ps1"
            path.write_text(source[:start] + mutant_body + source[end:], encoding="utf-8", newline="\n")
            process_results[name] = lease_process_state_probe(path)

    assert collapsed_unknown[unknown_absent]["lease_exists"] is False
    assert ignored_lock[dead_with_lock]["lease_exists"] is True
    assert open_guard[identityless_unknown]["before"] == "none"
    assert no_marker[unknown_absent]["lock_exists"] is False
    get_process_mutant = process_results["get_process"]
    start_time_mutant = process_results["start_time"]
    pid_reuse_mutant = process_results["pid_reuse"]
    assert get_process_mutant["get_process_error"] == "dead"
    assert start_time_mutant["start_time_error"] == "dead"
    assert pid_reuse_mutant["pid_reused"] == "live"


def test_admission_liveness_path_uses_production_functions_and_kills_constant_mutants() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-ADMISSION-LIVENESS-PRODUCTION-PATH"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    expected = {
        "dead_state": "dead",
        "dead_matches": False,
        "dead_signal": "none",
        "live_state": "live",
        "live_matches": True,
        "live_signal": "active_peer_lease",
        "reused_state": "dead",
        "reused_matches": False,
        "reused_signal": "none",
    }
    healthy = admission_liveness_path_probe(HARNESS_PATH)
    assert healthy == expected

    constant_mutants = {
        "Get-LeaseProcessState": '"live"',
        "Test-LeaseProcessMatches": "$true",
        "Get-AdditionalWorkSignal": '"none"',
    }
    results = {}
    for function_name, constant_return in constant_mutants.items():
        mutant_source = inject_function_return(source, function_name, constant_return)
        with make_tempdir(f"liveness-constant-{function_name.lower()}-") as tmp:
            mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
            mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
            results[function_name] = admission_liveness_path_probe(mutant_path)

    for mutant in results.values():
        assert mutant != expected
    for function_name in ("Get-LeaseProcessState", "Test-LeaseProcessMatches"):
        mutant = results[function_name]
        assert mutant["dead_signal"] == "active_peer_lease"
    mutant = results["Get-AdditionalWorkSignal"]
    assert mutant["live_signal"] == "none"


def test_archived_task_work_resolution_kills_hot_only_mutant() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-ARCHIVED-TASK-WORK-RESOLUTION"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    archive_index = '"Area_comun\\state\\TASK_INDEX_ARCHIVE.json"'
    hot_index = '"Area_comun\\state\\TASK_INDEX.json"'
    assert source.count(archive_index) == 1
    mutant_source = source.replace(archive_index, hot_index, 1)
    with make_tempdir("archived-task-hot-only-mutant-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = archived_task_descriptor_probe(mutant_path)
    healthy = archived_task_descriptor_probe(HARNESS_PATH)
    assert healthy is not None
    assert healthy["task_id"] == "TASK-1001"
    assert "src/target" in healthy["work_scope"]
    assert mutant is None


def test_glob_claim_scope_fails_closed_and_kills_guard_mutant() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-GLOB-SCOPE-FAILS-CLOSED"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    glob_guard = "if ($normalized -match '[*?\\[\\]]') { return $null }"
    dead_glob_guard = "if ($false) { return $null }"
    assert source.count(glob_guard) == 1
    mutant_source = source.replace(glob_guard, dead_glob_guard, 1)
    with make_tempdir("glob-scope-mutant-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = glob_claim_probe(mutant_path)
    healthy = glob_claim_probe(HARNESS_PATH)
    assert healthy == ["active_external_claim", "active_external_claim"]
    assert mutant == ["none", "none"]


def test_dirty_tree_veto_still_precedes_scope_admission() -> None:
    """PERMANENT_NEGATIVE: NEG-HARNESS-DIRTY-VETO-PRECEDES-SCOPE-ADMISSION"""
    source = HARNESS_PATH.read_text(encoding="utf-8")
    live_residue_guard = 'if ($residueState -eq "live") {'
    dead_wiring = '$residueState = "clean"\n    '
    assert source.count(live_residue_guard) == 1
    mutant_source = source.replace(live_residue_guard, dead_wiring + live_residue_guard, 1)
    with make_tempdir("dirty-veto-dead-wiring-") as tmp:
        mutant_path = Path(tmp) / "peer_mailbox_cron.ps1"
        mutant_path.write_text(mutant_source, encoding="utf-8", newline="\n")
        mutant = dirty_veto_probe(mutant_path)
    healthy = dirty_veto_probe(HARNESS_PATH)
    assert healthy["admission_calls"] == 0
    assert healthy["defer_reasons"] == ["worktree_residue_live"]
    assert mutant["admission_calls"] == 1


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
        test_post_delivery_window_honors_main_progress_extensions,
        test_silent_process_tree_cpu_is_work_derived_and_mutation_proven,
        test_process_tree_cpu_sample_distinguishes_recycled_pid,
        test_retry_exhaustion_alert_and_stalled_task_threshold_kill_mutant,
        test_preexec_defer_budget_kills_shared_counter_mutant,
        test_worktree_disk_proof_pairs_real_git_rename_records,
        test_zombie_sweeper_parses_real_git_quoted_rename_paths,
        test_git_status_readers_enumerate_untracked_files_without_overbroad_veto,
        test_embedded_repository_dirty_claim_is_fail_closed_and_mutation_proven,
        test_parent_ignore_boundary_separates_claim_veto_from_blocking_readers,
        test_residue_excludes_foreign_personal_and_caps_diagnostics,
        test_active_peer_lease_reports_owner_and_claim_veto_survives,
        test_scope_aware_claim_veto_kills_both_direction_mutants,
        test_scope_aware_lease_veto_kills_both_direction_mutants,
        test_atomic_exec_admission_kills_peer_specific_lock_mutant,
        test_orphan_lease_self_heal_matrix_requires_dead_owner_evidence,
        test_live_unreadable_lease_is_preserved_and_deadline_mutant_dies,
        test_lease_owner_lock_state_table_is_complete_and_mutation_proven,
        test_admission_liveness_path_uses_production_functions_and_kills_constant_mutants,
        test_archived_task_work_resolution_kills_hot_only_mutant,
        test_glob_claim_scope_fails_closed_and_kills_guard_mutant,
        test_dirty_tree_veto_still_precedes_scope_admission,
        test_new_instance_exports_identical_harness,
    ]
    failures: list[tuple[str, str]] = []
    for test in tests:
        try:
            test()
        except Exception:
            failures.append((test.__name__, traceback.format_exc()))
            print(f"FAIL {test.__name__}")
        else:
            print(f"PASS {test.__name__}")
    print(f"SUMMARY total={len(tests)} passed={len(tests) - len(failures)} failed={len(failures)}")
    for name, failure in failures:
        print(f"\n--- FAILURE {name} ---\n{failure}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
