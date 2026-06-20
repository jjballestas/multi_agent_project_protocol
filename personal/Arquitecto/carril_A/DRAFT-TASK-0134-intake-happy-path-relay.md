# DRAFT v2 - TASK-0134: REMEDIACION DE SEGURIDAD del intake (RF-14) - anti-impersonacion + relay acotado + camino feliz + accountability + UX

> DRAFT v2 en personal/Arquitecto; NO promovido. Espera ratificacion de DECISION-0052 v2 + ext2 SPEC-0086 v2.
> maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol. **Es REMEDIACION de un defecto de seguridad
> CRITICO ya mergeado (Zeus 42e7931), no solo "agregar el relay".** Insumo: veredicto adversarial del Analista.

## Contexto del defecto (anomalia DECISION-0018, ya en canonico)
`src/server.js` (Zeus 42e7931): `actorId = action.actorId || payload.actorId || "Arquitecto"` (linea 384) y
para acciones no-intake los `intents` vienen crudos del cliente (linea 371; solo se valida el kind). Endpoint
127.0.0.1 sin auth -> un POST local puede forjar decision/claim/task_status atestado firmado como Arquitecto.

## Alcance (remediacion)
1. **#1 ANTI-IMPERSONACION (CRITICO, bloqueante):**
   - Eliminar el trust de `payload.actorId` y de `payload.intents` crudos.
   - Cada accion gobernada = **builder SERVER-SIDE con forma estricta**: el servidor construye el intent
     canonicamente desde campos de datos validados; el cliente no inyecta intents.
   - `actorId` determinado SERVER-SIDE por accion. Relay-como-Arquitecto SOLO para la forma exacta
     `requirement-intake` (task_upsert requirement, author=Operador).
   - **Prueba negativa PERMANENTE (AC19):** forjar actorId/intents arbitrarios o cualquier forma !=
     requirement-intake como Arquitecto -> RECHAZADO (no firma, no escribe). En CI.
2. **#3 ACCOUNTABILITY (AC20):** evento con `endorsement:none`; firma=origen+transporte, no aval; test de
   que un relayado NO cuenta como autorado/avalado por el Arquitecto. El aval es la SPEC posterior.
3. **CAMINO FELIZ (AC15, write REAL no mock):** test de comportamiento permanente que demuestra
   execute+confirm -> escritura real (requirement en estado, seq, drift 0, author=Operador/relayed_by).
4. **RENDER honesto (AC18):** UI muestra firmante=Arquitecto + author=Operador; ningun verde "Operador firmo".
5. **#4 byte-identico:** asertar config/genesis/keys/version byte-identicos (no solo drift 0).
6. **PII (AC16):** redaccion estructural por patrones best-effort; NO sobre-afirmar PII-free; DEF-PII sigue gate.
7. **UX (Claude Design):** project-first + tipografia del selector destacada (rework de components/intake/).
8. **(opcional, follow-on) endpoint hardening:** token de confirmacion/same-origin/loopback-auth en EXECUTE
   contra drive-by (severidad menor una vez cerrado #1; decido si entra aqui o como pieza aparte).

## DoD / CONDICION DE CIERRE (innegociable)
- **(a) Prueba negativa de impersonacion (AC19) VERDE** + **(b) camino feliz con write REAL (AC15) VERDE.**
  TASK-0134 NO cierra sin ambas.
- AC18/AC20 + #4 byte-identico + AC16 + carry AC11/AC12/AC13/AC14/AC17 verdes.
- node --test/CI verde (incl. AC19 y AC15 permanentes); npm start ejecutable; vista Intake navega y ESCRIBE.
- validate exit 0 CON y SIN secretos (clon limpio, DECISION-0046); drift 0; #4 epoca 1.14.0 byte-identica;
  neutralidad limpia.
- **Nueva pasada del Analista sobre el fix de #1 ANTES de cerrar** (orden del operador).
- Reproducido por el checker (Arquitecto) desde clon limpio, incluyendo el write real Y la prueba de
  impersonacion; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Operador como firmante propio (re-genesis RF-9 roster, DIFERIDO).
- DEF-PII vivo / captura PII real (TASK-0118 gate).
