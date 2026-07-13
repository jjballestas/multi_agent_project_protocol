---
message_id: MSG-20260713-Arquitecto-to-Operador-FYI-encapsulacion-aegis-hecha
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: false
created_at: 2026-07-13
context_refs:
  - Area_comun/artifacts/CROSS-ATESTACION-hub-nova-registro.md
  - scripts/new_instance.py
  - scripts/validate_collaboration_state.py
one_line_summary: "Encapsulacion Aegis/ (modelo 2.A) HECHA Y PUSHEADA: NOVA retrofiteada (HEAD 5518b5a, sello preservado, sin re-genesis) + new_instance.py nace instancias encapsuladas con Aegis/.claude + hub 8b03d4d. Cross-atest Entrada 1 + erratum Entrada 0. Hora: 2026-07-13 ~17:10 local (UTC+2)."
---

# FYI - Encapsulacion Aegis/ (modelo 2.A) HECHA (2026-07-13 ~17:10 local, UTC+2)

Ejecutados los 3 GO (a+b+c) + new_instance.py con Aegis/.claude. Todo verde por exit-code, en clon limpio.

## (a) NOVA retrofiteada -> `Aegis/` (pusheada, NOVA HEAD 5518b5a)
- Todo el gobierno movido a la carpeta CONSTANTE `Aegis/` (git mv puro); raiz del repo SOLO producto
  (NOVA.sln, src/, apps/, tests/, docs/) + Aegis/.claude + Aegis/CLAUDE.md.
- **Sello byte-preservado -> SIN re-genesis:** events.jsonl 4f69a3dc..., canonical config C157FE00 (el
  genesis liga el canonical_hash del CONTENIDO, no la ruta). validate/scan/neutralidad 0 (root Aegis Y estilo-CI).
- CI en la raiz del repo (obliga GitHub) con working-directory: Aegis; el tooling se auto-localiza.

## (b) new_instance.py: instancias FUTURAS nacen encapsuladas (hub HEAD 8b03d4d)
- Tier **attested** (productos) nace en `target/Aegis/` con Aegis/.claude (config de gobernanza) + Aegis/CLAUDE.md
  + .gitattributes Aegis-scoped + CI working-directory. Flag `--governance-dir` (default Aegis).
- Validadores py+ps1 encapsulation-aware (aceptan CI en repo-root, backward-compat: el hub sigue verde).
- Bonus born-ready: reset de COMMIT_TRAILERS en instancias generadas (no heredan el gate del hub) -> validan al nacer.
- test_attested_instancing.py verde (actualizado a Aegis/).

## (c) Cross-atest Entrada 1 + ERRATUM Entrada 0
- Entrada 1 ancla la NOVA encapsulada (commit 5518b5a, config blob C2DE91F9, events 4f69a3dc, sello intacto).
- **Erratum (integridad):** la Entrada 0 registro config sha8 `5679362F` = valor CRLF del working copy nova-a2
  (autocrlf); el reproducible desde clon limpio (blob git LF) es **C2DE91F9**. El sello NUNCA estuvo afectado
  (canonical C157FE00, el genesis liga eso). Corregido append-only. Leccion: hashear el BLOB de git, no el working copy.

## Hallazgo settings anidados (empirico, lo que pediste probar)
- Claude Code enraiza en el CWD: lanzar gobernanza con cwd=Aegis/ carga SOLO Aegis/.claude (aislamiento
  bidireccional limpio). El "single-root por ahora" que aceptaste NO es forzado; se puede tener un `.claude` de
  gobernanza totalmente separado (caveat: trust gate por carpeta una vez). Scaffoldee Aegis/.claude como starter neutro.

## Deuda declarada (sin GO, para cuando quieras)
1. Sellar 2.A como enmienda DECISION-0050 (ya estaba pendiente; esto es cambio de contrato de layout).
2. `run_runtime_instantiation_cases.py` PRE-EXISTING broken (falta --analyst + GATE_SCRIPTS stale + neutralidad
   flaggea agent-ids) -- ortogonal a la encapsulacion (tiers coord/runtime intactos), limpieza aparte.

Fondo del hub intacto (2E35F26E / 1.14.0, dataset N=500, sello N=6). Estado: STANDBY.

-- Arquitecto
