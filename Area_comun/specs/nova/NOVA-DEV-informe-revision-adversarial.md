# NOVA-DEV - Informe de revision adversarial del paquete (TASK-0246)

Autor: Arquitecto - Fecha: 2026-07-03 - Task: TASK-0246 - Gate: Analista (checker-only)
Alcance revisado: NOVA_GOAL_Desarrollo_Aplicacion.md, NOVA_Architecture_ExperienciasGH.md,
NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md, NOVA_SPEC_Plantilla_Requisitos.md (NOVA-SPEC-T-001 v1.1),
NOVA_PRES_02_Presupuesto_Inicial.html. (Los PRES 01/03..12 y el maestro PRES-000 s.08 se leen incrementalmente
al generar cada SPEC; este informe es la ronda 1, foco P3.1.)

## 0. Veredicto general
El paquete tiene disciplina documental ALTA y un ciclo adversarial informal solido (SPEC 10 campos con citas
verificables + puntos de mira + protocolo del adversarial de 12 puntos + DoD exigente). Lo que le falta -- y es
exactamente lo que anade el brazo gobernado -- es la CAPA DE GOBIERNO ATESTADO: ledger firmado, ciclo de vida
formal, intake deterministico, checker estructuralmente independiente (Analista), mailbox, y la medicion como
mecanismo. Tomar: casi todo. Complementar: unificacion de formato + atestacion. No hay contradicciones LETALES
con la doctrina v1.18.0; si hay skew de fechas y colisiones de nombres que las SPEC deben blindar.

## 1. Hallazgos (tomar / complementar / contradicciones)

- **F-NOVA-01 (skew de fechas en la lista de procs verificados) - MEDIA.** El GOAL (2026-06-29, s.2) lista 14
  procs verificados y NO incluye `Approve_Initial_Budget_Draft`; NOVA-PRES-02 (2026-07-03, s.6 B-01) confirma que
  ESE proc SI existe (schema/142, THROW 50270-50278). La lista del GOAL quedo desactualizada 4 dias. RIESGO: una
  SPEC que confie en la lista del GOAL declararia una brecha inexistente (o al reves). REGLA (ya en la plantilla
  punto 2 de pre-vuelo, la refuerzo): toda SPEC verifica cada objeto BD contra la BD DESPLEGADA al momento de
  construir (OBJECT_DEFINITION / sys.objects), nunca contra la lista narrada del GOAL. El conector readonly
  `nova_sql_connector_readonly_s9` tiene SELECT/VIEW DEFINITION pero NO EXECUTE (Msg 229): las pruebas de paridad
  necesitan GRANT EXECUTE sobre los `Get_*`/procs de lectura al rol de verificacion, o SELECT directo a la `fn_*`
  documentando cual se uso.

- **F-NOVA-02 (colision de nombres P1-P6) - MEDIA.** "P1..P6" existe DOS veces: principios del maestro
  (NOVA-PRES-000 s.03) y fases del backlog del GOAL. La plantilla ya lo advierte (campo 6). ENFORCEMENT en las
  SPEC gobernadas: citar SIEMPRE `maestro-Pn` vs `GOAL-Pn`; el gate adversarial trata una cita ambigua como
  hallazgo.

- **F-NOVA-03 (dos plantillas compitiendo) - ALTA (la orden lo exige resolver).** Riesgo de tener NOVA-SPEC-T-001
  (10 campos) Y el intake-v2/DoR de DECISION-0084 como formatos separados. RESOLUCION (entregable de esta tarea):
  se UNIFICAN en un solo formato -- NOVA-SPEC-T-001 es el cuerpo, y cada uno de sus 10 campos satisface un
  requisito del intake-v2/DoR; se anade un bloque de gobierno (owner/ledger/gate/DoR) como preambulo. Mapeo en
  s.2. NO se emite intake-v2 por separado para tareas NOVA-DEV: la SPEC unificada ES el intake.

- **F-NOVA-04 (disciplina fuerte, cero gobierno atestado) - por diseno, es el tratamiento.** El paquete no tiene
  firmas/ledger/medicion (confirmado por el estudio de particion s.0-1). No es un defecto del paquete: es la
  VARIABLE que el estudio mide (gobernanza atestada, aditiva sobre disciplina ya buena). Complemento del brazo
  gobernado: la SPEC lleva DoR + el ciclo pasa por submit_intent + checker Analista + atestacion sha256.

