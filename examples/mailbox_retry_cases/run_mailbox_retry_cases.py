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

FALSIFICATION_CONTRACTS = (
    {
        "id": "retry-destructive-reset",
        "negative": "rollback rejects destructive reset",
        "mutation": '"destructive_reset": body + "\\n# reset --hard"',
        "boundaries": ("assert contract(body)", "assert not survivors"),
        "exercised_by": "run_nondestructive_rollback_contract",
    },
    {
        "id": "retry-worktree-reapply",
        "negative": "rollback does not reapply a captured worktree patch",
        "mutation": '"worktree_reapply": body + "\\n# WorktreePatch"',
        "boundaries": ("assert contract(body)", "assert not survivors"),
        "exercised_by": "run_nondestructive_rollback_contract",
    },
    {
        "id": "retry-mailbox-allowlist",
        "negative": "rollback preserves ledger-managed mailbox paths",
        "mutation": 'body.replace("if (Test-LedgerManagedPath -Path $path) { continue }", "")',
        "boundaries": ("assert contract(body)", "assert not survivors"),
        "exercised_by": "run_nondestructive_rollback_contract",
    },
    {
        "id": "retry-index-exit-gate",
        "negative": "rollback defers after an index restore failure",
        "mutation": 'reason=index_restore_failed\"; return }\', "")',
        "boundaries": ("assert contract(body)", "assert not survivors"),
        "exercised_by": "run_nondestructive_rollback_contract",
    },
    {
        "id": "retry-untracked-exit-gate",
        "negative": "rollback defers after untracked enumeration failure",
        "mutation": 'reason=untracked_enumeration_failed\"; return }\', "")',
        "boundaries": ("assert contract(body)", "assert not survivors"),
        "exercised_by": "run_nondestructive_rollback_contract",
    },
    {
        "id": "retry-quarantine-success-log",
        "negative": "an aborted exec preserves untracked residue and logs both recovery paths",
        "mutation": "body.replace('Write-Log \"ROLLBACK_QUARANTINED path=$path quarantine_path=$quarantineRelative\"', \"\", 1)",
        "boundaries": ('"ROLLBACK_QUARANTINED path=$path quarantine_path=$quarantineRelative" in text', "assert not survivors"),
        "exercised_by": "run_nondestructive_rollback_contract",
    },
    {
        "id": "retry-terminal-defer",
        "negative": "an exhausted defer is terminal",
        "mutation": 'text.replace("exhausted = $terminal", "exhausted = $false", 1)',
        "boundaries": ("assert contract(text)", "assert not survivors"),
        "exercised_by": "run_pregate_contract_mutants",
    },
    {
        "id": "retry-dirty-forensics",
        "negative": "dirty-tree forensics runs before lock acquisition",
        "mutation": 'text.replace("$residueState = Get-StagedResidueState", "# dirty-tree veto removed", 1)',
        "boundaries": ("assert contract(text)", "assert not survivors"),
        "exercised_by": "run_pregate_contract_mutants",
    },
    {
        "id": "retry-large-stderr-drain",
        "negative": "concurrent pipe drain terminates while the sequential mutant deadlocks",
        "mutation": "$stdout = $process.StandardOutput.ReadToEnd()",
        "boundaries": ("assert not (fixture / \"drain-test.lock\").exists()", "raise AssertionError(\"sequential pipe-drain control did not hang"),
        "exercised_by": "run_large_stderr_drain_case",
    },
    {
        "id": "retry-deleted-first-seen",
        "negative": "a deleted residue ages out of defer in the real loop",
        "mutation": 'runner_text.replace("$firstSeen.ContainsKey($relative)", "$false", 1)',
        "boundaries": ("exercise(runner_text, expect_exec=True)", "exercise(mutant, expect_exec=False)"),
        "exercised_by": "run_deleted_residue_real_loop_case",
    },
    {
        "id": "retry-pure-append-evidence",
        "negative": "growth without a byte-identical prefix cannot prove own work",
        "mutation": "$mutantRewriteGrow=((Get-Item -LiteralPath $path).Length -gt $before)",
        "boundaries": ("assert result == {\"append\": True", "\"mutant_rewrite_grow\": True"),
        "exercised_by": "run_pure_append_evidence_cases",
    },
    {
        "id": "retry-useful-own-evidence",
        "negative": "pure claims, including claims carrying commit metadata, do not confirm",
        "mutation": "commit_proxy_mutant = body.replace(",
        "boundaries": ('assert mutant_result["claim_with_commit"] is True', 'assert mutant_result["task_status"] is True'),
        "exercised_by": "run_useful_own_evidence_cases",
    },
    {
        "id": "retry-preexec-untracked-exit-gate",
        "negative": "pre-exec untracked enumeration failure defers launch",
        "mutation": "text.replace('if ($LASTEXITCODE -ne 0) { Register-PreExecDefer -Message $Message -Reason \"untracked_snapshot_failed\"; return }', \"\", 1)",
        "boundaries": ('\'Reason "untracked_snapshot_failed"\' in candidate', 'assert not survivors'),
        "exercised_by": "run_git_gate_contract_mutants",
    },
    {
        "id": "retry-apply-fail-visible",
        "negative": "failed index reapply emits APPLY_FAIL",
        "mutation": "apply_body.replace('Write-Log \"APPLY_FAIL index=$Index patch=$PatchPath exit=$LASTEXITCODE\"', \"\", 1)",
        "boundaries": ('\'Write-Log "APPLY_FAIL index=$Index patch=$PatchPath exit=$LASTEXITCODE"\' in candidate_apply', 'assert not survivors'),
        "exercised_by": "run_git_gate_contract_mutants",
    },
    {
        "id": "retry-expired-claim",
        "negative": "an expired external claim does not defer launch while a live claim does",
        "mutation": 'current.replace("$expires -le $now", "$expires -gt $now", 1)',
        "boundaries": (
            'assert_claim_behavior(current, label="current")',
            'assert_claim_behavior(old_form, label="old-form")',
            'assert probe(mutant, expired) == "active_external_claim"',
            'assert probe(mutant, live) == "none"',
        ),
        "exercised_by": "run_expired_claim_behavior_case",
    },
    {
        "id": "retry-utf8-residue-path",
        "negative": "a stale UTF-8 residue ages while a console-codepage mutant does not",
        "mutation": "[Text.Encoding]::GetEncoding(850)",
        "boundaries": ('assert output == "aborted"', 'assert mutant_output == "live"'),
        "exercised_by": "run_nul_residue_path_cases",
    },
    {
        "id": "retry-ledger-head-defer-order",
        "negative": "an unreadable ledger head keeps one stable defer cause until terminal",
        "mutation": "runner_text.replace(good_order, bad_order, 1)",
        "boundaries": (
            "assert terminal is expect_any_terminal, log",
            "assert expected_terminal is expect_expected_terminal, log",
            '"ledger_unreadable_wrong_cause"',
            "expect_any_terminal=False",
            "expect_any_terminal=True",
        ),
        "exercised_by": "run_unreadable_head_case",
    },
    {
        "id": "retry-ledger-preservation-property",
        "negative": "rollback verification rejects event or claim loss and accepts any conservative defer reason",
        "mutation": '"claims_ignored": lambda before, after, before_claims, after_claims:',
        "boundaries": (
            "assert all(actual == expected for _, actual, expected in property_results)",
            "assert all(actual == expected for _, actual, expected in defer_results)",
            "assert not survivors",
        ),
        "exercised_by": "run_rollback_ledger_preservation_property",
    },
)
RUNNER = ROOT / "scripts" / "harness" / "peer_mailbox_cron.ps1"
LEDGER_HEAD = ROOT / "scripts" / "ledger_head.py"


def ledger_preservation_holds(
    before_events: list[dict[str, object]],
    after_events: list[dict[str, object]],
    before_claims: dict[str, object],
    after_claims: dict[str, object],
) -> bool:
    """Compare the governed ledger state itself, independent of rollback logging."""
    return bool(before_events) and after_events == before_events and after_claims == before_claims


def conservative_rollback_defer_observed(log: str) -> bool:
    """Recognize the defer effect without coupling the contract to a reason name."""
    return any(
        re.search(r"(?:^|\s)ROLLBACK_DEFER reason=[A-Za-z0-9_]+(?:\s|$)", line)
        for line in log.splitlines()
    )


def run_rollback_ledger_preservation_property() -> None:
    """Event or claim loss fails; any conservative defer reason still passes.
    PERMANENT_NEGATIVE: retry-ledger-preservation-property
    """
    before = [{"seq": 41, "payload": {"intent_type": "claim"}}]
    claims = {"seq": 41, "claims": []}
    changed_claims = {"seq": 41, "claims": [{"claim_id": "lost-by-rollback"}]}
    cases = (
        ("events_lost", before, [], claims, claims, False),
        ("claims_changed", before, list(before), claims, changed_claims, False),
        ("empty_prestate", [], [], claims, claims, False),
        ("preserved", before, list(before), claims, dict(claims), True),
    )
    property_results = [
        (label, ledger_preservation_holds(before_events, after_events, before_claims, after_claims), expected)
        for label, before_events, after_events, before_claims, after_claims, expected in cases
    ]
    assert all(actual == expected for _, actual, expected in property_results), property_results
    defer_cases = (
        ("current_reason", "ROLLBACK_DEFER reason=ledger_unreadable_after_exec", True),
        ("renamed_reason", "ROLLBACK_DEFER reason=ledger_head_unreadable_after_exec", True),
        ("reason_with_context", "ts ROLLBACK_DEFER reason=quarantine_move_failed path=residue.txt", True),
        ("preserved_record", "ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=3 proof=disk", False),
        ("missing_defer", "ROLLBACK_QUARANTINED path=residue.txt", False),
    )
    defer_results = [
        (label, conservative_rollback_defer_observed(log), expected)
        for label, log, expected in defer_cases
    ]
    assert all(actual == expected for _, actual, expected in defer_results), defer_results
    mutants = {
        "accept_loss": lambda before, after, before_claims, after_claims: True,
        "claims_ignored": lambda before, after, before_claims, after_claims:
            bool(before) and after == before,
        "empty_accepted": lambda before, after, before_claims, after_claims:
            after == before and after_claims == before_claims,
    }
    survivors = [
        name
        for name, mutant in mutants.items()
        if all(
            mutant(before_events, after_events, before_claims, after_claims) == expected
            for _, before_events, after_events, before_claims, after_claims, expected in cases
        )
    ]
    literal_reason_survives = all(
        ("ROLLBACK_DEFER reason=ledger_unreadable_after_exec" in log) == expected
        for _, log, expected in defer_cases
    )
    if literal_reason_survives:
        survivors.append("literal_reason")
    assert not survivors, f"rollback preservation mutants survived: {survivors}"


