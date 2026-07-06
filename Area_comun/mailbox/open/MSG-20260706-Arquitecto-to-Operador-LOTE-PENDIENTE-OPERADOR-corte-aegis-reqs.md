---
message_id: MSG-20260706-Arquitecto-to-Operador-LOTE-PENDIENTE-OPERADOR-corte-aegis-reqs
from: Arquitecto
to: Operador
type: HANDOFF
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-06
context_refs:
  - Area_comun/decisions/DECISION-0093-corte-gobernanza-hub-aegis-inmediato.md
  - Area_comun/artifacts/CROSS-ATESTACION-hub-aegis-registro.md
  - Area_comun/artifacts/NOTA-DISENO-peones-vs-tokens-sello-etapa2.md
  - Area_comun/artifacts/PAQUETE-DEC-DOMINIO-P3x-sello-etapa2.md
one_line_summary: "LOTE acumulativo de items que esperan tu firma/accion. Cola de la directiva DRENADA en todo lo que no depende de ti: DECISION-0093 registrada, items 4/5 hechos, runbook multi-clon + DECISION-1001/1002 + reconocimiento Contabilidad commiteados en Aegis. 4 items esperan tu mano; ninguno frena al resto."
requested_action: "Drenar el lote cuando entres: (1) ejecutar el aprovisionador de firmantes en Aegis; (2) firmar DECISION-1001 y DECISION-1002; (3) adjudicar BR-C4 del paquete DEC P3.x; (4) crear el remoto GitHub privado de Aegis. Detalle y comandos exactos abajo."
question: "Item 1 del lote (unico bloqueo real): ejecutas tu `python scripts/provision_local_signers.py` en D:/Agentes/Zeus/NOVA/Aegis (acuna secretos HMAC locales + override; frontera DECISION-0057, el classifier me lo nego con razon), o delegas explicitamente esa ejecucion puntual en mi para poder correr el humo e2e?"
---

# LOTE-PENDIENTE-OPERADOR (05:30 local, 2026-07-06) - v1

Mensaje ACUMULATIVO (regimen del GOAL): cada item lleva su artefacto LISTO; nada de esto frena
la cola. Lo actualizo si se agregan pendientes.

## 1. Aprovisionar firmantes en Aegis (bloqueo real, frontera DECISION-0057)

- **Que paso:** la verificacion (autorizada) confirmo que Aegis NO tiene firmantes operativos:
  faltan `secrets/` (HMAC) y el override `event-state.runtime.json`. El classifier me nego dos
  veces el aprovisionamiento (copiar llaves = propagacion de credenciales; generar secretos =
  acunar identidad) -- correcto: el Arquitecto no reconfigura identidad/llaves (DECISION-0057).
- **Artefacto listo:** `scripts/provision_local_signers.py` en Aegis (commit `549e88b2`,
  neutral, lee agent_registry, genera secretos FRESCOS de instancia + override apuntando a las
  privadas ed25519 ya existentes en `D:/Agentes/protocol-secrets/`). Un comando:
  `cd D:/Agentes/Zeus/NOVA/Aegis && python scripts/provision_local_signers.py`
- **Al completarse:** corro YO el ciclo e2e de humo (task_upsert -> claim -> flip -> release,
  3 firmantes) + registro la Entrada 1 de cross-atestacion en el hub. La Entrada 0 (baseline
  pre-humo, head seq 3457) ya esta anclada (commit hub `635691d`).

## 2. Firmar DECISION-1001 y DECISION-1002 (Aegis, status: proposed)

- **DECISION-1001** (iniciativa unica ingenieria disciplinada: anti-vibecoding + intake
  fusionados; identidad de producto; fases A/B/C; 6 tareas descompuestas) y **DECISION-1002**
  (memoria hibrida RUTA UNICA; supersede DECISION-0071 explicito; lecciones Engram + reglas de
  aprendizajes externos absorbidas con cita; fases F0-F5; 6 tareas). Commit Aegis `6848ec8d`.
- Serie DECISION-1001+ nativa de Aegis para no colisionar con la serie 0085+ del hub
  (convencion documentada en 1001).
- **Al firmarse:** registro los intents `decision` en el ledger de Aegis (tras item 1) y
  promuevo la primera tarea de cada descomposicion segun el orden que fijes.

## 3. Adjudicar BR-C4 (paquete DEC dominio P3.x, ya entregado antes)

- `Area_comun/artifacts/PAQUETE-DEC-DOMINIO-P3x-sello-etapa2.md` (commit `52e52ed`): unico
  item real abierto = timing de cierre de BR-C4; 3 opciones con recomendacion (a: confirmar
  que no cierra -> pool Q4 baja a n=7 sin sorpresa). Desbloquea el sello de Etapa 2.

## 4. Crear el remoto GitHub privado de Aegis (runbook multi-clon s.1)

- El origin actual de Aegis es el remote local de prueba de TASK-0232 (rechaza push non-ff).
  La rama `main` local de Aegis tiene los commits nuevos (`856af587`, `549e88b2`, `6848ec8d`,
  `f7c2c3e4`) sin remoto real.
- **Artefacto listo:** `Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md` (Aegis,
  commit `549e88b2`): remoto privado, llaves propias por clon via override gitignored,
  maker/checker por POSESION de llave, e2e de humo entre 2 clones como gate de apertura de
  Contabilidad. Solo falta el repo privado en GitHub y `git remote set-url origin <url>`.

## Estado del resto de la directiva (sin dependencia tuya)

- DECISION-0093 (corte hub->Aegis, complemento 0088): registrada en el ledger del hub y
  pusheada (commit `e951dba`).
- Item 4 (nota peones-vs-tokens, ventanas por completitud certificada como regla) + item 5
  (enmienda s.26 del sello, declaracion arm-ortogonal): hechos (commit `638fc99`);
  TASK-0231 re-alcanzada con traza.
- Item 3 (Contabilidad): reconocimiento acotado entregado en Aegis (commit `f7c2c3e4`):
  57 formularios, 37 tablas (~203k registros), y HALLAZGO: ya existe esquema `Accounting`
  parcial (8 scripts + views) del trabajo de frontera de Presupuesto -- el analisis completo
  sigue siendo bloque multi-sesion, pero no arranca de cero.
- Veredictos del Analista sobre #10 y #11-13: siguen pendientes (2 ACTIONs vivos en open/),
  monitor armado.

-- Arquitecto
