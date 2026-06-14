---
decision_id: DECISION-0034
title: Catalogo de modos de fallo (MAST) + gobernador "merece un loop?" (Fase 0, E5+E6)
status: accepted
date: 2026-06-14
ratified_at: 2026-06-14
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0001, DECISION-0005, DECISION-0013, DECISION-0017, DECISION-0018, DECISION-0020, DECISION-0022, DECISION-0024, DECISION-0026, DECISION-0027, DECISION-0028, DECISION-0030, DECISION-0031, DECISION-0032]
phase: P2
---

# DECISION-0034 - Catalogo de modos de fallo (MAST) + gobernador "merece un loop?"

> Estado: ACCEPTED (ratificada por el operador 2026-06-14, tras pasada del analista, con 3 ajustes
> incorporados; misma MINOR 1.7.0). Cambio ADITIVO, documental, neutral de dominio. Arranca **Fase 0**
> acotada a **E5 + E6**. NO toca #3/flag, #4/chain/auth ni SA.4. #1/protocol_research queda DIFERIDO a
> su propia decision.
>
> **Ajustes del analista incorporados (2026-06-14):**
> 1. E5 - la columna `Incident?` no lleva conteo empirico de incidentes (eso es #1, diferido): solo
>    declara si se **cita** un incidente concreto por fila o el guardrail es preventivo; cada fila "Yes"
>    se reviso para citar un incidente real (DECISION/evento) o degradarse a "guardrail, sin incidente
>    propio" (empezando por FM-1.1).
> 2. E5 - se declara el limite: MAST es el **vocabulario**, no la superficie exhaustiva; el protocolo
>    tambien guarda modos NO-MAST no catalogados aqui (encoding/DECISION-0012, neutralidad de dominio,
>    secretos).
> 3. E6 - el gobernador anade **terminacion/convergencia NO-opcional** (condicion de parada/bound, o
>    contencion via sobre SA.4: budget/deadline/liveness, FM-1.5) y una **clausula de alcance temporal**:
>    liga expansiones decididas DESPUES de su entrada en vigor; NO revoca autoridad ya concedida (piloto
>    DECISION-0027).

## Contexto

La hoja de ruta (reconciliada en `Area_comun/artifacts/RECONCILIACION-hoja-de-ruta-20260614.md`)
situa en **Fase 0** dos entregables documentales que hoy no existen:

- **E5 - FAILURE_MODES.md**: el protocolo ha mitigado a lo largo de su evolucion una serie de fallos
  operacionales concretos (drift, anomalias no senaladas, colision de escrituras, stalls de liveness,
  topes de budget, arbol sucio no declarado, escalada a humano, errores de esquema), cada uno con su
  guardrail, pero **dispersos** entre decisiones y docs. Falta un **catalogo nombrado** que los
  vincule a un vocabulario reconocible y permita preguntarse, ante un fallo nuevo, "que modo es y que
  guardrail lo cubre".
- **E6 - gobernador del loop**: antes de construir scanners de descubrimiento (Fase 4 / E3) o de
  ampliar la autonomia supervisada (SA.4), no hay un **filtro explicito** que obligue a justificar que
  una tarea repetitiva **merece** convertirse en un loop autonomo. Sin ese filtro, el riesgo es
  construir automatizacion para trabajo que no la amortiza (coste, falta de verificacion objetiva).

## Decision

Se anaden **dos artefactos documentales aditivos y neutrales de dominio**:

### E5 - `Area_comun/protocol/FAILURE_MODES.md`

Catalogo **modo -> sintoma -> guardrail** que usa la **taxonomia MAST** (*Multi-Agent System failure
Taxonomy*, Cemri et al. 2025, "Why Do Multi-Agent LLM Systems Fail?") como **vocabulario** para nombrar
los 14 modos de fallo. Cada modo se mapea al incidente operacional real que el protocolo ya ha mitigado
(cuando existe) y al guardrail que lo contiene, con referencia a la DECISION/mecanismo concreto.

**Honestidad metodologica (innegociable):** el documento declara que es **"taxonomia MAST aplicada a
incidentes operacionales de este protocolo"**, NO una afirmacion de equivalencia 1:1 con MAST-Data ni un
estudio empirico (eso es #1, diferido). Donde un modo MAST **no tiene un incidente propio** en este repo,
el documento **lo dice explicitamente** y, si aplica, nombra el guardrail preventivo parcial. No se
inventan incidentes para rellenar la tabla.

### E6 - gobernador "merece un loop?" en `Area_comun/protocol/TASK_PROTOCOL.md`

Seccion nueva con un **check de 30 segundos** y un **checklist OBLIGATORIO** de 4 condiciones que debe
pasar cualquier propuesta antes de construir un `discovery_scanner` o un flujo de autonomia:

1. **Recurrencia** - se repite al menos **semanalmente**?
2. **Verificabilidad** - existe **verificacion automatizada / objetiva** del resultado?
3. **Economia** - el **budget absorbe el reintento** (el coste del loop, incluidos reintentos, cabe en
   los topes)?
4. **Capacidad** - requiere **tools de nivel senior** (justifica un agente dedicado en vez de un paso
   manual)?

**Regla de roadmap:** *no se construye E3 (scanners de Fase 4) antes que E6*, y ampliar SA.4 pasa este
checklist primero. El gobernador queda enlazado como **pre-check** de la Fase 4 (E3) y de toda ampliacion
de autonomia supervisada.

## Alcance / No-alcance

- **En alcance:** crear `FAILURE_MODES.md`; anadir la seccion del gobernador a `TASK_PROTOCOL.md`;
  enlazar ambos desde el onboarding (`Area_comun/README.md`) y desde la guia de review (seccion de
  review de `TASK_PROTOCOL.md`); acceptance estructural; SemVer **MINOR** + entrada en CHANGELOG.
- **Fuera de alcance:** NO se toca el flag de cost-attribution (#3), ni chain/firmas/anclaje (#4), ni
  `enforce`/`authoritative`, ni `subagents_enabled`, ni SA.4. **No se crea** `protocol_research/` ni se
  estudia el historial con MAST (#1): eso requiere su **propia decision** (montar repo satelite
  read-only) y queda DIFERIDO. No se cambia ningun comportamiento de runtime: ambos entregables son
  texto.

## Versionado y neutralidad (DECISION-0001)

Aditivo, sin remover ni cambiar comportamiento existente; solo anade documentacion y una regla de
proceso. **MINOR** (v1.7.0). Neutral de dominio: MAST es vocabulario generico de sistemas multi-agente y
el gobernador habla de loops/scanners genericos; **cero terminos de negocio** (nada de Galapa/ScanPay) ni
en el core ni en los `*.template.*`. Sin secretos.

## Consecuencias

- Existe un catalogo nombrado de modos de fallo con su guardrail, enlazado desde onboarding y review: un
  agente entrante puede mapear un fallo observado a un modo y a su contencion sin arqueologia de
  decisiones.
- Toda automatizacion futura (scanners E3, ampliacion SA.4) pasa por un filtro explicito de 4 condiciones
  antes de construirse: se evita automatizar trabajo que no la amortiza.
- Maker != checker intacto: este cambio no relaja ninguna autorizacion; anade proceso y documentacion.
- El honesto "MAST aplicado, no MAST-Data" deja la puerta abierta a #1 (estudio empirico) como decision
  separada, sin comprometer ahora una afirmacion que no se ha medido.