def extract_powershell_function_closure(
    source: str, roots: tuple[str, ...], *, provided: tuple[str, ...] = ()
) -> str:
    """Extract probe roots together with every harness-function dependency."""
    definitions = {
        match.group(1): match.group(0)
        for match in re.finditer(r"(?ms)^function ([A-Za-z0-9_-]+) \{.*?^\}", source)
    }
    missing = [name for name in roots if name not in definitions]
    if missing:
        raise AssertionError(f"PowerShell probe functions not found: {missing}")
    supplied = set(provided)
    ordered: list[str] = []
    visiting: set[str] = set()
    emitted: set[str] = set()

    def visit(name: str) -> None:
        if name in supplied or name in emitted:
            return
        if name in visiting:
            raise AssertionError(f"PowerShell probe dependency cycle at {name}")
        visiting.add(name)
        body = definitions[name]
        for candidate in definitions:
            if candidate == name or candidate in supplied:
                continue
            if re.search(r"(?<![-\w])" + re.escape(candidate) + r"(?![-\w])", body):
                visit(candidate)
        visiting.remove(name)
        emitted.add(name)
        ordered.append(body)

    for root in roots:
        visit(root)
    return "\n\n".join(ordered)


def run_outcome_parser_cases(sandbox: Path) -> None:
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    function_text = extract_powershell_function_closure(runner_text, ("Get-ExecOutcomeClass",))
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
    probe.unlink()


def run_torn_tail_case(sandbox: Path) -> None:
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    rollback_helpers = extract_powershell_function_closure(
        runner_text, ("Restore-TransientExecResidue",), provided=("Write-Log",)
    )
    events = sandbox / "runtime/state/events.jsonl"
    events.write_bytes(b'{"seq":1}\n{"seq":')
    probe = sandbox / "torn-tail-probe.ps1"
    probe.write_text(
        "$Root=(Get-Location).Path\n$RunsDir=$Root\n$log=@()\n"
        "function Write-Log { param([string]$Message) $script:log += $Message }\n"
        + rollback_helpers + "\n"
        "$before=[pscustomobject]@{readable=$true;seq=1;hash='before';torn_tail=$false}\n"
        "$head=git rev-parse HEAD\n"
        "Restore-TransientExecResidue -HeadBefore $head -IndexPatch '' -UntrackedBefore @() -LedgerHeadBefore $before\n"
        "$log | ConvertTo-Json -Compress\n",
        encoding="ascii",
    )
    output = run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(probe), cwd=sandbox).stdout
    assert "ROLLBACK_DEFER reason=ledger_torn_tail" in output, output
    assert events.read_bytes().endswith(b'{"seq":'), "torn-tail deferral mutated the queue"
    probe.unlink()


def run_nondestructive_rollback_contract() -> None:
    """Kill declared rollback-policy mutants before exercising the real loop.
    PERMANENT_NEGATIVE: retry-destructive-reset, retry-worktree-reapply, retry-mailbox-allowlist, retry-index-exit-gate, retry-untracked-exit-gate, retry-quarantine-success-log
    """
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    restore = re.search(r"(?ms)^function Restore-TransientExecResidue \{.*?^\}", runner_text)
    if not restore:
        raise AssertionError("Restore-TransientExecResidue function not found")
    body = restore.group(0)

    def contract(text: str) -> bool:
        index_reset = text.find("read-tree $HeadBefore")
        index_apply = text.find("Invoke-PreExecPatch -PatchPath $IndexPatch -Index $true")
        enumeration = text.find("ls-files --others --exclude-standard -z")
        first_move = text.find("Move-Item -LiteralPath")
        return all(
            (
                "reset --hard" not in text,
                "WorktreePatch" not in text,
                index_reset >= 0,
                index_apply > index_reset,
                "reason=index_restore_failed" in text,
                enumeration > index_apply,
                "reason=untracked_enumeration_failed" in text,
                first_move > enumeration,
                "Test-LedgerManagedPath -Path $path" in text,
                ".protocol-tmp\\rollback-quarantine" in text,
                "Move-Item -LiteralPath $full -Destination $destination -ErrorAction Stop" in text,
                "ROLLBACK_QUARANTINED path=$path quarantine_path=$quarantineRelative" in text,
                "reason=quarantine_move_failed" in text,
            )
        )

    assert contract(body), "non-destructive rollback contract is incomplete"
    mutants = {
        "destructive_reset": body + "\n# reset --hard",
        "worktree_reapply": body + "\n# WorktreePatch",
        "mailbox_allowlist_removed": body.replace("if (Test-LedgerManagedPath -Path $path) { continue }", ""),
        "index_exit_gate_removed": body.replace('if ($LASTEXITCODE -ne 0) { Write-Log "ROLLBACK_DEFER reason=index_restore_failed"; return }', ""),
        "untracked_exit_gate_removed": body.replace('if ($LASTEXITCODE -ne 0) { Write-Log "ROLLBACK_DEFER reason=untracked_enumeration_failed"; return }', ""),
        "quarantine_success_log_removed": body.replace('Write-Log "ROLLBACK_QUARANTINED path=$path quarantine_path=$quarantineRelative"', "", 1),
    }
    survivors = [name for name, mutant in mutants.items() if contract(mutant)]
    assert not survivors, f"rollback contract failed to kill declared mutants: {survivors}"


def run_pregate_contract_mutants() -> None:
    """Kill the declared TASK-0284 pre-gate regressions at their control points.
    PERMANENT_NEGATIVE: retry-terminal-defer, retry-dirty-forensics
    """
    text = RUNNER.read_text(encoding="utf-8-sig")

    def function_bodies(candidate: str) -> dict[str, str]:
        starts = list(re.finditer(r"(?m)^function\s+([A-Za-z0-9_-]+)\s*\{", candidate))
        return {
            match.group(1): candidate[match.start() : (starts[index + 1].start() if index + 1 < len(starts) else len(candidate))]
            for index, match in enumerate(starts)
        }

    def resolved_exec_lock_write(candidate: str) -> tuple[int, int]:
        bodies = function_bodies(candidate)
        invoke = bodies.get("Invoke-PeerForMessage", "")
        prelock = invoke.find("$residueState = Get-StagedResidueState")
        evidence_writers = {
            name
            for name, body in bodies.items()
            if "$LockPath" in body and "$MessageName" in body and "process_start_time_utc" in body
        }
        call_offsets = [
            match.start()
            for name in evidence_writers
            for match in re.finditer(rf"(?m)^\s*{re.escape(name)}\b", invoke)
        ]
        return prelock, min(call_offsets, default=-1)

    def contract(candidate: str) -> bool:
        prelock, lock_write = resolved_exec_lock_write(candidate)
        return all(
            (
                candidate.count("ReadToEndAsync()") >= 2,
                "WaitForExit(10000)" in candidate,
                "Task]::WaitAll" in candidate,
                "$ResiduePath" in candidate,
                "$firstSeen.ContainsKey($relative)" in candidate,
                "outcome=defer_terminal" in candidate,
                "exhausted = $terminal" in candidate,
                "Read-JsonWithDeadline" in candidate,
                prelock >= 0 and lock_write > prelock,
            )
        )

    assert contract(text), "TASK-0284 pre-gate contract is incomplete"
    bodies = function_bodies(text)
    invoke = bodies["Invoke-PeerForMessage"]
    evidence_writer = next(
        name
        for name, body in bodies.items()
        if "$LockPath" in body and "$MessageName" in body and "process_start_time_utc" in body
    )
    writer_call = re.search(rf"(?m)^(\s*{re.escape(evidence_writer)}\b[^\r\n]*\r?\n)", invoke)
    residue_line = re.search(r"(?m)^\s*\$residueState = Get-StagedResidueState\s*$", invoke)
    assert writer_call is not None and residue_line is not None
    moved_invoke = invoke[: writer_call.start()] + invoke[writer_call.end() :]
    moved_residue = moved_invoke.find(residue_line.group(0))
    assert moved_residue >= 0
    moved_invoke = moved_invoke[:moved_residue] + writer_call.group(1) + moved_invoke[moved_residue:]
    mutants = {
        "terminal_defer_removed": text.replace("exhausted = $terminal", "exhausted = $false", 1),
        "dirty_forensics_removed": text.replace("$residueState = Get-StagedResidueState", "# dirty-tree veto removed", 1),
        "exec_lock_write_moved_before_residue_probe": text.replace(invoke, moved_invoke, 1),
    }
    survivors = [name for name, mutant in mutants.items() if contract(mutant)]
    assert not survivors, f"pre-gate contract failed to kill declared mutants: {survivors}"


