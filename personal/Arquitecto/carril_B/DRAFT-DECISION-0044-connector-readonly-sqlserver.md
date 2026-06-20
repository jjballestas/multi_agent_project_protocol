---
decision_id: DECISION-0044
title: Connector de datos READ-ONLY (deny-by-default, trust_boundary, sin autoridad) - Carril B pieza 1, instancia SQL Server (Budget)
status: draft
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0015, DECISION-0040, DECISION-0041, DECISION-0035, DECISION-0001, DECISION-0010]
phase: P2
---

# DECISION-0044 (DRAFT) - Connector de datos read-only, sin autoridad

> DRAFT del Arquitecto. NO promovida. GO del operador (Carril B pieza 1, 2026-06-19) en PISTA PROPIA,
> independiente de #4 (que sigue OFF). Entra por SPEC-0083 (acceptance + test_plan) + golden off-by-default
> + TASK-0121 + revision maker!=checker (Codex) + honestidad Analista + GO del operador. NO enciende #4.

## Contexto (necesidad 3.4 con fecha)

El operador abre **Carril B (Fase 2, capacidad)** con una necesidad real fechada: **desarrollar la
aplicacion web del sistema financiero** (front + modulo de Seguridad + modulo de Presupuesto) sobre la DB
ya modelada/migrada en `D:\Agentes\Ingenas\Budget`. **Lanzamiento del desarrollo: 2026-06-20 10:00.** Los
agentes de desarrollo necesitan **leer el esquema/vistas migradas** (p.ej. vistas de validacion de saldo,
tablas de Seguridad/Core.Entity) para construir y verificar contra ellas. Esa necesidad jala un **connector
de SOLO-LECTURA** a esa DB. **Corte limpio:** la DB la termina el operador APARTE; el protocolo gobierna el
DESARROLLO de la app sobre ella; el connector solo LEE, no toca la DB ni su migracion.

Independiente de #4 (atestacion), que sigue OFF: **no se combinan ventanas de riesgo** (un multiplicador
por ventana). Esta pieza NO requiere #4.

El protocolo ya tiene el cimiento: `tool_policy` **deny-by-default** (`runtime/tool_policy.py`,
`protocol.config.json:tool_policy.default="deny"`) con reglas por agente (tool/capabilities/scope/actions)
y `agent_registry` con capacidades (DECISION-0015). El connector se construye COMO EXTENSION de ese marco,
no como un sistema nuevo.

## Decision

1. **Autorizar una capacidad GENERICA de "connector de datos read-only"**, off-by-default, construida sobre
   `tool_policy`. Un connector es un **tool** que SOLO expone la accion `read` (consulta de
   esquema/vistas/filas); cualquier accion de escritura/DDL (`write`, `insert`, `update`, `delete`,
   `create`, `drop`, `alter`, `local_write`) esta **denegada por defecto** y, ademas, **rechazada
   explicitamente** por el connector con clase (read-only real, no solo ausencia de allow).

