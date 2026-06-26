# Changelog

All notable changes to the **multi_agent_project_protocol** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
as scoped for a *protocol* (not a library): see
[`Area_comun/decisions/DECISION-0001-versionado.md`](Area_comun/decisions/DECISION-0001-versionado.md)
for what counts as MAJOR / MINOR / PATCH here.

> **Scope note.** Versions in this file describe **the protocol itself** (its structure,
> lifecycle, required fields, templates and validator). Each *instance* declares which protocol
> version it follows via `protocol_version` in its `protocol.config.json`. The protocol is **not**
> pushed automatically to instances; an instance adopts a new version through a decision of its own.

## [1.17.0] - 2026-06-26
> Note: capabilities shipped; the live instance `protocol_version` stays **1.14.0** under #4 (epoch versioning,
> DECISION-0047) -- no config change, no re-genesis. New registries (skills) live **outside** `protocol.config.json`.

### Added
- **Skills mechanism, FLOOR skills Fase 1 (DECISION-0061 / SPEC-0096 / TASK-0183).** New domain-neutral `skills/`
  layer mirroring `connectors/`: a registry `skills/skills.config.json` **outside** `protocol.config.json`
  (off-by-default per skill) + a deterministic, READ-ONLY cold-start loader. A skill is a governed doc the agent
  reads at cold-start to acquire a procedure; the loader grants no authority, imports no ledger/event-log writers,
  and rejects domain content placed in the neutral core (fail-closed). `scan_domain_neutrality` covers `skills/**`;
  CI runs `examples/skills_loader_cases`. Genesis/#4 untouched.
- **Three neutral profile skills, FLOOR skills Fase 1 pieza 2 (DECISION-0061 / SPEC-0097 / TASK-0184).** Minimal
  `profiles/financiero_presupuesto/` shell hosting `ddl-conventions`, `business-rule-vs-legacy`, and
  `migration-verification` skill docs (content in the profile, never the core), registered off-by-default; the
  loader resolves them under the profile path. No domain policy added to the core.

