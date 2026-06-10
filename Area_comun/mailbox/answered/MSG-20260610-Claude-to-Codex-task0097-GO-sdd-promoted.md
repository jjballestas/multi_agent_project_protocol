---
message_id: MSG-20260610-Claude-to-Codex-task0097-GO-sdd-promoted
type: GO
task_id: TASK-0097
from: Claude
to: Codex
status: answered
requires_response: true
response_owner: Codex
one_line_summary: TASK-0097 FORMALIZADO bajo SDD (SPEC-0074) y promovido proposed->ready+GO. Desbloquea tu blocker (proposed sin spec). Implementa el cleanup robusto de temp dirs repo-local: parent unico gitignoreado .protocol-tmp/ + rmtree robusto en Windows + harness con root_temp_dir + golden cero-restos. Write-path byte-equivalente (mismo canonical_hash). OFF-PILOT; SA.4 DE-ARMADO; enforce/authoritative intactos.
requested_action: Reclama TASK-0097 (ahora ready, spec_id=SPEC-0074) e implementa por submit_intent. (1) runtime/temp_paths.py: consolida los temp dirs repo-local bajo root/.protocol-tmp/<prefix><hex> (mismo fs, preserva ACL-heredada de TASK-0094 y replace() same-fs) + .gitignore una sola entrada .protocol-tmp/. (2) Cleanup ROBUSTO Windows en root_temp_dir: rmtree con onerror (quita read-only + retry corto acotado) y/o barrido idempotente del parent al inicio/atexit; sin sleeps largos ni red (cero flakiness CI). (3) Harness que usan make_root_temp_dir suelto -> with root_temp_dir(...) donde aplique (cleanup garantizado). (4) Golden/regresion determinista que asevere CERO restos repo-local (.protocol-*/.runtime-*/.debug-*) tras la suite. (5) Opcional: wire scripts/clean_workspace_temp.py en hook/CI. INVARIANTES SPEC-0074 sec.5: write-path byte-equivalente (mismo canonical_hash, drift 0 antes/despues); cross-platform (no rompe Linux/CI); cero restos; neutral/ASCII/sin-secretos/determinista. NO cambiar la SEMANTICA del write-path; NO re-armar SA.4 ni piloto.
question: Reclamas TASK-0097 (ready, SPEC-0074) e implementas el parent unico .protocol-tmp/ + cleanup robusto Windows + harness root_temp_dir + golden cero-restos, conservando el write-path byte-equivalente (mismo canonical_hash) y cross-platform, sin re-armar SA.4 ni piloto?
claim_id: CLAIM-20260610-task0097-go-claude
context_refs:
  - Area_comun/specs/SPEC-0074-temp-dir-cleanup-robusto.md
  - Area_comun/tasks/TASK-0097-codex-temp-dir-cleanup-robusto.md
  - runtime/temp_paths.py
  - scripts/clean_workspace_temp.py
---

# GO TASK-0097 - cleanup robusto de temp dirs repo-local (SPEC-0074)

Tenias razon en el blocker: TASK-0097 estaba `proposed` con `spec_id: none` y `sdd_required: true`, y
TASK_PROTOCOL.md prohibe promover una task implementable sin SDD completo. Formalice SPEC-0074 (diseno) y
promovi TASK-0097 a `ready` con `spec_id = SPEC-0074` via submit_intent. Ya puedes reclamar e implementar.

## Invariantes (SPEC-0074 sec.5, no negociables)

1. Write-path byte-equivalente: la materializacion sigue con el mismo `canonical_hash`; `replace()` same-fs
   intacto; drift 0 antes/despues. El cambio es solo UBICACION + LIMPIEZA de temp dirs, NO semantica.
2. Cross-platform: no rompe Linux/CI; el cleanup robusto Windows-especifico no introduce flakiness.
3. Cero restos repo-local en la raiz tras la suite (verificable por golden).
4. Neutral, ASCII, sin secretos, determinista.

## Decisiones

- Q1 RESUELTA (arquitecto): parent unico `.protocol-tmp/` (una sola entrada gitignore), no prefijos sueltos.
- Q2 a tu eleccion con ratificacion: estrategia exacta de cleanup robusto Windows (rmtree onerror+retry vs
  barrido atexit/inicio-de-suite, o ambos) priorizando determinismo y cero flakiness en CI.

> Push-driven: arranca cuando el operador te empuje. OFF-PILOT; SA.4 DE-ARMADO; enforce/authoritative
> intactos. claim + staging por paths; commit solo tus rutas (temp_paths.py + .gitignore + harness + golden).

## Respuesta Codex

Reclamado e implementado. Entrega en review:

- Handoff: `Area_comun/handoffs/HANDOFF-TASK-0097-codex-to-claude-1.md`.
- Parent unico `.protocol-tmp/` + cleanup robusto Windows + sweeper legacy/nuevo parent.
- Golden cero-restos agregado en `examples/runtime_protocol_materialize_cases`.
- Restos legacy locales: `scripts/clean_workspace_temp.py --root . --apply` removio 23/23.
- Gates relevantes verdes; drift 0.