- **F-NOVA-05 (is_current apunta a vigencia cerrada) - MEDIA, transversal.** NOVA-PRES-02 s.6 B-02/B-05: `is_current`
  apunta a 2026 (cerrada) y 2027 no tiene presupuesto inicial. Afecta a TODA SPEC que dependa de "vigencia actual"
  (lectura y aprobacion). REGLA transversal: la UI exige vigencia EXPLICITA hasta corregir el arranque 2027; ningun
  default de vigencia. Se refleja en cada SPEC del ambito Budget.

## 2. Unificacion NOVA-SPEC-T-001 v1.1 <-> intake-v2/DoR (DECISION-0084) -- formato UNICO

Un solo bloque por tarea. El cuerpo son los 10 campos de NOVA-SPEC-T-001; el preambulo de gobierno cubre el DoR.
Mapeo (por que NO hacen falta dos plantillas):

| intake-v2 / DoR (DECISION-0084) | Campo de NOVA-SPEC-T-001 v1.1 que lo satisface |
|---|---|
| type / goal | Preambulo (type) + Campo 1 Objetivo definido |
| target_user | Campo 2 Usuario objetivo definido |
| functional_scope | Campo 3 Alcance + Campo 4 Fuera de alcance |
| acceptance | Campo 7 Criterios de aceptacion (Given/When/Then + negativos por THROW) |
| verification_cmd | Campo 8 Pruebas / gates (unit + architecture + integracion vs BD real) |
| assets_inputs | Campo 5 Contenido / assets (objetos BD, endpoints, UI, docs) |
| tech_constraints | Campo 6 Restricciones tecnicas (10 reglas GOAL + maestro-Pn + STACK) |
| risks_list | Campo 9 Riesgos |
| priority | Campo 10 Prioridad (GOAL-Pn + severidad s.08 + dependencias) |
| scope_routes / out_of_scope | Campo 3/4 + Preambulo (rutas del repo producto Nova-X) |
| DoR (anti-vibecoding, interrogacion) | Preambulo de gobierno: owner/checker, ledger, aislamiento, gate adversarial |

**Preambulo de gobierno (DoR) obligatorio en cada SPEC gobernada:**
`spec_id`, `task_id` (hub), `owner_maker`, `checker` (Analista, estructuralmente independiente), `arm: gobernado`,
`isolation` (rutas del hermano baseline PROHIBIDAS; manifiesto de archivos leidos; columna leyo_codigo_hermano),
`db_verified_at` (fecha de verificacion contra la BD desplegada), `attestation` (sha256 del SPEC via intent del hub).

## 3. Alcance gobernado cubierto (aislamiento intra-par respetado)
SOLO brazo GOBERNADO (NOVA_ESTUDIO_Particion s.2.2): familia P3 completa (P3.1 primera_unidad, alcance congelado
-> P3.2/3.3/3.4 -> P3.5 fuera de Q4), pool Q4 (P4.4, P3.2-3.4, P2.3, P6.3, Get_*_List de BR-C3), BR-C4, miembros
gobernados de pares (al final, post-17-jul). **NO se leyeron** fuentes de unidades BASELINE (GOAL-P1, P2.1, P2.2,
P4.1, miembros baseline de pares). P3.1 es familia gobernada SIN hermano baseline -> sin conflicto de aislamiento.
Secuencia (recomendacion del Operador): P3.1 -> pool Q4 en orden del sorteo Etapa 2 -> pares al final.

## 4. Mejoras propuestas al NOVA_PROMPT (las aplica el Operador; los docs viven fuera del hub)
1. Sincronizar la lista de procs verificados del GOAL con la ultima verificacion de BD (F-NOVA-01) o reemplazarla
   por "verificar contra BD al construir" para evitar skew.
2. Volver explicito el enforcement `maestro-Pn` vs `GOAL-Pn` en el pre-vuelo (F-NOVA-02).
3. Anadir al DoD del GOAL el gancho de atestacion (sha256 de la SPEC/entrega) para el brazo gobernado.

## 5. Entregables de esta tarea (ronda 1)
- Este informe adversarial.
- SPEC-NOVA-P3-001 (P3.1 Initial Budget Draft) en formato unificado (ver `SPEC-NOVA-P3-001-initial-budget-draft.md`).
- Siguientes rondas: pool Q4 en orden de sorteo (P4.4, P3.2-3.4, P2.3, P6.3, Get_*_List) + pares gobernados
  al final. FYI al Operador al cerrar cada ronda.
