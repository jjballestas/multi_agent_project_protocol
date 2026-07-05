# CHECK - Turno de noche del Arquitecto (2026-07-05) -- para revisar al levantarte

> Cola que le coloque al Arquitecto (MSG-...-DIRECTIVA-turno-noche-cola-6h, ruteada). Ordenada por
> prioridad. Al levantarte, marca cada item y verifica la EVIDENCIA. Lo mas importante es (3) P4.1:
> es la ruta critica al 30-jul.

## Como verificar rapido (al levantarte)
```
cd /d/Agentes/multi_agent_project_protocol && git fetch origin && git log --oneline -25 origin/main
# estado de tareas:
python -c "import json;d=json.load(open('Area_comun/state/TASK_INDEX.json'));[print(t['id'],t['status'],t.get('owner')) for t in d['tasks'] if t['id']>='TASK-0246']"
# medicion capturada:
cat personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_journal.csv
```

## La cola (en orden) + que cuenta como HECHO

- [ ] **0. Cutover + higiene + responde directivas**
  - Evidencia: `mailbox/open/` con pocos mensajes (los consumidos archivados); respuestas mias (P4.1/PAR-2/P3.1) contestadas.

- [ ] **1. TASK-0252 (harness paridad) CERRADA**
  - Estaba en fix-loop 1/2 (Analista NOGO: guard BD bypasseable + rol no verificado + npm no reproducible).
  - HECHO = `TASK-0252` en `done`, veredicto OK del Analista, harness de paridad cableado al sandbox.

- [ ] **2. Gobierno registrado**
  - [ ] **PAR-2 condicional -> CONFIRMADO** (los procs `Annul_*` ya existen 10/10; condicion <=15-jul cumplida). Buscar nota/registro en el sello (s.4/s.11.1) o decision.
  - [ ] **Enmienda fechada** del grant surface (+2 EXECUTE de los Annul).
  - [ ] Filas de medicion **P2.1/P2.2 (seq 4-7)** commiteadas en `medicion_journal.csv`.

- [ ] **3. P4.1 -- RUTA CRITICA (lo mas importante)**  `SPEC-NOVA-P4-001 Apply_Budget_Modification`
  - HECHO ideal = `TASK` de P4.1 en `done`: build + adversarial (sesion separada) + gate verde.
  - [ ] **Medicion capturada:** fila OPEN + CLOSE en el journal con `tokens_total_atribuibles` real (del err.log), reworks, veredictos. (NO debe faltar, como paso con P2.1/P2.2.)
  - Es el **piso minimo del 30-jul**: sin P4.1 + miembro baseline PAR-1, el 30-jul dispara STOP-total.

- [ ] **4. Miembro baseline PAR-1 arrancado** (P4.2 o P4.3 segun el sello, <=17-jul)
  - HECHO = GO-eado a Codex y en progreso o done, con captura de medicion.

- [ ] **5. (Si sobro tiempo) Extra**
  - Superficie baseline PAR-2 (sobre los `Annul_*`, detras de P4.1/PAR-1) O avance de `TASK-0246`.

## Lo que NO debe haber pasado (banderas rojas -- si ves esto, algo se salio del carril)
- [ ] NINGUNA unidad del **pool Q4** construida: P4.4, P2.3, P2-004 (Get_*_List), P3.2/3.3/3.4, P6.3.  *(Romperia el estudio irreversible.)*
- [ ] **P3.1 NO construida** (debia quedar diferida a Sprint 1).
- [ ] Ninguna unidad baseline cerrada **sin su fila de medicion** (el hueco que ya cazamos con P2.1/P2.2).
- [ ] Sin edits manuales del ledger que causen drift.

## Blocked esperados (si aparecen)
Si el Arquitecto dejo algo `blocked`, su respuesta trae la pregunta concreta. Revisa esas primero: son
las unicas que necesitan tu decision. Todo lo demas debia avanzar solo.

## Resumen que te dejara el Arquitecto
En un mensaje `*-to-Operador-*` en el mailbox: TASK-0252 cerrada? / PAR-2 flip+enmienda? / P4.1 estado +
tokens / PAR-1 arrancado? / blocked pendientes.

---
**En una linea para revisar dormido->despierto:** si al levantarte ves **P4.1 en done con su fila de
medicion** y **PAR-1 arrancado**, el turno cumplio la ruta critica. Lo demas es bonus.
