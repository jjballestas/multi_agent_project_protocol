---
message_id: MSG-20260705-Operador-to-Arquitecto-ENCARGO-PAR-2-baseline-surface
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.4/s.13 (PAR-2 confirmado) + s.21 (criterio del sorteo PAR-1)
  - "D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/DATA/annulment-sandbox-evidence.txt (THROW reales de los Annul)"
one_line_summary: "ENCARGO: PAR-2 baseline surface (superficie C#/API sobre un Annul_*). En orden: (1) RESUELVE el sorteo baseline/gobernado de PAR-2 -- el sello NO especifica cual Annul es baseline (mismo hueco que PAR-1) -> aplica el MISMO criterio ya establecido en s.21 (string pre-existente result-independiente + algoritmo sellado + enmienda fechada transparente), SIN re-preguntar al operador (el criterio es precedente); los proc names Annul_Availability_Certificate/Annul_Commitment pre-existen (creados por el DBA) y son el string natural. (2) ESCRIBE la SPEC citando los THROW REALES de los procs (re-verificados contra OBJECT_DEFINITION, no asumidos -- precedente F-0246-02): guard CDP=50283 / RP=50293, idempotencia CDP=50281 / RP=50291, tenant=50100. (3) COORDINA el pre-flight de BD AMPLIADO (el operador se lo pasa al DBA): VIEW DEFINITION sobre los 2 Annul + sus tablas de reverso + triggers via tabla padre, y SELECT sobre las vistas Y LAS TABLAS BASE que leen (leccion P4.2/Budget_Adjustment). (4) GO Codex -> ciclo completo con guard de procedencia (sin mock) + aislamiento PAR-2 + captura CLOSE con tag=ARRANQUE (convencion pre-30-jul). Frontera: la superficie es la unidad medida; los procs son hardening (hecho)."
requested_action: "[ENCARGO] Arranca PAR-2 baseline surface (la superficie C#/API sobre un Annul_*, unidad medida de PAR-2; los procs ya existen, hardening hecho). EN ORDEN: (1) RESUELVE EL SORTEO baseline/gobernado de PAR-2. El sello (s.4/s.3.2) NO especifica cual de {Annul_Availability_Certificate, Annul_Commitment} es baseline vs gobernado -- es el MISMO hueco que PAR-1. APLICA EL MISMO CRITERIO YA ESTABLECIDO (s.21, resolucion de PAR-1): string pre-existente RESULT-INDEPENDIENTE + algoritmo sellado (SHA-256(string + semilla 1844242), paridad h[0]) + enmienda fechada transparente con los strings candidatos declarados. NO RE-PREGUNTES AL OPERADOR: el criterio ya es precedente (el operador lo fijo en PAR-1). Los proc names 'Annul_Availability_Certificate' / 'Annul_Commitment' PRE-EXISTEN (el DBA los creo antes de esta decision) y son el string natural pre-existente; corre el algoritmo sobre ellos y registra el resultado como enmienda fechada (sello s.22). Si por consistencia resulta Annul_Availability_Certificate=baseline (espeja PAR-1 donde Availability=baseline, orden de cadena CDP antes que RP), documentalo; si el algoritmo da otro resultado, respeta el resultado -- lo que importa es que el string no se elija por su resultado. (2) ESCRIBE LA SPEC-NOVA del miembro baseline citando los THROW REALES del proc (RE-VERIFICADOS contra OBJECT_DEFINITION, NO un rango asumido -- precedente F-0246-02): del reporte del DBA (annulment-sandbox-evidence.txt): guard bloqueante CDP=THROW 50283 / RP=THROW 50293, idempotencia CDP=50281 / RP=50291, tenant=50100. Codex los re-verifica contra el proc desplegado (ya tendra VIEW DEFINITION -- ver punto 3). Patron: hereda el congelado de P4.1/ajustes; el Annul es reverso (3 efectos: presupuestal libera saldo al padre, documental estado 'A', contable no-op en CDP/RP como se documento). (3) PRE-FLIGHT DE BD AMPLIADO -- el Asesor le pasa al operador el requerimiento para el DBA (aplicando el ESTANDAR-entregable-DBA con la leccion P4.2): para budget_sandbox_verifier sobre el Annul baseline: EXECUTE (ya concedido), VIEW DEFINITION sobre el proc + sus tablas de reverso (Availability_Certificate_Reversal/_Line o Commitment_Reversal/_Line) + triggers via tabla padre, y SELECT sobre las VISTAS Y LAS TABLAS BASE que el proc lee (no solo vistas -- leccion P4.2/Budget_Adjustment/SQL 229). Coordina con el operador que el DBA lo aplique ANTES de la F-NOVA-01 para no repetir round-trips. (4) GO A CODEX -> CICLO COMPLETO: build de la superficie (API+Application+UI sobre el proc, delega la mutacion al proc, NO reimplementa saldos en C#) -> adversarial informal en SESION SEPARADA con el GUARD DE PROCEDENCIA (evidencia del sandbox real DB_NAME+login+OBJECT_DEFINITION+delta real, NO mock in-memory) + aislamiento PAR-2 (NO leer la implementacion del miembro gobernado) -> F-NOVA-01 (criterios GWT + THROW re-verificados + reset por task_id entre corridas) -> CLOSE con captura de tokens (err.log antes de rotar, --corpus explicito) y tag_incidente_maquinaria=ARRANQUE (convencion: toda unidad pre-30-jul = arranque). FRONTERA: la superficie C# es la unidad MEDIDA (PAR-2 baseline); los procs Annul son hardening (fuera del estudio, ya hechos). RESPONDE con: (a) sorteo PAR-2 resuelto (cual Annul = baseline) + enmienda registrada; (b) SPEC escrita citando THROW reales; (c) pre-flight de BD coordinado con el operador/DBA; (d) GO a Codex."
question: ""
---

# ENCARGO - PAR-2 baseline surface

Arranca la superficie medida de PAR-2 (C#/API sobre un `Annul_*`; los procs ya existen -- hardening hecho).

## En orden
1. **Sorteo baseline/gobernado de PAR-2** -- el sello NO especifica cual Annul es baseline (mismo hueco que
   PAR-1). Aplica el **MISMO criterio de s.21** (string pre-existente result-independiente + algoritmo
   sellado + enmienda fechada transparente). **NO re-preguntes al operador** -- el criterio es precedente.
   Los proc names `Annul_Availability_Certificate`/`Annul_Commitment` pre-existen -> son el string natural.
   Registra como enmienda fechada (s.22).
2. **SPEC** citando los **THROW REALES** (re-verificados contra OBJECT_DEFINITION, no asumidos): guard
   CDP=50283 / RP=50293, idempotencia CDP=50281 / RP=50291, tenant=50100. Hereda el patron de P4.1.
3. **Pre-flight de BD AMPLIADO** (el Asesor te lo coordina via operador->DBA): VIEW DEFINITION sobre el
   Annul + tablas de reverso + triggers via tabla padre, y **SELECT sobre vistas Y TABLAS BASE** que lee
   (leccion P4.2/Budget_Adjustment). Aplicar ANTES de F-NOVA-01.
4. **GO Codex -> ciclo completo:** build (delega al proc, no reimplementa saldos) -> adversarial con guard
   de procedencia (sin mock) + aislamiento PAR-2 -> F-NOVA-01 -> CLOSE + tokens + **tag=arranque**.

## Responde
(a) sorteo PAR-2 resuelto + enmienda; (b) SPEC con THROW reales; (c) pre-flight coordinado; (d) GO a Codex.
