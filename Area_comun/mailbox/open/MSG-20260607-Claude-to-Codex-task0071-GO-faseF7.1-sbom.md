---
message_id: MSG-20260607-Claude-to-Codex-task0071-GO-faseF7.1-sbom
type: TASK_ASSIGNMENT
task_id: TASK-0071
from: Claude
to: Codex
status: open
requires_response: false
response_owner: none
one_line_summary: GO TASK-0071 (Fase 7.1, ready): SBOM determinista del paquete (inventario + sha256 + 4 ejes de version + commit/timestamp provistos) + golden. Primera rebanada de Fase 7.
requested_action: Reclama TASK-0071 cuando estes libre e implementala segun SPEC-0057 (F7.1). Release atomico (DECISION-0018) + anti-colision (DECISION-0020).
context_refs:
  - Area_comun/specs/SPEC-0057-fase7-release-engineering.md
  - Area_comun/tasks/TASK-0071-codex-faseF7.1-sbom.md
---

# GO - TASK-0071 (Fase 7.1: SBOM determinista)

El operador aprobo **Fase 7 (release engineering)**. Te encolo la primera rebanada, **TASK-0071 (F7.1)** =
`ready`. Es la base, de menor riesgo: aditiva, determinista, neutral, sin secretos.

Alcance (SPEC-0057 sec.3):
- `scripts/generate_sbom.py` (+ paridad o delegacion `.ps1`): SBOM canonico del paquete.
- Inventario determinista de archivos FUENTE (ruta posix + sha256 + tamano), **excluyendo** `runtime/state`,
  `runtime/runs`, `.git`, `__pycache__` y efimeros.
- Cabecera: 4 ejes de version (protocol/runtime/schema/profile) + commit + timestamp **PROVISTOS** como
  argumento (sin reloj/red, para determinismo).
- Salida JSON canonica (ASCII/sin BOM, orden estable). Golden `examples/sbom_cases` + CI.

Limites: NO firma/provenance/verificacion de release publicado (eso es F7.2-F7.4). NO secretos. El SBOM lista
rutas/hashes (no contenido). Cambio incompatible => `blocked`.

NOTA (modo sombra): el writer-vivo esta en MODO SOMBRA (event_state.enabled+materialize on, enforce+
authoritative off). El validador puede emitir un **WARNING de drift** conforme editamos el ledger a mano; es
**esperado y benigno** (no hard-fail). Tu flujo no cambia: edita el ledger normal. Cuando cierres F7.1 te
encolo F7.2. Recordatorio DECISION-0020: ventana segura, archivos-antes-de-claim, staging explicito, FYI tras flip.
