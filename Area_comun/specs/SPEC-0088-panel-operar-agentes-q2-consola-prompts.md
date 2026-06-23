# SPEC-0088 - Panel "Operar Agentes" (Q2): consola de prompts agente-a-agente desde el front

- **Estado:** draft (Arquitecto autora desde los REQ aprobados por el operador; pendiente registro en ledger).
- **Fecha:** 2026-06-24. **Maker:** Codex. **Checker:** Arquitecto + pasada Analista (PII/no-bypass).
- **Origen (REQ del operador, sdd seed):** REQ-269EBF78 / REQ-68896287BC ("Consola de prompts agente-a-agente
  desde el front"). Duplicados por reintentos de "Canal ocupado"; se consolidan a esta SPEC.
- **Relacionada:** SPEC-0086 (front MVP, RF-14 intake, AC16 PII / AC17 no-bypass / AC58 auto-push), DECISION-0050
  (front = panel del operador), DECISION-0057 (activacion de runtimes), debate
  personal/Arquitecto/carril_A/DEBATE-front-agent-console-roster.md. Repo producto: D:/Agentes/Zeus/Zeus-protocol.

## Objetivo

Que el operador pueda HABLARLE a los agentes (Arquitecto/Codex/Analista/workers) desde el front y ver sus
respuestas, sin VS Code ni terminal. El canal NO es nuevo: es el **mailbox gobernado** (MSG-*.md, ASCII,
atestable) expuesto en UI. La consola de prompts = compose de mailbox gobernado + vista de hilo; NO un segundo
escritor ni un bypass del gobierno.

## Alcance / Out of scope

- En alcance: vista "Operar Agentes" con selector de agente + caja de prompt + envio gobernado al mailbox + vista
  de hilo (prompt del operador + respuestas del agente) read-only sobre el canonico.
- Fuera de alcance (otras piezas del panel): despertar/detener runtime del agente (Q1, control de runtime), alta de
  agentes (Q3 roster), supervisor always-on (decision aparte). El "despertar al destino" se DIFIERE a Q1; en Q2 el
  agente vivo procesa su mailbox como hoy.

## acceptance_criteria

- **AC1 - Vista con selector de agente + prompt.** Una vista "Operar Agentes" (o panel) con un COMBO de agente
  (los agentes del agent_registry: Arquitecto/Codex/Analista + workers de producto registrados) + una caja de
  prompt (texto) + boton "Enviar". El combo se puebla del registro real (no hardcodeado). Behavior-test: el combo
  lista los agentes del registro; sin agente seleccionado, "Enviar" deshabilitado.
- **AC2 - Enviar compone un MSG gobernado al mailbox (no bypass).** "Enviar" compone un mensaje al mailbox
  (`Area_comun/mailbox/open/MSG-<ts>-Operador-to-<agente>-...md`) con: `from: Operador`, `relayed_by: Arquitecto`,
  `to: <agente>`, `type: DIRECTIVE` (o QUESTION), `status: open`, una marca `operator_directive: true`, y el cuerpo
  del prompt. La escritura va por el CAMINO GOBERNADO del front (commit + auto-commit-push AC58); NO crea una ruta
  de escritura de estado/ledger fuera de lo gobernado (carry AC17); el prompt NO concede autoridad nueva al agente
  (sigue operando bajo sus reglas/capabilities). Behavior-test: enviar produce un MSG mailbox bien formado con la
  marca operator_directive; no toca submit_intent-state ni capabilities; el contrato negativo de no-bypass se mantiene.
- **AC3 - Guarda PII + ASCII en el prompt (carry AC16).** El cuerpo del prompt se canaliza ASCII y el texto libre se
  redacta/marca en el plano publicable; se advierte al operador (no incluir PII de terceros). Behavior-test: un
  prompt con patrones tipo NIT/razon social/SQL -> el plano publicable no expone el literal; canal ASCII.
- **AC4 - Vista de hilo (conversacion) read-only.** La vista muestra el HILO con el agente seleccionado leyendo el
  mailbox (open + archived) filtrado por `to/from = <agente>` (y la marca operator_directive para los del operador):
  el prompt del operador + las respuestas del agente, en orden. Es READ-ONLY sobre el canonico (via el lector
  canonico read-only ya existente); no inventa estado. Behavior-test: dado un mailbox con prompt del operador +
  respuesta del agente -> el hilo los muestra en orden; PII redactada en el render.
- **AC5 - Estado de envio claro.** Al enviar, indicador de "enviando" + resultado: exito (mensaje en el hilo) o
  error AMABLE (carry AC72: si el ledger/canal esta ocupado -> "Canal ocupado, intente mas tarde", no el error
  crudo). Behavior-test: envio ok -> aparece en el hilo; contencion -> mensaje amable.
- **AC6 - Off-by-default / sin riesgo nuevo.** La consola solo ESCRIBE al mailbox gobernado y LEE el canonico; no
  enciende capacidades vivas ni concede autoridad. #4 byte-identica (no toca protocol.config.json). El agente
  destino procesa el mailbox cuando este vivo (despertarlo es Q1, fuera de alcance).

## DoD

- AC1-AC6 verdes con behavior-tests deterministas; carry AC16/AC17/AC58/AC72. node --test clon limpio exit 0;
  validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4 byte-identica.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA (PII + no-bypass +
  que el prompt no concede autoridad).
- REPRO: en el front, seleccionar Codex, escribir un prompt, Enviar -> aparece un MSG mailbox to:Codex con la marca
  operator_directive; el hilo lo muestra; (con Codex vivo) Codex responde y la respuesta aparece en el hilo.

## Notas de diseno

- La marca `operator_directive: true` distingue un prompt libre del operador de los handoffs SDD; el agente lo
  atiende pero sigue sus reglas (no es una orden que salte gobernanza). Un prompt del operador a Codex que pida
  implementar algo deberia, idealmente, derivar en el flujo SDD normal (GO/tarea), no en codigo directo; eso lo
  decide el agente segun sus reglas.
- El claim para escribir el MSG mailbox debe ser FILE-SCOPED al MSG concreto (DECISION-0042) y, con el grano fino
  (DECISION-0059/TASK-0164), no bloquea a otros escritores.
- No duplicar canal: reutiliza el lector canonico read-only del front y el patron de auto-commit-push (AC58).