def run_deleted_residue_real_loop_case() -> None:
    """A real deleted path ages into EXEC_START; removing first-seen persistence blocks it.
    PERMANENT_NEGATIVE: retry-deleted-first-seen
    """
    runner_text = RUNNER.read_text(encoding="utf-8-sig")

    def exercise(candidate: str, expect_exec: bool, *, declare_scope: bool = True) -> None:
        fixture = Path(tempfile.mkdtemp(prefix="task0284-deleted-loop-"))
        try:
            (fixture / "Area_comun/mailbox/open").mkdir(parents=True)
            (fixture / "Area_comun/state").mkdir(parents=True)
            (fixture / "runtime/state").mkdir(parents=True)
            (fixture / "scripts/harness/prompts").mkdir(parents=True)
            (fixture / "scripts/harness/peer_mailbox_cron.ps1").write_text(candidate, encoding="utf-8")
            shutil.copy2(LEDGER_HEAD, fixture / "scripts/ledger_head.py")
            (fixture / "runtime/protocol_replay.py").write_text(
                "def protocol_state_drift(root): return {'has_drift': False}\n", encoding="ascii"
            )
            (fixture / "runtime/state/events.jsonl").write_text("", encoding="ascii")
            (fixture / "Area_comun/state/CLAIMS.json").write_text('{"claims":[]}\n', encoding="ascii")
            (fixture / "protocol.config.json").write_text("{}\n", encoding="ascii")
            (fixture / ".gitignore").write_text(".protocol-tmp/\n", encoding="ascii")
            tracked = fixture / "deleted-residue.txt"
            tracked.write_text("tracked\n", encoding="ascii")
            message = fixture / "Area_comun/mailbox/open/MSG-delete.md"
            message.write_text(
                "---\nfrom: Arquitecto\nto: TestPeer\ntype: ACTION\ntask_id: TASK-0001\nstatus: open\n"
                "requires_response: true\nresponse_owner: TestPeer\nrequested_action: test\n---\n",
                encoding="ascii",
            )
            task_file = fixture / "Area_comun/tasks/TASK-0001-deleted-residue.md"
            task_file.parent.mkdir(parents=True)
            task_file.write_text(
                "---\ntask_id: TASK-0001\nfile: Area_comun/tasks/TASK-0001-deleted-residue.md\n"
                + ("intake:\n  scope_routes:\n    - unrelated-scope.txt\n" if declare_scope else "")
                + "---\n",
                encoding="ascii",
            )
            (fixture / "Area_comun/state/TASK_INDEX.json").write_text(
                '{"tasks":[{"id":"TASK-0001","file":"Area_comun/tasks/TASK-0001-deleted-residue.md"}]}\n',
                encoding="ascii",
            )
            (fixture / "Area_comun/state/TASK_INDEX_ARCHIVE.json").write_text(
                '{"tasks":[]}\n', encoding="ascii"
            )
            prompt = fixture / "scripts/harness/prompts/test.prompt.md"
            prompt.write_text("Process @@MESSAGE_PATH@@ under @@ROOT@@.\n", encoding="ascii")
            fake = fixture / "fake-agent.cmd"
            fake.write_text("@echo OUTCOME: definitive\r\n", encoding="ascii")
            run("git", "init", cwd=fixture)
            run("git", "config", "user.email", "retry@example.invalid", cwd=fixture)
            run("git", "config", "user.name", "TestPeer", cwd=fixture)
            run("git", "add", ".", cwd=fixture)
            run("git", "commit", "-m", "fixture", cwd=fixture)
            tracked.unlink()
            command = [
                "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                str(fixture / "scripts/harness/peer_mailbox_cron.ps1"),
                "-PeerId", "TestPeer", "-CoordinatorId", "Coordinator", "-Root", str(fixture), "-PromptFile", str(prompt),
                "-AgentExe", str(fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
                "-MaxNoCoordinatorRounds", "5", "-ExecTimeoutSeconds", "10",
                "-MaxTransientRetries", "2", "-PreExecDeferTimeoutSeconds", "1",
                "-RetryBackoffSeconds", "0", "-AbortedResidueMinutes", "0",
            ]
            run(*command, cwd=fixture, timeout=20)
            log = (fixture / ".protocol-tmp/testpeer_mailbox_cron/testpeer_mailbox_cron.log").read_text(encoding="utf-8")
            assert ("EXEC_START " in log) is expect_exec, log
            if not expect_exec:
                expected_reason = "worktree_residue_live" if declare_scope else "message_scope_ambiguous"
                assert f"outcome=defer_terminal reason={expected_reason}" in log, log
        finally:
            shutil.rmtree(fixture, ignore_errors=True)

    exercise(runner_text, expect_exec=True)
    mutant = runner_text.replace("$firstSeen.ContainsKey($relative)", "$false", 1)
    assert mutant != runner_text, "first-seen mutant was not applied"
    exercise(mutant, expect_exec=False)
    exercise(runner_text, expect_exec=False, declare_scope=False)


def run_large_stderr_drain_case(sandbox: Path) -> None:
    """>64 KB stderr drains under the deadline; the sequential mutant deadlocks and leaves its lock.
    PERMANENT_NEGATIVE: retry-large-stderr-drain
    """
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    git_helper = extract_powershell_function_closure(runner_text, ("Get-GitStatusPorcelainUtf8",))
    fixture = Path(tempfile.mkdtemp(prefix="task0284-stderr-"))
    try:
        fake_git = fixture / "git.exe"
        source = fixture / "fake-git.cs"
        source.write_text(
            "using System; class FakeGit { static void Main() { Console.Error.Write(new string('E', 131072)); } }\n",
            encoding="ascii",
        )
        run(
            r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
            "/nologo", "/out:" + str(fake_git), str(source), cwd=fixture,
        )

        def make_probe(name: str, helper: str) -> Path:
            probe = fixture / name
            probe.write_text(
                "$Root=(Get-Location).Path\n"
                "$env:PATH='" + str(fixture).replace("'", "''") + ";'+$env:PATH\n"
                "$lock=Join-Path $Root 'drain-test.lock'\n"
                "Set-Content -LiteralPath $lock -Value locked -Encoding ASCII\n"
                "try {\n" + helper + "\n$result=Get-GitStatusPorcelainUtf8\n"
                "if(-not $result.ok){throw 'git helper failed'}\n"
                "} finally { Remove-Item -LiteralPath $lock -Force -ErrorAction SilentlyContinue }\n",
                encoding="ascii",
            )
            return probe

        good = make_probe("concurrent.ps1", git_helper)
        run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(good), cwd=fixture, timeout=15)
        assert not (fixture / "drain-test.lock").exists(), "concurrent drain left an orphan lock"
        sequential_text = git_helper.replace(
            "$stdoutTask = $process.StandardOutput.ReadToEndAsync()\n        $stderrTask = $process.StandardError.ReadToEndAsync()",
            "$stdout = $process.StandardOutput.ReadToEnd()\n        $stderr = $process.StandardError.ReadToEnd()",
            1,
        ).replace("$raw = $stdoutTask.Result", "$raw = $stdout", 1)
        sequential = make_probe("sequential.ps1", sequential_text)
        try:
            run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(sequential), cwd=fixture, timeout=3)
        except subprocess.TimeoutExpired:
            pass
        else:
            raise AssertionError("sequential pipe-drain control did not hang on >64 KB stderr")
        assert (fixture / "drain-test.lock").exists(), "sequential hang did not demonstrate orphan-lock risk"
    finally:
        shutil.rmtree(fixture, ignore_errors=True)


def run_expired_claim_behavior_case(sandbox: Path) -> None:
    """Expired claims are inactive and live claims are active across equivalent predicates.
    PERMANENT_NEGATIVE: retry-expired-claim
    """
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    signal = extract_powershell_function_closure(
        runner_text, ("Get-AdditionalWorkSignal",), provided=("Test-LeaseProcessMatches",)
    )
    claims = sandbox / "Area_comun/state/CLAIMS.json"
    original_claims = claims.read_bytes()
    expired = "2000-01-01T00:00:00Z"
    live = "2999-01-01T00:00:00Z"

    def probe(helper: str, expires_at: str) -> str:
        claims.write_text(
            '{"claims":[{"owner":"Other","status":"active","expires_at":"'
            + expires_at
            + '"}]}\n',
            encoding="ascii",
        )
        path = sandbox / "claim-expiry-probe.ps1"
        path.write_text(
            "$Root=(Get-Location).Path\n$PeerId='TestPeer'\n$LeasePath=''\n"
            "function Test-LeaseProcessMatches { param($Lease) return $false }\n"
            + helper + "\nGet-AdditionalWorkSignal\n",
            encoding="ascii",
        )
        return run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(path), cwd=sandbox).stdout.strip()

    current = signal
    current_predicate = "if ($expires -le $now) { continue }"
    old_predicate = "if (-not ($expires -gt $now)) { continue }"
    assert current_predicate in current, "current expiry predicate not found"

    def assert_claim_behavior(helper: str, *, label: str) -> None:
        assert probe(helper, expired) == "none", f"{label}: expired claim counted as active"
        assert probe(helper, live) == "active_external_claim", f"{label}: live claim counted as inactive"

    assert_claim_behavior(current, label="current")
    old_form = current.replace(current_predicate, old_predicate, 1)
    assert_claim_behavior(old_form, label="old-form")
    mutant = current.replace("$expires -le $now", "$expires -gt $now", 1)
    assert mutant != current, "expiry predicate mutation did not apply"
    assert probe(mutant, expired) == "active_external_claim", "broken predicate accepted an expired claim"
    assert probe(mutant, live) == "none", "broken predicate rejected a live claim"
    (sandbox / "claim-expiry-probe.ps1").unlink(missing_ok=True)
    claims.write_bytes(original_claims)


def run_pure_append_evidence_cases(sandbox: Path) -> None:
    """Only a byte-identical prefix plus an appended own event may prove work.
    PERMANENT_NEGATIVE: retry-pure-append-evidence
    """
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    helpers = extract_powershell_function_closure(
        runner_text, ("Get-OwnEvidence",), provided=("Write-Log",)
    )
    events = sandbox / "runtime/state/events.jsonl"
    old = b'{"seq":1,"actor":"Other"}\n'
    own = b'{"seq":2,"actor":"TestPeer","applied":true,"actor_auth":{"method":"ed25519","keyid":"testpeer:v1","sig":"new"},"payload":{"intent_type":"task_status"}}\n'
    events.write_bytes(old)
    probe = sandbox / "pure-append-probe.ps1"
    probe.write_text(
        "$Root=(Get-Location).Path\n$PeerId='TestPeer'\nfunction Write-Log { param([string]$Message) }\n"
        + helpers
        + "\n$path=Join-Path $Root 'runtime/state/events.jsonl'\n"
        + "$before=(Get-Item -LiteralPath $path).Length\n$hash=Get-FilePrefixSha256 -Path $path -Length $before\n"
        + f"[IO.File]::AppendAllText($path, '{own.decode('ascii').strip()}'+[Environment]::NewLine, [Text.Encoding]::ASCII)\n"
        + "$append=Get-OwnEvidence -LedgerBytesBefore $before -LedgerPrefixSha256Before $hash\n"
        + f"[IO.File]::WriteAllText($path, '{own.decode('ascii').strip()}'+[Environment]::NewLine+'{own.decode('ascii').strip()}'+[Environment]::NewLine, [Text.Encoding]::ASCII)\n"
        + "$rewriteGrow=Get-OwnEvidence -LedgerBytesBefore $before -LedgerPrefixSha256Before $hash\n"
        + "$mutantRewriteGrow=((Get-Item -LiteralPath $path).Length -gt $before)\n"
        + "[IO.File]::WriteAllText($path, '{}'+[Environment]::NewLine, [Text.Encoding]::ASCII)\n"
        + "$rewriteShrink=Get-OwnEvidence -LedgerBytesBefore $before -LedgerPrefixSha256Before $hash\n"
        + "[pscustomobject]@{append=$append;rewrite_grow=$rewriteGrow;rewrite_shrink=$rewriteShrink;mutant_rewrite_grow=$mutantRewriteGrow}|ConvertTo-Json -Compress\n",
        encoding="ascii",
    )
    result = json.loads(run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(probe), cwd=sandbox).stdout)
    assert result == {"append": True, "rewrite_grow": False, "rewrite_shrink": False, "mutant_rewrite_grow": True}, result
    events.write_text("", encoding="ascii")
    probe.unlink()