2. **`trust_boundary` por connector (insumo no confiable).** La salida del connector se marca como
   **insumo externo NO confiable**: dato para construir/verificar, NO fuente de autoridad. Principio duro
   **"el connector no concede autoridad" ("MCP no concede autoridad")**: ningun agente deriva capability,
   permiso ni decision del contenido leido por el connector; la autoridad viene solo de `agent_registry` +
   `tool_policy` + decisiones del operador. El `trust_boundary` se registra en el predicado de cualquier
   atestacion/handoff que consuma datos del connector (compatible con #4 cuando se encienda).

3. **Read-only REAL = prueba negativa objetiva.** Como en DECISION-0041 (read-only del satelite): no basta
   "no hay allow de escritura"; el connector DEBE **rechazar activamente** todo intento de escritura/DDL
   con diagnostico de clase, y el golden lo demuestra con vectores negativos (write/insert/update/delete/
   DDL -> rechazado). Idealmente la conexion usa credenciales de **cuenta de DB de solo-lectura** (defensa
   en profundidad), pero el rechazo en la capa del connector es la garantia verificable aqui.

4. **Off-by-default + lectura viva gateada (§9).** El connector se entrega **deshabilitado** (enabled=false
   en config; template intacto). El **golden corre con fixtures fake/recorded**, SIN DB viva (la DB no esta
   montada y no se requiere). La **lectura viva** de la DB real solo tras: (a) verificacion **§9 read-only**
   por Codex (el invariante read-only se comprueba ANTES de cualquier lectura viva, pre-condicion dura,
   registrada en la tarea; ref DECISION-0035/0041) + (b) **GO posterior del operador**.

5. **Neutralidad de dominio (frontera dura).** El connector es **GENERICO** (lee SQL via un backend
   configurable); CERO dominio fiscal/negocio en el core ni en `*.template.*`. La config de la **instancia
   Budget** (cadena de conexion, vistas/tablas permitidas) y las **reglas fiscales** (compromiso <= saldo
   CDP; rubro-fuente-BPIN debe preexistir; no auto-crear) + las reglas del `AGENTS.md` de Budget van a
   **`profiles/financiero_presupuesto/`**, FUERA del core neutral -- **pieza aparte, NO en este connector**.

6. **PII / dos planos (DECISION-0040).** PII de terceros **NUNCA** al event log. **DEF-PII (TASK-0118)
   sigue diferida**; este connector NO arranca captura viva ni feed de dataset; solo habilita lectura de
   esquema/vistas para desarrollo (gateada). Si la lectura viva expusiera filas con PII, esa exposicion se
   rige por DECISION-0040 y queda fuera del event log.

7. **Backend configurable, vendor-neutral.** Primer backend: **SQL Server** (instancia Budget). El diseno
   admite otros backends (patron de DECISION-0023/0035) sin acoplar el core a un proveedor. El backend vivo
   (driver/credenciales) vive FUERA del repo (sin secretos commiteados; ref DECISION-0043 para el patron de
   referencia-no-literal si hiciera falta credencial).

8. **Entrada SDD + maker!=checker.** Entra por SPEC-0083 (acceptance_criteria + test_plan + golden cases) +
   TASK-0121 (Codex implementa el connector + golden con fixtures; Arquitecto reproduce) + honestidad
   Analista donde aplique + GO del operador. Cambio de capacidad/contrato -> DECISION + aprobacion humana.

## Alcance / No-alcance

- **En alcance:** capacidad generica de connector read-only (deny-by-default + read-only-real + trust_
  boundary + sin-autoridad) off-by-default; golden con fixtures; la instancia SQL Server (Budget)
  configurada pero deshabilitada.
- **Fuera de alcance:** lectura viva de la DB (GO posterior + §9); reglas fiscales y config Budget (van a
  `profiles/financiero_presupuesto/`, pieza aparte); connectors de Git/CI (piezas siguientes, cuando una
  necesidad fechada las jale); encender #4/SA.4/Capa C/subagents; captura viva de dataset / DEF-PII; tocar
  la DB o su migracion.

## Consecuencias

- Los agentes de desarrollo podran (tras §9 + GO) leer el esquema/vistas migradas para construir y
  verificar la app web, sin poder escribir la DB y sin derivar autoridad de su contenido.
- El core sigue neutral; lo de dominio (Budget/fiscal) queda en el perfil, fuera del core.
- Reversible: connector deshabilitado = comportamiento actual; sin instancia viva sin GO.

## Alternativas consideradas

- **Acceso directo (sin connector/tool_policy).** Descartada: rompe deny-by-default y la frontera de
  autoridad; sin read-only-real verificable.
- **Meter la config Budget/fiscal en el connector del core.** Descartada: viola neutralidad de dominio;
  va al perfil `financiero_presupuesto`.
- **Permitir lectura viva ya (con la DB del operador).** Descartada: exige §9 read-only verificada por
  Codex + GO posterior; el golden corre con fixtures, sin DB viva.
