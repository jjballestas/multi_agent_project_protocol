# Carril A - Instrumentacion de tesis (DRAFTS para revision + GO del operador)

> Autor: Arquitecto. Fecha: 2026-06-19. Estado: **DRAFT en area privada** (no tocan el ledger).
> Promocion via `submit_intent` SOLO tras GO del operador. Sin GO no se enciende nada.
> Brief: `personal/operador/09_Asistente_pipeline-presupuesto-tesis.md`.

## GO del operador al encuadre (2026-06-19) - estado: REVIEW-READY

El operador dio GO al encuadre (no a promover; sin promocion al ledger hasta vistos Analista+Codex + GO
explicito). Confirmaciones (verificadas por el asistente, git HEAD 86b9476):

- **A1 (#4):** ACTIVACION gateada + endurecimiento grado-tesis REFERENCIANDO DECISION-0029 (no
  duplicada). TASK-0101/0102/0103/0113 todas done; `chain_enabled`/`agent_signatures_enabled`/
  `anchor_enabled` = false. Encuadre correcto.
- **A3 (§9):** MISMO PATRON aplicado - precondicion de enforcement read-only REAL que REFERENCIA
  DECISION-0035 (no la redecide). Nota de encuadre anadida al draft A3.
- **A2 (GATE-DATASET):** DECISION NUEVA (no existe decision previa de base legal/PII).
- **Ventana de riesgo:** Carril A solo; #4 ON antes del primer handoff real (no retrofiteable); NO
  combinar con SA.4 / authoritative-teeth / subagents.

El operador reactiva a Analista (honestidad/metodologia) y Codex (invariante de codigo) para la
revision paralela. Los drafts A1/A2/A3 quedan listos para revision. A la espera de sus vistos + GO
del operador antes de promover por `submit_intent` (SemVer MINOR + CHANGELOG).

## 0. Reconciliacion previa (honestidad - LEER PRIMERO)

El brief pide "DECISION + SPEC #4 atestacion de autoria" como si fuera de cero. **No lo es.** El
MECANISMO #4 ya existe, construido off-by-default:

- **DECISION-0029** (accepted 2026-06-12): politica "firmantes cruzados sin consenso" (prev_hash +
  firma por agente + anclaje externo), con modelo de amenaza y limites declarados.
- **TASK-0101** (done): `prev_hash` encadenado en `eventlog.py` (`event_state.chain_enabled`, OFF).
- **TASK-0102** (done): firma por agente / atestacion (`agent_signatures_enabled`, OFF; backend
  `local-ed25519`; `signature_config.public_keys = {}` VACIO).
- **TASK-0103** (done): anclaje externo periodico (`anchor_enabled`, OFF; backend `git-remote`).
- **TASK-0113** (done): fix de interaccion chain+auth (seguro encender ambos); golden combinado en CI.

Estado vivo en `protocol.config.json`: `chain_enabled:false`, `agent_signatures_enabled:false`,
`anchor_enabled:false`, `event_auth.enabled:false`, `public_keys:{}`.

**Implicacion:** Carril A·A1 NO es disenar el mecanismo otra vez. Es lo que DECISION-0029 sec. nota
difirio explicitamente: "su encendido exige SPEC cerrada + golden cases verdes + aprobacion explicita
posterior del operador". Es decir: **(1) ACTIVACION gateada off->piloto->on**, **(2) endurecimiento
grado-tesis** (modelo de amenaza A1-A4 documentado, manipulation-check >=99%, identidad/llaves por
agente provisionadas, cadencia de anclaje), **(3) provisioning de llaves publicas** (hoy `{}`).

**Recomendacion del Arquitecto:** redactar A1 como **DECISION de ACTIVACION que referencia
DECISION-0029** (no una decision duplicada que re-decida la politica). Asi quedan los DRAFTS. Si el
operador prefiere otro encuadre, lo ajusto antes de promover.

## 1. Los 3 entregables del Carril A (este paquete)

| Draft | Que es | Gobierna |
|-------|--------|----------|
| `DRAFT-DECISION-0039-activacion-atestacion-autoria.md` | A1 - DECISION de activacion #4 | encender chain+firmas+anclaje off->piloto->on, grado-tesis |
| `DRAFT-SPEC-0081-activacion-atestacion-autoria.md` | A1 - SPEC (acceptance_criteria + test_plan) | manipulation-check >=99%, provisioning de llaves, piloto, prueba negativa |
| `DRAFT-DECISION-0040-gate-dataset.md` | A2 - DECISION GATE-DATASET | base legal + dos planos (CERO PII de Budget en el event log) + DPIA-lite + ToS |
| `DRAFT-DECISION-0041-precondicion-acoplamiento-readonly.md` | A3 - DECISION precondicion §9 | enforcement read-only REAL del satelite antes de lectura viva (#2/#3) |

(IDs DRAFT; los IDs finales y la version SemVer se asignan al promover por `submit_intent`.)

## 2. Restriccion de orden DURA (del brief, innegociable)

**#4 atestacion ON antes del primer handoff real del modulo-app.** La cripto encadenada NO es
retrofiteable: si se enciende despues, el historial previo no es atestable. Por eso Carril A va PRIMERO
y por eso el encadenado debe estar ON en el momento de captura del primer handoff = T0 del dataset.

## 3. Flujo (del brief)

```
Arquitecto redacta DRAFTS (este paquete)
   -> Analista (honestidad/metodologia) + Codex (invariante de codigo) revisan EN PARALELO
   -> operador da GO
   -> Arquitecto promueve por submit_intent (SemVer MINOR + CHANGELOG; DECISION + SPEC + tareas)
   -> recien entonces: provisioning de llaves -> piloto -> manipulation-check -> GO -> ON
```

**Dependencia de coordinacion:** Analista y Codex estan en STAND-DOWN (cierre del trio). La revision
en paralelo requiere que el **operador los reactive**. No los reactivo yo (ciclo de agentes: el
operador activa por proceso). Aviso, no actuo.

## 4. Invariantes respetados en estos drafts

- Escritor unico: NO escribo el ledger; drafts en area privada. Promocion solo por `submit_intent`.
- Neutralidad de dominio: reglas fiscales NO aparecen aqui (van al perfil en Carril B, no al core).
- Dos planos / sin PII (DECISION-0033): reforzado en A2 (la PII de Budget jamas entra al event log).
- Un multiplicador de riesgo por ventana: la activacion #4 es SU PROPIA ventana (no se combina con
  SA.4, ni con cambios de authoritative, ni con subagents).
- Regla 3.4: cada pieza la jala una necesidad real con fecha (instrumentar el modulo-app de Presupuesto).

## 5. Que NO hice (a proposito)

- No promovi nada al ledger (sin GO).
- No encendi ningun flag.
- No re-arme cron ni reactive a Codex/analista (lo hace el operador).
- No toque Carril B/C (sin GO explicito).