def run_useful_own_evidence_cases(sandbox: Path) -> None:
    """Only applied, coherently signed useful work confirms an exec.
    PERMANENT_NEGATIVE: retry-useful-own-evidence
    """
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    helpers = extract_powershell_function_closure(
        runner_text, ("Get-OwnEvidence",), provided=("Write-Log",)
    )
    body = helpers

    def contract(candidate: str) -> bool:
        return all(
            (
                "$event.applied -ne $true" in candidate,
                ".StartsWith($expectedKeyPrefix, [StringComparison]::Ordinal)" in candidate,
                '$intentType -in @("task_status", "task_upsert", "decision")' in candidate,
                "if (-not $hasUsefulIntent) { continue }" in candidate,
                "$hasCommit" not in candidate,
            )
        )

    assert contract(body), "useful-own-evidence contract is incomplete"
    mutants = {
        "applied_gate_removed": body.replace("if ($event.applied -ne $true) { continue }", "", 1),
        "key_actor_gate_removed": body.replace(
            'if (-not ([string]$event.actor_auth.keyid).StartsWith($expectedKeyPrefix, [StringComparison]::Ordinal)) { continue }',
            "",
            1,
        ),
        "useful_work_gate_removed": body.replace("if (-not $hasUsefulIntent) { continue }", "", 1),
    }
    survivors = [name for name, mutant in mutants.items() if contract(mutant)]
    assert not survivors, f"useful-evidence contract failed to kill declared mutants: {survivors}"

    events = sandbox / "runtime/state/events.jsonl"
    probe = sandbox / "useful-evidence-probe.ps1"
    cases = {
        "pure_claim": ("claim", True, "testpeer:v1", "", False),
        "exception": ("exception.recorded", True, "testpeer:v1", "", False),
        "rejected_status": ("task_status", False, "testpeer:v1", "", False),
        "foreign_key": ("task_status", True, "other:v1", "", False),
        "task_status": ("task_status", True, "testpeer:v1", "", True),
        "task_upsert": ("task_upsert", True, "testpeer:v1", "", True),
        "decision": ("decision", True, "testpeer:v1", "", True),
        "claim_with_commit": ("claim", True, "testpeer:v1", "abc123", False),
    }
    def exercise(candidate: str) -> dict[str, bool]:
        rendered = [
            "$Root=(Get-Location).Path",
            "$PeerId='TestPeer'",
            "function Write-Log { param([string]$Message) }",
            candidate,
            "$path=Join-Path $Root 'runtime/state/events.jsonl'",
            "$results=[ordered]@{}",
        ]
        for name, (intent_type, applied, keyid, commit, _) in cases.items():
            event = {
                "seq": 2,
                "actor": "TestPeer",
                "applied": applied,
                "actor_auth": {"method": "ed25519", "keyid": keyid, "sig": "fixture"},
                "payload": {"intent_type": intent_type},
            }
            if commit:
                event["payload"]["commit"] = commit
            encoded = json.dumps(event, separators=(",", ":"))
            rendered.extend(
                (
                    "[IO.File]::WriteAllText($path,'{}'+[Environment]::NewLine,[Text.Encoding]::ASCII)".format("{}"),
                    "$before=(Get-Item -LiteralPath $path).Length",
                    "$hash=Get-FilePrefixSha256 -Path $path -Length $before",
                    "[IO.File]::AppendAllText($path,'{}'+[Environment]::NewLine,[Text.Encoding]::ASCII)".format(encoded.replace("'", "''")),
                    f"$results['{name}']=Get-OwnEvidence -LedgerBytesBefore $before -LedgerPrefixSha256Before $hash",
                )
            )
        rendered.append("$results|ConvertTo-Json -Compress")
        probe.write_text("\n".join(rendered) + "\n", encoding="ascii")
        return json.loads(run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(probe), cwd=sandbox).stdout)

    result = exercise(body)
    assert result == {name: expected for name, (*_, expected) in cases.items()}, result
    commit_proxy_mutant = body.replace(
        "if (-not $hasUsefulIntent) { continue }",
        "$hasCommit = -not [string]::IsNullOrWhiteSpace([string]$event.payload.commit)\n        if (-not ($hasUsefulIntent -or $hasCommit)) { continue }",
        1,
    )
    mutant_result = exercise(commit_proxy_mutant)
    assert mutant_result["claim_with_commit"] is True, mutant_result
    assert mutant_result["task_status"] is True, mutant_result
    events.write_text("", encoding="ascii")
    probe.unlink()


def run_git_gate_contract_mutants() -> None:
    """Both git probes fail closed and an apply failure remains visible.
    PERMANENT_NEGATIVE: retry-preexec-untracked-exit-gate, retry-apply-fail-visible
    """
    text = RUNNER.read_text(encoding="utf-8-sig")
    apply_fn = re.search(r"(?ms)^function Invoke-PreExecPatch \{.*?^\}", text)
    if not apply_fn:
        raise AssertionError("Invoke-PreExecPatch function not found")
    apply_body = apply_fn.group(0)

    def contract(candidate: str, candidate_apply: str) -> bool:
        return all(
            (
                'Reason "untracked_snapshot_failed"' in candidate,
                'reason=untracked_enumeration_failed' in candidate,
                'Write-Log "APPLY_FAIL index=$Index patch=$PatchPath exit=$LASTEXITCODE"' in candidate_apply,
            )
        )

    assert contract(text, apply_body), "git exit/logging contract is incomplete"
    mutants = {
        "preexec_gate_removed": (
            text.replace('if ($LASTEXITCODE -ne 0) { Register-PreExecDefer -Message $Message -Reason "untracked_snapshot_failed"; return }', "", 1),
            apply_body,
        ),
        "apply_fail_log_removed": (
            text,
            apply_body.replace('Write-Log "APPLY_FAIL index=$Index patch=$PatchPath exit=$LASTEXITCODE"', "", 1),
        ),
    }
    survivors = [name for name, mutant in mutants.items() if contract(*mutant)]
    assert not survivors, f"git gate contract failed to kill declared mutants: {survivors}"


def run_nul_residue_path_cases(sandbox: Path) -> None:
    """A stale non-ASCII residue must age; a console-codepage mutant must not.
    PERMANENT_NEGATIVE: retry-utf8-residue-path
    """
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    helper_text = extract_powershell_function_closure(
        runner_text, ("Get-StagedResidueState",), provided=("Write-Utf8NoBom",)
    )
    paths = [sandbox / "fresh residue.txt", sandbox / "residuo-anadido-\u00f1.txt"]
    probe = Path(tempfile.mkdtemp(prefix="task0281-residue-probe-")) / "nul-residue-probe.ps1"
    probe.write_text(
        "$Root=(Get-Location).Path\n$AbortedResidueMinutes=60\n"
        "$ResiduePath=Join-Path $Root '.protocol-tmp/residue-first-seen.json'\n"
        "New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ResiduePath)|Out-Null\n"
        "function Write-Utf8NoBom { param([string]$Path,[string]$Content) [IO.File]::WriteAllText($Path,$Content,(New-Object Text.UTF8Encoding($false))) }\n"
        + helper_text
        + "\nGet-StagedResidueState\n",
        encoding="ascii",
    )
    try:
        for path in paths:
            path.write_text("dirty\n", encoding="ascii")
            output = run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(probe), cwd=sandbox).stdout.strip()
            assert output == "live", (path.name, output)
            path.unlink()

        target = paths[-1]
        (sandbox / ".protocol-tmp/residue-first-seen.json").unlink(missing_ok=True)
        target.write_text("dirty\n", encoding="ascii")
        stale = time.time() - 7200
        target.touch()
        import os
        os.utime(target, (stale, stale))
        output = run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(probe), cwd=sandbox).stdout.strip()
        assert output == "aborted", f"stale UTF-8 residue did not age: {output!r}"
        (sandbox / ".protocol-tmp/residue-first-seen.json").unlink(missing_ok=True)
        decoding_mutant = probe.with_name("decoding-mutant.ps1")
        decoding_mutant.write_text(
            probe.read_text(encoding="ascii").replace(
                "New-Object System.Text.UTF8Encoding($false, $true)",
                "[Text.Encoding]::GetEncoding(850)",
            ),
            encoding="ascii",
        )
        mutant_output = run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(decoding_mutant), cwd=sandbox).stdout.strip()
        assert mutant_output == "live", "stale-path case failed to kill the console-codepage mutant"
        target.unlink()
    finally:
        shutil.rmtree(probe.parent, ignore_errors=True)


def run(*args: str, cwd: Path, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=True)


def retry_exhausted_events(log: str) -> list[dict[str, str]]:
    events = []
    for line in log.splitlines():
        if "RETRY_EXHAUSTED" not in line:
            continue
        fields = {}
        for token in line.split("RETRY_EXHAUSTED", 1)[1].split():
            if "=" in token:
                key, value = token.split("=", 1)
                fields[key] = value
        events.append(fields)
    return events


