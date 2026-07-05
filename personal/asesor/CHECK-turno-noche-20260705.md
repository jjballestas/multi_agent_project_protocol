# CHECK - Turno de noche del Arquitecto (2026-07-05) -- para revisar al levantarte

> **ACTUALIZADO 2026-07-05 (turno EN CURSO).** Casillas marcadas = verificado contra git/journal.
> Resumen: items 0, 1 y 2 HECHOS; item 3 (P4.1, ruta critica) EN CURSO con su OPEN ya capturado;
> item 4 (PAR-1) pendiente. Sin banderas rojas.

## Estado en una linea
`0252 cerrada + PAR-2 confirmado + higiene` DONE  ->  `P4.1 (TASK-0253) in_review, OPEN capturado`  ->  falta CLOSE de P4.1 + PAR-1.

## Como verificar rapido (al levantarte)
```
cd /d/Agentes/multi_agent_project_protocol && git fetch origin && git log --oneline -25 origin/main
python -c "import json;d=json.load(open('Area_comun/state/TASK_INDEX.json'));[print(t['id'],t['status'],t.get('owner')) for t in d['tasks'] if t['id']>='TASK-0246']"
cut -d, -f1-6 personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_journal.csv
```

## La cola (en orden) + que cuenta como HECHO

- [x] **0. Cutover + higiene + responde directivas**
  - HECHO: mailbox higienizado en 3 lotes (12 consumidos archivados; commits 5b59054 / 4738709 / a01467a).

- [x] **1. TASK-0252 (harness paridad) CERRADA**
  - HECHO: remediacion (b7fff3e) -> Analista OK/CERRABLE -> review_approved (e9918a9) -> **done**.

- [x] **2. Gobierno registrado**
  - [x] **PAR-2 condicional -> CONFIRMADO** + **enmienda fechada** del grant (+2 EXECUTE Annul) -- registrado en e9918a9.
  - [x] Filas de medicion **P2.1/P2.2 (seq 4-7)** presentes en `medicion_journal.csv`.

- [!] **3. P4.1 -- RUTA CRITICA (BLOQUEADA, necesita al operador)**  `TASK-0253 / SPEC-NOVA-P4-001`
  - [x] GO-eada a Codex (4c78b62) + **fila OPEN capturada** (journal seq 8).
  - [x] Adversarial informal dio NO-GO (4 hallazgos: F-NOVA-01, saldo-por-vista, ProblemDetails generico, UI sin formulario).
  - [x] Codex remedio 3 de 4 (saldo via vw_Initial_Budget_Line_Balance, ProblemDetails especifico, UI editable) -- Nova-Budget commit 00a3f47; dotnet test 35 PASS, npm PASS.
  - [~] **DESBLOQUEO COMPLETO** (ambos inputs de F-NOVA-01 resueltos):
    - [x] **`NOVA_BUDGET_SANDBOX_RESET_SQL`** -> `Budget.Reset_Sandbox_Mutator_Baseline` (revision Asesor PASA, cuadre validado). Grant 108.
    - [x] **`NOVA_BUDGET_PARITY_CONNECTION_STRING`** -> configurada en el ENTORNO DE USUARIO DE WINDOWS (secreto SOLO ahi, no en archivos; DBA valido conexion + reset dry_run OK sin mutar). Ruteado (575ee75).
    - [ ] **FALTA (Arquitecto):** relanzar el cron de Codex (los procesos abiertos no recargan env vars) -> desbloquear TASK-0253 (blocked->in_progress) -> F-NOVA-01 corre -> CLOSE + tokens + patron congelado.
  - Nota de seguridad: el Arquitecto se auto-freno bien al intentar escribir la password a disco; el secreto quedo solo en la env var de usuario (canal acordado). Disciplina correcta.

- [ ] **4. Miembro baseline PAR-1 arrancado** (P4.2 o P4.3 segun el sello, <=17-jul)
  - Pendiente: arranca cuando P4.1 cierre y congele el patron.

- [ ] **5. (Si sobro tiempo) Extra**
  - Superficie baseline PAR-2 (sobre los `Annul_*`) O avance de `TASK-0246`. Aun no.

## Lo que NO debe haber pasado (banderas rojas) -- TODAS LIMPIAS al corte
- [x] NINGUNA unidad del **pool Q4** construida (P4.4, P2.3, P2-004, P3.2/3.3/3.4, P6.3). LIMPIO.
- [x] **P3.1 NO construida** (diferida a Sprint 1). LIMPIO.
- [x] Ninguna unidad baseline cerrada **sin su fila de medicion**. LIMPIO (0252 no es fila de estudio; P4.1 tiene OPEN).
- [x] Sin edits manuales del ledger que causen drift. LIMPIO.

## Blocked esperados (si aparecen)
Ninguno al corte. Si el Arquitecto deja algo `blocked`, su respuesta trae la pregunta concreta.

## Resumen que te dejara el Arquitecto
En un mensaje `*-to-Operador-*` en el mailbox (aun no emitido; el turno sigue).

---
**Lectura dormido->despierto:** al corte, la ruta critica va BIEN -- 0252+gobierno+higiene cerrados y P4.1
GO-eada con su OPEN capturado. Falta que P4.1 pase a **done con su CLOSE** y que **arranque PAR-1**; ahi
el piso minimo del 30-jul queda construido.
