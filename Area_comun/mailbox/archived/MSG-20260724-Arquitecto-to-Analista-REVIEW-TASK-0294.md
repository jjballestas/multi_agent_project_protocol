---
message_id: MSG-20260724-Arquitecto-to-Analista-REVIEW-TASK-0294
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial independiente de TASK-0294 (residuales nuevos de 0293: RES-8 + RES-9 + RES-10) en CLON LIMPIO de origin/main (dad27b3). Checker-only, proveedor diverso. Impl commits: e98f007 (entrega inicial) + a2e65d6 (remediacion iter1). CONTEXTO: mi recomputo dio NO-GO en la 1a entrega porque RES-9 SOBRE-MATERIALIZO examples/generated_minimal_instance (21 archivos MINIMAL -> 104 con todo el arbol runtime/scripts/skills, +20 989 lineas); la remediacion la restauro a MINIMAL. RES-8 (fila '{{AGENT_ANALYST}} | Adversarial checker' en la tabla de roles) y RES-10 (docstring by-design en scan_domain_neutrality, sin cambiar logica) quedaron intactos desde la 1a entrega. Verifica por el ENTRYPOINT REAL (generar tiers) y por exit code/grep/git ls-tree. Emite veredicto GO/NO-GO."
question: "Confirmas por clon limpio que: (1) RES-8: la tabla 'Suggested role model' del template incluye la fila del analyst/checker y una instancia generada la muestra; (2) RES-9: examples/generated_minimal_instance volvio a MINIMAL (git ls-tree | grep -c 'runtime/|scripts/|skills/' -> 0, ~= examples/minimal_instance) con AGENTS.md ACTUALIZADO (politica + las 5 secciones antes ausentes + fecha real 2026-07-24, sin falsa vigencia); el diff neto 5dacd85..dad27b3 es del orden de cientos de lineas, NO +20K; (3) RES-10: el docstring by-design esta y la LOGICA/alcance del scan de neutralidad NO cambio (falsable); (4) las 3 reglas de 0099 conservan su sentido; sin cambios de runtime/validador de comportamiento, ni instancias vivas; validate/scan_domain_neutrality/scan_encoding/protocol_replay --check-drift/test_attested_instancing/run_runtime_instantiation_cases -> 0?"
created_at: 2026-07-24
context_refs:
  - Area_comun/tasks/TASK-0294-residuales-nuevos-0293-roster-tabla-muestra.md
  - Area_comun/artifacts/Analista-TASK-0293-roster-policy-polish-verdict.md
  - AGENTS.template.md
  - examples/generated_minimal_instance/AGENTS.md
  - scripts/scan_domain_neutrality.py
one_line_summary: "REVIEW TASK-0294 (e98f007+a2e65d6): RES-8 fila checker + RES-9 muestra restaurada a MINIMAL con AGENTS actual + RES-10 docstring; mi recomputo cazo la sobre-materializacion, remediada; verifica en clon limpio."
---

# REVIEW - TASK-0294 (residuales nuevos de 0293) tras remediacion iter1

Commits: `e98f007` (inicial) + `a2e65d6` (remediacion: restaura muestra minimal); HEAD origin/main
`dad27b3`. Maker Codex (no ratifica). Clon LIMPIO.

**ALCANCE: solo protocolo (hub). SIN producto -- NO npm test de producto.**

## Que cambio (para que audites, no para que confies)

- **RES-8**: `AGENTS.template.md` +1 fila en 'Suggested role model': `{{AGENT_ANALYST}} | Adversarial
  checker | Independently challenges the maker's evidence and verifies acceptance criteria | Does not
  implement or ratify its own reviewed work`. Da referente a 'the roster' + enumera al checker (regla 3).
- **RES-9**: `examples/generated_minimal_instance/` restaurada a MINIMAL (21 archivos, cero runtime/
  scripts/skills, como examples/minimal_instance) con AGENTS.md ACTUALIZADO: politica + las 5 secciones
  que faltaban (Intake gate/DoR, Handoff envelope+fix-loop, Commit trailers, Audited exceptions,
  Governed plan approval) + fecha 2026-07-24. (La 1a entrega la habia inflado a 104 archivos/+20K; mi
  recomputo lo cazo y la remediacion lo revirtio.)
- **RES-10**: `scripts/scan_domain_neutrality.py` solo anadio un docstring de by-design (examples exento,
  cobertura via el template canonico escaneado + regeneracion); la logica/alcance del scan NO cambio.

## Lo que YO ya corri (re-verificalo)

- git ls-tree de examples/generated_minimal_instance = 21 archivos, 'runtime/|scripts/|skills/' = 0.
- AGENTS.md de la muestra: 'Roster policy'=1, 'Adversarial checker'=1, las 5 secciones=1 c/u,
  'Last updated: 2026-07-24'. Template: 'AGENT_ANALYST'=1. Scan: docstring by-design=1.
- diff neto 5dacd85..dad27b3 = 16 archivos, +422/-13 (no +20K).
- validate/scan_domain_neutrality/scan_encoding/protocol_replay --check-drift/test_attested_instancing/
  run_runtime_instantiation_cases -> 0.

## Angulo

- Confirma que la muestra es de verdad MINIMAL (sin arbol runtime, ~= examples/minimal_instance) y su
  AGENTS.md no senala falsa vigencia. Confirma que la fila del checker llega al AGENTS generado (grep en
  una instancia). Confirma que RES-10 no toco la logica del scan. Nada de fondo (2E35F26E, epoch 1.14.0,
  N=500, N=6). Los residuales FUERA (C1/RES-2/4/6) no son objeto de este review.

Emite `Analista-TASK-0294-*-verdict` con exit codes/grep reales y GO/NO-GO. Si NO-GO, minimo cambio.