def run_unreadable_head_case(sandbox: Path, prompt: Path, fake: Path) -> None:
    """PERMANENT_NEGATIVE: retry-ledger-head-defer-order

    A valid old own event must not confirm work when the head helper fails, and
    resetting the stable defer before the readability check must kill the test.
    """
    helper = sandbox / "scripts/ledger_head.py"
    instrumented_runner = sandbox / "scripts/harness/peer_mailbox_cron.ps1"
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    instrumented_runner.write_text(runner_text, encoding="utf-8")
    helper.write_text("raise SystemExit(23)\n", encoding="ascii")
    events = sandbox / "runtime/state/events.jsonl"
    events.write_text(
        '{"seq":1,"actor":"TestPeer","actor_auth":{"method":"ed25519",'
        '"keyid":"testpeer:v1","sig":"old-signature"}}\n',
        encoding="ascii",
    )
    run("git", "add", "scripts/harness/peer_mailbox_cron.ps1", "scripts/ledger_head.py", "runtime/state/events.jsonl", cwd=sandbox)
    run("git", "commit", "-m", "fixture unreadable ledger head", cwd=sandbox)
    def exercise(
        runner: Path,
        *,
        expect_expected_terminal: bool,
        expect_any_terminal: bool,
    ) -> None:
        runtime = sandbox / ".protocol-tmp/testpeer_mailbox_cron"
        runtime.mkdir(parents=True)
        (runtime / "testpeer_mailbox_cron.lock").write_text("orphan\n", encoding="ascii")
        command = [
            "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(runner),
            "-PeerId", "TestPeer", "-CoordinatorId", "Coordinator", "-Root", str(sandbox), "-PromptFile", str(prompt),
            "-AgentExe", str(fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
            "-MaxNoCoordinatorRounds", "6", "-ExecTimeoutSeconds", "20",
            "-MaxTransientRetries", "5", "-PreExecDeferTimeoutSeconds", "2",
            "-RetryBackoffSeconds", "0", "-AbortedResidueMinutes", "0",
        ]
        process = subprocess.Popen(command, cwd=sandbox, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log_path = runtime / "testpeer_mailbox_cron.log"
        deadline = time.monotonic() + 12
        log = ""
        while time.monotonic() < deadline and process.poll() is None:
            if log_path.exists():
                log = log_path.read_text(encoding="utf-8")
            events = retry_exhausted_events(log)
            if any(event.get("outcome") == "defer_terminal" for event in events):
                break
            time.sleep(0.1)
        events = retry_exhausted_events(log)
        terminal = any(event.get("outcome") == "defer_terminal" for event in events)
        expected_terminal = any(
            event.get("defers") == "3"
            and event.get("attempts") == "0"
            and event.get("signal") == "watchdog"
            and event.get("outcome") == "defer_terminal"
            and event.get("reason") == "ledger_unreadable_before_exec"
            for event in events
        )
        assert terminal is expect_any_terminal, log
        assert expected_terminal is expect_expected_terminal, log
        (runtime / "testpeer_mailbox_cron.stop").write_text("stop\n", encoding="ascii")
        process.communicate(timeout=10)
        assert process.returncode == 0, log
        assert not (sandbox / ".protocol-tmp/fake-count.txt").exists(), "agent ran with an unreadable ledger head"
        seen_path = runtime / "testpeer_mailbox_cron.seen.json"
        seen = json.loads(seen_path.read_text(encoding="utf-8")) if seen_path.exists() else {}
        assert "MSG-retry.md" not in seen, "old own evidence consumed the message"
        assert "outcome=confirmed" not in log, log
        assert "SELF_HEAL_ORPHAN_LOCK owner=TestPeer reason=missing_lease" in log, log
        assert not (runtime / "testpeer_mailbox_cron.lock").exists(), "head failure left an orphan lock"
        shutil.rmtree(sandbox / ".protocol-tmp")

    exercise(
        instrumented_runner,
        expect_expected_terminal=True,
        expect_any_terminal=True,
    )
    good_order = (
        "        $ledgerHeadBefore = Get-LedgerHead\n"
        "        if (-not [bool]$ledgerHeadBefore.readable) { Register-PreExecDefer -Message $Message -Reason \"ledger_unreadable_before_exec\"; return }\n"
        "        Reset-PreExecDefer -Message $Message\n"
    )
    bad_order = (
        "        Reset-PreExecDefer -Message $Message\n"
        "        $ledgerHeadBefore = Get-LedgerHead\n"
        "        if (-not [bool]$ledgerHeadBefore.readable) { Register-PreExecDefer -Message $Message -Reason \"ledger_unreadable_before_exec\"; return }\n"
    )
    mutant_text = runner_text.replace(good_order, bad_order, 1)
    assert mutant_text != runner_text, "ledger-head defer-order mutation did not apply"
    mutant_runner = instrumented_runner
    mutant_runner.write_text(mutant_text, encoding="utf-8")
    run("git", "add", "scripts/harness/peer_mailbox_cron.ps1", cwd=sandbox)
    run("git", "commit", "-m", "mutate ledger head defer order", cwd=sandbox)
    exercise(
        mutant_runner,
        expect_expected_terminal=False,
        expect_any_terminal=False,
    )
    wrong_cause_text = runner_text.replace(
        'Register-PreExecDefer -Message $Message -Reason "ledger_unreadable_before_exec"',
        'Register-PreExecDefer -Message $Message -Reason "ledger_unreadable_wrong_cause"',
        1,
    )
    assert wrong_cause_text != runner_text, "ledger-head wrong-cause mutation did not apply"
    mutant_runner.write_text(wrong_cause_text, encoding="utf-8")
    run("git", "add", "scripts/harness/peer_mailbox_cron.ps1", cwd=sandbox)
    run("git", "commit", "-m", "mutate ledger head defer cause", cwd=sandbox)
    exercise(
        mutant_runner,
        expect_expected_terminal=False,
        expect_any_terminal=True,
    )
    shutil.copy2(RUNNER, instrumented_runner)
    shutil.copy2(LEDGER_HEAD, helper)
    events.write_text("", encoding="ascii")
    run("git", "add", "scripts/harness/peer_mailbox_cron.ps1", "scripts/ledger_head.py", "runtime/state/events.jsonl", cwd=sandbox)
    run("git", "commit", "-m", "restore readable ledger head fixture", cwd=sandbox)


def run_unstaged_residue_case(sandbox: Path, prompt: Path, fake: Path) -> None:
    """Environmental defers escape to a terminal state at the configured bound."""
    residue = sandbox / "unstaged-residue.txt"
    residue.write_text("dirty\n", encoding="ascii")
    runtime = sandbox / ".protocol-tmp/testpeer_mailbox_cron"
    runtime.mkdir(parents=True, exist_ok=True)
    recovery_fake = runtime / "fake-recovery.cmd"
    recovery_fake.write_text("@echo OUTCOME: definitive\r\n", encoding="ascii")
    command = [
        "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER),
        "-PeerId", "TestPeer", "-CoordinatorId", "Coordinator", "-Root", str(sandbox), "-PromptFile", str(prompt),
        "-AgentExe", str(recovery_fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
        "-MaxNoCoordinatorRounds", "8", "-ExecTimeoutSeconds", "20",
        "-MaxTransientRetries", "3", "-PreExecDeferTimeoutSeconds", "2",
        "-RetryBackoffSeconds", "0", "-AbortedResidueMinutes", "60",
    ]
    process = subprocess.Popen(command, cwd=sandbox, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log_path = runtime / "testpeer_mailbox_cron.log"
    deadline = time.monotonic() + 12
    log = ""
    while time.monotonic() < deadline:
        if log_path.exists():
            log = log_path.read_text(encoding="utf-8")
            if any(
                event.get("defers") == "3"
                and event.get("attempts") == "0"
                and event.get("signal") == "watchdog"
                and event.get("outcome") == "defer_terminal"
                and event.get("reason") == "worktree_residue_live"
                for event in retry_exhausted_events(log)
            ):
                break
        time.sleep(0.1)
    else:
        process.kill()
        stdout, stderr = process.communicate()
        raise AssertionError(f"residue watchdog signal missing:\n{log}\n{stdout}\n{stderr}")
    retry = json.loads((runtime / "testpeer_mailbox_cron.retry.json").read_text(encoding="utf-8"))
    assert retry["MSG-retry.md"]["attempts"] == 0 and retry["MSG-retry.md"]["exhausted"], retry
    assert retry["MSG-retry.md"]["outcome"] == "defer_terminal", retry
    residue.unlink()
    remaining = run("git", "status", "--porcelain=v1", "--untracked-files=all", cwd=sandbox).stdout
    assert remaining == "", f"fixture did not become clean after environmental veto: {remaining!r}"
    stdout, stderr = process.communicate(timeout=15)
    assert process.returncode == 0, stdout + stderr
    log = (runtime / "testpeer_mailbox_cron.log").read_text(encoding="utf-8")
    assert "reason=worktree_residue_live" in log, log
    assert "outcome=definitive" not in log, log
    seen_path = runtime / "testpeer_mailbox_cron.seen.json"
    seen = json.loads(seen_path.read_text(encoding="utf-8")) if seen_path.exists() else {}
    assert "MSG-retry.md" not in seen, "terminally deferred message was re-executed"
    shutil.rmtree(sandbox / ".protocol-tmp")


def run_disordered_ledger_case(sandbox: Path, prompt: Path) -> None:
    """Historical own evidence before the byte baseline cannot confirm a new exec."""
    events = sandbox / "runtime/state/events.jsonl"
    events.write_text(
        '{"seq":99,"actor":"TestPeer","actor_auth":{"method":"ed25519","keyid":"testpeer:v1","sig":"old"}}\n'
        '{"seq":1,"actor":"Other","actor_auth":{"method":"ed25519","keyid":"other:v1","sig":"tail"}}\n',
        encoding="ascii",
    )
    fake = sandbox / "fake-noop.cmd"
    fake.write_text("@echo no new evidence\r\n", encoding="ascii")
    command = [
        "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER),
        "-PeerId", "TestPeer", "-CoordinatorId", "Coordinator", "-Root", str(sandbox), "-PromptFile", str(prompt),
        "-AgentExe", str(fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
        "-MaxNoCoordinatorRounds", "3", "-ExecTimeoutSeconds", "20",
        "-MaxTransientRetries", "1", "-RetryBackoffSeconds", "0", "-AbortedResidueMinutes", "0",
    ]
    run(*command, cwd=sandbox, timeout=20)
    runtime = sandbox / ".protocol-tmp/testpeer_mailbox_cron"
    log = (runtime / "testpeer_mailbox_cron.log").read_text(encoding="utf-8")
    assert "outcome=unconfirmed" in log, log
    assert "outcome=confirmed" not in log, log
    assert any(
        event.get("attempts") == "1"
        and event.get("signal") == "watchdog"
        and event.get("outcome") == "unconfirmed"
        for event in retry_exhausted_events(log)
    ), log
    shutil.rmtree(sandbox / ".protocol-tmp")
    fake.unlink()


def run_post_delivery_timeout_case() -> None:
    """A signed delivery starts a shorter bounded window for slow post-delivery work."""
    fixture = Path(tempfile.mkdtemp(prefix="task0300-post-delivery-"))
    try:
        (fixture / "Area_comun/mailbox/open").mkdir(parents=True)
        (fixture / "Area_comun/state").mkdir(parents=True)
        (fixture / "runtime/state").mkdir(parents=True)
        (fixture / "runtime").mkdir(exist_ok=True)
        (fixture / "scripts/harness/prompts").mkdir(parents=True)
        (fixture / "scripts").mkdir(exist_ok=True)
        shutil.copy2(RUNNER, fixture / "scripts/harness/peer_mailbox_cron.ps1")
        shutil.copy2(LEDGER_HEAD, fixture / "scripts/ledger_head.py")
        (fixture / "runtime/protocol_replay.py").write_text(
            "def protocol_state_drift(root): return {'has_drift': False}\n", encoding="ascii"
        )
        (fixture / "runtime/state/events.jsonl").write_text("", encoding="ascii")
        (fixture / "Area_comun/state/CLAIMS.json").write_text('{"claims":[]}\n', encoding="ascii")
        (fixture / "Area_comun/state/TASK_INDEX.json").write_text(
            '{"tasks":[{"id":"TASK-0300","owner":"TestPeer","status":"in_review",'
            '"file":"Area_comun/tasks/TASK-0300-post-delivery.md"}]}\n',
            encoding="ascii",
        )
        (fixture / "Area_comun/state/TASK_INDEX_ARCHIVE.json").write_text(
            '{"tasks":[]}\n', encoding="ascii"
        )
        task_file = fixture / "Area_comun/tasks/TASK-0300-post-delivery.md"
        task_file.parent.mkdir(parents=True)
        task_file.write_text(
            "---\ntask_id: TASK-0300\nfile: Area_comun/tasks/TASK-0300-post-delivery.md\n"
            "intake:\n  scope_routes:\n    - post-delivery-output.txt\n---\n",
            encoding="ascii",
        )
        (fixture / "protocol.config.json").write_text("{}\n", encoding="ascii")
        (fixture / ".gitignore").write_text(".protocol-tmp/\n", encoding="ascii")
        (fixture / "Area_comun/mailbox/open/MSG-post.md").write_text(
            "---\nfrom: Arquitecto\nto: TestPeer\ntype: ACTION\ntask_id: TASK-0300\nstatus: open\n"
            "requires_response: true\nresponse_owner: TestPeer\nrequested_action: test\n---\n",
            encoding="ascii",
        )
        prompt = fixture / "scripts/harness/prompts/test.prompt.md"
        prompt.write_text("Process @@MESSAGE_PATH@@.\n", encoding="ascii")
        core = fixture / "slow-post.ps1"
        core.write_text(
            "$event='{\"seq\":1,\"actor\":\"TestPeer\",\"applied\":true,"
            "\"actor_auth\":{\"method\":\"ed25519\",\"keyid\":\"testpeer:v1\",\"sig\":\"fixture\"},"
            "\"payload\":{\"intent_type\":\"task_status\",\"task_id\":\"TASK-0300\","
            "\"transitions\":{\"task_status\":{\"from\":\"in_progress\",\"to\":\"in_review\"}}}}'\n"
            "Add-Content -LiteralPath 'runtime/state/events.jsonl' -Value $event -Encoding ASCII\n"
            "Start-Sleep -Seconds 30\n",
            encoding="ascii",
        )
        fake = fixture / "slow-post.cmd"
        fake.write_text('@powershell.exe -NoProfile -File "%~dp0slow-post.ps1"\r\n', encoding="ascii")
        run("git", "init", cwd=fixture)
        run("git", "config", "user.email", "retry@example.invalid", cwd=fixture)
        run("git", "config", "user.name", "TestPeer", cwd=fixture)
        run("git", "add", ".", cwd=fixture)
        run("git", "commit", "-m", "fixture", cwd=fixture)
        started = time.monotonic()
        try:
            run(
                "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER),
                "-PeerId", "TestPeer", "-CoordinatorId", "Coordinator", "-Root", str(fixture), "-PromptFile", str(prompt),
                "-AgentExe", str(fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
                "-MaxNoCoordinatorRounds", "3", "-ExecTimeoutSeconds", "20",
                "-PostDeliveryTimeoutSeconds", "2", "-MaxTransientRetries", "1", "-RetryBackoffSeconds", "0",
                "-ProgressFreshSeconds", "0", "-ProgressHardCapSeconds", "1",
                cwd=fixture, timeout=15,
            )
        except subprocess.TimeoutExpired as exc:
            log_path = fixture / ".protocol-tmp/testpeer_mailbox_cron/testpeer_mailbox_cron.log"
            raise AssertionError(log_path.read_text(encoding="utf-8") if log_path.exists() else "timeout without log") from exc
        elapsed = time.monotonic() - started
        log = (fixture / ".protocol-tmp/testpeer_mailbox_cron/testpeer_mailbox_cron.log").read_text(encoding="utf-8")
        assert elapsed < 18, elapsed
        assert "POST_DELIVERY_WINDOW_START" in log and "POST_DELIVERY_TIMEOUT" in log, log
        window_started = re.search(r"(?m)^(\S+) POST_DELIVERY_WINDOW_START", log)
        window_expired = re.search(r"(?m)^(\S+) POST_DELIVERY_TIMEOUT", log)
        assert window_started and window_expired
        measured = time.mktime(time.strptime(window_expired.group(1), "%Y-%m-%dT%H:%M:%S")) - time.mktime(
            time.strptime(window_started.group(1), "%Y-%m-%dT%H:%M:%S")
        )
        assert 1 <= measured <= 4, measured
        assert "TREE_KILL_COMPLETE" in log and "outcome=transient" in log, log
        assert "RETRY_EXHAUSTED" in log, log
    finally:
        shutil.rmtree(fixture, ignore_errors=True)


def run_exec_running_heartbeat_case() -> None:
    """A long text-mode exec emits configurable liveness logs, and removing them fails."""
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    heartbeat_line = (
        'Write-Log "EXEC_RUNNING pid=$($process.Id) '
        'elapsed=$($elapsedSeconds)s message=$($Message.Name)"'
    )
    assert heartbeat_line in runner_text

    def exercise(candidate: str) -> tuple[int, str]:
        fixture = Path(tempfile.mkdtemp(prefix="task0302-exec-running-"))
        try:
            (fixture / "Area_comun/mailbox/open").mkdir(parents=True)
            (fixture / "Area_comun/state").mkdir(parents=True)
            (fixture / "runtime/state").mkdir(parents=True)
            (fixture / "runtime").mkdir(exist_ok=True)
            (fixture / "scripts/harness/prompts").mkdir(parents=True)
            (fixture / "scripts").mkdir(exist_ok=True)
            (fixture / "scripts/harness/peer_mailbox_cron.ps1").write_text(candidate, encoding="utf-8")
            shutil.copy2(LEDGER_HEAD, fixture / "scripts/ledger_head.py")
            (fixture / "runtime/protocol_replay.py").write_text(
                "def protocol_state_drift(root): return {'has_drift': False}\n", encoding="ascii"
            )
            (fixture / "runtime/state/events.jsonl").write_text("", encoding="ascii")
            (fixture / "Area_comun/state/CLAIMS.json").write_text('{"claims":[]}\n', encoding="ascii")
            (fixture / "Area_comun/state/TASK_INDEX.json").write_text(
                '{"tasks":[{"id":"TASK-0302","owner":"TestPeer","status":"in_progress",'
                '"file":"Area_comun/tasks/TASK-0302-heartbeat.md"}]}\n',
                encoding="ascii",
            )
            (fixture / "Area_comun/state/TASK_INDEX_ARCHIVE.json").write_text(
                '{"tasks":[]}\n', encoding="ascii"
            )
            task_file = fixture / "Area_comun/tasks/TASK-0302-heartbeat.md"
            task_file.parent.mkdir(parents=True)
            task_file.write_text(
                "---\ntask_id: TASK-0302\nfile: Area_comun/tasks/TASK-0302-heartbeat.md\n"
                "intake:\n  scope_routes:\n    - heartbeat-output.txt\n---\n",
                encoding="ascii",
            )
            (fixture / "protocol.config.json").write_text("{}\n", encoding="ascii")
            (fixture / ".gitignore").write_text(".protocol-tmp/\n", encoding="ascii")
            (fixture / "Area_comun/mailbox/open/MSG-heartbeat.md").write_text(
                "---\nfrom: Arquitecto\nto: TestPeer\ntype: ACTION\ntask_id: TASK-0302\nstatus: open\n"
                "requires_response: true\nresponse_owner: TestPeer\nrequested_action: test\n---\n",
                encoding="ascii",
            )
            prompt = fixture / "scripts/harness/prompts/test.prompt.md"
            prompt.write_text("Process @@MESSAGE_PATH@@.\n", encoding="ascii")
            slow = fixture / "slow-heartbeat.ps1"
            slow.write_text("Start-Sleep -Seconds 4\n", encoding="ascii")
            fake = fixture / "slow-heartbeat.cmd"
            fake.write_text('@powershell.exe -NoProfile -File "%~dp0slow-heartbeat.ps1"\r\n', encoding="ascii")
            run("git", "init", cwd=fixture)
            run("git", "config", "user.email", "retry@example.invalid", cwd=fixture)
            run("git", "config", "user.name", "TestPeer", cwd=fixture)
            run("git", "add", ".", cwd=fixture)
            run("git", "commit", "-m", "fixture", cwd=fixture)
            run(
                "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                str(fixture / "scripts/harness/peer_mailbox_cron.ps1"),
                "-PeerId", "TestPeer", "-CoordinatorId", "Coordinator", "-Root", str(fixture), "-PromptFile", str(prompt),
                "-AgentExe", str(fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
                "-MaxNoCoordinatorRounds", "3", "-ExecTimeoutSeconds", "20", "-HeartbeatSeconds", "1",
                "-MaxTransientRetries", "1", "-RetryBackoffSeconds", "0", cwd=fixture, timeout=15,
            )
            log = (fixture / ".protocol-tmp/testpeer_mailbox_cron/testpeer_mailbox_cron.log").read_text(
                encoding="utf-8"
            )
            return (
                len(re.findall(r"(?m) EXEC_RUNNING pid=\d+ elapsed=\d+s message=MSG-heartbeat\.md$", log)),
                log,
            )
        finally:
            shutil.rmtree(fixture, ignore_errors=True)

    heartbeat_count, heartbeat_log = exercise(runner_text)
    assert heartbeat_count >= 3, heartbeat_log
    mutant = runner_text.replace(heartbeat_line, "", 1)
    mutant_count, mutant_log = exercise(mutant)
    assert mutant_count == 0, mutant_log


def run_pre_delivery_and_liveness_cases() -> None:
    """Claims do not start delivery timing; progress extends once, while a stale frozen exec is killed."""
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    assert 'transitions.task_status.to -cne "in_review"' in runner_text
    assert "EXEC_PROGRESSING" in runner_text and "EXEC_HUNG" in runner_text

    fixture = Path(tempfile.mkdtemp(prefix="task0303-liveness-"))
    try:
        (fixture / "Area_comun/mailbox/open").mkdir(parents=True)
        (fixture / "Area_comun/state").mkdir(parents=True)
        (fixture / "runtime/state").mkdir(parents=True)
        (fixture / "runtime").mkdir(exist_ok=True)
        (fixture / "scripts/harness/prompts").mkdir(parents=True)
        (fixture / "scripts").mkdir(exist_ok=True)
        shutil.copy2(RUNNER, fixture / "scripts/harness/peer_mailbox_cron.ps1")
        shutil.copy2(LEDGER_HEAD, fixture / "scripts/ledger_head.py")
        (fixture / "runtime/protocol_replay.py").write_text(
            "def protocol_state_drift(root): return {'has_drift': False}\n", encoding="ascii"
        )
        (fixture / "runtime/state/events.jsonl").write_text("", encoding="ascii")
        (fixture / "Area_comun/state/CLAIMS.json").write_text('{"claims":[]}\n', encoding="ascii")
        (fixture / "Area_comun/state/TASK_INDEX.json").write_text(
            '{"tasks":[{"id":"TASK-0303","owner":"TestPeer","status":"in_progress",'
            '"file":"Area_comun/tasks/TASK-0303-liveness.md"}]}\n', encoding="ascii"
        )
        (fixture / "Area_comun/state/TASK_INDEX_ARCHIVE.json").write_text(
            '{"tasks":[]}\n', encoding="ascii"
        )
        task_file = fixture / "Area_comun/tasks/TASK-0303-liveness.md"
        task_file.parent.mkdir(parents=True)
        task_file.write_text(
            "---\ntask_id: TASK-0303\nfile: Area_comun/tasks/TASK-0303-liveness.md\n"
            "intake:\n  scope_routes:\n    - liveness-output.txt\n---\n",
            encoding="ascii",
        )
        (fixture / "protocol.config.json").write_text("{}\n", encoding="ascii")
        (fixture / ".gitignore").write_text(".protocol-tmp/\n", encoding="ascii")
        (fixture / "Area_comun/mailbox/open/MSG-work.md").write_text(
            "---\nfrom: Arquitecto\nto: TestPeer\ntype: ACTION\ntask_id: TASK-0303\nstatus: open\n"
            "requires_response: true\nresponse_owner: TestPeer\nrequested_action: test\n---\n",
            encoding="ascii",
        )
        prompt = fixture / "scripts/harness/prompts/test.prompt.md"
        prompt.write_text("Process @@MESSAGE_PATH@@.\n", encoding="ascii")
        core = fixture / "progress.ps1"
        core.write_text(
            "$claim='{\"seq\":1,\"actor\":\"TestPeer\",\"applied\":true,"
            "\"actor_auth\":{\"method\":\"ed25519\",\"keyid\":\"testpeer:v1\",\"sig\":\"fixture\"},"
            "\"payload\":{\"intent_type\":\"task_status\",\"task_id\":\"TASK-0303\","
            "\"transitions\":{\"task_status\":{\"from\":\"ready\",\"to\":\"in_progress\"}}}}'\n"
            "Add-Content runtime/state/events.jsonl $claim -Encoding ASCII\n"
            "1..20 | ForEach-Object { Write-Error ('working-' + $_); Start-Sleep -Milliseconds 400 }\n",
            encoding="ascii",
        )
        fake = fixture / "progress.cmd"
        fake.write_text('@powershell.exe -NoProfile -File "%~dp0progress.ps1"\r\n', encoding="ascii")
        run("git", "init", cwd=fixture)
        run("git", "config", "user.email", "retry@example.invalid", cwd=fixture)
        run("git", "config", "user.name", "TestPeer", cwd=fixture)
        run("git", "add", ".", cwd=fixture)
        run("git", "commit", "-m", "fixture", cwd=fixture)
        started = time.monotonic()
        run(
            "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER),
            "-PeerId", "TestPeer", "-CoordinatorId", "Coordinator", "-Root", str(fixture), "-PromptFile", str(prompt),
            "-AgentExe", str(fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
            "-MaxNoCoordinatorRounds", "3", "-ExecTimeoutSeconds", "2", "-PostDeliveryTimeoutSeconds", "1",
            "-ProgressFreshSeconds", "0", "-ProgressExtensionSeconds", "2", "-ProgressHardCapSeconds", "3",
            "-MaxTransientRetries", "1", "-RetryBackoffSeconds", "0", cwd=fixture, timeout=15,
        )
        elapsed = time.monotonic() - started
        log = (fixture / ".protocol-tmp/testpeer_mailbox_cron/testpeer_mailbox_cron.log").read_text(encoding="utf-8")
        assert "POST_DELIVERY_WINDOW_START" not in log, log
        assert "EXEC_PROGRESSING" in log and "reason=run_log_growing" in log, log
        assert "EXEC_HUNG" in log and "reason=hard_cap" in log, log
        assert "TREE_KILL_COMPLETE" in log, log
        assert elapsed >= 4, elapsed
    finally:
        shutil.rmtree(fixture, ignore_errors=True)


def run_frozen_exec_with_production_freshness_case() -> None:
    """A self-bumped lease heartbeat cannot keep a frozen exec alive."""
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    progress_helper = extract_powershell_function_closure(runner_text, ("Get-ExecProgressState",))
    assert "heartbeat_fresh" not in progress_helper

    fixture = Path(tempfile.mkdtemp(prefix="task0304-frozen-production-freshness-"))
    try:
        (fixture / "Area_comun/mailbox/open").mkdir(parents=True)
        (fixture / "Area_comun/state").mkdir(parents=True)
        (fixture / "runtime/state").mkdir(parents=True)
        (fixture / "runtime").mkdir(exist_ok=True)
        (fixture / "scripts/harness/prompts").mkdir(parents=True)
        (fixture / "scripts").mkdir(exist_ok=True)
        shutil.copy2(RUNNER, fixture / "scripts/harness/peer_mailbox_cron.ps1")
        shutil.copy2(LEDGER_HEAD, fixture / "scripts/ledger_head.py")
        (fixture / "runtime/protocol_replay.py").write_text(
            "def protocol_state_drift(root): return {'has_drift': False}\n", encoding="ascii"
        )
        (fixture / "runtime/state/events.jsonl").write_text("", encoding="ascii")
        (fixture / "Area_comun/state/CLAIMS.json").write_text('{"claims":[]}\n', encoding="ascii")
        (fixture / "Area_comun/state/TASK_INDEX.json").write_text(
            '{"tasks":[{"id":"TASK-0304","owner":"TestPeer","status":"in_progress",'
            '"file":"Area_comun/tasks/TASK-0304-frozen.md"}]}\n', encoding="ascii"
        )
        (fixture / "Area_comun/state/TASK_INDEX_ARCHIVE.json").write_text(
            '{"tasks":[]}\n', encoding="ascii"
        )
        task_file = fixture / "Area_comun/tasks/TASK-0304-frozen.md"
        task_file.parent.mkdir(parents=True)
        task_file.write_text(
            "---\ntask_id: TASK-0304\nfile: Area_comun/tasks/TASK-0304-frozen.md\n"
            "intake:\n  scope_routes:\n    - frozen-output.txt\n---\n",
            encoding="ascii",
        )
        (fixture / "protocol.config.json").write_text("{}\n", encoding="ascii")
        (fixture / ".gitignore").write_text(".protocol-tmp/\n", encoding="ascii")
        (fixture / "Area_comun/mailbox/open/MSG-frozen.md").write_text(
            "---\nfrom: Arquitecto\nto: TestPeer\ntype: ACTION\ntask_id: TASK-0304\nstatus: open\n"
            "requires_response: true\nresponse_owner: TestPeer\nrequested_action: test\n---\n",
            encoding="ascii",
        )
        prompt = fixture / "scripts/harness/prompts/test.prompt.md"
        prompt.write_text("Process @@MESSAGE_PATH@@.\n", encoding="ascii")
        frozen = fixture / "frozen.ps1"
        frozen.write_text("Start-Sleep -Seconds 30\n", encoding="ascii")
        fake = fixture / "frozen.cmd"
        fake.write_text('@powershell.exe -NoProfile -File "%~dp0frozen.ps1"\r\n', encoding="ascii")
        run("git", "init", cwd=fixture)
        run("git", "config", "user.email", "retry@example.invalid", cwd=fixture)
        run("git", "config", "user.name", "TestPeer", cwd=fixture)
        run("git", "add", ".", cwd=fixture)
        run("git", "commit", "-m", "fixture", cwd=fixture)
        started = time.monotonic()
        run(
            "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER),
            "-PeerId", "TestPeer", "-CoordinatorId", "Coordinator", "-Root", str(fixture), "-PromptFile", str(prompt),
            "-AgentExe", str(fake), "-AgentProvider", "Codex", "-IntervalSeconds", "1",
            "-MaxNoCoordinatorRounds", "3", "-ExecTimeoutSeconds", "2", "-PostDeliveryTimeoutSeconds", "1",
            "-ProgressFreshSeconds", "15", "-ProgressExtensionSeconds", "2", "-ProgressHardCapSeconds", "8",
            "-MaxTransientRetries", "1", "-RetryBackoffSeconds", "0", cwd=fixture, timeout=15,
        )
        elapsed = time.monotonic() - started
        log = (fixture / ".protocol-tmp/testpeer_mailbox_cron/testpeer_mailbox_cron.log").read_text(encoding="utf-8")
        assert "EXEC_HUNG" in log and "reason=no_progress" in log, log
        assert "reason=hard_cap" not in log, log
        assert "TREE_KILL_COMPLETE" in log, log
        assert elapsed < 12, elapsed
    finally:
        shutil.rmtree(fixture, ignore_errors=True)


def run_complete_tree_kill_case() -> None:
    """The real kill helper removes intact and mid-kill re-parented process trees."""
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    tree_kill_helper = extract_powershell_function_closure(
        runner_text, ("Stop-LeaseProcessTree",), provided=("Write-Log", "Test-LeaseProcessMatches")
    )

    sweep = """        foreach ($childPid in $killOrder) {
            Stop-Process -Id $childPid -Force -ErrorAction SilentlyContinue
        }"""
    assert sweep in tree_kill_helper
    no_compensating_sweep = tree_kill_helper.replace(sweep, "", 1)

    def exercise(candidate: str, reparent_during_snapshot: bool) -> list[int]:
        fixture = Path(tempfile.mkdtemp(prefix="task0301-reparent-tree-kill-"))
        process = None
        pids: list[int] = []
        try:
            grand = fixture / "grand.ps1"
            child = fixture / "child.ps1"
            root = fixture / "root.ps1"
            grand.write_text("Set-Content grand.pid $PID -Encoding ASCII; Start-Sleep -Seconds 60\n", encoding="ascii")
            child.write_text(
                "Set-Content child.pid $PID -Encoding ASCII; Start-Process powershell.exe -ArgumentList @('-NoProfile','-File','grand.ps1') -WindowStyle Hidden; Start-Sleep -Seconds 60\n",
                encoding="ascii",
            )
            root.write_text(
                "Set-Content root.pid $PID -Encoding ASCII; Start-Process powershell.exe -ArgumentList @('-NoProfile','-File','child.ps1') -WindowStyle Hidden; Start-Sleep -Seconds 60\n",
                encoding="ascii",
            )
            process = subprocess.Popen(["powershell.exe", "-NoProfile", "-File", str(root)], cwd=fixture)
            deadline = time.monotonic() + 10
            pid_files = ("root.pid", "child.pid", "grand.pid")
            while time.monotonic() < deadline and not all((fixture / name).exists() for name in pid_files):
                time.sleep(0.1)
            assert all((fixture / name).exists() for name in pid_files), "process tree did not start"
            pids = [int((fixture / name).read_text().strip()) for name in pid_files]
            reparent_hook = ""
            if reparent_during_snapshot:
                reparent_hook = (
                    f"$script:IntermediatePid={pids[1]}\n"
                    "function Get-CimInstance {\n"
                    "  [CmdletBinding()] param([string]$ClassName)\n"
                    "  $snapshot=@(CimCmdlets\\Get-CimInstance $ClassName -ErrorAction Stop)\n"
                    "  Stop-Process -Id $script:IntermediatePid -Force -ErrorAction Stop\n"
                    "  Wait-Process -Id $script:IntermediatePid -ErrorAction SilentlyContinue\n"
                    "  return $snapshot\n"
                    "}\n"
                )
            probe = fixture / "kill.ps1"
            probe.write_text(
                "$ErrorActionPreference='Stop'\n$LogPath='kill.log'\n"
                "function Write-Log { param([string]$Message) Add-Content -LiteralPath $LogPath -Value $Message -Encoding ASCII }\n"
                "function Test-LeaseProcessMatches { param($Lease) return $true }\n"
                + reparent_hook
                + candidate
                + f"\n$lease=[pscustomobject]@{{pid={pids[0]};cmdline='fixture-agent';task_or_msg_id='tree'}}\n"
                "$null=Stop-LeaseProcessTree -Lease $lease -Reason 'regression'\n",
                encoding="ascii",
            )
            run("powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(probe), cwd=fixture)
            time.sleep(0.5)
            alive = []
            for pid in pids:
                check = subprocess.run(
                    ["powershell.exe", "-NoProfile", "-Command", f"if(Get-Process -Id {pid} -ErrorAction SilentlyContinue){{exit 1}}"]
                )
                if check.returncode != 0:
                    alive.append(pid)
            return alive
        finally:
            for pid in pids:
                subprocess.run(
                    ["powershell.exe", "-NoProfile", "-Command", f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            if process is not None:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
            shutil.rmtree(fixture, ignore_errors=True)

    assert exercise(tree_kill_helper, reparent_during_snapshot=False) == []
    reparent_survivors = exercise(tree_kill_helper, reparent_during_snapshot=True)
    assert reparent_survivors == [], reparent_survivors
    mutant_survivors = exercise(no_compensating_sweep, reparent_during_snapshot=True)
    assert len(mutant_survivors) == 1, mutant_survivors


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
        (sandbox / "Area_comun/state/CLAIMS.json").write_text('{"seq":0,"claims":[]}\n', encoding="ascii")
        (sandbox / ".gitignore").write_text(".protocol-tmp/\n", encoding="ascii")
        (sandbox / "predirty.txt").write_text("baseline\n", encoding="ascii")
        (sandbox / "Area_comun/tasks").mkdir(parents=True)
        (sandbox / "Area_comun/decisions").mkdir(parents=True)
        (sandbox / "Area_comun/tasks/TASK-fixture.md").write_text(
            "---\ntask_id: TASK-0001\nfile: Area_comun/tasks/TASK-fixture.md\n"
            "intake:\n  scope_routes:\n    - unrelated-scope.txt\n---\nbaseline-task\n",
            encoding="ascii",
        )
        (sandbox / "Area_comun/state/TASK_INDEX.json").write_text(
            '{"tasks":[{"id":"TASK-0001","file":"Area_comun/tasks/TASK-fixture.md"}]}\n',
            encoding="ascii",
        )
        (sandbox / "Area_comun/state/TASK_INDEX_ARCHIVE.json").write_text(
            '{"tasks":[]}\n', encoding="ascii"
        )
        message = sandbox / "Area_comun/mailbox/open/MSG-retry.md"
        message.write_text(
            "---\nfrom: Arquitecto\nto: TestPeer\ntype: ACTION\ntask_id: TASK-0001\nstatus: open\n"
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
            "  Set-Content -Path (Join-Path $root 'Area_comun/mailbox/open/MSG-window.md') -Value incoming -Encoding ASCII\n"
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
            "  Set-Content -Path (Join-Path $root 'Area_comun/state/CLAIMS.json') -Value '{\"seq\":3,\"claims\":[]}' -Encoding ASCII\n"
            "  Copy-Item -LiteralPath (Join-Path $root 'runtime/state/events.jsonl') -Destination (Join-Path $root '.protocol-tmp/signed-events-before-rollback.jsonl') -Force\n"
            "  Copy-Item -LiteralPath (Join-Path $root 'Area_comun/state/CLAIMS.json') -Destination (Join-Path $root '.protocol-tmp/claims-before-rollback.json') -Force\n"
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
            "  Copy-Item -LiteralPath $eventPath -Destination (Join-Path $root '.protocol-tmp/ambiguous-events-fixture.txt')\n"
            "  $repair=Join-Path $root '.protocol-tmp/repair-events.ps1'\n"
            "  $logPath=Join-Path $root '.protocol-tmp/testpeer_mailbox_cron/testpeer_mailbox_cron.log'\n"
            "  $proofPath=Join-Path $root '.protocol-tmp/ambiguous-events-after-rollback.txt'\n"
            "  Set-Content -LiteralPath $repair -Value \"`$deadline=(Get-Date).AddSeconds(10)`nwhile((Get-Date) -lt `$deadline){if((Test-Path -LiteralPath '$logPath') -and (Select-String -LiteralPath '$logPath' -Pattern 'ROLLBACK_DEFER reason=[A-Za-z0-9_]+' -Quiet)){Copy-Item -LiteralPath '$eventPath' -Destination '$proofPath' -Force; Set-Content -LiteralPath '$eventPath' -Value @('$($lines[0])','$($lines[1])','$($lines[2])') -Encoding ASCII; exit 0}; Start-Sleep -Milliseconds 25}`nexit 23\" -Encoding ASCII\n"
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
        run_nondestructive_rollback_contract()
        run_rollback_ledger_preservation_property()
        run_pregate_contract_mutants()
        run_deleted_residue_real_loop_case()
        run_large_stderr_drain_case(sandbox)
        run_expired_claim_behavior_case(sandbox)
        run_pure_append_evidence_cases(sandbox)
        run_useful_own_evidence_cases(sandbox)
        run_git_gate_contract_mutants()
        run_nul_residue_path_cases(sandbox)
        run_unreadable_head_case(sandbox, prompt, fake)
        run_unstaged_residue_case(sandbox, prompt, fake)
        run_disordered_ledger_case(sandbox, prompt)
        run_exec_running_heartbeat_case()
        run_post_delivery_timeout_case()
        run_pre_delivery_and_liveness_cases()
        run_frozen_exec_with_production_freshness_case()
        run_complete_tree_kill_case()
        (sandbox / "runtime/state/events.jsonl").write_text("", encoding="ascii")
        (sandbox / "predirty.txt").write_text("peer-content\n", encoding="ascii")
        governed_predirty = {
            "Area_comun/tasks/TASK-fixture.md": (
                "---\ntask_id: TASK-0001\nfile: Area_comun/tasks/TASK-fixture.md\n"
                "intake:\n  scope_routes:\n    - unrelated-scope.txt\n---\npeer-task-edit\n"
            ),
            "Area_comun/mailbox/archived/MSG-predirty.md": "peer-msg-edit\n",
            "Area_comun/state/CLAIMS.json": '{"seq":0,"claims":[],"peer":"edit"}\n',
            "runtime/state/events.jsonl": "",
        }
        for relative, content in governed_predirty.items():
            (sandbox / relative).write_text(content, encoding="ascii")
        try:
            result = run(
                "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUNNER),
                "-PeerId", "TestPeer", "-CoordinatorId", "Coordinator", "-Root", str(sandbox), "-PromptFile", str(prompt),
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
        assert not (sandbox / "residue.txt").exists(), f"aborted exec residue survived outside quarantine; log={log}"
        quarantined = list((sandbox / ".protocol-tmp/rollback-quarantine").glob("*/residue.txt"))
        assert len(quarantined) == 1 and quarantined[0].read_text(encoding="ascii").strip() == "residue", (
            f"aborted exec residue was not preserved in quarantine; found={quarantined!r}; log={log}"
        )
        quarantine_relative = quarantined[0].relative_to(sandbox).as_posix()
        assert f"ROLLBACK_QUARANTINED path=residue.txt quarantine_path={quarantine_relative}" in log, (
            f"successful quarantine did not log both recovery paths; log={log}"
        )
        assert (sandbox / "Area_comun/tasks/TASK-residue.md").exists(), "ambiguous residue beside signed events was destroyed"
        assert (sandbox / "Area_comun/mailbox/open/MSG-window.md").read_text(encoding="ascii").strip() == "incoming", (
            "mailbox message deposited during the exec window was quarantined"
        )
        events = (sandbox / "runtime/state/events.jsonl").read_text(encoding="ascii").splitlines()
        events_before_rollback = (
            sandbox / ".protocol-tmp/signed-events-before-rollback.jsonl"
        ).read_text(encoding="ascii").splitlines()
        claims_before_rollback = json.loads(
            (sandbox / ".protocol-tmp/claims-before-rollback.json").read_text(encoding="ascii")
        )
        claims_after_rollback = json.loads(
            (sandbox / "Area_comun/state/CLAIMS.json").read_text(encoding="ascii")
        )
        ambiguous_fixture = (sandbox / ".protocol-tmp/ambiguous-events-fixture.txt").read_text(encoding="ascii").splitlines()
        assert ambiguous_fixture[1] == "{not-json", f"ambiguous ledger fixture was not produced: {ambiguous_fixture!r}"
        ambiguous_after_rollback = (sandbox / ".protocol-tmp/ambiguous-events-after-rollback.txt").read_text(encoding="ascii").splitlines()
        assert ambiguous_after_rollback == ambiguous_fixture, (
            "ambiguous ledger changed before the repair barrier: "
            f"fixture={ambiguous_fixture!r}; after_rollback={ambiguous_after_rollback!r}; log={log}"
        )
        parsed_before_rollback = [json.loads(line) for line in events_before_rollback]
        parsed_after_rollback = [json.loads(line) for line in events]
        assert ledger_preservation_holds(
            parsed_before_rollback,
            parsed_after_rollback,
            claims_before_rollback,
            claims_after_rollback,
        ), (
            "signed ledger state changed across rollback: "
            f"before_events={parsed_before_rollback!r}; after_events={parsed_after_rollback!r}; "
            f"before_claims={claims_before_rollback!r}; after_claims={claims_after_rollback!r}; log={log}"
        )
        assert not governed_message.exists(), "signed mailbox archive deletion was rolled back"
        assert (sandbox / "Area_comun/mailbox/archived/MSG-gov.md").exists(), "signed mailbox archive addition was rolled back"
        assert (sandbox / "Area_comun/state/TASK_INDEX_ARCHIVE.json").exists(), "signed prune archive was destroyed"
        assert (sandbox / "Area_comun/decisions/DECISION-test.md").exists(), "signed decision document was destroyed"
        assert (sandbox / "ambiguous-residue.txt").exists(), "mid-log ambiguity was rolled back"
        assert (sandbox / "predirty.txt").read_text(encoding="ascii") == "exec-content\n", "worktree content was rewritten"
        assert (sandbox / "Area_comun/tasks/TASK-fixture.md").read_text(encoding="ascii") == (
            governed_predirty["Area_comun/tasks/TASK-fixture.md"]
        )
        predirty_status = run("git", "status", "--porcelain", "--", "predirty.txt", cwd=sandbox).stdout
        assert predirty_status.startswith(" M "), f"pre-exec index state was not restored: {predirty_status!r}"
        assert "outcome=unconfirmed" in log and "RETRY_SCHEDULED attempt=1" in log
        assert "outcome=transient" in log and "RETRY_SCHEDULED attempt=2" in log
        assert "RETRY_SCHEDULED attempt=3" in log
        assert conservative_rollback_defer_observed(log), (
            f"no conservative rollback defer was observed; log={log}"
        )
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
