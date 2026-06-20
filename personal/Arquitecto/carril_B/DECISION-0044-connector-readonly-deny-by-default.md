---
decision_id: DECISION-0044
title: Carril B pieza 1 - capacidad de connector READ-ONLY (deny-by-default, trust_boundary por conector, el connector no concede autoridad); primer adaptador SQL Server
status: accepted
ratified_at: 2026-06-19
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0040, DECISION-0041, DECISION-0035, DECISION-0002, DECISION-0022]
phase: P2
---

# DECISION-0044 - Capacidad de connector read-only, deny-by-default

> ACCEPTED por el operador (GO Carril B pieza 1, 2026-06-19,
> MSG-20260619-Operador-to-Arquitecto-carril-B-GO-connector-sqlserver-ro). **Pista propia, independiente
> de #4** (sigue OFF; no combina ventanas de riesgo). Cambio aditivo, neutral de dominio. Habilita el
> DISENO del connector; el USO VIVO contra una DB real es un GO POSTERIOR del operador tras verificacion
> read-only REAL por Codex (§9), espejo de DECISION-0041. Implementacion gateada via SPEC-0083 + TASK-0121.

## Contexto (la necesidad, regla 3.4)

El modulo-app de Presupuesto arranca sobre una DB ya migrada por el operador (Access -> SQL Server, en
`D:\Agentes\Ingenas\Budget`). Para arrancar el desarrollo se necesita **verificar la migracion** (legacy
-> DB migrada), las **convenciones DDL** y reglas vs legacy. Eso requiere **leer** la DB. El protocolo
gobierna el DESARROLLO del modulo-app (DECISION-0040: el dataset de tesis es la COORDINACION de agentes,
no la DB/PII); la DB la mantiene el operador APARTE. Hoy el protocolo **no tiene capacidad de connector**:
un agente no tiene una via gobernada, read-only y con frontera de confianza para leer una fuente externa.

- Necesidad: verificar la migracion y convenciones DDL como parte del arranque del modulo-app.
- Fecha: ventana de dogfooding actual (2026-06-19). El operador ajusta si hay un hito mas estrecho.

## Decision

1. **Introducir una capacidad de CONNECTOR, neutral de dominio, en una capa propia `connectors/`.** Un
   connector es una capacidad de **LECTURA** de una fuente externa, gobernada por un **`trust_boundary`
   explicito por conector**. La capa es aditiva y paralela a `profiles/`/`examples/` (DECISION-0002): el
   **core neutral no la importa** ni la referencia en gates/CI obligatorios. Primer y unico conector por
   ahora: un adaptador **SQL Server read-only** (tecnologia generica de RDBMS = neutral; NO dominio).

2. **El connector NO concede autoridad ("MCP no concede autoridad").** El dato leido por un connector es
   **evidencia/insumo**, nunca fuente de autoridad ni via de mutacion. Un connector: (a) **no escribe** el
   ledger (`Area_comun/state/*.json`), el event log (`runtime/state/events.jsonl`) ni la fuente externa;
   (b) **no otorga capacidades** a ningun agente ni decide nada; (c) leer **no emite eventos**. Si en el
   futuro un connector se expone via MCP u otro transporte, el mismo principio y `trust_boundary` aplican:
   el transporte no concede autoridad.

3. **Deny-by-default y read-only REAL (no por convencion).** El connector solo deja pasar operaciones
   **explicitamente de lectura**; todo lo demas se **RECHAZA con clase de error explicita ANTES de tocar
   la fuente** (no se "filtra despues"). Espejo de DECISION-0041 / prueba negativa de A1: el read-only se
   demuestra con una **prueba negativa OBJETIVA y registrada** (todo intento de escritura/mutacion -
   INSERT/UPDATE/DELETE/MERGE, DDL CREATE/ALTER/DROP/TRUNCATE, EXEC no-allowlisted, multi-statement con
   escritura - es rechazado), no con una asercion en codigo o docs.

4. **Precondicion de USO VIVO (GATEADA, espejo DECISION-0041; dueno Codex §9).** Antes de que el connector
   corra contra una **DB real**, debe existir enforcement read-only REAL **en dos planos**: (a)
   connector-side, el clasificador deny-by-default de (3); (b) server-side, una **identidad/login de
   minimo privilegio** (solo lectura, p.ej. `db_datareader` + `ApplicationIntent=ReadOnly`) de modo que un
   intento de escritura lo **RECHACE el servidor**, no solo el connector. Codex verifica (§9) **antes de
   cualquier lectura viva**: revision sustantiva (no grep) de que no hay ruta de escritura, **+ prueba
   negativa objetiva registrada** (escritura rechazada por el servidor) **+ GO posterior del operador**.
   Sin esa verificacion + GO, **no hay lectura viva** (fail-closed, no se cae en silencio).

