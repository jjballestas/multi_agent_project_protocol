# ORDEN AL ARQUITECTO - F0.2: DECISION-hub Vision Nova (paste-ready)

Copiar desde la linea "ORDEN" hasta el final del documento en la sesion del Arquitecto.

---

ORDEN DEL OPERADOR AL ARQUITECTO - F0.2 (DECISION-hub Vision Nova)

CONTEXTO: GO F0 emitido. La directiva F0.1 esta commiteada en
personal/operador/vision-nova/F0/DIRECTIVA-OPERADOR-F0.1-20260702.md (leela PRIMERO).
Veredicto base: Area_comun/artifacts/ANALISTA-pivote-v2-veredicto.md (8 bloqueantes).
Ultima decision registrada: DECISION-0082 -> la nueva es DECISION-0083 (verifica el
siguiente id libre antes de escribir).

PASO 0 - PRECONDICION (verificar, no asumir):
1. La orden STOP-START previa (higiene de areas + stand-down de crons + rama
   vision-nova) NO estaba ejecutada al 2026-07-02 ~19:50: no existe la rama
   vision-nova, el working tree sigue sucio (untracked masivo en personal/Arquitecto)
   y la higiene de Codex sigue pendiente (MSG-20260702-Operador-to-Codex-ACTION-
   higiene-area-personal.md sigue en open/ sin FYI de respuesta; el Analista SI
   respondio). Si sigue asi, ejecuta PRIMERO esa orden completa: higiene, tree
   limpio, gates verdes por exit-code, stand-down graceful de crons, pull, crear
   rama vision-nova con push -u, y verificar que harness/monitor operan en la rama.
2. TODAS las operaciones de ledger de esta orden van SOBRE LA RAMA vision-nova.
3. Preflight completo de la skill arquitecto-ledger-ops: cold-start, claim anidado
   #self file-scoped, ASCII puro, gates por exit-code, commitear ANTES de pedir
   cualquier review.

PASO 1 - Registrar DECISION-0083 via submit_intent (intent decision). Contenido:

- titulo: "Vision Nova - supersede parcial de DECISION-0077 (fork Zeus-Aegis
  descartado), ajuste de DECISION-0078 (brazo C condicional), re-alcance del backlog
  0230-0234 hacia employee-ready/Nova y arquitectura de repos hub/instancias"
- status: accepted (GO escrito del operador: directiva F0.1)
- supersedes: [DECISION-0077 PARCIAL - solo la meta de producto fork/productizacion;
  SOBREVIVEN: numeracion TASK-02xx, prefijos en titulo, gobernanza en el hub,
  restricciones de neutralidad y sandbox]
- relates_to: [DECISION-0050, DECISION-0078, DECISION-0081, DECISION-0082,
  GOAL-VISION-NOVA-001, DIRECTIVA-OPERADOR-F0.1-20260702,
  ANALISTA-pivote-v2-veredicto]
- scope: product
- deciders: [operador humano, Arquitecto]

Cuerpo (adaptar redaccion, conservar TODOS los puntos):

1. FIN DEL FORK: la productizacion de Zeus-Aegis como producto instalable deja de ser
   meta activa. Zeus-Aegis se conserva como PANEL F1 read-only del hub (DECISION-0050
   punto 4). No se tira trabajo: 0222/0223/0226/0229 done quedan como estan.
2. NUEVA META ACTIVA: GOAL-VISION-NOVA-001 = metodologia employee-ready + instancia
   nova-budget distribuida + estudio pre-registrado. Prefijo de titulos de tareas
   nuevas/re-alcanzadas: [VISION-NOVA][Fx.y] + relates_to GOAL-VISION-NOVA-001
   (misma convencion de DECISION-0077: el agrupamiento va en titulo+relates_to,
   nunca en el id).
3. AJUSTE DECISION-0078 (sigue proposed): el brazo C (peon -> gate -> critico ->
   firmante) pasa de brazo simultaneo a FASE CONDICIONAL (Fase 3, condicional a la
   aritmetica pre-registrada del backlog, item F3.2 del tablero). La muestra pasa de
   "tareas sandbox" a tareas reales de Nova Budget bajo gobierno completo, manteniendo
   el sandbox piloto-peones como entorno de ensayo. 0078 no se ratifica hasta el
   sellado del pre-registro (F3.4).
