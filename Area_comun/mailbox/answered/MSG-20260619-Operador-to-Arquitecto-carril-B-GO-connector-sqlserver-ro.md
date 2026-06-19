---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-B-GO-connector-sqlserver-ro
type: DECISION
task_id: none
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
one_line_summary: GO a Carril B pieza 1 - connector SQL Server READ-ONLY de la DB migrada (D:\Agentes\Ingenas\Budget). Necesidad 3.4 CONFIRMADA = desarrollo de la app web (front + Seguridad + Presupuesto), lanzamiento 2026-06-20 10:00 (o antes). Pista propia, independiente de #4 (OFF). Flujo DECISION->SPEC->golden off-by-default, deny-by-default, trust_boundary, "MCP no concede autoridad". Read-only real; lectura viva = s9 verificada por Codex + GO posterior. Cero dominio en core.
requested_action: "Abrir Carril B en pista propia (no combinar con la ventana de #4). Construir DECISION + SPEC (acceptance_criteria + test_plan) + golden determinista off-by-default para un connector SQL Server READ-ONLY de la DB en D:\\Agentes\\Ingenas\\Budget. Deny-by-default + trust_boundary por conector + 'MCP no concede autoridad'. Golden con fixtures fake/recorded (sin DB viva). maker!=checker (Codex reproduce); honestidad Analista donde aplique. NO encender #4. NO uso vivo del connector sin s9 + GO posterior."
question: "Confirmas el scope (connector SQL Server read-only, off-by-default, golden con fixtures, sin lectura viva hasta s9+GO) y arrancas el flujo DECISION->SPEC->golden?"
context_refs:
  - AGENTS.md
  - Area_comun/decisions/DECISION-0040-gate-dataset.md
  - Area_comun/decisions/DECISION-0041-precondicion-acoplamiento-readonly.md
  - Area_comun/tasks/TASK-0118-codex-def-pii.md
deadline_or_blocking_level: high
---

# GO Carril B - pieza 1: connector SQL Server READ-ONLY

Abre **Carril B** (Fase 2 capacidad) en **pista propia, independiente de #4** (sigue OFF; no combines
ventanas de riesgo). Primera y unica pieza por ahora: connector de **solo-lectura** a la DB ya migrada en
`D:\Agentes\Ingenas\Budget`, para habilitar verificacion de regla de negocio vs legacy / convenciones DDL
/ verificacion de migracion.

## Flujo (SDD, gateado)
DECISION -> SPEC (`acceptance_criteria` + `test_plan`) -> golden determinista -> **off-by-default**.
maker!=checker (Codex reproduce) + honestidad Analista donde aplique.

## Principios duros (no negociables)
- **Deny-by-default** y **`trust_boundary` por conector**; principio explicito **"MCP no concede
  autoridad"** (el connector lee; no autoriza ni decide).
- **Read-only real:** prueba negativa objetiva (todo intento de escritura RECHAZADO). La **lectura viva**
  de la DB solo tras verificacion s9 read-only por Codex **+ GO del operador**; el golden corre con
  **fixtures fake/recorded**, sin DB viva (la DB no esta montada y no se requiere para el golden).
- **Neutralidad de dominio:** CERO dominio fiscal/negocio en el core ni en `*.template.*`. Las reglas
  fiscales (compromiso <= saldo CDP; rubro-fuente-BPIN debe preexistir; no auto-crear) y las del
  `AGENTS.md` de Budget van a `profiles/financiero_presupuesto/`, **fuera** del core neutral -- pieza
  aparte, NO en este connector.
- **Regla 3.4 (necesidad con fecha) - CONFIRMADA por el operador:** necesidad = **desarrollar la
  aplicacion web del sistema financiero** (diseno de front + modulo de Seguridad + modulo de Presupuesto)
  sobre la DB ya modelada en `D:\Agentes\Ingenas\Budget`; el connector read-only lo jala que los agentes
  de desarrollo necesitan **leer el esquema/vistas migradas** (p.ej. `Budget.vw_Commitment_Availability_
  Validation`, vistas de saldo, tablas de Seguridad/Core.Entity) para construir y verificar contra ellas.
  **Fecha: lanzamiento del desarrollo 2026-06-20 10:00** (o antes si los tests del diseno de la DB pasan
  antes). NOTA: la DB la termina el operador APARTE; el protocolo gobierna el DESARROLLO de la app sobre
  ella (corte limpio).
- **PII de terceros NUNCA al event log** (dos planos, DECISION-0040). **DEF-PII (TASK-0118) sigue
  diferida**; no se arranca captura viva aqui.
- **No tocar** la DB ni su migracion (el connector solo lee). #4 OFF; nada de provisioning/flip aqui.

## Entregable
DECISION + SPEC + golden off-by-default, en canonico, validador verde + drift 0. El **uso vivo** del
connector es un **GO posterior** mio tras s9 verificada por Codex. Git + CI quedan como piezas siguientes,
solo cuando una necesidad fechada las jale. Reporta al cerrar. Canal ASCII.