### Added (governance; implementation in the Zeus-protocol product repo, DECISION-0050)
- **Architect console (DECISION-0062) and its runtime launcher (DECISION-0063).** Live Operator<->Architect console:
  a persistent runtime bridge + conversational UI with streaming + hardened, redacted audit (outside #4) + a
  launcher (the bridge's spawned command) running an interactive Architect with its **existing** identity. Hard
  invariants: no-bypass (every state mutation still goes through `submit_intent`), runtime-only (never reconfigures
  identity/keys/registry), single session, off-by-default + operator-present, PII-redacted audit that never reaches
  the #4 event log. Code/tests live in `Zeus-protocol`; only the governance (DECISIONs/SPECs) is recorded here.

## [1.16.0] - 2026-06-22
> Note: capability documented; the live instance `protocol_version` stays **1.14.0** under #4 (epoch
> versioning, DECISION-0047) -- no config change, no re-genesis.

### Added
- **Architect agent-activation faculty (DECISION-0057).** The Architect/orchestrator role may activate
  (launch/relaunch) and stand-down the agent runtimes it needs to fulfil a queued task, and stops idle
  agents for cost control. Runtime-only (never reconfigures identity/keys/registry); honours an explicit
  operator stop; activation grants no live/risk capability (live-use, #4 config, external pushes stay
  separate operator GOs); single instance; audited. AGENTS.md s.3 roles updated.
- **Extractor agent registration design (DECISION-0058).** New `Extractor` agent for document extraction
  in file-ingestion v2, backed by a LOCAL VLM (zero external egress; file content never leaves the host).
  Chunked design (per-page/per-chunk -> bounded context per call, scales to any document size; accumulate
  + dedup candidates), egress boundary = localhost endpoint only (allowlisted in the AC46 deny-all guard),
  minimal tool_policy (read upload-store + write no-ledger candidates only), honest authorship (signs its
  own candidates), human PII gate (AC43) unchanged, off-by-default. Registration = governed
  re-genesis-boundary ceremony (registry + keypair). Design accepted; implementation + ceremony gated.

## [1.15.0] - 2026-06-19
> Note: capability implemented + TASK-0121 done, but the live instance `protocol_version` stays
> **1.14.0**: under #4 (chain ON) the genesis hash = `canonical_hash(protocol.config.json)`, so bumping
> the version would invalidate `chain.genesis`; a real version bump needs a coordinated
> re-genesis-boundary. The connector registry lives outside `protocol.config.json` precisely to avoid
> touching genesis.

### Added
- **FLOOR Fase 2 piece 2 in review (DECISION-0048 / SPEC-0087 / TASK-0125):** added a domain-neutral
  `ci_readonly` connector for reading CI run/job status, conclusion, and summaries through a
  deny-by-default classifier. Dispatch, rerun, cancel, approve, secret/variable mutation, workflow edits,
  shell-injection, multi-command, unknown-verb, and unsafe-argument vectors are rejected before backend
  access. Registry entry `fixture-ci-ro` lives in `connectors/connectors.config.json`, outside
  `protocol.config.json`, defaults to `enabled:false`, and live use remains fail-closed pending later s9
  least-privilege verification plus operator GO. Golden `examples/connector_ci_cases` covers trust
  boundary, fixture reads, 11 negative vectors with 0 backend calls, no authority imports/writes,
  off-by-default fail-closed, registry outside protocol config, and PII-like fixture data staying in memory.
- **FLOOR Fase 2 piece 1 in review (DECISION-0048 / SPEC-0085 / TASK-0123):** added a domain-neutral
  `git_readonly` inspection connector governed by deny-by-default operation classification. Allowed verbs
  are limited to `status`, `log`, `diff`, `show`, `ls-files`, `rev-parse`, and `blame`; mutating,
  non-allowlisted, shell-injection, multi-command, and unsafe-argument vectors are rejected before backend
  access. The connector registry entry lives in `connectors/connectors.config.json`, outside
  `protocol.config.json`, defaults to `enabled:false`, and live use remains fail-closed pending later s9
  least-privilege verification plus operator GO. Golden `examples/connector_git_cases` covers trust
  boundary, fixture reads, 10 negative vectors with 0 backend calls, no authority imports/writes,
  off-by-default fail-closed, registry outside protocol config, and PII-like fixture data staying in memory.
- **Carril B piece 1 implemented (DECISION-0044 / SPEC-0083 / TASK-0121):** added a domain-neutral
  `connectors/` layer for read-only external-source adapters with explicit `trust_boundary`,
  deny-by-default classification, and the principle that a connector grants no authority. First adapter:
  `sqlserver_readonly` with a deterministic `FixtureBackend`. The connector registry lives in
  `connectors/connectors.config.json` outside `protocol.config.json`, defaults to `enabled:false`, and the
  live path fails closed without attempting a connection. Golden
  `examples/connector_sqlserver_readonly_cases` covers trust boundary, fixture reads, 7 negative vectors,
  no ledger/event-log writer imports, no state/event-log writes, off-by-default live fail-closed, registry
  outside protocol config, and PII-like data staying in memory only. CI runs the suite and
  `scan_domain_neutrality` now includes `connectors/`. Live use against a real source remains gated by a
  later operator GO plus server-side least-privilege verification.

## [1.14.0] - 2026-06-19

### Fixed
- **Replay/snapshot now secret-independent (DECISION-0046 / SPEC-0084 / TASK-0122).** Enabling #4 surfaced
  that `replay_events` treated `unresolved_key` / `missing_key` (secret absent in this checkout =
  environment, not a security finding) the same as `invalid_signature` / `missing_signature` (real tamper):
  a state-mutating rejection + skip. That made the materialized state depend on whether the gitignored
  secrets were present, so a clean clone without secrets could not reproduce the live state and
  `validate_collaboration_state` failed there. Fix: partition the reasons
  (`EVENT_AUTH_UNVERIFIABLE_REASONS` vs `EVENT_AUTH_TAMPER_REASONS`); UNVERIFIABLE reasons apply the event
  normally without a state rejection, TAMPER still rejects+skips. Canonical state is now secret-independent
  (`validate --root .` exit 0 from a clean clone WITHOUT secrets AND from the live instance WITH secrets,
  same hash); tamper detection unchanged. Golden `examples/replay_secret_independent_cases` (in CI).
  maker=Arquitecto, checker=Codex (AC1-AC6 reproduced green). #4 stays ON; T0 boundary (DECISION-0045)
  intact.

### Changed (live instance only; not the neutral protocol/template)
- **#4 security stack ACTIVATED (chain + agent_signatures + anchor + event_auth ON; DECISION-0045).** The
  live instance now signs/chains/anchors its event log: Ed25519 per-agent signatures (public keys in
  `signature_config.public_keys`, privates wrapper-side outside the repo; A2 independence declared WEAK for
  this pilot — all keypairs minted in one ceremony), HMAC `event_auth` via gitignored `secret_file`
  (DECISION-0043 loader), and a git-remote anchor to a dedicated sibling repo `D:\Agentes\audit-anchor`
  (A3 independence WEAK — same disk, declared). Pilot verified GREEN in a clean clone before any canonical
  write: AC2 health 1.0 (>=0.99), AC3 6/6 negative vectors rejected, AC5 rollback byte-equivalent, live
  smoke (real keys sign+chain + anchor wrote), full validator + drift 0.
- **One-time T0 boundary; pre-T0 history sealed (DECISION-0045).** A prior sanctioned #4 pilot had written
  immutable artifacts to the live event log, structurally blocking a clean re-enable. The operative ledger
  of the thesis dataset now starts fresh at T0; pre-T0 history (seq 1-671) is preserved in git (commit
  `94d2e58`) + a cold export `pre_t0_ledger_seal/` (sha256 recorded) outside the operative validation path,
  and cryptographically bound into the T0 genesis via `protocol.config.json.pre_t0_provenance` +
  `chain_manifest.json`. **TASK-0117 done.** Enforced lesson: no #4 pilot/ceremony ever runs against the
  live log again — always a throwaway copy.

## [1.13.0] - 2026-06-19
> Correction (2026-06-26): this block was previously mislabeled `## [Unreleased]` while sitting between [1.14.0] and
> [1.12.0]. Its content shipped in the live instance pre-#4 (chain still OFF). Numbered here to restore CHANGELOG
> order and version truth (audit-first coherence); no content was changed.

### Added
- **TASK-0120 implementation (SPEC-0082):** `event_auth` HMAC secrets can now be resolved from
  `secret_file` or `secret_env` at signing/verification time without mutating `read_protocol_config`.
  Resolution is fail-closed, path-safe, root-explicit, and covered by `event_auth_secret_resolution_cases`;
  the validator rejects literal event-auth secrets for live actors in committed config. #4 remains OFF.
- **TASK-0117 harness build (SPEC-0081, #4 still OFF):** added deterministic attestation health cases
  (AC1/AC2 N=20/AC4/AC5), six binary negative attestation goldens (AC3), and read-only enforcement
  negative cases for DECISION-0041. CI runs the new suites; no pilot or flag activation is included.

### Changed (live instance only; not the neutral protocol/template)
- **Ledger actor renamed `Claude` -> `Arquitecto`** (operator order). `protocol.config.json`
  `agent_roles.architect = "Arquitecto"`; `runtime/regenesis.py --actor-id Arquitecto` wrote a fresh
  genesis from hot state (drift 0, history preserved). `submit_intent` now requires `--actor-id Arquitecto`
  (capabilities `[architect, reviewer, orchestrator, qa]`); the analyst voice signs `Analista`. Generic
  template defaults (`context.DEFAULT_AGENT_ROLES`, `router` fallback) stay `Claude` — they are not the
  live instance. No protocol/template/contract change; isolated goldens unaffected.

## [1.12.0] - 2026-06-19

### Added
- **DECISION-0043 + SPEC-0082 + TASK-0120 (cargador HMAC `event_auth` fuera del repo):** resolucion del
  secreto HMAC de `event_auth` por referencia (`secret_file` keyfile gitignored / `secret_env`), fuera del
  config commiteado, como precondicion de activacion de #4 (SPEC-0081 AC1, capa HMAC). El secreto resuelto
  no entra a genesis/canonical_json/prev_hash; fail-closed ante referencia irresoluble; gate dedicado de
  no-literal-commiteado; path-safety con allowlist. La privada Ed25519 sigue wrapper-side. Aditivo, neutral,
  off-by-default; TASK-0120 queda `ready` (owner Codex) para implementar. **#4 permanece OFF**
  (chain/agent_signatures/anchor/event_auth = false).

## [1.11.0] - 2026-06-19

### Added
- **TASK-0119 / DECISION-0042 enforcement:** `submit_intent` now rejects `claim acquire` scopes under
  `Area_comun/mailbox/` unless the entry names a concrete `MSG-*.md` file, and both validators flag active
  mailbox directory claims with `mailbox claim must be file-scoped: <entry>`. Released historical claims are
  not re-failed. Golden coverage added in `examples/mailbox_claim_scope_cases` and CI.

## [1.10.0] - 2026-06-19

**Carril A (instrumentacion de tesis del modulo-app de Presupuesto) promovido - documental/gateado; #4 sigue OFF.**
Aditivo, neutral de dominio. Base: GO de promocion del operador + OK de Codex (re-verificacion aprobable) +
cruce read-only del asistente; convergencia de tres revisiones independientes.

### Added
- **DECISION-0039** - activacion gateada de la atestacion de autoria (#4), off->piloto->on; referencia
  DECISION-0029 (no rediseno). **No enciende #4** (flags OFF); el encendido es un GO posterior tras el
  piloto. Implementacion gateada: TASK-0117.
- **SPEC-0081** - criterios de la activacion #4: provisioning (AC1: public_keys + event_auth.keys + anchor
  remoto), salud >=99% (AC2, denominador independiente, NO seguridad), prueba negativa binaria (AC3, 6
  vectores, golden por vector), rollback (AC5).
- **DECISION-0040** - GATE-DATASET: base legal (Ley 1581/2012 + RGPD; ausencia de persona fisica en el
  dataset), dos planos (estructural para el sujeto-por-hash + disciplinario para el predicado), DPIA-lite
  (incluye al operador humano), verificacion de ToS. Tarea diferida DEF-PII (TASK-0118) antes de #2/#3.
- **DECISION-0041** - precondicion de acoplamiento read-only REAL del satelite (verificada por Codex, s.9,
  con prueba negativa objetiva) antes de cualquier lectura viva; referencia DECISION-0035 (no la redecide).
- **DECISION-0042** - claims sobre el mailbox deben ser file-scoped (prohibido dir-level del canal
  compartido); guard de enforcement = TASK-0119. Addendum a DECISION-0020 tras un incidente real.
- **TASK-0117/0118/0119** (owner Codex, proposed, gateadas): activacion #4 / DEF-PII / guard mailbox.

### Notes
- Off-by-default intacto en template y config vivo; #4 (chain/agent_signatures/anchor/event_auth) sigue
  OFF. protocol_version 1.9.3 -> 1.10.0. Drift 0; validador/encoding/neutralidad verdes.

## [1.9.3] — 2026-06-15

**Unique run-id per real run (TASK-0096, trio 3/3 — closes the OFF-PILOT trio).** Additive, OFF-PILOT,
domain-neutral. No gate/claim semantics changed; replay/recorded paths stay deterministic.

### Fixed
- `runtime/orchestrator.py`: the real (subprocess) LLM invoker now **requires an explicit `--run-id`** and
  **rejects a run-id whose run-log already exists** (`real_invoker_run_id_error`), so two real runs can
  neither share a run-log nor accumulate onto a prior one; replay/recorded keep their deterministic
  `default_run_id`. Goldens assert it: `runtime_real_adapter_cases` (fresh-run-id required, invoker does not
  run otherwise) and `supervised_autonomy_cases` (two consecutive real runs use distinct logs,
  `turns_total==1` each — no cross-run metric aggregation — one line per log). No `Date.now()`/random on
  deterministic paths. Independent adversarial pass: Analista CONCURRO. Suites green (llm_adapter,
  real_adapter, supervised_autonomy, runtime_loop, budget, observability, cost_attribution);
  validator/encoding/neutrality clean; drift 0.

## [1.9.2] — 2026-06-15

**Self-consistent runtime turn commits (TASK-0095, trio 2/3).** Additive, OFF-PILOT, domain-neutral. No
gate/claim semantics changed.

### Fixed
- `runtime/apply.py`: `apply_gate_and_commit` now derives the task `.md` paths mutated by the turn's
  transitions (`task_file_commit_paths`, scoped to the turn's `task_status`/`task_upsert` ids — no
  over-inclusion) and includes them in `commit_turn`. After a turn with a transition, the committed
  snapshot keeps `TASK_INDEX` and the task `.md` aligned (no transient dirty `.md`). Golden
  `runtime_apply_cases` asserts the working tree is clean for the task `.md` and HEAD carries the new
  status. Regressions green (runtime_loop, real_adapter, intent_flow).

## [1.9.1] — 2026-06-15

**Release LF-reproducibility scoped to future releases (v1.2.0+); v1.1.0 documented as pre-normalization
(DECISION-0037, TASK-0100).** Additive, OFF-PILOT, domain-neutral. The signed v1.1.0 manifest/signature are
**untouched**.

### Added
- Root **`.gitattributes`** (`* text=auto eol=lf` + binary patterns) so release checkouts normalize to LF
  cross-platform from **v1.2.0 onward**. Verified: `git add --renormalize .` on HEAD changes no
  SBOM-included bytes (signature safe).
- **`dist/v1.1.0/KNOWN_LIMITATIONS.md`** — honest, non-euphemistic record that v1.1.0 is not LF-reproducible
  from a clean checkout: byte classification of the 757 SBOM files vs the recorded commit 04436c3 = **616
  LF / 127 CRLF / 14 non-EOL**; the 14 non-EOL imply the manifest was generated from a **dirty working
  tree** (not a clean checkout), and `runtime/protocol_replay.py` is **irreproducible from refs**;
  `verify.integrity.json ok:true` is emitter-local, not third-party reproducibility. Corrects the false
  SPEC-0075 premise (127 blobs were CRLF at the release commit; true only for current HEAD).
- **`verify_release.py`**: informational `release_scope` note for the pre-normalization protocol release
  1.1.0. It does **not** change `ok`, does **not** suppress diffs, and does **not** touch the signed
  manifest.

### Notes
- v1.1.0's signature/manifest are **not** regenerated or re-signed (option B rejected: the original tree is
  partially lost, so re-signing would fabricate a clean v1.1.0 that never existed — worse for integrity).
  A `verify_release` of v1.1.0 failing under a clean LF checkout is **expected and documented**.
- The two honest figures measure different bases: the **616/127/14** classification is vs the recorded
  commit 04436c3, while `verify_release`'s **diff.changed (~30)** is vs the live working tree (HEAD, already
  LF). Both correct.
