---
spec_id: SPEC-0056-neutralidad-exime-runtime-state
task_id: TASK-0070
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0022, DECISION-0017]
relates_to: [SPEC-0055, SPEC-0052]
---

> Fix de gate descubierto al intentar la activacion sombra del writer-vivo (3.b). El scan de neutralidad
> cubre `runtime/**` y por tanto escanea `runtime/state/` (event log + snapshots content-addressed
> generados por el runtime), que embeben el estado de protocolo vivo (puede referenciar el dominio del
> piloto). Aditivo, config-gated, paridad py/.ps1 (ambos leen el mismo config). NO debilita el boundary de
> neutralidad del core. Desbloquea la activacion sombra.

# SPEC-0056 - Neutralidad exime runtime/state (dato generado por el runtime)

## 1. Problema

`domain_neutrality.scan_globs` incluye `runtime/**`. Eso escanea tambien `runtime/state/` que es **dato
GENERADO por el runtime** (event log `events.jsonl`, `snapshot.json`, y snapshots content-addressed
`runtime/state/snapshots/<hash>.json`). Esos snapshots son una materializacion del ledger vivo
(TASK_INDEX/PROJECT_STATE/CLAIMS) y por diseno pueden contener terminos del dominio de la instancia (p.ej. la
referencia al piloto). Resultado: emitir el genesis del writer-vivo hace fallar el scan de neutralidad
(`runtime/state/snapshots/...: trading`), aunque el core sigue siendo neutral.

Inconsistencia: el ledger vivo `Area_comun/state/*.json` **ya esta exento** (solo se escanean los
`*.template.json`) y `runtime/runs/` ya esta en `.gitignore`. `runtime/state/` deberia tratarse igual:
es instancia-generada, no fuente del protocolo.

## 2. Solucion (aditiva, paridad py/.ps1)

1. **Exencion de neutralidad:** anadir `runtime/state/**` a `domain_neutrality.exempt_globs` en
   `protocol.config.json` (vivo) y `protocol.config.template.json` (master). El scan sigue cubriendo la
   FUENTE del runtime (`runtime/*.py`, `runtime/adapters/**`, `runtime/*.md`, etc.); solo deja de policiar
   el estado generado. Paridad automatica: `scan_domain_neutrality.py` y `.ps1` leen `exempt_globs` del
   mismo config.
2. **.gitignore:** NO gitignorar `runtime/state/` de forma general: en modo autoritativo el event log y los
   snapshots son fuente de verdad y deben commitearse. Documentar el razonamiento (queda committable; la
   neutralidad lo exime por ser dato de instancia, no core). (Si se quisiera, ignorar solo artefactos
   efimeros concretos, pero NO los snapshots/log autoritativos.)
3. **Sin cambio de boundary:** el core permanece neutral; runtime/state es dato de instancia (analogo al
   ledger vivo ya exento). No requiere DECISION nueva (consistencia con exenciones existentes); enlaza
   DECISION-0022/0017.

## 3. Tests (golden determinista)

1. Un archivo bajo `runtime/state/` (p.ej. un snapshot) con un termino del denylist => el scan **PASA**
   (exento). Caso en `examples/neutrality_scan_cases` (+ paridad ps1) o golden nuevo.
2. Un termino del denylist en una FUENTE del runtime escaneada (p.ej. `runtime/foo.py`) => el scan sigue
   **FALLANDO** (la exencion no abre un agujero en el core).
3. Regresion: el resto del scan de neutralidad intacto; suite de gates verde.

## 4. Verificacion adicional (sanity de la activacion, no parte del entregable de codigo)

- Tras el fix: re-emitir un genesis del writer-vivo sobre el estado vivo NO debe hacer fallar la neutralidad.
  (Esto lo valida el arquitecto al re-intentar la activacion sombra; el entregable de la tarea es el fix +
  golden.)

## 5. Fuera de alcance

- Encender event_state/enforce/authoritative (eso es la activacion, decision del operador).
- Cambiar que terminos estan en el denylist.
- Cambios al contrato del turn schema.

## 6. SemVer

- MINOR (correccion de gate aditiva/consistencia; no debilita el boundary del core; no cambia contrato).