5. **Off-by-default; el golden corre sin DB viva.** La capacidad **se entrega DESHABILITADA** (registro de
   connectors fuera de `protocol.config.json`, default `enabled:false`). El golden corre **integramente
   con fixtures (result sets grabados/fake)**, determinista, **sin red ni DB**. Con la capacidad OFF no se
   intenta ninguna conexion viva (fail-closed). **Genesis intacto:** el registro de connectors vive FUERA
   de `protocol.config.json` y NO lo consume `compute_genesis_prev_hash` -> aterrizar la capacidad
   off-by-default **no cambia genesis ni el drift** (no requiere re-genesis), igual que el resolutor de
   DECISION-0043 no toco genesis.

6. **Frontera de datos / PII (DECISION-0040).** Las salidas del connector **no se persisten** al event log
   ni al estado; **PII de terceros NUNCA al event log** (dos planos). **DEF-PII (TASK-0118) sigue
   diferida**: esta pieza fija la FRONTERA (el connector no escribe ledger/eventos), no un detector de PII;
   no se arranca captura viva aqui.

7. **Neutralidad de dominio innegociable.** CERO termino fiscal/negocio en `connectors/` ni en sus tests.
   Las reglas fiscales (compromiso <= saldo CDP; rubro-fuente-BPIN debe preexistir; no auto-crear) y las
   del `AGENTS.md` de Budget van a `profiles/financiero_presupuesto/`, **fuera del core neutral y fuera de
   este connector** - pieza aparte que jala una necesidad fechada distinta, NO en esta decision.

8. **Independiente de #4.** Esta capacidad **no toca** ni depende de los flags de #4
   (chain/agent_signatures/anchor/event_auth); no se enciende, provisiona ni flipea nada de #4 aqui. Pista
   de riesgo separada.

9. **Cambio de capacidad/contrato -> esta DECISION + SPEC + aprobacion humana (SDD).** SPEC-0083
   (acceptance_criteria + test_plan + golden off-by-default); TASK-0121 la implementa (Codex), el
   Arquitecto reproduce (maker!=checker). El uso vivo es un GO posterior tras §9.

## Alcance / No-alcance

- **En alcance:** capa `connectors/` neutral; framework de connector con `trust_boundary` + deny-by-default
  read-only + "no concede autoridad"; primer adaptador SQL Server read-only con backend de fixtures; gate
  de neutralidad; golden off-by-default; precondicion de uso vivo (§9 + GO) nombrada con dueno (Codex).
- **Fuera de alcance:** lectura viva contra la DB real (GO posterior tras §9); el perfil
  `profiles/financiero_presupuesto/` y cualquier regla fiscal; connectors de Git/CI (piezas siguientes
  cuando una necesidad fechada las jale); exposicion MCP concreta; encender/provisionar/flipear #4; tocar
  la DB de Budget o su migracion (el connector solo lee, y aun no en vivo).

## Consecuencias

- El protocolo gana una via gobernada, read-only y con frontera de confianza para leer fuentes externas,
  sin meter dominio al core y sin perturbar genesis/drift (capacidad off-by-default, registro fuera del
  config canonicalizado).
- Habilita la secuencia: capacidad (esta, off) -> verificacion read-only REAL por Codex (§9, dos planos) +
  GO del operador -> lectura viva acotada para verificar la migracion/DDL.
- Reversible: con la capacidad OFF el runtime se comporta como hoy; ningun gate/CI del core depende del
  connector.

## Alternativas consideradas

- **Connector con guard read-only solo por convencion + grep estatico.** Descartada: el grep es evadible y
  la convencion no es enforcement (misma logica que DECISION-0041); por eso deny-by-default + prueba
  negativa objetiva, y server-side least-privilege para el uso vivo.
- **Meter el registro de connectors en `protocol.config.json`.** Descartada como forma primaria: cambiaria
  el dict canonicalizado -> re-genesis y superficie de drift por una capacidad off-by-default. Un registro
  fuera del config deja genesis intacto (espejo DECISION-0043).
- **Poner el SQL Server connector bajo `profiles/financiero_presupuesto/`.** Descartada: el adaptador es
  tecnologia neutral (RDBMS); meterlo en el perfil mezclaria capacidad con dominio. El perfil llevara las
  reglas fiscales, que CONSUMEN el connector, no el connector mismo.
- **Permitir lectura viva ya en esta pieza.** Descartada: sin §9 (dos planos) + GO seria una garantia
  convencional sobre datos reales (posible PII). El golden con fixtures cubre el contrato sin DB viva.
