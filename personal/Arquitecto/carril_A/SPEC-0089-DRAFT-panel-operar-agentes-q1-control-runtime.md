# SPEC-0089 (DRAFT) - Panel "Operar Agentes" (Q1): control de runtime (vivo/dormido + activar/detener) + despertar al destino

- **Estado:** DRAFT en personal/Arquitecto/carril_A (pendiente promocion al ledger + GO). Maker: Codex. Checker: Arquitecto + pasada Analista (no-bypass / no-autoridad / allowlist).
- **Fecha:** 2026-06-24. Repo producto: D:/Agentes/Zeus/Zeus-protocol.
- **Origen (REQ del operador):** REQ-885632826E ("Boton Enviar al Arquitecto" en el Intake) + REQ-9442785DD6 ("Indicador vivo/dormido y boton activar/detener por agente").
- **Relacionada:** SPEC-0086 (front MVP, AC17 no-bypass / AC58 auto-push / AC72 error amable), SPEC-0088 (Q2 consola), DECISION-0057 (el Arquitecto activa/detiene runtimes; runtime-only, nunca reconfigura identidad/keys/registry, honra stop del operador), DECISION-0050 (front=panel del operador).

## Objetivo

Que el operador VEA si cada agente esta vivo o dormido (con su ultimo latido) y pueda activarlo/detenerlo desde el
front, y que al montar un requisito en el Intake pueda "Enviar al Arquitecto" (registrar + despertar al Arquitecto si
esta dormido), sin VS Code ni terminal. El control de runtime es **runtime-only** (DECISION-0057): arranca/detiene el
runtime de un agente REGISTRADO; NUNCA ejecuta un comando arbitrario, NUNCA concede autoridad de riesgo, NUNCA toca
identidad/keys/registry/#4.

## Alcance / Out of scope

- En alcance: (1) indicador vivo/dormido + ultimo latido por agente, DERIVADO del estado real del runtime; (2) boton
  activar/detener por agente, acotado al agent_registry (allowlist), accion gobernada server-side; (3) "Enviar al
  Arquitecto" en el Intake = requirement-intake gobernado (ya existe) + notificacion mailbox + despertar al Arquitecto
  si dormido + el front marca "tomado".
- Fuera de alcance: alta/baja de agentes (Q3 roster = re-genesis-boundary), conceder capabilities nuevas, supervisor
  always-on (decision aparte), ejecutar comandos arbitrarios.

## acceptance_criteria

- **AC1 - Indicador vivo/dormido + ultimo latido (real).** Por cada agente del agent_registry, el front muestra
  vivo/dormido y su ultimo latido, DERIVADO del estado real del runtime (heartbeat/proceso), no estatico ni
  hardcodeado. Fail-safe: si no hay senal -> "dormido/desconocido", nunca "vivo" falso. Behavior-test: dado un
  heartbeat reciente -> vivo; sin heartbeat o antiguo -> dormido.
- **AC2 - Activar/detener runtime por agente (allowlist, gobernado).** Boton activar/detener por agente; la accion es
  server-side gobernada y SOLO aplica a un agente REGISTRADO (allowlist del agent_registry); jamas compone un comando
  arbitrario (sin shell injection: el server mapea agent_id -> su runtime conocido). Activar/detener es runtime-only
  (DECISION-0057): no reconfigura identidad/keys/registry, no concede capabilities. Behavior-test: activar un agente
  conocido invoca el arranque mapeado; un agent_id no registrado/arbitrario -> rechazo 400 (no ejecuta nada).
- **AC3 - "Enviar al Arquitecto" desde el Intake (REQ-885).** En el Intake, un boton "Enviar al Arquitecto" que: (a)
  registra el requisito por el camino gobernado (requirement-intake -> submit_intent, ya existente, llega al canonico);
  (b) notifica al Arquitecto por el mailbox (MSG gobernado) y (c) despierta su runtime si esta dormido (AC2); (d) el
  front indica "tomado/registrado". Behavior-test: presionar -> requirement-intake gobernado + MSG al Arquitecto +
  (si dormido) activar; el front muestra el estado tomado. NO push manual del operador.
- **AC4 - No concede autoridad / no-bypass (carry AC17).** Activar un agente NO le concede autoridad de riesgo; el
  agente sigue bajo sus reglas/capabilities. Ninguna accion de este panel crea una ruta de escritura de estado fuera
  de lo gobernado (submit_intent / MSG gobernado). Behavior-test: el contrato negativo no-bypass se mantiene; activar
  no altera capabilities ni #4.
- **AC5 - Estado claro + error amable (carry AC72).** "activando/deteniendo" + exito o error AMABLE (canal/ocupado o
  runtime no disponible -> mensaje amable, no traceback crudo). Behavior-test: exito refleja nuevo estado; fallo ->
  mensaje amable.
- **AC6 - Off-by-default / sin riesgo nuevo / #4 byte-id.** El panel solo arranca/detiene runtimes de agentes
  registrados y escribe por el camino gobernado; #4 byte-identica (no toca protocol.config.json). Sin secretos al log.

## DoD

- AC1-AC6 verdes con behavior-tests deterministas; carry AC16/AC17/AC58/AC72. node --test clon limpio exit 0;
  validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4 byte-identica.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA (foco: allowlist sin
  comando arbitrario; activar no concede autoridad; no-bypass; vivo/dormido derivado real, sin falso-vivo).
- REPRO: en el front, ver vivo/dormido por agente; activar un agente dormido -> pasa a vivo; en el Intake "Enviar al
  Arquitecto" -> requisito al canonico + MSG + (si dormido) Arquitecto activado + "tomado".

## Notas de diseno

- La accion activar/detener debe ser una ALLOWLIST estricta agent_id -> runtime conocido (mapa server-side), NUNCA un
  comando del cliente. Esta es la barrera de seguridad central; el Analista la prueba con un agent_id arbitrario.
- "Vivo/dormido" se deriva de una senal real (p.ej. mtime del heartbeat/cron log del agente, o proceso); definir la
  fuente canonica de heartbeat por agente. Fail-safe a "dormido".
- DECISION-0057 ya autoriza al Arquitecto a activar/detener runtimes; el front expone ESA capacidad al operador con
  los rails (allowlist, runtime-only, honra stop). El despertar-al-destino que Q2 difirio se implementa aqui (AC3).
- Consolida REQ-885632826E + REQ-9442785DD6 (ambos del mismo extraction_task TASK-EXTRACT-1F5C13A7B5).