4. RE-ALCANCES (task_upsert, mismo id, titulo nuevo + sufijo
   "[re-alcance: pivote Vision Nova, DECISION-0083]"):
   - TASK-0230 -> [VISION-NOVA][F2.1] new_instance de nova-budget desde tag v1.18.0
     + perfil de instancia (arm/mode + taxonomia de riesgo). El bootstrapper Electron
     MUERE del alcance.
   - TASK-0232 -> [VISION-NOVA][F2.3] harness distribuido pull->escribir->push
     inmediato (claims visibles entre clones) + hosting privado de la instancia.
     El instalador firmado de Windows MUERE del alcance.
   - TASK-0233 -> [VISION-NOVA][F2.2] verificacion e2e distribuida: un clon limpio
     opera 1 tarea completa solo via Git (owner Analista; se registra/promueve
     despues de F2.1).
   - TASK-0234 -> [VISION-NOVA][F2.5] runbook de onboarding remoto de empleados
     (objetivo <=1 dia, medido; alimenta HP6).
   - TASK-0231 se CONSERVA proposed, re-alcanzada a [VISION-NOVA][F6.1] fase peones
     bajo DECISION-0078 ajustada (sandbox D:/Agentes/Zeus/piloto-peones intacto).
5. ARQUITECTURA DE REPOS:
   - Hub (multi_agent_project_protocol) = casa VIVA del TOOL (runtime, validador,
     templates, doctrina) + ARCHIVO INMUTABLE (ledger atestado #4, decisiones,
     corpus sellado). La doctrina SIEMPRE se desarrolla en el hub antes de instanciar.
   - Instancias (nova-budget primero) = repos consumidores creados desde RELEASE TAG
     del hub via new_instance; se actualizan solo via upgrade_instance; JAMAS empujan
     al hub. Repos de instancia/producto bajo D:/Agentes/Zeus/ (DECISION-0050).
   - Modo distribuido = Git puro: empleados con clones del repo de instancia en
     hosting privado, pull->write->push; sin acceso al hub.
   - Spec-repo publico (Apache-2.0, sin residuos de instancia) = FUTURO, Carril B,
     gateado por CB.1 y el presupuesto CB (<=1 dia/semana medido con stop).
6. LOS 8 BLOQUEANTES de la ronda 2 quedan incorporados como obligaciones mapeadas al
   tablero: (1)->F3.1, (2)->F1.2, (3)->F1.3, (4)->F1.4, (5)->gate CB, (6)->esta
   DECISION, (7)->CB.2, (8)->F3.4. Los bloqueantes 1, 2, 3, 4 y 8 son PRECONDICION
   del Sprint 1 (30-jul); el 5 y el 7 gatean solo el Carril B.
7. INVARIANTES: dataset TFM N=500 sellado intocable; 5 pineados; epoch v1.14.0
   PINNED; core neutral; sin secretos; Engram cerrado (DECISION-0081) y PROHIBIDO
   gentle-ai install en maquinas Nova.

PASO 2 - Re-alcances del punto 4 como task_upsert en la MISMA transaccion atomica
--intents que la decision (o transaccion inmediatamente posterior si el runtime lo
exige). Validar contra el estado intermedio.

PASO 3 - Commit con pathspec explicito (decision .md + state/*.json + tasks/*.md
re-alcanzadas) + los 3 gates por exit-code (validate + scan_encoding + neutralidad).
Nada de directorios anchos.

PASO 4 - Actualizar el tablero pipeline-vision-nova.html via skill
arquitecto-pipeline-vision-nova: F0.1 = hecho (ev: commit de la directiva) y
F0.2 = hecho (ev: commit de DECISION-0083), sello de hora real, updated_by Arquitecto.

PASO 5 - FYI al operador via mailbox (ASCII, sin requires_response) con: hash del
commit de la DECISION, estado de los re-alcances, estado de la rama vision-nova y
resultado de los gates. Push de la rama.

LIMITES: NO promover tareas F1 todavia (la orden F1 llega aparte con el backlog
descompuesto). NO tocar el dataset sellado ni los pineados. NO relanzar crons de
peers hasta que el operador lo pida.
