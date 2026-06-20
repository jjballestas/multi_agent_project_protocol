---
id: TASK-0130
title: Proyecto-front MVP etapa 6 - Multi-proyecto (selector read-only, modelo hub-centrico) + Kickoff RF-10 gobernado (DECISION-0049 / DECISION-0050 / SPEC-0086)
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0049, DECISION-0050, DECISION-0029, DECISION-0047]
created_at: 2026-06-20
---

# TASK-0130 - Proyecto-front MVP etapa 6 (Multi-proyecto + Kickoff RF-10)

## Objective

Ultima etapa del MVP-T0 (SPEC-0086), sobre etapas 1-4 done. Cierra el front como herramienta diaria
del operador: **selector multi-proyecto read-only** + **kickoff RF-10 gobernado**. Modelo
**HUB-CENTRICO** (confirmado por el operador; DECISION-0050): la gobernanza de todos los proyectos vive
en el HUB UNICO (este protocolo = dataset atestado); los repos producto rotan bajo `D:\Agentes\Zeus\`.
Etapa 5 (roster RF-9) queda **DEFERIDA** (pull-based; sin agente que agregar). Al cerrar, front
ejecutable (`npm start`). En `D:\Agentes\Zeus\Zeus-protocol`. maker=Codex, checker=Arquitecto.

## Insumo de diseno

Design system de Claude Design en `D:\Agentes\Zeus\Zeus-protocol\design\interface\` (citar por hash el
commit relevante; componentes dashboard/selector/canonical-indicator/badges). El diseno alimenta la UI;
NO bloquea la logica. Tokens dark-first ya establecidos en etapas previas.

## Alcance (SPEC-0086 etapa 6, modelo hub-centrico)

**Multi-proyecto (RF-12 MVP-light minimo):**
- Selector/dashboard **READ-ONLY** de los repos PRODUCTO bajo `D:\Agentes\Zeus\`: descubrir los
  directorios; para cada repo git mostrar resumen read-only (HEAD short, branch, ultimo commit,
  limpio/sucio). Directorios no-git (p.ej. NOVA, una instancia separada) se listan como read-only sin
  leer su gobernanza.
- La **GOBERNANZA** (vistas RF-1..RF-4: tasks/claims/ledger/atestacion) SIGUE apuntando al **HUB UNICO**
  (dataset, DECISION-0050). El selector NO cambia la fuente de gobernanza ni lee Area_comun de otros dirs.
- Indicador por repo (canonical/working_tree o git clean/dirty) **DERIVADO del estado real** (no estatico,
  no verde hardcodeado).

**Kickoff (RF-10) gobernado:**
- Lanzar un proyecto nuevo desde la UI = registrar su PRIMER handoff gobernado (T0) **EN EL HUB** via
  `submit_intent` (transaccion atomica idempotente, con actor/timestamp; AC2, 0 bypass de gates/#4/drift).
- El `git-init` del repo producto bajo Zeus es paso del **OPERADOR** (out-of-band). El front **NO** agrega
  ninguna ruta de escritura raw nueva (sin git-init ni escritura de FS de producto desde el front); SOLO
  emite la transaccion de gobernanza por `submit_intent`.
- **Prueba negativa:** no existe ruta en el front que cree repo o escriba estado/ledger sin `submit_intent`.

**Restricciones:** read-only sobre el canonico del hub (objetos git/origin, no working tree) para la
gobernanza; sin tocar #4/config (epoca 1.14.0 pinned, DECISION-0047); codigo SOLO en Zeus-protocol;
gobernanza/cita en Area_comun; PII-free; canal ASCII para lo que escribe al protocolo.

## DoD

- Selector multi-proyecto read-only operativo (lista repos bajo Zeus + resumen git read-only; gobernanza
  = hub unico; indicador honesto por repo).
- Kickoff RF-10 emite el T0 gobernado SOLO via `submit_intent` (sin bypass); **prueba negativa** verde
  (sin ruta de escritura directa ni git-init desde el front).
- **AC11 PERMANENTE (test de COMPORTAMIENTO):** todo badge/indicador nuevo del selector
  (canonical/working_tree/clean-dirty) se DERIVA de verificacion real -> verificacion que FALLA /
  no-canonico / indeterminado = **NO-verde**; valido = verde; nunca verde hardcodeado. El test falla si un
  refactor repinta verde un estado fallido.
- `node --test` verde (>= los 13 actuales + nuevos), gateado por EXIT REAL; `node --check` OK; front
  ejecutable (`npm start`).
- Gates del protocolo: `validate_collaboration_state.py --root .` **CON y SIN secretos** exit 0
  (DECISION-0046); drift 0; `scan_encoding` / `scan_domain_neutrality` exit 0. Epoca 1.14.0 pinned, #4 ON.
- SPEC-0086 AC1 (read-only canonico) / AC2 (escritura solo via submit_intent + prueba negativa) / AC6
  (neutralidad/acoplamiento) / AC7 (CI verde) / AC9 (determinismo/trazabilidad) / AC10 (gates protocolo) /
  AC11 (honestidad regresion-proof). maker=Codex / checker=Arquitecto; reproduccion del checker desde clon
  limpio. Reporta a in_review con claim file-scoped + `submit_intent`. Codigo en Zeus-protocol; cita en
  Area_comun (dataset).
- Con RF-10 verde, el MVP-T0 cierra RF-1..RF-8 + RF-10 (+ RF-4 atestacion); **RF-9 (roster, etapa 5) queda
  DEFERIDA explicitamente** (pull-based, sin agente que agregar).

## Verification

- CI del producto verde (`node --test`) incluyendo: casos de COMPORTAMIENTO del indicador del selector
  (estado real falla -> no-verde; valido -> verde; indeterminado -> warn) y **prueba negativa del kickoff**
  (toda escritura via submit_intent; sin ruta directa ni git-init desde el front).
- Gates del protocolo exit 0 (con y sin secretos), drift 0, gateado por EXIT REAL del validador.
