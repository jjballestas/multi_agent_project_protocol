---
decision_id: DECISION-0044
title: Capacidad neutral de conector de datos READ-ONLY (deny-by-default, trust_boundary, sin autoridad desde el dato) - Carril B pieza 1
status: draft
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0033, DECISION-0040, DECISION-0041, DECISION-0035, DECISION-0010]
phase: P2
---

# DECISION-0044 (DRAFT) - Conector de datos READ-ONLY (capacidad neutral)

> DRAFT del Arquitecto. NO promovida. GO del operador (Carril B pieza 1, 2026-06-19): abrir Carril B en
> pista propia INDEPENDIENTE de #4 (sigue OFF; no combinar ventanas de riesgo). Entra por SPEC-0083 +
> TASK-0121 + golden off-by-default + maker!=checker (Codex reproduce) + honestidad Analista. NO enciende
> #4. NO lectura viva de la DB sin verificacion s.9 (DECISION-0041) + GO posterior del operador.

## Contexto (necesidad con fecha, regla 3.4)

El arranque del modulo-app de Presupuesto bajo el protocolo necesita VERIFICAR la migracion (legacy ->
DB migrada en `D:\Agentes\Ingenas\Budget`) y convenciones DDL. Necesidad = esa verificacion; fecha =
ventana de dogfooding actual (2026-06-19). Para eso el protocolo necesita una capacidad de LEER una
fuente de datos externa de forma gobernada, SIN poder escribirla y SIN derivar autoridad de su contenido.
Esta es la primera y unica pieza de Carril B por ahora (connectors Git/CI y el perfil fiscal son piezas
posteriores que jalara su propia necesidad fechada).

**Corte limpio (DECISION-0001/brief):** el connector SOLO LEE; no toca la DB ni su migracion. La DB la
gobierna el operador aparte. El dataset de tesis sigue siendo la coordinacion de agentes, no la DB/PII.

## Reuso de primitivas existentes (menos superficie, mas neutral)

- **`runtime/tool_policy.py`** ya da allowlist **deny-by-default** + scope por agente. El connector es un
  recurso gobernado por tool_policy: deshabilitado salvo allow explicito + scope.
- **`trust_boundary`** ya existe en el predicado de atestacion (DECISION-0029/SPEC-0081): el dato que
  cruza al protocolo desde una fuente externa lleva su `trust_boundary`. El connector reusa ese concepto:
  todo resultado se etiqueta con su frontera de confianza (no se "limpia" ni se eleva a autoritativo).
- **Sin autoridad desde el contenido** (linaje DECISION-0033/cost-attribution): el runtime nunca deriva
  capability/decision/permiso del contenido de un evento. El connector lo extiende: su salida es DATO de
  ENTRADA, jamas una autorizacion.

## Decision

1. **Autorizar una capacidad NEUTRAL de conector de datos READ-ONLY** en el core. Un connector es un
   adaptador de SOLO-LECTURA a una fuente externa: expone `read(selector) -> records`; **no expone
   metodos de escritura**. La primera implementacion concreta es un adaptador SQL Server read-only contra
   la DB migrada; el FRAMEWORK es neutral (SQL Server es tecnologia, no dominio).

2. **Deny-by-default.** El connector no hace nada salvo que el config lo habilite Y tool_policy lo permita
   con scope. Off-by-default en el template y en la instancia hasta que una necesidad fechada lo encienda.

3. **`trust_boundary` por conector.** Cada connector declara su `trust_boundary` (etiqueta de la fuente).
   Todo record set devuelto se ETIQUETA con `{connector_id, trust_boundary, read_only:true}`. El dato
   externo no se vuelve autoritativo por entrar.

4. **"MCP/connector no concede autoridad" (principio duro).** La salida de un connector es DATO DE
   ENTRADA: el runtime NUNCA deriva de ella una capability, una decision, un permiso ni una transicion de
   estado. Leer un valor no autoriza nada (extiende DECISION-0033). Verificable estructuralmente.

5. **Read-only REAL (prueba negativa objetiva, ref DECISION-0041).** El adaptador abre la fuente en modo
   solo-lectura (login/credencial read-only; SQL Server: usuario read-only + `ApplicationIntent=ReadOnly`)
   Y rechaza por allowlist toda sentencia de escritura (DML/DDL/EXEC). **Todo intento de escritura =
   RECHAZADO con clase** (binario, bloqueante). La credencial read-only vive FUERA del repo (patron del
   keyfile gitignored de DECISION-0043); cero secretos commiteados.

6. **Lectura viva GATEADA (s.9 + GO).** El golden corre con fixtures **fake/recorded**, SIN DB viva (la
   DB no esta montada ni se requiere). La lectura VIVA de la DB real solo tras: (a) Codex verifica el
   invariante read-only s.9 (DECISION-0041, prueba negativa objetiva) ANTES de cualquier lectura viva, y
   (b) GO posterior del operador. Esta decision NO autoriza lectura viva.

7. **Neutralidad de dominio (innegociable).** CERO dominio fiscal/negocio en el core ni en `*.template.*`.
   Las reglas fiscales (compromiso <= saldo CDP; rubro-fuente-BPIN debe preexistir; no auto-crear) y las
   del `AGENTS.md` de Budget van a `profiles/financiero_presupuesto/` -- pieza APARTE, NO en este
   connector ni en esta decision.

8. **PII de terceros NUNCA al event log** (DECISION-0040, dos planos). El connector no captura PII al log;
   DEF-PII (TASK-0118) sigue diferida; aqui no se arranca captura viva.

9. **SDD + maker!=checker.** Entra por SPEC-0083 (acceptance_criteria + test_plan + golden) + TASK-0121
   (Codex implementa, Arquitecto reproduce) + honestidad Analista donde aplique. Independiente de #4 (no
   combinar ventanas de riesgo; #4 OFF).

## Alcance / No-alcance

- **En alcance:** framework neutral de connector read-only + adaptador SQL Server read-only + golden con
  fixtures + deny-by-default + trust_boundary + no-autoridad + prueba negativa de escritura.
- **Fuera de alcance:** lectura viva de la DB (s.9 + GO posterior); connectors Git/CI (piezas siguientes);
  perfil `financiero_presupuesto` con reglas fiscales (pieza aparte, fuera del core); encender #4 /
  provisioning / flip; tocar la DB o su migracion; captura de PII.

## Consecuencias

- El modulo-app puede verificar migracion/DDL de forma gobernada y atestable, sin poder escribir la DB y
  sin que el dato externo conceda autoridad.
- Reversible/seguro: off-by-default; deshabilitado se comporta como hoy (sin connector).
- Habilita (con su propio GO) las piezas siguientes de Carril B y, mas adelante, el primer handoff real
  del modulo-app (T0, que exige #4 ON -- pista aparte).

## Alternativas consideradas

- **Connector read-write con guardas.** Descartada: el corte limpio + el riesgo no lo justifican; la
  necesidad es VERIFICAR (leer), no escribir. Read-only by-construction es mas simple y seguro.
- **Meter el adaptador SQL Server como dominio.** Rechazada por confusion de capas: SQL Server es stack,
  no dominio; lo fiscal va al perfil. El framework es neutral.
- **Lectura viva ya.** Descartada: exige s.9 + GO; el golden con fixtures prueba el contrato sin DB viva.