- No change to #3 (cost-attribution flag), #4 (chain/signatures/anchor) or SA.4.

## [1.9.0] — 2026-06-14

**Minimal narration hardened to a uniform hard rule for all agents (DECISION-0036).** Additive,
documentation-only; sharpens the DECISION-0005 narration addendum. Domain-neutral.

### Changed
- `AGENTS.md` §7 + `AGENTS.template.md` §7: the minimal-narration bullet now requires **zero
  intra-execution narration** (no prose between tool calls; process reasoning to the internal channel;
  user-facing output reserved for one self-contained final report), binding **all agents uniformly**, with
  unchanged carve-outs (substantive content where the reasoning IS the deliverable + one blocking
  question) and a flaggable-process-anomaly clause (DECISION-0018). Enforcement is normative + peer-flag,
  not an automated gate (narration is model output, not validator-gateable today).

## [1.8.0] — 2026-06-14

**Research satellite authorized: protocol_research (read-only, unidirectional) — structure + scaffolding
(DECISION-0035).** Additive, documentation-only in the Core; domain-neutral; no Core behavior change.

### Added
- **DECISION-0035** authorizes a SEPARATE, read-only research repo `protocol_research/` (sibling at
  `d:\Agentes\protocol_research`). Documents the UNIDIRECTIONAL coupling (satellite reads the Core via
  `../multi_agent_project_protocol`; does not write the Core — sustained by separate-repo + read-only
  convention + static inspection, not sandboxed in this phase; Core has no dependency on the satellite),
  names the hard-stop gates **GATE-DATASET** (legal: #1 citability/publication + #2/#3 production),
  **GATE-INST** (institutional: ablation/TFM) and **PRE-REG** (pre-registration), and scopes #1
  (MAST-over-own-history dataset, INTERNAL — internal use needs no gate — comparability to MAST-Data
  reported as a limit, not "citable" until GATE-DATASET).
- Scope = STRUCTURE + SCAFFOLDING only: the satellite runs nothing and publishes nothing. Stubs for
  #2 (PROV exporter), #3 (cost-attribution feed) and the ablation/TFM harness are OFF and non-executable
  (inert `.py.stub`), each behind its named gate.

### Notes
- The satellite is a separate repository; it is not committed into the Core. Populating/executing/
  publishing any component requires clearing its gate plus a decision of its own. No change to #3 (flag),
  #4 (chain/signatures/anchor) or SA.4.

## [1.7.0] — 2026-06-14

**Fase 0 (E5+E6): named failure-mode catalog + loop governor (DECISION-0034).** Additive,
documentation-only, domain-neutral. No runtime behavior change.

### Added
- **`Area_comun/protocol/FAILURE_MODES.md`** — named catalog mapping the 14 MAST failure modes
  (Cemri et al. 2025) to this protocol's mitigated operational incidents and their guardrails
  (drift/DECISION-0017, anomaly/0018, collision/0020, liveness/0013, budget/deadline, dirty-tree,
  escalation, schema, maker!=checker). Honest scope: MAST *applied to protocol incidents*, not 1:1 with
  MAST-Data; the `Incident?` column cites a concrete incident or marks the guardrail preventive-only (no
  tally); modes with no own incident (FM-2.1, FM-2.6) are marked, and MAST is noted as the vocabulary,
  not the exhaustive failure surface (non-MAST guards: encoding/DECISION-0012, neutrality, secrets).
  Linked from onboarding (`Area_comun/README.md`) and the review guide.
- **Loop governor "Does It Deserve a Loop?"** in `Area_comun/protocol/TASK_PROTOCOL.md` — mandatory
  4-condition pre-check (recurrence / objective verification / budget absorbs retry / senior tools) +
  30-second check before building any discovery scanner or autonomy flow; a non-optional
  termination/convergence requirement (explicit bound or the SA.4 budget/deadline/liveness envelope); a
  scope-in-time clause (binds future expansions, does not revoke authority already granted, e.g. the SA.4
  pilot DECISION-0027); roadmap rule "no E3 before E6" and standing pre-check for SA.4 expansion.

### Notes
- `#1 / protocol_research` (empirical MAST study over project history) remains deferred to its own
  decision. No change to #3 (cost-attribution flag), #4 (chain/signatures/anchor) or SA.4.

## [1.6.0] — 2026-06-14

**Cost-attribution per handoff/decision/agent, activated in the live instance (DECISION-0033), plus a
latent chain+auth fix (TASK-0113).** Additive over 1.5.0; off-by-default in the shipped template.

### Added
- **`cost.attributed` annotation event (runtime/eventlog.py, budget.py, metrics.py).** Imputes producer
  tokens per **handoff / decision / agent**, two-plane (protocol plane carries only the metric + a
  `subject_hash`; the payload is referenced by hash, never copied). The event is `applied:false`, so
  `replay_protocol_state` skips it — no state mutation, no drift — and it is emitted outside
  `submit_intent` (annotation, like attestations/anchors). Off-by-default via
  `metrics.cost_attribution_enabled` (absent ⇒ false). Schema hardening (adversarial pass-3): canonical
  `subject` per dimension (`{handoff_id}`/`{decision_id}`/`{agent_id}`, no prose) so logically-equal
  emissions hash identically; `cost_unit`/`cost_schema` tags (`tokens_total`/`"2"`) with the summarizer
  rejecting rows that lack them; `subject_hash` documented as a **pseudonym** (RGPD/Ley 1581), not
  anonymous; `actor` restricted to an agent vocabulary. `cost_tokens` = producer total (self-reported);
  `context_tokens` = the runtime's `assembled_context_tokens` input proxy (chars/divisor), captured per
  handoff in the immutable corpus. Golden `examples/runtime_cost_attribution_cases` + CI.

### Changed
- **Live instance:** `metrics.cost_attribution_enabled=true` (template stays false). Hot-verified on a
  real handoff (recorded == an independently measured count, not a literal), drift 0, replay==hot.
- **`runtime/eventlog.py::event_without_chain_fields` now excludes `event_auth` (TASK-0113, SPEC-0080).**
  Fixes a latent bug where, with `chain_enabled` **and** `event_auth.enabled` both on, `append_event`
  computed `prev_hash` without `event_auth` while `validate_chain` recomputed with it — invalidating the
  chain. The signature still covers `prev_hash`. Golden `examples/chain_auth_combined_cases` (chain +
  auth + cost together, plus a tampering-detected negative). No live exposure (both flags off-by-default).

## [1.5.0] — 2026-06-13

**The architect/orchestrator can close its own analysis-tasks (DECISION-0032).** Additive over 1.4.0; a
state-authorization relaxation scoped to `type==analysis` owned by the actor. Other task types and
analysis-tasks owned by someone else keep requiring `implementer`.

### Changed
- **`task_status_capability` (runtime/submit_intent.py):** for `type==analysis` tasks owned by the actor,
  transitions to `in_review`/`done`/`blocked` accept `{orchestrator, architect}` instead of requiring
  `implementer`. Fixes the gap where the architect (no implementer capability) could not close its own
  analysis-tasks via the standard `in_progress → in_review → done` path (seen in TASK-0109/0110). The
  mutation still flows through `submit_intent` (single-writer, DECISION-0022); maker≠checker for
  implementations is unchanged. Golden: `examples/analysis_close_cases/` (GC-1..GC-4). (DECISION-0032)
- **TASK-0109 closed to `done`** via the new capability (validating the fix end-to-end).

## [1.4.0] — 2026-06-13

**Measured activation of context compaction in the live instance (SPEC-0078 / TASK-0106).** Additive and
reversible over 1.3.0; turns the off-by-default compaction policy ON in this instance with a threshold
derived from our own baseline (measure, don't assume — DECISION-0008). The shipped master
`protocol.config.template.json` stays off-by-default.

### Changed
- **`runtime.context_policy.compaction_enabled=true`** and
  **`assembled_context_warn_tokens=16000`** in the live `protocol.config.json`. Threshold derived from the
  observed `assembled_context_tokens` distribution (baseline TASK-0106 `8494`/`13598` + live `8168`; max
  ~13.6k → max +~18% margin ≈ 16000, below the 20000 cold-start hard budget) so warning/fallback only
  fires on genuine bloat. Criterion documented in SPEC-0078 §2.1-bis. Measured effect: per-turn assembled
  context drops ~59% (full `20021` → assembled `8168`); consolidation is structural (no LLM in the hot
  path); goldens GC-1..GC-9 green. `subagents_enabled` stays `false` (DECISION-0024 needs separate GO).
  **Reversible:** `compaction_enabled=false` restores legacy behavior.

> **Scope note.** This affects **runtime turns** (the context the runtime assembles per turn). The effect
> on interactive sessions arrives when the loop directs turns; the loop is currently off.

## [1.3.0] — 2026-06-13

**Minimal intra-execution narration (DECISION-0005 addendum).** Additive and domain-neutral over 1.2.0;
a behavioral style rule, no code or format change. Derived from the TASK-0110 A/B measurement
(measure, don't assume — DECISION-0008).

### Added
- **Minimal-narration golden rule (DECISION-0005 addendum 2026-06-13).** Agents minimize step-by-step
  process narration during execution; the final report/handoff stays self-contained and auditable and
  prevails. Bounded scope: does NOT apply to substantive content (analysis, review voices, specs,
  decisions, where the reasoning IS the deliverable); brevity never sacrifices completeness or
  auditability (preserves DECISION-0018/0020 and CLAUDE.md rule 7). Landed as a `Collaboration Protocol`
  bullet in `AGENTS.md` §7 and `AGENTS.template.md` §7. Evidence: TASK-0110 (reduces output substantially
  without loss of correctness/coverage; caveats: tiny tasks = ceiling, output proxy chars/4, one run per
  cell — no percentage recorded as a promise).

## [1.2.0] — 2026-06-13

**Cross-signed tamper-evidence (DECISION-0029) + slim-views just-in-time cold-start
(DECISION-0030).** Additive and domain-neutral over 1.1.0; every previously valid turn report
stays valid and the new capabilities ship off-by-default in the templates. This MINOR records the
implementation of the three independent-signer audit pieces (chained `prev_hash`, per-agent
attestation, external anchoring) and the live activation of derived slim-views that cut this
instance's cold-start from ~17.4k to ~8.8k tokens.

### Added
- **Chained `prev_hash` event log (DECISION-0029 piece 2a).** Each event carries
  `prev_hash = SHA256(event || prev)`; genesis = `SHA256(canonical_json(protocol.config.json))`.
  `validate_chain` detects alteration, insertion, deletion and reordering, with an archive-boundary
  anchor so pruning preserves verifiability. Flag `event_state.chain_enabled` (default false).
  (TASK-0101 / SPEC-0076)
- **Per-agent authorship attestation (DECISION-0029 piece 2b).** `agent.attestation` events with an
  in-toto-compatible predicate and a configurable, vendor-neutral signature backend
  (`local-ed25519` / keyless-OIDC / external-command). `validate_agent_signatures` enforces
  maker!=checker reviewer attestations. No private keys in the repo (public keys only); missing
  `cryptography` falls back to `backend_unavailable`. Flag `event_state.agent_signatures_enabled`
  (default false). (TASK-0102 / SPEC-0071)
- **External chain anchoring (DECISION-0029 piece 2c).** Periodic `chain.anchor` of the head digest
  to a write-independent medium (git-remote default, transparency-log, or RFC 3161 TSA);
  `verify_anchor_monotonicity` is anti-rollback. `remote_url` empty by default (no secrets); a real
  remote fails closed. Flag `event_state.anchor_enabled` (default false). (TASK-0103 / SPEC-0072)
- **Slim-views derived state + just-in-time cold-start (DECISION-0030).** The runtime materializes
  compact, regenerable projections `TASK_INDEX.slim.json`, `PROJECT_STATE.slim.json`,
  `CLAIMS.slim.json` (hot statuses only, minimal fields) in the same atomic batch as the full views;
  `slim_view_drift` is folded into the drift gate so a slim can never diverge from the snapshot.
  `measure_context_cost` reports cold-start full vs slim. Flag `event_state.slim_views_enabled`.
  (TASK-0105 / SPEC-0077)

### Changed
- **Live instance cold-start promoted to slim-views.** `event_state.slim_views_enabled=true` and
  `token_cost.coldstart_globs` now point to the `*.slim.json` projections (full views and the event
  log are no longer loaded at start). Measured before/after: **~17.4k -> ~8.8k tokens** (<10k target
  met, real not projected). Gated promotion per DECISION-0008/0014; reversible (flag -> false +
  globs -> full). The shipped master `protocol.config.template.json` stays conservative
  (`slim_views_enabled=false`, `coldstart_globs` on full views): new instances measure first.

### Notes
- All four flags ship **off-by-default** in the templates; legacy logs without `prev_hash`/
  signatures/anchors keep validating. Goldens: `chain_cases` 10/10, `agent_signature_cases` 10/10,
  `anchor_cases` 10/10, `slim_view_cases` 7/7.

## [1.1.0] — 2026-06-10

**Runtime-authoritative activation + supervised-autonomy SA.4 pilot + operator human guide and
authentic release signing.** Additive and domain-neutral over 1.0.0; every previously valid turn
report stays valid and the shipped templates stay off-by-default. This MINOR records the live
activation of the protocol-state event-log writer, the first bounded real-invoker autonomy pilot,
the neutral operator human guide with its deterministic HTML generator, and a configurable
external-command release-signing backend — all gated and reversible.

### Added
- **Live single-writer (event-sourced state).** `event_state.enforce=true` then
  `authoritative=true` activated in the live instance: the event log is the source of truth, state
  is reconstructed by `replay(log)`, and manual edits to `Area_comun/state/*.json` hard-fail as
  drift (B.3). All ledger transitions now flow through `runtime/submit_intent.py`. Reversible
  (flags → false restores shadow). (DECISION-0022)
- **New `submit_intent` intents** `project_narrative` (updates `next_actions`/`risks`/
  `open_questions`) and `protocol_prune` (retires terminal hot entries), so narrative updates and
  pruning run through `submit_intent` under enforce. (TASK-0085 / SPEC-0066)
- **Config guard `event_state_config_error`**: rejects an incoherent `event_state` chain
  (`authoritative⇒enforce⇒materialize⇒enabled`, runtime tier) in the validator, `submit_intent`
  and `apply` — kills the "false-secure" config. (TASK-0086 / SPEC-0067)
- **Supervised-autonomy SA.4 lock-lift** (off-by-default): the real subprocess invoker may run
  multi-turn only when both `runtime.real_invoker` and `runtime.supervised_autonomy` are registered
  and both `--allow-*` flags are passed; otherwise the `--once` lock holds (byte-equivalent). Run for
  **one bounded pilot, validated end-to-end with the real `codex exec` invoker** (orchestrator-acquired
  claim, gate ACCEPT, clean claim lifecycle, checkpoint after turn 1), then **de-armed back to
  off-by-default** (the shipped default). (DECISION-0027 / TASK-0088 / TASK-0091 / SPEC-0064 §4)
- **Orchestrator acquires the routed owner's claim before the turn** (gap-8 fix): the `claim` step,
  formerly a no-op, now acquires the routed owner's claim via `submit_intent` before the adapter
  (idempotent with a pre-claim, conflict-rejects before the adapter, releases the acquired claim on
  every terminal/rejection outcome — no orphan). (TASK-0093 / SPEC-0070)
- **Windows-sandbox tempfile/ACL hardening** of the authoritative write-path: materialization staging
  and rollback backups use repo-local inherited-ACL temp dirs instead of `%TEMP%` `0o700` dirs that
  blocked the unelevated sandbox token; materialization stays byte-equivalent (same `canonical_hash`).
  Operational runbook documented (`Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md`).
  (TASK-0094 / SPEC-0071)
- **Agent Teams bridge, layers A+B** (gate enforcement + append-only audit), off-by-default; layer C
  (authoritative mapping) deferred. (DECISION-0025 / TASK-0083 / SPEC-0065)
- **Cross-FS materialize fix** for Windows when temp and repo live on different drives; regression
  golden added.
- **Golden rule:** every agent updates its memory after each commit. (DECISION-0026)
- **Operator human guide (neutral) + deterministic HTML generator.** A 21-section operator guide
  master (`Area_comun/protocol/HUMAN_GUIDE.template.md`) and `scripts/generate_human_guide.py`
  (+ `.ps1` parity) that renders `.md → .html` byte-deterministically (stdlib-only, no network/JS/CDN),
  with `--check` drift control, integrated schema validation and tier-awareness; goldens + CI/githook
  wiring. The `.md` is the single source of truth; the HTML is a generated artifact ("GENERATED — DO
  NOT EDIT" banner). Domain-neutral master; the live dogfooding guide (`HUMAN_GUIDE.md`) and the
  `examples/human_guide_instance/` example are generated via the generator.
  (TASK-0037 / TASK-0098 / SPEC-0072)
- **Configurable external-command release-signing backend (authenticity).** `sign_release.py` and
  `verify_release.py` gain an `external-command` backend (configured only by CLI flags, nothing of the
  backend persisted in the repo) that wraps/verifies the `protocol_release_signature.v1` schema while
  preserving `subject_digest == manifest.sbom_hash` and the deterministic fixture HMAC backend.
  Vendor-neutral — no provider hardcoded (cosign/minisign/gpg are the emitter's configuration); the
  digest binding is checked before the backend runs; golden uses a deterministic fake/recorded backend
  (no network, no keys). The release SBOM now excludes `dist/**` so adding a signature/bundle under
  `dist/` does not change the signed `sbom_hash`. (TASK-0099 / SPEC-0073 / DECISION-0023 §4)

### Notes
- Templates (`*.template.*`) unchanged; new instances stay off-by-default.
- Adoption follow-up resolved — posture B (DECISION-0028): `enforce` is the single-writer mechanism
  (its B.3 hard-gate rejects manual ledger edits), `authoritative` is the declarative mode marker with
  no behavior callers; no authoritative-specific teeth are wired and the TASK-0086 guard already
  rejects authoritative-without-enforce. Closes the last adoption blocker (TASK-0087).

## [1.0.0] — 2026-06-07

**First stable release — the protocol-methodology as a distributable product.** Promotes the
protocol to `1.0.0` (human-approved per
[DECISION-0001](Area_comun/decisions/DECISION-0001-versionado.md)). **MAJOR** as a stabilization
milestone: the contract, the N-agent runtime, the security/guardrails layer, the real-LLM wrapper
and the adoption/distribution track are now consolidated and supported as a package. Additive and
domain-neutral over v0.10.0 — every previously valid turn report stays valid and the runtime stays
gated/off-by-default in templates.

### Added
- **Distribution track (D2) complete** — adoption tiers `coordination`/`runtime`
  ([DECISION-0019](Area_comun/decisions/DECISION-0019-distribucion-runtime.md), TASK-0058),
  tier-aware `upgrade_instance` + `runtime_version` (TASK-0061), adoption docs (TASK-0063), and the
  package versioning guide
  [`PACKAGE_VERSIONING.md`](Area_comun/protocol/PACKAGE_VERSIONING.md) — 4 version axes + adopter
  SemVer + per-tier compatibility + migration notes (TASK-0064 / D2.4).
- **Real-LLM wrapper** — vendor-neutral CLI adapter over `SubprocessInvoker` (presets claude/codex),
  off-by-default with explicit registration, no secrets, no autonomy
  ([DECISION-0021](Area_comun/decisions/DECISION-0021-activacion-wrapper-llm.md), TASK-0062).
- **Engine (D0) closed** — N-agent observability (`trace_id`/spans/`summarize_nagent`, TASK-0059) and
  budget/deadline A10 (TASK-0060), config-gated and byte-equivalent when off.
- **Security/guardrails core (Phase 5)** — anti-injection invariant G1 (TASK-0054), deny-by-default
  tool-policy (TASK-0056), envelope signing / event-auth HMAC (TASK-0057).
- **Anti-collision rule** for concurrent ledger writes
  ([DECISION-0020](Area_comun/decisions/DECISION-0020-regla-anti-colision.md)) — formalized and
  propagated to `AGENTS.md`/`AGENTS.template.md` sec.7 and `TASK_PROTOCOL.md`.
- **Prune hygiene** — `prune_state` now condenses `PROJECT_STATE#next_actions` into a deterministic,
  idempotent sentinel (config-gated `recent_next_actions`), closing the Layer-A follow-up (SPEC-0051,
  TASK-0065).
- Human-facing **methodology inventory report** (HTML) under `Area_comun/reports/`.

### Notes
- Post-v1.0 work (Phase B event-log live-writer of protocol state, Phase 7 release engineering,
  supervised autonomy) stays gated behind explicit human approval.

## [0.10.0] — 2026-06-06

N-agent **core consolidation** release. Packages the N-agent runtime phases 1-4 and the full
**Layer A** consolidation, plus three protocol decisions. **MINOR** — additive, domain-neutral,
back-compatible (the legacy N=2 path stays byte-equivalent; every previously valid turn report stays
valid; runtime stays gated/off-by-default in templates).

### Added
- **N-agent runtime core (phases 1-4)** against [SPEC-0038](Area_comun/specs/SPEC-0038-n-agent-registry.md):
  - Phase 1 — agent registry + capability resolution + semantic turn validation (TASK-0043).
  - Phase 2 — append-only event log: writer-only `seq`, per-aggregate `aggregate_version`/idempotency +
    leases/fencing, snapshot/compaction, negative replay (TASK-0044).
  - Phase 3 — deterministic weighted-least-loaded router with author exclusion and fairness gate
    (TASK-0045).
  - Phase 4 — Review/QA state machine: defect logs, canonical `failure_signature`, loop-cut to
    `architect_review`, evidence-gated `done` (TASK-0046).
- **Layer A — core consolidation**:
  - A.5 runtime suites wired into CI (TASK-0047).
  - A.1 event log as **live writer of the control-plane** (Phase A): `assert_snapshot_matches` hard-gate
    in `apply` and in the global validator when `runtime/state` exists; fallback intact
    (TASK-0048, [SPEC-0039](Area_comun/specs/SPEC-0039-event-log-writer-vivo.md), DECISION-0017 scope A->B).
  - A.6 author-of-record hardening (I1/I2 read from state, not payload) (TASK-0049).
  - A.2 golden N=3/N=5 (reviewer/QA separation + deterministic load balancing) (TASK-0050).
  - A.3 property-based invariants I1-I8 (TASK-0051).
  - A.4 concurrency simulation (10 implementers / 100 tasks: conflicts recorded, no snapshot
    corruption, fairness, zero double-applications) (TASK-0052).
  - A.7 explicit turn-schema SemVer (`schema_version 1.1.0` + `Area_comun/protocol/SCHEMA_VERSIONING.md`)
    (TASK-0053).
- **`turn_schema` is now versioned** (`schema_version: 1.1.0`, additive metadata).

### Decisions
- [DECISION-0016](Area_comun/decisions/DECISION-0016-areas-personales-onboarding.md) — personal areas under
  `personal/<id>/` + onboarding rule.
- [DECISION-0017](Area_comun/decisions/DECISION-0017-event-log-writer-vivo.md) — event-log-as-live-writer
  scope: A->B incremental (Phase A done; Phase B gated).
- [DECISION-0018](Area_comun/decisions/DECISION-0018-notificacion-de-anomalias.md) — anomaly notification
  between agents via mailbox.

### Notes
- The full global test plan (SPEC-0038 sec.15.3-15.5: N=3/N=5 golden, property-based, concurrency) is covered.
- Phase B (event log as live writer of the **protocol state**) and Phases 5-7 remain **gated**.

## [0.9.0] — 2026-06-06

Runtime **M2 hito 2** release: the orchestration runtime gains its **first real (non-replay) agent
invoker**, vendor-neutral and gated, all **additively and off-by-default** (`runtime.enabled:false`,
default adapter still `replay`). Running a real agent requires explicit opt-in flags
(`--adapter llm --llm-invoker subprocess --allow-real-invoker --llm-command <cmd> --once`) and a human
gate for the first live run. **MINOR** — additive, domain-neutral, back-compatible (every previously
valid turn report stays valid).

### Added
- **Real LLM adapter** (TASK-0036, [SPEC-0035](Area_comun/specs/SPEC-0035-adapter-llm-real.md)):
  `runtime/adapters/llm_adapter.py` — `LLMAdapter(AgentAdapter)` driven by a **pluggable `Invoker`**.
  `RecordedInvoker` (transcript `recorded_invoker.v1`, no network) keeps golden cases deterministic;
  `SubprocessInvoker` runs a **generic external command** (vendor-neutral: Claude SDK / Codex CLI are
  configurations of this invoker, not the base). Orchestrator flags `--adapter llm`,
  `--llm-invoker recorded|subprocess`, `--llm-command`, `--allow-real-invoker`. Limits reuse M1: the real
  invoker requires `enabled` + `--allow-real-invoker` + `--llm-command` + `--once`; `changed_paths`
  outside the active claim are rejected; per-turn budget aborts before mutating state. Default stays
  `replay`; CI never uses the real invoker. Golden `examples/llm_adapter_cases/` (once, replay-comparative
  `llm==replay`, allowlist rejection, budget abort, `enabled:false` abort).
- **Windows-safe subprocess command parsing** (TASK-0039,
  [SPEC-0036](Area_comun/specs/SPEC-0036-subprocess-invoker-windows-safe.md)):
  `SubprocessInvoker.from_command` tokenizes via `CommandLineToArgvW` on Windows (and `shlex` on POSIX),
  so a real `--llm-command` with native backslash paths and quoted spaces works instead of failing with
  `WinError 2`. Golden subprocess case runs end-to-end with the host-native separator.

### Notes
- First **real run on the live repo** executed under human approval (DECISION-0009 decision #2): the
  runtime closed a task with one gated M1 commit via the real subprocess invoker. Run-logs
  (`runtime/runs/`) are local audit traces and are git-ignored.
- Autonomous multi-turn loop, mailbox automation and a real LLM wrapper remain **M2 (later milestones)**
  and gated.

## [0.8.0] — 2026-06-06

Runtime **M1** release: the orchestration runtime gains its **first safe writer** and closes the
turn loop **deterministically**, all **additively and off-by-default** (`runtime.enabled:false`).
Nothing runs real agents yet — M1 proves the apply/gate/commit engine and the loop via a **replay
adapter**; real LLM adapters and autonomous multi-agent operation are M2 (and turning the runtime on
requires human approval). **MINOR** — additive, domain-neutral, back-compatible.

### Added
- **Turn apply + gate + commit/revert** (TASK-0030, [SPEC-0029](Area_comun/specs/SPEC-0029-turn-apply-gate.md)):
  `runtime/apply.py` (writes only if `validate_turn` passes), `runtime/gate.py` (validator + neutrality
  scan) and `runtime/vcs.py` (one commit per green turn; `git restore` + task `blocked` on a red gate).
  Honors the write-allowlist and row-scoped claims. Golden `examples/runtime_apply_cases/` (repo-fixture, 4/4).
- **Vendor-neutral agent adapter + replay + run loop** (TASK-0031,
  [SPEC-0030](Area_comun/specs/SPEC-0030-adapter-replay-loop.md)): `runtime/adapters/base.py`
  (`AgentAdapter` Protocol + `ContextPack`/`TurnReport`), `runtime/adapters/replay.py` (deterministic
  report replay), `runtime/runlog.py` (JSONL run-log with injectable `--run-id` + deterministic
  `RUN-<sha256>` default), and `runtime/orchestrator.py` `--run/--once/--max-iter` reusing the
  apply+gate+commit engine. `--plan` stays read-only. Golden `examples/runtime_loop_cases/` (5/5):
  `--once`=1 turn/1 commit, deterministic sequence cut by `--max-iter`, `human_required` hard-stop
  (no commit), `--plan` no-regression, `runtime.enabled:false` aborts `--run`.
- **M1 design + specs** (TASK-0029): `Area_comun/artifacts/DISENO-runtime-m1.md` + SPEC-0029/0030,
  refining the M1/M2 boundary (M1 deterministic via replay; real agents = M2).

### Notes
- Off-by-default and vendor-neutral: swapping the replay adapter for a future real adapter does **not**
  touch the loop. Activating `runtime.enabled:true` is a human-owner decision (DECISION-0009).

## [0.7.0] — 2026-06-05

Token-efficiency release: the protocol now **measures** its own context cost and trims the biggest
sources of cold-start bloat, cutting cold-start ~**75%** (≈37k → ≈9k proxy tokens) with no loss of
traceability. Also lands, **additively and off-by-default**, the runtime control-plane foundation (M0)
and a row-scoped state-claim model that lets two agents work in parallel without serializing on the
shared state files. **MINOR** — additive, domain-neutral, back-compatible.

### Added
- **Token-efficiency decision + design** ([DECISION-0008](Area_comun/decisions/DECISION-0008-eficiencia-de-tokens.md),
  TASK-0022): `Area_comun/artifacts/DISENO-eficiencia-de-tokens.md` + SPEC-0023/0024/0025 with a measured baseline.
- **Context-cost meter** `scripts/measure_context_cost.py`/`.ps1` (TASK-0023, SPEC-0023): deterministic
  chars/token proxy over cold-start globs + state dead-weight + mailbox frontmatter overhead; `--json`
  and `--budget` (warning); configurable `token_cost` block in `protocol.config(.template).json`;
  read-only. Golden `examples/context_cost_cases/`.
- **State pruning to history** (TASK-0024, SPEC-0024): `Area_comun/state/CLAIMS_ARCHIVE.json` /
  `TASK_INDEX_ARCHIVE.json` (+ templates); the validator reads **hot ∪ archive** (cross-ref duplicate
  detection). Cold-start **37 391 → ≈9k tokens (-75%)**; nothing deleted (archive ≠ delete).
- **Minimal mailbox frontmatter** (TASK-0025, SPEC-0025): a minimal variant + omission rule in
  `MAILBOX_MESSAGE_TEMPLATE.md`; the validator already tolerates omitted optional fields (back-compat).
  Golden `examples/compact_comms_validation_cases/minimal_frontmatter/` (-61% frontmatter chars on the example).
- **Runtime control-plane M0** ([DECISION-0009](Area_comun/decisions/DECISION-0009-runtime-orquestacion.md),
  TASK-0026/0027): `runtime/turn_schema.json` (strict turn contract), deterministic router, turn
  validator (schema + write-allowlist + race detection) and `orchestrator --plan` dry-run;
  `runtime.enabled:false` by default (`runtime/**` added to the neutrality scan). Golden
  `examples/runtime_turn_cases/`, `examples/runtime_router_cases/`.
- **Row-scoped state claims** ([DECISION-0011](Area_comun/decisions/DECISION-0011-claims-por-fila-estado.md),
  TASK-0028, SPEC-0028): claim scopes may target `TASK_INDEX.json#TASK-XXXX` /
  `PROJECT_STATE.json#active_tasks/TASK-XXXX`; same-row conflicts still caught, distinct rows no longer
  collide. Bare paths keep whole-file semantics (back-compat). Golden `examples/row_scoped_claim_cases/`.
- **Runtime M1/M2 design** (TASK-0029): `DISENO-runtime-m1.md` + SPEC-0029/0030 (apply+gate+commit/revert,
  adapter interface + replay loop) and `DISENO-runtime-m2.md` (real adapters + autonomous loop) — design
  only; implementation tracked as TASK-0030/0031 and later.

## [0.6.0] — 2026-06-05

Operational robustness: the protocol's own quality gates now run in CI, validation harnesses no
longer fail just because a runtime is missing, and instances get assisted version-adoption tooling.
**MINOR** release — additive, domain-neutral, no breaking changes. Closes the audit findings
(weak Python portability, incomplete CI, manual adoption/migration).

### Added
- **Operational robustness decision**
  ([DECISION-0006](Area_comun/decisions/DECISION-0006-robustez-operacional.md), TASK-0016): design
  (`Area_comun/artifacts/DISENO-robustez-operacional.md`) + specs SPEC-0017/0018/0019; defines the
  *neutral surface* and *adoptable set* reused by the scan and upgrade tools.
- **Complete CI** (TASK-0017): `.github/workflows/validate.yml` now also runs the PowerShell
  validator (dogfood + minimal), the SDD/compact/neutrality harnesses and the domain-neutrality
  scan — every gate promised in `AGENTS.md` §5 actually runs.
- **Domain-neutrality scan** `scripts/scan_domain_neutrality.py`/`.ps1` (TASK-0017): configurable via
  a `domain_neutrality` block in `protocol.config(.template).json` (denylist + scan/exempt globs,
  word-boundary match); `enabled:false`/absent ⇒ no-op. Golden cases in
  `examples/neutrality_scan_cases/`, `.py`↔`.ps1` parity.
- **Runtime-tolerant harnesses** (TASK-0018, DECISION-0006 §1): `run_sdd_cases.ps1` and
  `run_compact_comms_cases.ps1` resolve runtimes with fallback (`python`/`py -3`/`python3`,
  `pwsh`/`powershell`), mark the absent half `SKIPPED (WARNING)`, check parity only when both run,
  fail only on logic or no runtime, and always print a summary.
- **Assisted version upgrade** `scripts/upgrade_instance.py`/`.ps1` (TASK-0019, DECISION-0006 §4):
  read-only adoption report of deltas (`nuevo`/`cambiado`/`igual`/`eliminado`) between an instance
  and the master; does **not** modify the instance (adoption stays a per-instance decision,
  DECISION-0001). Fixtures in `examples/upgrade_cases/`, `.py`↔`.ps1` parity.
- **Claim-before-shared-draft rule**
  ([DECISION-0007](Area_comun/decisions/DECISION-0007-claim-before-shared-draft.md), TASK-0020):
  an agent must hold an active claim before creating/editing any draft on shared paths; unclaimed
  work is not overwritten — ask via one concrete mailbox question. Propagated to `AGENTS.md`,
  templates and protocol docs.

### Notes
- MINOR per DECISION-0001 §4 (additive, neutral). Hardening (require both runtimes, WARNING→build
  error, auto-apply upgrades) would be MAJOR (out of scope).
- Validator and domain-neutrality scan green (Python) on root; `.ps1` halves and CI verified by
  Codex/CI (PowerShell run blocked in the architect session by an environment deny-rule).
- Backlog opened, not in this release: TASK-0021 (mailbox-hygiene soft-checks).

## [0.5.0] — 2026-06-05

Compact, token-efficient agent communication: reference canonical artifacts instead of
reconstructing context in long conversations. **MINOR** release — additive, neutral, no length
limits, historical messages and handoffs remain valid.

### Added
- **Compact communication policy**
  ([DECISION-0005](Area_comun/decisions/DECISION-0005-comunicacion-compacta-token-efficient.md)):
  reference by ID/path, one intention (and one question) per message, send deltas, close the loop
  with standard codes (`ACK`/`FYI`/`OK`/`REVIEW`/`CHANGES`/`BLOCKED`/`DONE`/`DECISION_REQUIRED`/
  `HUMAN_REQUIRED`), move long content to artifacts/specs/reports/decisions.
- New `Area_comun/protocol/MAILBOX_MESSAGE_TEMPLATE.md` and a "Compact / token-efficient
  communication" section in `COMMUNICATION_PROTOCOL.md`.
- `HANDOFF_TEMPLATE.md` (compact note), `TASK_PROTOCOL.md` (one concrete question before blocking),
  `TASK_TEMPLATE.md` (`communication_budget`), `HUMAN_REPORT_TEMPLATE.md` (communication status).
- **Soft mailbox validations** (TASK-0014) in `validate_collaboration_state.py`/`.ps1`:
  `open`+`requires_response:true` ⇒ `requested_action` and `question` (ERROR); missing `context_refs`
  when referencing existing work (WARNING). Additive, `.py`↔`.ps1` parity, **no length checks**,
  historical/legacy messages exempt. Golden cases in `examples/compact_comms_validation_cases/`.
- **Reference instance** `examples/compact_communication_case/` (TASK-0015): compact mailbox
  (REVIEW→OK) + compact handoff, validates green.

### Notes
- MINOR per DECISION-0001 §4 (additive). Hardening (length limits, mandatory codes everywhere) would
  be MAJOR (out of scope). Validators green on root + all examples + SDD and compact-comms golden cases.

## [0.4.0] — 2026-06-05

Spec-Driven Development (SDD): clarity before execution. Implementable tasks must declare a spec,
execution pipeline, acceptance criteria, linked decisions, test plan and closure criteria before
they can start. **MINOR** release — additive, config-gated (off by default), no retroactive
migration of historical tasks.

### Added
- **SDD policy** ([DECISION-0004](Area_comun/decisions/DECISION-0004-sdd-pipeline-y-cierre.md),
  TASK-0008): the six SDD fields (`spec_id`, `execution_pipeline`, `acceptance_criteria`,
  `linked_decisions`, `test_plan`, `closure_criteria`) for implementable task types and four
  lightweight fields for discovery/analysis/review/documentation/triage; ambiguity ⇒ ask, never
  invent steps; design + rollout specs in `Area_comun/artifacts/DISENO-SDD.md` and
  `Area_comun/specs/SPEC-0009..0013`.
- **Protocol templates updated for SDD** (TASK-0009): `TASK_PROTOCOL.md` (SDD gate +
  clarity-before-execution + task `type`), `TASK_TEMPLATE.md`, `HANDOFF_TEMPLATE.md` (criteria +
  tests + spec deviations), `HUMAN_REPORT_TEMPLATE.md`.
- **Reusable spec templates** in `Area_comun/specs/` (TASK-0010): `SPEC_TEMPLATE`,
  `PROJECT_BRIEF_TEMPLATE`, `REQUIREMENTS_TEMPLATE`, `ACCEPTANCE_CRITERIA_TEMPLATE`,
  `TEST_PLAN_TEMPLATE`, `TRACEABILITY_MATRIX_TEMPLATE`.
- **Profile-aware → SDD-aware validators** (TASK-0011): config-gated SDD checks in
  `validate_collaboration_state.py`/`.ps1` (block `sdd` in `protocol.config.template.json`,
  default `enabled:false`), pre-SDD exemption, ERROR/WARNING rules, golden cases in
  `examples/sdd_validation_cases/` with `.py`↔`.ps1` parity.
- **Reference instance** `examples/minimal_sdd_instance/` (TASK-0012, `sdd.enabled:true`, validates
  green) and **SDD onboarding** section in `README_INSTANCIACION.md` (TASK-0013).

### Notes
- MINOR per DECISION-0001 §4 (additive, config-gated). `enabled:false`/absent ⇒ validators behave
  exactly as before. Retroactive enforcement to all tasks would be MAJOR (out of scope); TASK-0001..0007
  remain pre-SDD with no migration.
- Validators green on root and all examples (`minimal_instance`, `generated_minimal_instance`,
  `dotnet_enterprise_instance`, `minimal_sdd_instance`) plus SDD and profile golden cases.

## [0.3.0] — 2026-06-05

Professional profiles: the protocol becomes layered (core / profiles / examples) and can be
composed with optional, stack-specific profiles — the core stays domain-neutral. **MINOR** release
(backward-compatible, additive).

### Added
- **Core / profiles / examples architecture**
  ([DECISION-0002](Area_comun/decisions/DECISION-0002-core-perfiles-profesionales.md), TASK-0005):
  the `profiles/` layer with `profiles/README.md`, a neutral `PROFILE_TEMPLATE/`
  (`profile.manifest.template.json` + README + `docs/`/`templates/`/`prompts/`), the
  `profile.manifest` contract, and `Area_comun/artifacts/ARQUITECTURA-core-profiles.md`.
- **First professional profile** `profiles/dotnet_enterprise/` (TASK-0006): ADRs, branching,
  artifact model, SQL Server governance, template versioning, secure AI use, secret handling,
  container-network security, Azure DevOps pipelines, Dev Container / Docker SQL Server / DB
  bootstrap templates, onboarding and a .NET master prompt — all packaged as an **optional**
  extension with a `profile.manifest.json`. Source traceability in `docs/SOURCE_MAP.md`; secrets
  sanitized to placeholders.
- **`adopted_profiles` contract**
  ([DECISION-0003](Area_comun/decisions/DECISION-0003-adopted-profiles-contract.md)) and
  **profile-aware validators** (TASK-0007): optional `adopted_profiles` in
  `PROJECT_STATE.template.json` and additive checks in both `validate_collaboration_state.py` and
  `.ps1` (schema, id/version match against the manifest, `requires_protocol_version` compatibility,
  dependencies, duplicates) with `.py` ↔ `.ps1` parity and golden cases in
  `examples/profile_validation_cases/`.
- Reference instance `examples/dotnet_enterprise_instance/` (core + `dotnet_enterprise`, validates
  green, declares `adopted_profiles` + an instance adoption decision).

### Notes
- MINOR release per DECISION-0001 §4 (additive, no human approval required). Instances **without**
  `adopted_profiles` validate exactly as before (backward compatible).
- Validators green on root, `examples/minimal_instance/`, `examples/generated_minimal_instance/`,
  `examples/dotnet_enterprise_instance/` and all `examples/profile_validation_cases/`.

## [0.2.0] — 2026-06-05

Protocol enrichment: more portable, versioned and easier to instantiate. Domain-neutral core.

### Added
- **Versioning policy** ([DECISION-0001](Area_comun/decisions/DECISION-0001-versionado.md)) and
  this `CHANGELOG.md`: SemVer adapted to a file-based protocol (MAJOR/MINOR/PATCH with concrete
  examples), the release procedure, and human approval required for MAJOR releases.
- **`protocol_version`** declaration: new field in `protocol.config.template.json`
  (placeholder `{{PROTOCOL_VERSION}}`) and in this repo's live `protocol.config.json` and
  `examples/minimal_instance/`, so every instance records the protocol version it follows.
- **Cross-platform Python validator** `scripts/validate_collaboration_state.py` plus CI workflow
  `.github/workflows/validate.yml` (TASK-0002), complementing the PowerShell validator.
- **Scaffolding script** `scripts/new_instance.py` (TASK-0004): stdlib-only, renders the
  `*.template.*` masters into a valid instance, populates `protocol_version`, and fails on any
  unresolved `{{...}}` placeholder. Documented in `README_INSTANCIACION.md`.
- Roadmap to v0.2.0 in `Area_comun/artifacts/ROADMAP-v0.2.0.md` (TASK-0001).

### Notes
- v0.2.0 is a **MINOR** release (backward-compatible additions); no human approval required per
  DECISION-0001 §4. Validators green on root, `examples/minimal_instance/` and
  `examples/generated_minimal_instance/`.

## [0.1.0] — 2026-06-05

Initial extraction and bootstrap of the reusable, domain-neutral multi-agent protocol.

### Added
- Shared contract `AGENTS.md` and Claude-specific rules `CLAUDE.md`.
- `Area_comun/` protocol docs: `TASK_PROTOCOL.md`, `COMMUNICATION_PROTOCOL.md`,
  `HANDOFF_TEMPLATE.md`, `TASK_TEMPLATE.md`, human report template.
- Live state artifacts: `PROJECT_STATE.json`, `TASK_INDEX.json`, `CLAIMS.json`, mailbox,
  handoffs, decisions and reports folders.
- Shipped masters: `*.template.*` files and `protocol.config.template.json`.
- Reference instance `examples/minimal_instance/` (validates green).
- PowerShell validator `scripts/validate_collaboration_state.ps1`.

[Unreleased]: https://example.invalid/compare/v0.6.0...HEAD
[0.6.0]: https://example.invalid/compare/v0.5.0...v0.6.0
[0.5.0]: https://example.invalid/compare/v0.4.0...v0.5.0
[0.4.0]: https://example.invalid/compare/v0.3.0...v0.4.0
[0.3.0]: https://example.invalid/compare/v0.2.0...v0.3.0
[0.2.0]: https://example.invalid/compare/v0.1.0...v0.2.0
[0.1.0]: https://example.invalid/releases/tag/v0.1.0
