---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-A-GO-piloto-flip-4
type: DECISION
task_id: TASK-0117
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
one_line_summary: GO A ABRIR LA VENTANA DE PILOTO DE #4 (su propia ventana de riesgo, sin combinar con Carril B/connector ni SA.4/Capa C/subagents; un multiplicador). DEADLINE DURO: #4 ON antes del primer handoff gobernado del desarrollo de la app (T0, no retrofiteable), objetivo antes de 2026-06-20 10:00. Secuencia provisioning -> re-genesis -> piloto REAL (operador presente + rollback armado) -> flip si VERDE. Cargador HMAC ya listo (v1.13.0). #4 sigue OFF hasta el flip.
requested_action: "Abrir la ventana de piloto de #4 en copia LIMPIA que persiste (clon fuera del mount que se re-trunca; restore->verify clean==HEAD->apply->read-back->push, como en la promocion). Ejecutar: (1) Provisioning AC1; (2) re-genesis en arbol limpio -> drift 0; (3) PILOTO REAL AC2/AC3/AC5 con operador presente + rollback armado; (4) si VERDE: flip de los 4 flags -> #4 ON + SemVer MINOR + CHANGELOG + cerrar TASK-0117 done + REPORTAR (resultado piloto, version, drift 0). Si NO verde: NO flip, diagnosticar, reportar."
question: "Confirmas la ventana de piloto de #4 y ejecutas provisioning -> re-genesis -> piloto REAL -> flip-si-verde en copia limpia, dejando #4 ON antes del primer handoff gobernado de la app (objetivo < 2026-06-20 10:00)?"
context_refs:
  - Area_comun/specs/SPEC-0081-activacion-atestacion-autoria.md
  - Area_comun/tasks/TASK-0117-codex-activacion-4-atestacion.md
  - Area_comun/decisions/DECISION-0039-activacion-atestacion-autoria.md
  - Area_comun/decisions/DECISION-0040-gate-dataset.md
  - Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md
deadline_or_blocking_level: blocking
---

# GO - ventana de piloto de #4 (provisioning -> re-genesis -> piloto REAL -> flip)

Abro tu gate: **enciende #4** por la secuencia gateada. Motivo/fecha (regla 3.4): el desarrollo de la app
web (front + Seguridad + Presupuesto) arranca **2026-06-20 10:00** (o antes); su primer handoff gobernado
= **T0 del dataset**, y #4 debe estar **ON antes** de el (DECISION-0039, no retrofiteable). Ventana PROPIA:
no la combines con el connector (Carril B) ni SA.4/Capa C/subagents; **un solo multiplicador**.

## Disciplina de ejecucion (leccion de la promocion - OBLIGATORIA)
Provisioning, re-genesis y flip MUTAN config+event log. Corre TODO en una **copia limpia que persiste**
(clon fresco fuera del mount que se re-trunca): `restore/checkout limpio == HEAD -> verify (py_compile +
validate --root . verde + drift 0) -> apply -> read-back en disco -> commit + push a canonico`. Si entre
verify y commit se re-trunca, **abortar** y reintentar. NO operar sobre el working tree volatil de D:.

## 1. Provisioning (AC1)
- **Anchor (Opcion A, decidida):** crea repo git DEDICADO y HERMANO `D:\Agentes\audit-anchor` (`git init`,
  NO anidado; debe EXISTIR antes de `anchor_enabled=true`). `anchor_config.remote_url = D:\\Agentes\\audit-anchor`
  (ruta absoluta PLANA, NO `file://`), `branch=audits/default`, `identity=runtime-anchor`. **Riesgo
  residual A3 DECLARADO** (mismo disco; ya en DECISION-0029). Fase B (push externo) queda para despues.
- **Firmas:** cada agente del registry acuna su par Ed25519 (privada wrapper-side, FUERA del repo, via
  `llm_turn_wrapper`); registra la **publica** en `signature_config.public_keys`. `agent_registry` al dia.
- **HMAC event_auth:** por el **cargador ya construido (v1.13.0, DECISION-0043/SPEC-0082)** -> `secret_file`
  gitignored (NO literal inline). Scan de secretos limpio + check dedicado AC4 (no literal de actor vivo).
- **Smoke AC1:** tras (a)-(c), `append_event` y el primer anclaje NO fallan; sin ellos, fallan (negativo).

## 2. Re-genesis
Introducir las referencias/claves cambia genesis -> **re-genesis coordinado** en el arbol limpio -> drift 0,
replay == hot.

## 3. PILOTO REAL (operador presente + rollback armado + 1 multiplicador)
Encender chain+firmas+anclaje+event_auth en ventana acotada y correr **en vivo**: AC2 (salud >=99%, N=20,
denominador del event log), AC3 (6 vectores RECHAZADOS), AC5 (rollback byte-equivalente, replay==hot,
drift 0). Checkpoint humano. **Rollback armado** (4 flags a false) listo para abortar.

## 4. Flip (solo si VERDE)
Si el piloto pasa con mi GO: deja los 4 flags en true (chain + agent_signatures + anchor + event_auth) en
la instancia viva -> **#4 ON**; SemVer **MINOR** + CHANGELOG; cierra **TASK-0117 done**; REPORTA de
inmediato (resultado del piloto, version, drift 0). **Si NO verde: NO enciendas, diagnostica y reporta.**

## Limites / recordatorios
- #4 ON es el techo: **no** mas alla sin GO nuevo. DEF-PII (TASK-0118) sigue diferida; PII de terceros
  NUNCA al event log (dos planos, DECISION-0040) - relevante porque la app leera Seguridad/Presupuesto con
  PII. Codex y crons activos. Estoy **presente** para el checkpoint del piloto. Canal ASCII.
