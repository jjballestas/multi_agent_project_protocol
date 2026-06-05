---
id: TASK-0002
owner: Codex
status: done
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0001]
phase: P0
reviewed_by: Claude
review: OK
---

# TASK-0002 - Validador multiplataforma (Python) + workflow de CI

## objetivo
Dar al protocolo un **validador multiplataforma** (hoy solo existe el de PowerShell, atado a
Windows) y **CI** que lo ejecute automaticamente, para que el protocolo sea usable y verificable
en cualquier SO.

## entradas
- Validador actual de referencia: `scripts/validate_collaboration_state.ps1` (logica canonica).
- `protocol.config.json` (`state_invariants`), `examples/minimal_instance/`.
- `AGENTS.md` (neutralidad de dominio).

## archivos_relevantes
- crea: `scripts/validate_collaboration_state.py` (equivalente funcional al .ps1).
- crea: `.github/workflows/validate.yml` (corre el validador sobre `examples/minimal_instance`
  y sobre la raiz del repo en cada push/PR).
- lee: `scripts/validate_collaboration_state.ps1`.

## entregables
- `scripts/validate_collaboration_state.py` con paridad funcional (mismos chequeos:
  state_invariants, task files, status match, deliverables de done/in_review, mailbox, claims,
  handoffs con requires_response).
- `.github/workflows/validate.yml` verde.
- Handoff a Claude para revision cruzada.

## definition_of_done
- [x] El validador Python da el MISMO veredicto que el .ps1 sobre `examples/minimal_instance`
      (OK) y detecta los mismos fallos en casos negativos.
- [x] CI corre el validador en push/PR y queda verde.
- [x] Sin dependencias pesadas (stdlib si es posible); multiplataforma.
- [x] Mantiene neutralidad de dominio; sin secretos.
- [x] Reclamar en `CLAIMS.json` (scope `scripts/`, `.github/`) antes de editar; handoff autocontenido.

## riesgos
- Divergencia de logica entre .ps1 y .py: documentar la paridad y, si se desea, deprecar uno.

## preguntas_abiertas
- ¿Mantener ambos validadores (.ps1 + .py) o deprecar el .ps1? Proponer en el handoff; decision
  del operador/Claude.

## notas_de_ejecucion
- 2026-06-05 Codex implementa `scripts/validate_collaboration_state.py` con stdlib, agrega
  `.github/workflows/validate.yml`, valida raiz y ejemplo con PowerShell/Python, y prueba casos
  negativos temporales.

