# Analista -- veredicto TASK-0346: el censo de los 66 runners

Reviewer: Analista (independent adversarial checker)
Date: 2026-08-09 (local time UTC+2)
Task: TASK-0346 -- treinta y cinco runners de CI fuera de toda puerta de aceptacion
Instruction: `Area_comun/mailbox/open/MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0346.md`
Scope declared by Arquitecto: SOLO el hub, SIN PRODUCTO EN ALCANCE.

**Recommendation: OK-CLOSABLE**, with four residuals declared below. None of them
falsifies the measure; three of them are material for the partition that follows.

---

## 1. Canonical anchor and reproduction

| item | value |
|---|---|
| commit under review | `27581eeb6b110a03012ba29548957fb1cf394314` |
| protocol HEAD at review start | `9f88d7e1` (`27581eeb` is an ancestor) |
| clean clone | `git clone --no-hardlinks` of the hub into `D:/Aegis_Scratch/protocol/t0346-review/hub`, `git checkout 27581eeb` |
| second independent tree | `git worktree add --detach ../hub2 27581eeb` (different execution order) |
| third tree (mutation probes) | `git worktree add --detach ../hub3 27581eeb` |
| python | 3.12.10 |
| powershell | Windows PowerShell 5.1 only (pwsh 7 absent -- see residual R5) |

Nothing was measured in a hot working tree. Every verdict below is an exit code.

### Protocol gates at `27581eeb` (clean worktree `hub3`)

```
python scripts/validate_collaboration_state.py --root .   EXIT=0   OK: collaboration state is valid.
python scripts/scan_encoding.py                           EXIT=0   OK: encoding scan is clean.
python scripts/scan_domain_neutrality.py --root .         EXIT=0
python scripts/check_falsification_contracts.py --root .  EXIT=0
python runtime/protocol_replay.py --check-drift --root .  EXIT=0   PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=8246
```

---

## 2. A -- el universo recontado independientemente: 66, y las dos exclusiones son correctas

I did not read his number and check it. I re-derived the set from
`.github/workflows/validate.yml`, restricted to tokens appearing inside `run:` blocks
(indentation-scoped parser, not a whole-file grep):

```
unique runner paths (.py/.ps1) inside run: blocks = 66
total invocations                              = 67
duplicated: examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1  x2  (lines 35, 132)
non-runner examples/ tokens in run: blocks:
            examples/minimal_instance  x2  (lines 70, 78)  -- --root argument of the two validators
```

**66 confirmed.** Both declared exclusions are exactly right: the neutrality scanner is
invoked twice and counted once, and the two `minimal_instance` invocations are validators
taking a `--root`, not runners under `examples/`. All 66 exist on disk; none is wired but
missing. The order of my derivation matches rows 1..66 of his table one-for-one.

I also reproduced the framing number of the intake independently: of the 66, exactly **35**
appear nowhere in any file under `Area_comun/tasks/` -- a deliberately generous test
(anywhere in the file, not only `verification_cmd`) that still lands on 35.

## 3. B -- verificacion de los veredictos: no muestreo, corri los 66. Dos veces.

The instruction asked for a sample. A sample answers "is he lying somewhere"; running the
whole set answers "is the measure right". The set is cheap enough (~14 min sequential) that
there was no reason to accept the weaker answer.

**Full sequential run in the clean clone (`hub`), order 1..66 -- the same order CI uses:**

```
PASS 49    FAIL 17    total 66
FAIL ids: [19, 20, 24, 26, 29, 30, 33, 40, 42, 43, 44, 48, 49, 51, 52, 60, 63]
```

That is his declared post-fix saldo, **49 / 17, with the identical set of seventeen ids**.
The 48/18 initial figure follows arithmetically: runner 18 is the only one he repaired, and
I confirmed by mutation (section 5) that it fails without the repair.

**Second measurement, independent tree, different execution order** (`hub2`, 64 of the 66;
runners 3 and 64 were left to the full run for time): every verdict identical. So 64 runners
were measured twice, in two trees, in two orders, and no verdict moved.

| | |
|---|---|
| runners measured | 66 of 66 |
| verdicts reproduced | 66 of 66 |
| **verdict mismatches** | **0** |
| measured in both trees | 64 (all agreeing) |

**Answer to your first question: no. No declared PASS fails, and no declared FAIL passes.**
Not one, over the whole set, twice.

### Symptoms spot-checked against the actual output

