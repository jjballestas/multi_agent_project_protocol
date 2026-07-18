---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-prep-via2-N6-tareas-gobernadas-f33-runbook
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-18
context_refs:
  - Area_comun/artifacts/DRAFT-SELLO-ETAPA2-estructura-arquitecto.md
  - Area_comun/decisions/DECISION-0094-sello-preregistro-contabilidad-N6.md
  - personal/asesor/COMANDOS-julian-gate-nominal-7b.md
one_line_summary: "PREP completa de la Via 2 / N=6 (NO abrir build): 3 deliverables. (1) Promover a tareas GOBERNADAS las 6 unidades reservadas del N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) en el TASK_INDEX de NOVA con task_id + scope, estado READY/reservada, SIN flip a in_progress (jheredia no puede task_upsert). (2) F3.3 VERDE para Contabilidad: confirmar cierre de la instrumentacion + eventos de medicion por unidad cableados sobre las corridas de Julian (PREP-INSTRUMENTACION-MEDICION-contabilidad). (3) Runbook de Julian por-unidad: adaptar COMANDOS-julian al N=6 con el event_auth NOVA (jheredia-hmac:v1) + la leccion de stagear tambien tasks/<task>.md + push inmediato + prueba negativa. Freeze anti-HARKing intacto: NO construir hasta el GO del Operador + confirmacion jheredia. Declara la dependencia con el sello E2/reconciliacion 26-29. Autoridad delegada al Asesor para dudas."
---

# DIRECTIVA - PREP completa Via 2 / N=6 (wiring, NO build)

## Objetivo
Dejar la Via 2 (build MEDIDO de las 6 unidades de Contabilidad, Julian maker, pre-registro
DECISION-0094) LISTA PARA ARRANCAR, de modo que el unico gatillo restante sean las dos decisiones
SOBERANAS del Operador: (a) confirmar jheredia:v1 operativo, (b) GO a abrir el build. Esto es
WIRING/preparacion, NO ejecucion: NINGUNA unidad se construye en esta directiva.

## Deliverable 1 - Promover las 6 unidades a tareas GOBERNADAS (ready/reservada)
Registra en el TASK_INDEX de NOVA (tu task_upsert; jheredia no puede) las 6 unidades del N=6:
R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c (las de Notion con Reservada-para-medicion + Ejecutor
Julian). Por unidad: task_id estable + scope de claim (state + tasks/<task>.md + CLAIMS) +
puntero a su spec SDD peon-ready (ya enlazada en Notion: spec + reglas de negocio + requerimientos
+ objetos BD). Estado = READY, flag reservada-para-medicion. NO las flipees a in_progress: siguen
sin construir hasta el freeze + GO. Deja el .md de cada tarea creado y consistente con el index
(index=file), para que el clon de Julian no vea mismatch.

## Deliverable 2 - F3.3 VERDE para Contabilidad
Confirma que la instrumentacion de medicion F3.3 (SPEC-NOVA-F3.3; TASK-0249 paso por re-juicios
del Analista) esta CERRADA verde y NO dependiente de archivos locales no atestados. Cablea/verifica
los eventos por unidad medida de Julian (cost.attributed y familia, per PREP-INSTRUMENTACION-
MEDICION-contabilidad) de modo que el build del N=6 quede MEDIDO desde la primera unidad. Si queda
algun residuo de los re-juicios, cierralo o declara exactamente que falta. Reporta el estado real.

## Deliverable 3 - Runbook de Julian por-unidad
Produce el runbook operativo del N=6 para Julian (maker jheredia:v1), adaptando COMANDOS-julian-
gate-nominal-7b.md al build medido. DEBE incluir, corregido para NOVA (no Aegis):
- event_auth NOVA: key_id jheredia-hmac:v1, secret_file protocol-secrets/jheredia-eventauth.key;
  clon en D:/Agentes/NOVA-Suite/NOVA, gobernanza bajo Aegis/, secret_root protocol-secrets/.
- Flujo por unidad: claim acquire (scope con el task_id de la unidad) -> build -> in_review ->
  (Analista ratify en su maquina/llave) -> done; release claim; validate exit 0.
- LECCION DURA: stagear SIEMPRE state/ + tasks/<task>.md + runtime/state/events.jsonl + snapshot;
  push INMEDIATO tras cada flip (un flip sin pushear es invisible al clon par).
- Prueba negativa por gate (firmar como Analista DEBE fallar por llave ausente).
- Guardrails: privada de Julian jamas sale de su maquina; NUNCA corre el anchor; nunca task_upsert;
  maker != checker por posesion fisica de llave; hub 2E35F26E/1.14.0 intacto.

## Freeze anti-HARKing (no negociable)
Las 6 siguen RESERVADAS y SIN CONSTRUIR hasta (a) el freeze del pre-registro / sello y (b) el GO
del Operador. Promover a tarea gobernada READY es wiring, no build. Construir antes del freeze
contamina el pre-registro. Respetalo.

## Frontera y secuencia (declara la dependencia)
Esto es PREP; el arranque del build es del Operador. DECLARA explicitamente en tu RESP la
dependencia real: el build medido del N=6, bajo DECISION-0094, puede arrancar de forma
independiente al sello E2 completo, o requiere el sello E2 (bloqueado por la reconciliacion
26-29-jul)? Necesito saber que exactamente desbloquea el GO del Operador y que queda acoplado al
calendario 26-29 / 30-jul. Reporta el estado de la base de BD de Contabilidad del DBA (la vi
ENTREGADA en design-source al 11-jul; confirma que sigue siendo la base para el build).

## Gobernanza y autoridad
maker != checker intacto (Julian maker; Analista checker, maquina/llave separada). El Operador
delega en el Asesor autoridad para resolver dudas de diseno de esta prep (numeracion de task_id,
detalle de scope, forma del runbook). Pregunta por mailbox y el Asesor responde con la disciplina
de siempre. El Asesor escala al Operador SOLO por firma soberana, decision de adopcion/arranque, o
stall. Fondo intocable N=500 / 2E35F26E / 1.14.0. Reporta al cerrar los 3 deliverables.

-- Operador (via Asesor). 18-jul.
