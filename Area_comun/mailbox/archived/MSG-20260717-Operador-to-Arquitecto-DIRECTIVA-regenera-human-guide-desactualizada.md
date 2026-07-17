---
message_id: MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-regenera-human-guide-desactualizada
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/protocol/HUMAN_GUIDE.template.md
  - Area_comun/specs/SPEC-0072-guia-humana-operativa-generador-html.md
one_line_summary: "El operador pide actualizar HUMAN_GUIDE.html (raiz), desactualizada (dice protocol 1.1.0 / runtime 0.11.0 / Actualizado 2026-06-10; el real es epoch 1.14.0 / release v1.19.0). Actualiza la FUENTE .md + REGENERA con generate_human_guide.py; pasa golden case human_guide_cases + scan_domain_neutrality + scan_encoding. MANTENLA NEUTRAL de dominio: NADA de nomina/Nova-Payroll/contabilidad; el contenido especifico del proyecto va en otros vehiculos (doc de medicion + Notion + manual)."
requested_action: "[DIRECTIVA] Actualiza la fuente .md de la guia humana (version/epoch/runtime al estado real, changelog con las entradas hasta hoy en terminos NEUTRALES de metodologia: capa operacional born-operational 0096, instancias, capacidad de memoria persistente/revive employee-ready si procede; roster evolucionado descrito neutral) y REGENERA HUMAN_GUIDE.html. Pasa los 3 gates (golden human_guide + neutralidad + encoding). Devuelve cuando este verde."
question: "Confirmas la regeneracion neutral (sin dominio) con el estado real, o ves algun bloqueo de neutralidad en mencionar la capacidad de memoria como metodologia?"
---

# DIRECTIVA - Regenera HUMAN_GUIDE.html (desactualizada) desde la fuente, neutral

## El problema
`HUMAN_GUIDE.html` (raiz) esta desactualizada: `Actualizado 2026-06-10`, dice `protocol 1.1.0 /
runtime 0.11.0`, roster de 2 roles. El estado real: **epoch 1.14.0 / release v1.19.0**, capa
operacional born-operational (0096), instancias, dos-trios. Es un artefacto GENERADO
(`generate_human_guide.py`, fuente unica .md, golden case + gates) -> se actualiza la FUENTE y se
REGENERA, no se edita el HTML a mano.

## Que actualizar (en la fuente .md, luego regenerar)
- Version/epoch/runtime al estado real; fecha; entrada de changelog.
- Changelog en terminos NEUTRALES de metodologia: capa operacional born-operational (0096),
  instanciacion, y -- si pasa neutralidad -- la capacidad de MEMORIA PERSISTENTE + REVIVE
  employee-ready como capacidad de la metodologia (su promocion al master es Fase 3+ post-ventana;
  menciona como adoptada-pendiente-de-cableado si lo ves prudente).
- Roster: describe el modelo evolucionado en terminos neutrales.

## Restriccion dura (NEUTRALIDAD)
La guia es CORE/neutral de dominio (scan_domain_neutrality). **NADA de nomina, Nova-Payroll,
contabilidad, PII ni terminos de dominio.** El contenido especifico del proyecto (que se midio,
que se hizo) va en OTROS vehiculos que preparo yo: doc de medicion (operador) + Notion + manual de
Julian. La guia solo describe la METODOLOGIA generica.

## Gates
Regenera + pasa: golden `human_guide_cases`, `scan_domain_neutrality`, `scan_encoding`. Fondo
intocable (2E35F26E / 1.14.0 / N=500). Devuelve cuando verde.

-- Operador (via Asesor).