I did not stop at exit codes; I read the failure payloads and compared them to the symptom
column.

| # | declared symptom | measured | verdict |
|---:|---|---|---|
| 19 | la muestra execute de entrega omite `obstacles` | counterexample: `semantic: delivery turn is missing the obstacles block`, sample_index 0, seed `concurrency-v1` | exact |
| 26 | prune deja drift en `TASK_INDEX_ARCHIVE.json` y `CLAIMS_ARCHIVE.json` | 1 case, both archive paths named with hot vs replay hashes | exact |
| 33 | override rechaza la clave `event_auth.method` como no soportada | `EventLogError: event_state runtime override event_auth contains unsupported keys: method` | exact |
| 40 | ocho casos, placeholder sin resolver en `scripts/memory/test_memory_db.py` | 8 cases, all `Unresolved placeholders remain in generated instance: scripts\memory\test_memory_db.py` | exact |
| 44 | `case_explicit_registry`, `AssertionError` sin mensaje | 1 case, `case_explicit_registry`, `"error": ""` | exact |
| 49 | siete casos con `AssertionError` sin mensaje | 7 cases | exact |
| 51 | `case_enriched_log_and_summary` y `case_budget_exhausted` | exactly those 2 | exact |
| 52 | tres casos | 3 | exact |
| 60 | cinco casos | 5 | exact |
| 42 | una entrega omite `obstacles`; otro caso no encuentra `eventlog_events` | 2 cases | exact |
| 43 | **cuatro** casos `fail_qa`/`checks_failed` | **8** failing cases | undercount -- R2 |
| 48 | **tres** casos con asercion vacia | **7** empty-assert cases (9 total) | undercount -- R2 |
| 63 | budget stand-in, entrega rechazada por ausencia de `obstacles` | 2 cases; one is an unrelated empty assert | partial -- R2 |
| 20 | dos sintomas | 3 cases (third is an empty assert) | partial -- R2 |
| 24 | dos fixtures sin `obstacles` **+ dos controles de limpieza por residuos bajo `.protocol-tmp/`** | 2 cases, both `missing the obstacles block`; zero mentions of `.protocol-tmp` | second half does NOT reproduce -- R3 |

## 4. C -- AC3: no hay arreglos encubiertos

`27581eeb` touches ten files. Seven are ledger/state written by `submit_intent`
(`CLAIMS`, `PROJECT_STATE`, `TASK_INDEX` and their slim views, `runtime/state/events.jsonl`,
`runtime/state/snapshot.json`) and one is the task file itself. **Exactly one code file
changes: `examples/runtime_property_cases/run_runtime_property_cases.py`, +17 lines**, all of
it the `obstacles` member and the `friction` predicate that feeds it.

No production file. No second runner. No workflow edit. None of the other seventeen failures
is touched, and none of them silently flipped: they all still fail, with the same ids.
**AC3 met.**

## 5. D -- AC1: el diagnostico es correcto, y el arreglo es portante

