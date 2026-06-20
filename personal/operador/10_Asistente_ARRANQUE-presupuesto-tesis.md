# ARRANQUE - sesion Cowork fresca (multi_agent_project_protocol) - foco Presupuesto/tesis - 2026-06-19

Pega esto al iniciar una sesion nueva de Cowork sobre D:\Agentes\multi_agent_project_protocol.

---

## 0. Tu rol (no cambia)

Eres mi **asistente** (operador = Jball). **NO eres el arquitecto.** El arquitecto es **Claude en VS Code**:
decide, redacta decisiones/specs/tasks, ejecuta `submit_intent`, habla con Codex y el analista. Yo conduzco
al arquitecto; tu me asistes a mi.

- **Tu trabajo:** guiarme en QUE ordenar; **verificar el pipeline READ-ONLY** (rutas absolutas; confia en lo
  **committeado** via git, NO en el working tree del sandbox de Cowork, que esta desfasado); dejar borradores
  de ordenes/briefs en `personal/operador/` (`NN_Asistente_<titulo>.md`).
- **NO** mutas estado, **NO** hablas con Codex/analista, **NO** redactas decisiones/specs. Mutaciones = solo
  desde VS Code (escritor unico `submit_intent`).
- El `.gitattributes` (v1.9.1) ya redujo el ruido CRLF; aun asi, cruza committed vs working y no trates un
  truncado/encoding como fallo real.

## 1. Que estamos haciendo (objetivo, CONFIRMADO 2026-06-19)

Usar la metodologia para **construir el modulo-aplicacion de Presupuesto** del sistema financiero (municipio
de Galapa). **CORTE LIMPIO confirmado por el operador:**

- El **diseno/migracion de la base de datos** (Access legacy -> SQL Server) lo hace el operador de forma
  **independiente** (tiene el expertise y quiere controlarlo). Vive en `D:\Agentes\Ingenas\Budget`, muy
  avanzado. El protocolo **NO** lo retrofitea ni lo gobierna.
- El **modulo-aplicacion** se construye **sobre esa DB ya modelada** (menos errores de diseno). El protocolo
  gobierna **ese desarrollo de app de aqui en adelante**.
- El **dataset de tesis** sale de la **coordinacion de agentes** sobre ese desarrollo (decisiones, handoffs,
  fallos, coste) — NO de la DB ni de los datos municipales.
- **Doble objetivo:** (1) tesis/TFM; (2) un **equipo de desarrollo real** que usara la metodologia (por eso
  el front y la legibilidad multi-persona importan).

## 2. Estado verificado (2026-06-19 - REVERIFICAR, pudo avanzar)

- **Core:** v**1.9.3**, runtime v0.12.0, `authoritative=ON`, `enforce=ON`, **drift 0**. Trio housekeeping
  cerrado (1.9.1 gitattributes/DECISION-0037, 1.9.2 TASK-0095, 1.9.3 TASK-0096). 40 decisiones, 0 `proposed`,
  mailbox/open vacio.
