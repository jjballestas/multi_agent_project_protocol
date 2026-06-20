# 09 — Pipeline: Presupuesto bajo la metodología, instrumentado para tesis

> Brief del asistente (operador = Jball) para que el **Arquitecto** lo registre por DECISION/SPEC vía
> `submit_intent`. Read-only por mi parte; no muto estado. Decisión de GO = del operador.
> Fecha: 2026-06-19. Base verificada: Core v1.9.3 · satélite `protocol_research` (stubs) · `D:\Agentes\Ingenas\Budget`.

---

## 0. Estado real verificado (punto de partida)

- **Core (motor):** v1.9.3, runtime v0.12.0, `authoritative=ON`, drift 0, trío housekeeping cerrado.
  Fase 0 hecha; **#3 cost-attribution ON**. **Fase 1 (skills), Fase 2 (connectors), perfil de dominio: SIN EMPEZAR.**
- **Satélite:** estructura + stubs OFF. **#2 PROV = stub (no construido)**, #3 feed = stub, #1 dataset = schema sin datos,
  harness = stub. **#4 atestación de autoría = OFF** (chain/signatures/anchor false).
- **#4 es lo único NO retrofiteable:** el encadenado `prev_hash` + firma por agente debe estar ON **en el momento
  de captura**. Si se enciende después, el historial previo no es atestable. Por eso #4 va PRIMERO.
- **Presupuesto (`Budget`):** migración Access→SQL Server **muy avanzada** (DDL + loads reales: rubros, fuentes,
  proyectos, presupuesto inicial, CDPs, compromisos, ajustes; terceros `maco009t` = 10.676 entidades con NIT).
  Reglas fiscales documentadas. Hoy se desarrolla **fuera del protocolo**, con `AGENTS.md` propio.
- **PII presente:** terceros con NIT ⇒ **GATE-DATASET (Ley 1581/2012 + RGPD) es obligatorio**, no opcional.

---

## 1. Decisión de alcance que define todo — CORTE LIMPIO (requiere tu GO)

El protocolo **no** gobierna ni retrofitea la migración de DB ya hecha (retrofitear violaría la regla 3.4 y daría
un dataset débil — honestidad no-retrofit). El protocolo gobierna **el desarrollo del módulo-aplicación de
Presupuesto de aquí en adelante** (casos de uso, reglas fiscales en código, API/UI sobre la DB migrada).

- **De ahí sale el dataset de tesis:** la *coordinación de agentes* (decisiones, handoffs, fallos, coste), **no**
  los datos municipales ni la migración pasada.
- **Corte limpio:** el **primer handoff real del módulo-app** = primer punto de dato, capturado en caliente.
- La migración de DB hecha queda como insumo/fundación; no se reimporta al ledger.

> **Recomendación:** corte limpio. Confírmalo antes de que el arquitecto registre nada.

---

## 2. Restricción de orden DURA (única innegociable)

**#4 atestación debe estar ON antes del primer handoff real del módulo-app.** No retrofiteable. Todo lo demás
puede reordenarse; esto no.

---

## 3. El pipeline — 3 carriles + track del usuario

### CARRIL A — Instrumentación de tesis (PRIMERO; cierra antes del primer handoff)

- **A1 · #4 atestación de autoría** (SEED-INV, el corazón del TFM). DECISION + SPEC:
  `prev_hash` encadenado en `eventlog.py` + **identidad/firma por agente** (Ed25519 o keyless) + **anclaje externo**
  periódico del digest de cabeza. Modelo de amenaza A1–A4 (doc. 02). off-by-default → piloto → on.
  *Manipulation check:* ≥99 % de atestaciones bien formadas en runs legítimos, o el instrumento está roto.
- **A2 · GATE-DATASET** (DECISION de despeje legal): base jurídica (Ley 1581/2012 Galapá + RGPD Cons.26),
  minimización, **esquema de DOS PLANOS** (solo plano de protocolo; payload por hash; **CERO texto libre; CERO PII
  de terceros en el event log**), DPIA-lite, verificación de ToS del proveedor LLM. Aprobación por escrito registrada.
- **A3 · §9 acoplamiento read-only** (Codex): enforcement read-only **real** del satélite (Core montado/clonado
  read-only o identidad sin permiso de escritura) **antes** de cualquier lectura en vivo por #2/#3. Pre-condición dura, registrada.
- **A4 · Encendido:** tras A2+A3, activar #4 + #2 PROV + #3 feed. (#1 interno puede poblarse sin GATE-DATASET.)

### CARRIL B — Capacidad de producción (Fase 1 + 2 + perfil) — SOLO lo que Presupuesto exige