The conclusion ("obsolete generator, not a production defect; TASK-0259 remediation 1,
commit `c725e9bd`, made it obsolete") is independently confirmed by dates and content:

- `run_runtime_property_cases.py` last changed **2026-06-06** (`470335e2`, TASK-0051).
- `runtime/turn_validate.py` gained `validate_delivery_obstacles` / `friction_sensors` on
  **2026-07-22** in `c725e9bd`, "gate obstacles on objective friction", which the commit
  itself declares mutation-proved. Six weeks of gap. Production is the approved side.

I then checked the repair is load-bearing rather than decorative, by mutating **production
code** (the delivered fixture), not a runner's own mutants:

| mutant | expectation | measured |
|---|---|---|
| M1 -- delete the whole `obstacles` member (pre-fix state) | must FAIL | `rc=1` |
| M2 -- always emit `[]` (friction branch dead) | must FAIL | `rc=1` |
| M3 -- always emit a non-empty obstacle (clean branch dead) | -- | `rc=0` |
| M4 -- as delivered | must PASS | `rc=0`, `OK: 26 deterministic property samples passed (I1..I8)` |

M1 and M2 both die, so both branches of the predicate carry weight -- this is not an
"add `[]` everywhere" patch. **M3 surviving is correct, not a hole:** TASK-0259's contract
says a frictionless delivery *may* use `[]`, it does not forbid narration, and the
anti-theater direction is separately mutation-covered by runner 65
(`run_runtime_turn_obstacle_cases.py`, which pins `blocked`, `assign_fix`, `checks_failed`
and the revert proxy). I checked that before drawing a conclusion from M3.

**AC1 met.**

## 6. AC6 -- verificado contra el run real, y mi lectura coincide con la tuya

```
gh run view 31291178449
  headSha    a669f82d4191f8a78f64adbe6055a3eb9a1925f6
  job powershell-linux-parity   success
  job falsification-runners     success
  job validate                  failure
     step 20  Check systematic state pruning          success
     step 31  Run runtime property invariant cases    success
     step 32  Run runtime concurrency simulation ...  failure
```

`27581eeb` is an ancestor of `a669f82d`, so the repair is inside the run -- the success is
not a pre-fix accident. Step 32 is census runner 19, which AC3 forbade him to touch.

**Under the criterion you set -- own steps green, remaining failures attributed by id -- AC6
is met, and my reading is the same as yours.** I add one precision: the AC6 paragraph is not
at the anchor you cited. It was written in `527a8b0b`, after `27581eeb`. AC1 through AC5 are
all evaluable at the cited commit; AC6 is not, which is why I judged it against the Actions
run directly rather than against the tree.

## 7. E -- AC4: es una propuesta, no una implementacion; y mi opinion sobre ella

**Propone y no impone: confirmado.** No registry file, no schema, no validator, no workflow
step exists in the commit. AC5 is deferred with its reason stated and the deferral is
legitimate -- the negative cannot be written before the mechanism is chosen.

Now the opinion you asked for. **Your second question -- ata la propiedad o es otra lista a
mano -- has a split answer: one half ties a property, the other half is a list.**

**What genuinely ties.** The bidirectional derivation (every runner derived from
`validate.yml` has exactly one live row; no row points at a runner that does not exist) is a
real mechanical invariant, the same shape as the drift check. You cannot add a `run:` line
without a row, and you cannot leave a row pointing at nothing. Accept that half.

**What does not tie, and why it matters.**

1. **`acceptance_gate` declares coverage; nothing measures it.** A row says "these task
   classes must carry this gate in `verification_cmd`". Nothing verifies that any task ever
   did, or that a maker ever ran it. That is TASK-0330's finding one level up -- declared
   coverage read as executed coverage. His own text warns against using historical text
   search over closed tasks as false proof, and then does not supply the replacement proof.
2. **The `protocol_ci` SLA is decoration unless computed.** "SLA de ultima ejecucion verde"
   with nothing deriving it from real Actions data is a field someone edits. Today it would
   be violated by seventeen runners and no mechanism would say so.
3. **The escape hatch has no cost.** Any inconvenient runner can be reclassified
   `protocol_ci` with a nominal owner and the gate stays green. Nothing bounds that drift, so
   the registry converges to all-`protocol_ci` and the invariant becomes vacuous.
4. **The universe is keyed on the wrong side.** He keys the registry on "wired in CI". I
   found **16 runner scripts under `examples/*/run_*.{py,ps1}` that are not wired at all**
   (see R4). Under his key they are invisible, and deleting a `run:` line becomes a silent
   exit from the whole regime with the gate green.
5. **The proposed AC5 mutants only kill the half that works.** "Add a synthetic runner with
   no row -> must fail" tests the derivation. There is no mutant for a row that claims
   `acceptance_gate` coverage no task honours, and none for a long-past SLA. A negative that
   only exercises the working half is green by construction.

**My recommendation to you, before this goes to the operator:** take the bidirectional
derivation, and require four amendments -- (a) key the universe on "a runner file exists
under `examples/`", with wiring status as a field, not on "is wired"; (b) make
`acceptance_gate` rows provable by execution -- the gate must be injectable by the intake
validator into `verification_cmd`, so the claim is enforced at promotion rather than
asserted in a row; (c) compute the `protocol_ci` green-SLA from real Actions run data so a
stale row goes red by itself; (d) require one mutant per failure mode above, not only the
missing-row one. With those, it ties the property. Without (b) and (c), it is a
hand-maintained list with a ledger's clothing on.

---

## 8. Residuals declared

**R1 -- el arreglo del AC1 corrige las tres instancias, no la clase.** The fixture's
`friction` predicate covers `{changes_requested, qa_failed, architect_review}`,
`{reject_review, fail_qa}` and `checks_failed`. Production's `friction_sensors` additionally
treats `task_status:blocked`, `review_qa:assign_fix` and the revert prose proxy as friction.
Measured directly against production:

```
to=blocked            obstacles=0  sensors=task_status:blocked
                      errors=['semantic: objective friction (task_status:blocked) requires non-empty obstacles']
event=assign_fix      obstacles=0  sensors=review_qa:assign_fix
                      errors=['semantic: objective friction (review_qa:assign_fix) requires non-empty obstacles']
to=in_review clean    obstacles=0  sensors=-                    errors=[]
to=qa_failed          obstacles=1  sensors=qa_failed,fail_qa,checks_failed   errors=[]
```

Today's sample set never reaches `blocked` or `assign_fix`, so the runner is green and the
verdict stands. Add one such sample and it breaks again for exactly the same reason. Not an
AC failure -- no AC asked for class coverage -- but this is the drift that will recur.
The durable fix is a parity check between the fixture's sensor set and production's, with a
negative that dies when production's set grows and the fixture's does not.

**R2 -- la columna de sintomas subestima el trabajo en cuatro filas.** Verdicts are right;
counts are not. Row 43 says four cases and there are eight; row 48 says three empty asserts
and there are seven (of nine total); rows 63 and 20 each describe one fewer case than
measured. Whoever partitions those four will under-scope by roughly half.

**R3 -- la segunda mitad del sintoma de la fila 24 no reproduce, en ningun arbol ni orden.**
Declared: "ademas fallan dos controles de limpieza por residuos bajo `.protocol-tmp/`".
Measured in the full sequential run (same order as CI and as his census) and again in the
second tree: exactly two failing cases, both `delivery turn is missing the obstacles block`,
and **zero occurrences of `.protocol-tmp` anywhere in the runner's output**. That symptom is
a property of the tree his census ran in -- accumulated residue from earlier runners -- not
of the runner. A census taken in a residue-carrying tree records contamination as a runner
defect. Hand this to whoever partitions 24 or they will chase a phantom for half of it, and
consider requiring future censuses to run each runner from a residue-free tree.

**R4 -- 16 runners bajo `examples/` no estan cableados en CI en absoluto.** Correctly outside
AC2's universe, which is the CI-wired set, but decisive for AC4:
`agent_signature_cases`, `analysis_close_cases`, `anchor_cases`, `chain_cases`,
`context_cost_cases`, `context_policy_cases`, `improvement_offer_cases`,
`mailbox_archive_cases`, `mailbox_hygiene_cases`, `mailbox_report_cases`,
`malformed_json_cases`, `prune_state_cases`, `row_scoped_claim_cases`,
`runtime_plan_approval_cases`, `scratch_discipline_cases`, `slim_view_cases`.
Nobody runs these and CI does not either.

**R5 -- la evidencia del AC1 vive fuera del estado canonico.** The task file says the
conclusion was recorded in `personal/Codex/DIAG-TASK-0346-before-fix-20260809.md` before the
edit. That file is **untracked**: a clean clone at `27581eeb` cannot see it. Its mtime
(04:03:05) does precede the fix commit (04:36:29) and its content is correct and detailed, so
I accept the claim -- but the ordering that AC1 demands ("no se toca nada antes de esa
conclusion") is not provable from canonical state, because the diagnosis text and the fix
landed in the same commit. Cheap to avoid next time: commit the diagnosis first.

**R6 -- paridad de plataforma no medida.** Only Windows PowerShell 5.1 was available here, so
the four `.ps1` runners (1, 10, 11, 62) were measured on 5.1, not on pwsh 7. All four pass.
Runner 5 declares its own pwsh-7 POSIX parity as unmeasured locally, matching his note.

---

## 9. Closure

The deliverable of this task is the measure, and the measure holds. The universe is 66 and I
re-derived it rather than accepted it; both exclusions are correct; 66 of 66 verdicts
reproduce in a clean clone, 64 of them twice in two trees and two orders, with zero
mismatches and the identical set of seventeen failing ids; the AC1 diagnosis is correct on
dates and content and its repair dies under two independent mutations; the diff contains
exactly one code file and no hidden fixes; AC4 is a proposal and not an implementation; and
AC6 is real in a real Actions run that contains the fix.

**OK-CLOSABLE.** Route R1, R2, R3 and R4 as separate partitioned items -- R3 before anyone
picks up runner 24, and R4 before the AC4 mechanism is specified, since it changes the key.

-- Analista
