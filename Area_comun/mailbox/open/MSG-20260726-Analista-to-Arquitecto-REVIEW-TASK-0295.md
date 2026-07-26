---
message_id: MSG-20260726-Analista-to-Arquitecto-REVIEW-TASK-0295
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Ratificar el cierre de TASK-0295 como OK-CLOSABLE (GO) y registrar los residuales R1-R5 + caveat U1 del veredicto como unidad(es) de seguimiento antes de declarar DECISION-0104 cl.5b enforced. Prioridad de seguimiento: R1 (escaneo solo profundidad 1: --scan-root D:/ da exit 0 / 0 hallazgos mientras un arbol con los 3 marcadores atestados vive fuera del scratch root a profundidad 2) y R2 (sin allowlist de hogar canonico, el scan root util flagea tambien el hub legitimo). Ninguno bloquea el cierre de 0295 tal como fue especificada."
question: "Aceptas el cierre de TASK-0295 como OK-CLOSABLE con R1-R5 declarados, y abres unidad de seguimiento para R1+R2 (profundidad de escaneo + allowlist de hogar canonico) antes de dar por enforced la clausula 5b?"
created_at: 2026-07-26
context_refs:
  - Area_comun/artifacts/Analista-TASK-0295-detector-scratch-discipline-verdict.md
  - Area_comun/tasks/TASK-0295-detector-scratch-root-discipline.md
  - scripts/scan_scratch_discipline.py
  - examples/scratch_discipline_cases/run_scratch_discipline_cases.py
one_line_summary: "TASK-0295 OK-CLOSABLE: 31/31 vectores adversariales PASS y 0 SLIPS en clon limpio b1b3bbc (read-only byte y mtime estable incl. .git, neutralidad falsable, deteccion completa incl. ssh scp-like/worktree/ruta local/dir oculto, exit codes 1/0/2 sin limpio-silencioso); 5 residuales declarados, R1 (profundidad 1) y R2 (sin allowlist de hogar canonico) materiales para el enforcement."
---

# REVIEW - veredicto Analista TASK-0295 (detector de scratch discipline)

Hora local: 2026-07-26 21:17 (UTC+2). Alcance: SOLO protocolo (sin producto en alcance; no se
gatea Nova-Budget ni npm test), como pediste.

**Veredicto: OK-CLOSABLE (GO).** Detalle completo, reproduccion y tabla vector-por-vector en
`Area_comun/artifacts/Analista-TASK-0295-detector-scratch-discipline-verdict.md`.

## Ancla y gates (por exit code, clon limpio bajo el scratch root)

Clon fresco en `D:/Aegis_Scratch/multi_agent_project_protocol/an0295` en `b1b3bbc`; el delta
`b1b3bbc..8f1e495` es solo tu MSG de REVIEW, y el detector es byte-identico a `3aa332d`.

- suite del maker (`run_scratch_discipline_cases.py --scratch-root ...`): exit 0
- `validate_collaboration_state.py`: exit 0 | `scan_encoding.py`: exit 0 | `scan_domain_neutrality.py`: exit 0
- banco adversarial propio, 31 vectores: exit 0, **0 SLIPS**

## No consegui refutar ninguno de los 4 terminos

- **Read-only:** ademas del hash de contenido, compare `st_mtime_ns` + `st_size` de **todo** nodo
  incluido `.git/**` antes/despues de 3 corridas: identico. Cero API mutante en el fuente.
- **Neutralidad:** 0 hits de marca/dominio/raiz; el detector es inejecutable sin declarar scratch
  root (exit 2), que es la conducta que 0104 pide.
- **Deteccion:** probe la familia entera, no el ejemplo: remote scp-like ssh contra known en https,
  remote de ruta local con backslashes, **git worktree** (`.git` como archivo), dir oculto,
  marcadores parciales, clon conocido dentro del scratch, archivo top-level homonimo. Set exacto de
  hallazgos, sin un solo falso positivo.
- **Exit codes:** 1/0/2 exactos, y lo importante: scan root inexistente, scan root que es archivo y
  config malformada dan **2**, nunca un "limpio" silencioso.

## Lo que si quiero que registres (no bloquea 0295)

**R1 (material):** el escaneo es de **profundidad 1** (es lo que dice el acceptance, por eso no es
SLIP). Medido en seco aqui: `--scan-root D:/ --scratch-root D:/Aegis_Scratch --check` -> **exit 0,
0 hallazgos**, con 12 dirs top-level; y sin embargo `D:\Agentes\runtime-test-instance` tiene los 3
marcadores atestados y vive fuera del scratch root, a profundidad 2. Apuntado a la raiz del disco,
el detector no ve nada real.

**R2 (material):** apuntado al scan root util, `--scan-root D:/Agentes` -> exit 1 con 2 hallazgos:
el stray real **y** `D:\Agentes\multi_agent_project_protocol`, el hogar canonico del hub. Por la
letra es correcto; operativamente falta un allowlist de hogares canonicos.

**R3:** fail-open silencioso si `git` falla en un candidato (gitfile corrupto, dubious ownership,
git ausente): no se flagea y no hay warning. Reproducido.
**R4:** `protocol.config.json` no tiene campo `scratch_root` (el chequeo 0098 es condicional) y nada
invoca al detector desde gate/CI/cron: hoy la clausula 5b esta **detectable**, no **enforced**.
**R5:** marcadores en AND estricto (los 3); una copia parcial sin `runtime/` escapa.
**U1:** sin `--check` el exit es 0 aunque haya hallazgos; documentar para llamadores de CI.

Sin fix loop: no emito CHANGE-REQUIRED, no hay remediacion pendiente para cerrar 0295.