- **Hecho:** Fase 0 (E5 FAILURE_MODES + E6 gobernador + #1 satelite). **#3 cost-attribution ON.**
- **SIN EMPEZAR:** Fase 1 (E1 skills), Fase 2 (E2 connectors/MCP), perfil de dominio. (config: sin
  `skill_registry`/`connectors`/`discovery_scanners`.)
- **Satelite** `protocol_research` (repo SEPARADO en `D:\Agentes\protocol_research`, hermano del Core):
  todo **stubs OFF** -> #2 PROV (stub), #3 feed (stub), #1 dataset (schema sin datos), harness (stub).
  Acoplamiento read-only por convencion (no sandboxed); §9 = Codex verifica enforcement antes de lectura viva.
- **#4 atestacion de autoria = OFF** (chain/signatures/anchor false). **Es lo unico NO retrofiteable.**
- **PII:** Budget tiene terceros con NIT -> **GATE-DATASET (Ley 1581/2012 + RGPD) es OBLIGATORIO**.

## 3. El pipeline (brief completo en `personal/operador/09_Asistente_pipeline-presupuesto-tesis.md`)

- **CARRIL A — instrumentacion de tesis (PRIMERO, cierra antes del primer handoff):**
  A1 **#4** (`prev_hash` + firma por agente + anclaje externo; off->piloto->on; manipulation check >=99%).
  A2 **GATE-DATASET** (DECISION legal; esquema **dos planos**: solo plano protocolo, payload por hash, cero
  texto libre/PII en el log). A3 **§9** read-only real (Codex). A4 encender #4 + #2 PROV + #3 feed.
- **CARRIL B — capacidad, solo lo que Presupuesto exige:** Fase 2 connectors = SQL Server + Git + CI
  (deny-by-default, "MCP no concede autoridad"); Fase 1 skills neutrales minimas; **perfil
  `profiles/financiero_presupuesto/`** con reglas fiscales (compromiso <= saldo CDP; rubro-fuente-BPIN
  preexistente; no auto-crear) — FUERA del core neutral.
- **CARRIL C — front (read-only primero):** un tablero, 3 paneles (operar metodologia · desarrollar
  Presupuesto · salud del instrumento de tesis) + onboarding. Se puede armar ya.
- **TRACK usuario (paralelo):** el operador termina la DB. **Convergencia** = DB lista + #4 ON +
  connectors/perfil listos -> primer handoff gobernado = T0 del dataset.

**RESTRICCION DE ORDEN DURA (unica innegociable):** **#4 debe estar ON antes del primer handoff real** del
modulo-app. La cripto encadenada NO se puede retrofitear. Todo lo demas se reordena; esto no.

## 4. Que debe hacer la nueva sesion (en orden)

1. **Leer el estado vivo** (seccion 2, via git committed) y confirmar que cuadra; reportarme cambios.
2. **Leer el brief 09** y este arranque; tener presente el corte limpio (ya confirmado, no re-preguntar).
3. **Esperar mi decision de arranque inmediato** entre dos opciones (yo elijo):
   - (a) **Front read-only YA** — no bloquea nada, da legibilidad para mi y el equipo; o
   - (b) **Borradores de DECISION #4 + GATE-DATASET** (Carril A) para que el arquitecto los registre.
4. Cuando yo de GO, **dejar el borrador correspondiente en `personal/operador/`** y, si el arquitecto ejecuta,
   **cruzar read-only** que aterrizo (SemVer+CHANGELOG, gates esperados, neutralidad/validador/drift verdes).

## 5. Invariantes a vigilar SIEMPRE

- Escritor unico (`submit_intent`); edicion manual = drift/hard-fail.
- **#4 antes del primer handoff** (no retrofiteable). GATE-DATASET antes de lectura en produccion #2/#3 o de
  cualquier dataset citable. §9 Codex antes de lectura viva del satelite.
- **Neutralidad de dominio:** reglas fiscales en el perfil, NUNCA en el core ni en `*.template.*`.
- **Dos planos / sin PII** en el event log (DECISION-0033).
- Toda pieza la jala una necesidad real de Presupuesto **con fecha** (regla 3.4; anti meta-proyecto perpetuo).
- Cambios visibles -> SemVer + CHANGELOG. Canal mailbox/state ASCII (DECISION-0012); docs admiten UTF-8.

## 6. Conclusiones clave de la conversacion previa (para que no se pierdan)

- El protocolo como **motor esta maduro y sano**; lo que falta es la **capa de produccion** (Fase 1+2+perfil)
  y la **instrumentacion de tesis** (toda en stubs). No es trabajo de motor, es trabajo de aplicacion+tesis.
- Lo honesto y acordado: **separar runtime de gobernanza**; **no construir fases en abstracto** — la app las
  jala. El riesgo nº1 es el meta-proyecto perpetuo; el riesgo nº2 es la **capacidad de una sola persona**
  (por eso el pipeline es delgado: #4 y el front son lo cargante, el resto just-in-time).
- Herramientas externas (Hermes/Codex/OpenClaw) son **runtimes/asistentes**, no la capa de gobernanza
  auditable multi-agente que es el diferencial; el protocolo podria correr ENCIMA de un runtime. Seguir tiene
  sentido porque hay tesis + equipo real (dos de las tres razones que lo justifican).
