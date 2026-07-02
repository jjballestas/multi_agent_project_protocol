# SPEC-F1-EXCEPTION-TRAILERS - exception.recorded + trailers bloqueantes (v0.1)

Estado: DRAFT del Asesor para F0; el Arquitecto la refina y Codex la implementa en F1.
Cubre los items F1.2 y F1.3 del tablero (bloqueantes 2 y 3 de la ronda 2). Cierra las
rutas de reinterpretacion post-hoc del pre-registro: ayudas invisibles por chat/llamada,
arbitrajes sin rastro, suspensiones sin evento y commits de fix sin linkage.

## PARTE A - Evento `exception.recorded` (item F1.2)

### A.1 Intent nuevo en submit_intent

```json
{
  "intent": "exception",
  "payload": {
    "exception_id": "EXC-XXXX",
    "kind": "manual_intervention | assist | arbitration | suspension | scope_change | intake_exempt | risk_reclass | budget_overrun | other",
    "task_id": "TASK-XXXX | null",
    "actor": "<id del que registra>",
    "beneficiary": "<id del ayudado | null>",
    "summary": "<ASCII, 1-3 lineas, sin PII>",
    "channel": "chat | call | mailbox | in_person | other",
    "impact": "none | time | scope | quality",
    "publishable": true
  }
}
```

- Firmado ed25519 como todo evento del ledger; entra a la cadena #4.
- `kind` es enum CERRADO (cero prosa libre en campos estructurales, leccion
  DECISION-0071/B): lo no clasificable va a `other` + summary.
- `summary` ASCII y sin PII: nombres de personas se refieren por id de agente/rol.
- `budget_overrun` es el kind que implementa el stop del Carril B (bloqueante 5):
  exceso de 1 dia/semana => evento + pausa.

### A.2 Reglas de uso (doctrina en TASK_PROTOCOL)

- U1: toda ayuda/des-atasco de un empleado u agente (HP6: evento manual.intervention),
  todo arbitraje de defecto, toda suspension de sprint y toda reclasificacion de
  riesgo SE REGISTRA como exception.recorded. Lo que no este registrado no existe
  para el estudio; el estudio declara esta regla en el pre-registro.
- U2: los exception.recorded del periodo se LISTAN en el reporte publico del estudio
  (inviolabilidad: el operador puede arbitrar, pero queda rastro publicable).
- U3: exencion de intake (SPEC-F1-gate-intake R5) exige kind=intake_exempt previo.

## PARTE B - Trailers bloqueantes de commit (item F1.3)

### B.1 Formato exacto (trailers git estandar, ultima seccion del mensaje)

```text
Task-Id: TASK-0241            # obligatorio en commits que tocan rutas gobernadas
Task-Id: none                 # alternativa SOLO con Ops-Reason
Ops-Reason: <motivo corto>    # obligatorio si Task-Id: none
Fixes-Task: TASK-0241         # obligatorio ADEMAS si el commit es fix/revert/hotfix
```

Regex de validacion: `^Task-Id: (TASK-\d{4}|none)$` y `^Fixes-Task: TASK-\d{4}$`.
Un commit es fix/revert/hotfix si su subject matchea
`^(fix|revert|hotfix)(\(|:|!)` (conventional commits).

### B.2 Reglas de validacion

- V1: el validador escanea los commits desde un `trailer_start_seq`/commit de arranque
  registrado en la DECISION de adopcion (los commits historicos quedan EXENTOS; no se
  reescribe historia). PRECONDICION DE ACTIVACION (hallazgo F-2 del Arquitecto
  2026-07-02): `trailer_start_seq` se fija en un punto POSTERIOR al despliegue de
  F1-E (harnesses de Codex/Analista y flujo del Arquitecto emitiendo trailers).
  Activar V2-V5 con harnesses sin actualizar = auto-DoS del ledger (cada commit de
  peer falla validate); PROHIBIDO. La implementacion de F1-C puede construirse antes,
  pero el boundary de activacion espera a F1-E.
- V2: commit posterior al arranque que toca rutas gobernadas (Area_comun/**, runtime/**,
  scripts/**, protocol.config.json) sin trailer `Task-Id:` valido => validate exit != 0.
- V3: commit fix/revert/hotfix sin `Fixes-Task:` valido => exit != 0. `Fixes-Task`
  debe referir una tarea EXISTENTE en TASK_INDEX (o archivo).
- V4: `Task-Id: none` sin `Ops-Reason:` => exit != 0. El uso de `none` se reporta
  (conteo en el reporte del estudio; si crece, es Goodhart y se revisa).
- V5: texto libre ambiguo NO cuenta: solo el trailer exacto pasa (mata "fixes the
  task from yesterday" en el cuerpo).

### B.3 Casos de prueba minimos (DoD de F1.3, sobre repo fixture)

(N1) commit gobernado sin Task-Id; (N2) fix sin Fixes-Task; (N3) Fixes-Task a tarea
inexistente; (N4) none sin Ops-Reason; (P1) commit gobernado con Task-Id valido;
(P2) fix con ambos trailers; (P3) commit pre-arranque exento; (P4) ruta personal/**
exenta.
