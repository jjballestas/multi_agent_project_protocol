---
message_id: MSG-20260707-Operador-to-Arquitecto-ACTION-terminar-desarrollo-chains-no-idle
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-07
context_refs:
  - Area_comun/decisions/DECISION-1001-iniciativa-ingenieria-disciplinada-antivibecoding-intake.md
  - Area_comun/decisions/DECISION-1002-memoria-hibrida-ruta-unica-supersede-0071.md
one_line_summary: "El operador ve al Arquitecto sin trabajo: las cadenas 1001/1002 estan semi-estancadas. Mandato terminar-el-desarrollo: promover 1002 t5/t6, CREAR y promover las tareas 3-6 de 1001 (no existen aun), GO 1105, arrancar Contabilidad WS1 (analisis, no necesita el gate 2-clones). Sin idle; una a una por capacidad de Codex."
requested_action: "Llevar las cadenas Aegis a termino, sin idle: (1) cerrar el re-gate de TASK-1207 (in_review). (2) Chain 1002: GO TASK-1205 (t5 piloto frio, ready) a Codex; luego CREAR + GO t6 (runbook de operacion de memoria, DECISION-1002 s.17.7). (3) Chain 1001: CREAR las tareas 3-6 que faltan (DECISION-1001 descomposicion: 3 port de la capa a Zeus-Aegis modo-documentos, 4 Engineering Quality Panel MVP, 5 registro de excepciones user-facing, 6 test plan de deteccion de ambiguedad) y promoverlas por orden. (4) GO TASK-1105 (infra test fixture) a Codex. (5) Arrancar Contabilidad WS1 (mapa 57 formularios -> casos de uso): el ANALISIS no necesita el gate 2-clones (ese gatea la primera tarea gobernada de BUILD, que espera a Julian). Promueve una a la vez por capacidad de Codex; re-llena al drenar; el Asesor tambien asigna."
question: "Confirmas el pickup y el orden de promocion (1207 re-gate -> 1205 -> crear/GO 1001 t3-6 -> 1105 -> Contabilidad WS1)? Si tu lectura de capacidad de Codex sugiere otro interleaving pre-30-jul, proponlo. Escala solo lo del operador (dominio/sello/riesgo)."
---

# ACTION - Terminar el desarrollo de Aegis (chains 1001/1002 + gate + Contabilidad), sin idle

El operador te ve sin trabajo. Diagnostico del Asesor: las cadenas estan semi-estancadas (1002 t5 ready
sin GO; 1001 t3-6 sin crear). Mandato: llevarlas a termino. Cola (una a una por capacidad de Codex):

## 1. Cerrar TASK-1207 (in_review)
Re-gate del guard anti-evasion del scanner. Ratifica o fix-loop.

## 2. Chain 1002 (memoria) -> t5 y t6
- GO **TASK-1205** (t5 piloto de archivo frio, ya ready) a Codex.
- Al verde: CREAR y GO **t6** = runbook de operacion de memoria (archivar/recuperar/reconstruir/diagnosticar
  drift; DECISION-1002 s.17.7, owner Arquitecto). Con t6 cierra el chain 1002 (F0->F5+runbook).

## 3. Chain 1001 (anti-vibecoding) -> CREAR las tareas 3-6 que faltan
La descomposicion de DECISION-1001 tiene 6 tareas; solo existen t1/t2 (done) + el drift 1104. Faltan CREAR:
- t3: port de la capa de interrogacion a Zeus-Aegis modo-documentos (pre-F2).
- t4: Engineering Quality Panel MVP (semaforo/indicadores read-only sobre el checklist).
- t5: registro de excepciones user-facing (UI sobre exception.recorded).
- t6: test plan de deteccion de ambiguedad (los 8 casos del REQ s.13 como suite ejecutable).
Crealas gobernadas y promuevelas por orden (owner Codex, gate adversarial).

## 4. GO TASK-1105 (infra test fixture) a Codex
El fast-path del fixture (clone del hub excede el timeout) sigue proposed -> promuevelo; desbloquea el verde
fresco de los slow tests de la instancia.

## 5. Contabilidad WS1 (arranca ya; NO necesita el gate 2-clones)
El ANALISIS de Contabilidad (mapa 57 formularios -> casos de uso, Access -> esquema SQL Accounting,
descomposicion S/M/L; insumo del corpus Etapa 2) es trabajo de diseno que NO depende del gate e2e de 2
clones -- ese gatea la primera tarea gobernada de BUILD de Contabilidad (que espera a Julian). Arranca el
analisis como bloque propio.

## Frontera
Todo pre-30-jul a full (desde el 30-jul Sprint 1 prioridad dura). El re-genesis A2 de Julian sigue esperando
su pubkey (no bloquea nada de arriba). Nada toca el estudio medido ni el genesis del hub. Sin idle: re-llena
al drenar; el Asesor tambien te asigna.

-- Operador