- **B1 · Fase 2 (E2 connectors/MCP)** — solo los que el módulo necesita: **SQL Server** (lectura del modelo migrado),
  **Git** (repo del módulo), **CI**. `deny-by-default`, `trust_boundary` por conector, la DECISION fija que
  **MCP no concede autoridad**. DECISION + SPEC + golden. (No construir conectores de otros módulos.)
- **B2 · Fase 1 (E1 skills) mínimas** — skills **neutrales** reutilizables: verificar regla de negocio contra el
  legacy, convenciones DDL, verificación de migración. Digestión a 4–5 reglas por run. CERO dominio en el core.
- **B3 · Perfil de dominio** `profiles/financiero_presupuesto/` — las reglas fiscales (compromiso ≤ saldo del CDP;
  combinación rubro-fuente-BPIN debe preexistir; no auto-crear rubros/fuentes/proyectos), convenciones SQL, y las
  reglas del `AGENTS.md` de Budget plegadas como perfil. **Fuera** del core neutral.

### CARRIL C — Front (lanzar la metodología + desarrollar Presupuesto) — qué debe contener

Un solo front, tres paneles + onboarding:

1. **Operar la metodología** (legibilidad operador/equipo): estado vivo (`TASK_INDEX` / `PROJECT_STATE` / `CLAIMS`),
   qué está reclamado / in-progress / blocked, **qué me toca a mí**, últimas decisiones, **estado de gates**
   (¿#4 on? ¿GATE-DATASET despejado?), indicador de drift, `mailbox/open`.
2. **Desarrollar Presupuesto** (vista de proyecto): `migration_index` por grupo de tablas, entidades hechas/pendientes,
   **checklist de reglas de negocio fiscales**, enlaces a objetos SQL, cola de handoffs del módulo.
3. **Panel de tesis** (que el instrumento esté sano): % de atestaciones bien formadas (#4), eventos capturados,
   cost-attribution por handoff, estado de GATE-DATASET / GATE-INST / PRE-REG.
4. **Onboarding**: cómo conducir al orquestador (no editas estado a mano; intents/handoffs/claims) + glosario
   (intent, handoff, claim, gate, decision).

Entrega: **read-only primero** (snapshot del repo), luego vivo. La versión delgada se puede armar ya (no bloquea nada).

### TRACK USUARIO (paralelo) — terminar diseño/migración de la DB de Presupuesto

Sigue su ritmo. **Punto de convergencia:** DB lista **+** #4 ON **+** connectors/perfil listos → primer handoff real
del módulo-app = T0 del dataset de tesis.

---

## 4. Orden y paralelismo

```
  CARRIL A (instrumentación) ── A1 (#4) + A2 (GATE-DATASET) + A3 (§9) DEBEN cerrar
        │                        antes del primer handoff real del módulo-app
        │
        ├─ CARRIL B (capacidad) ── puede AVANZAR en paralelo a A,
        │                          pero NO hay primer handoff real hasta que A esté ON
        ├─ CARRIL C (front) ────── en paralelo desde YA (read-only)
        └─ TRACK usuario (DB) ──── en paralelo
                                   │
                                   ▼
              CONVERGENCIA → primer handoff gobernado + instrumentado = T0 dataset
```

---

## 5. Guardrails (regla 3.4 + invariantes del protocolo)

- **Toda pieza la jala una necesidad real de Presupuesto con fecha.** Nada especulativo (anti meta-proyecto perpetuo).
- **Neutralidad de dominio:** reglas fiscales en el perfil, nunca en el core ni en `*.template.*`.
- **Dos planos / sin PII** en el event log (DECISION-0033).
- **Escritor único** (`submit_intent`): el desarrollo del módulo-app también pasa por el protocolo.
- **SemVer + CHANGELOG** en cada cambio visible; cada mejora entra por DECISION → SPEC (acceptance + test_plan) →
  golden → off-by-default.

---

## 6. Riesgos honestos

- **Capacidad (una persona) = Riesgo nº 2 del roadmap.** El pipeline es deliberadamente delgado: #4 y el front son
  lo cargante; el resto, just-in-time. No abrir Fase 4/5 todavía.
- **Corte limpio vs retrofit:** recomiendo corte limpio. Retrofitear la migración hecha daría dataset débil.
- **GATE-DATASET es real** (terceros con NIT = PII): es prerrequisito legal, no formalidad.
- **El Budget hoy vive fuera del protocolo:** el corte limpio evita el costo de onboarding retroactivo.

---

## 7. Arranque inmediato recomendado (3 cosas)

1. **Front read-only ya** — no bloquea nada, da legibilidad para ti y el equipo. (Lo puedo armar de inmediato.)
2. **Borradores de DECISION para el arquitecto:** #4 (A1) + GATE-DATASET (A2) — el carril que destraba la tesis.
3. **Confirmar el corte limpio** (§1) — define el alcance de todo lo demás.
