---
decision_id: DECISION-0040
title: GATE-DATASET - base legal y esquema de dos planos para instrumentar el desarrollo del modulo-app de Presupuesto (Ley 1581/2012 + RGPD; base = ausencia de persona fisica en el dataset)
status: accepted
ratified_at: 2026-06-19
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0033, DECISION-0035, DECISION-0010, DECISION-0001]
phase: P2
---

# DECISION-0040 - GATE-DATASET (despeje legal + dos planos)

> ACCEPTED por el operador (GO de promocion 2026-06-19); aprobacion por escrito registrada como esta
> DECISION. Cambio aditivo, documental, neutral de dominio en el Core. La tarea diferida DEF-PII queda
> registrada como TASK-0118 (no se construye ahora, regla 3.4).

## Contexto

El protocolo gobernara el **desarrollo del modulo-aplicacion de Presupuesto** sobre la DB ya migrada
(Access -> SQL Server, trabajo independiente del operador en `D:\Agentes\Ingenas\Budget`). **Corte
limpio (DECISION-0001 + brief):** el protocolo NO retrofitea la migracion; gobierna el desarrollo de
aqui en adelante. El **dataset de tesis es la coordinacion de agentes** (decisiones, handoffs, fallos,
coste), **NO** los datos municipales ni la migracion.

**El hecho nuevo que obliga este gate:** el modulo-app toca una DB con **PII real de terceros** (tabla
`maco009t` = 10.676 entidades con NIT). GATE-DATASET fue NOMBRADO como hard-stop en DECISION-0035 /
`gates/GATES.md` del satelite, pero sin despejarlo. Esta decision es el despeje legal y, sobre todo,
fija el **invariante que mantiene licita la instrumentacion interna sin consentimiento por evento**: la
PII de Budget **jamas entra al event log**.

## Decision

1. **Esquema de DOS PLANOS (DECISION-0033) - lo ESTRUCTURAL vs lo DISCIPLINARIO (honestidad; revision Analista+Codex).**
   - **Garantia ESTRUCTURAL (verificada):** el **sujeto** de cada artefacto entra por `canonical_hash`,
     no por contenido. Eso es estructural y verificable.
   - **NO es estructural HOY (control DISCIPLINARIO, DECISION-0018):** el event log SI admite **texto
     libre** en campos de predicado/metadato del payload (p.ej. `deliverables`, `title`, `description`,
     `notes`, `review`) y en handoffs/mailbox. **NO existe un scan de PII**: `scan_encoding` solo valida
     ASCII/canal y `scan_domain_neutrality` solo terminos de dominio -- un NIT es ASCII y no es termino de
     dominio, asi que **ningun gate actual lo detecta** (verificado sobre `runtime/state/events.jsonl`).
     Por tanto "cero PII de terceros en el event log" es HOY un **control disciplinario + regla de
     boundary**, NO una propiedad estructural. (Esta es la objecion central de la revision; se incorpora.)
   - **Regla operativa:** la PII de Budget (NIT, razon social, datos de terceros) **permanece en SQL
     Server y no se escribe en plano de protocolo**. Un evento/handoff/mailbox que incluya un dato de
     tercero es una violacion de boundary (anomalia DECISION-0018), no un caso aceptable.
   - **Endurecimiento estructural = DIFERIDO** (ver "Tarea diferida" abajo): detector de PII real /
     exporter del plano publicable, condicion ANTES de la captura viva publicable (#2/#3), NO de Carril A.

2. **Base legal y minimizacion.** La linea de carga es **la ausencia de datos de persona fisica en el
   dataset de coordinacion**: los **actores son ids de agente NO humano** (no personas fisicas) y la PII
   de terceros de Budget queda excluida del plano de protocolo. Datos que no son de persona fisica quedan
   fuera del ambito subjetivo de **Ley 1581/2012** y **RGPD**. **Correccion (revision Analista):** NO se
   invoca RGPD Cons.26 para "sacar el dato del ambito" -- Cons.26 dice que los datos **seudonimizados
   siguen DENTRO** del ambito (solo los anonimos quedan fuera), y el `subject_hash` es **seudonimo y
   re-identificable**, no anonimo. Por eso la base NO descansa en el seudonimo, sino en que el corpus no
   contiene personas fisicas; el mapeo de reidentificacion del actor-agente **no forma parte del
   dataset**. Minimizacion: solo el plano de protocolo necesario para estudiar la coordinacion. (El unico
   humano del corpus -- el operador -- se trata en la DPIA-lite, sec.4.)

3. **Limitacion de finalidad.** El dataset se usa para investigacion sobre **coordinacion de agentes**.
   No se usa para perfilar terceros ni para decisiones sobre personas (no hay datos de personas en el).

4. **DPIA-lite (evaluacion de impacto ligera).**
   - *Que datos:* plano de protocolo (agentes, tareas, decisiones, coste, hashes). No PII de terceros.
   - *Persona fisica en el corpus:* el **operador humano** SI aparece (las DECISIONs lo nombran como
     `deciders: [operador humano]`; da los GO). Es la **unica persona fisica**. Se trata como
     **investigador/responsable del tratamiento que consiente sobre sus propios datos**, y figura como
     **etiqueta de rol** ("operador humano"), no como nombre/identificador directo. (Correccion de la
     revision Analista: la version previa lo omitia.)
   - *Por que:* medir como coordinan los agentes el desarrollo del modulo-app.
   - *Riesgo:* reidentificacion del actor-agente (seudonimo); fuga de PII de Budget al log por error de un
     agente (control disciplinario hoy, sin detector).
   - *Mitigacion:* sujeto por hash (estructural) + regla de boundary (disciplinaria) + actores = ids no
     humanos + mapeo de reidentificacion fuera del dataset. **NO** se afirma que `scan_encoding`/canal
     detecte PII (no lo hace: solo ASCII/canal). El detector de PII real es la **tarea diferida** (abajo).

5. **Verificacion de ToS del proveedor LLM.** Antes de instrumentar, verificar por escrito que enviar
   **plano de protocolo (sin PII de terceros)** al proveedor LLM esta permitido por sus terminos, y que
   **ninguna PII de terceros de Budget se envia al LLM**. Registrar el resultado de la verificacion.

6. **Checklist de franqueo (de GATES.md) - alcance de ESTE despeje.** Esta decision despeja GATE-DATASET
   para la **instrumentacion INTERNA** del desarrollo del modulo-app (capturar la coordinacion como
   historial propio, sin PII de produccion). La **citabilidad/publicacion** del dataset y la
   **produccion** de los exportadores #2 (PROV) / feed #3 contra el Core vivo siguen condicionadas a:
   - **Aserciones de honestidad verificables para #1:** cero claim 1:1 con MAST-Data; cero "citable"
     hasta franqueo pleno; cero numeros sin corpus validado.
   - **Enforcement read-only REAL** antes de que #2/#3 corran contra el Core vivo (DECISION-0041 / A3).
   - **Base legal + minimizacion + de-linking** del payload para cualquier publicacion.
   - Para salida TFM/tesis: **GATE-INST** (aprobacion institucional/etica) + **PRE-REG** (pre-registro
     de hipotesis/metricas) ademas de este gate.

## Tarea diferida (regla 3.4 - condicion de captura viva, NO bloqueo de Carril A)

Se registra como **tarea con fecha** (se formaliza en `TASK_INDEX` al promover; **NO se construye ahora**):

- **DEF-PII: detector de PII real + exporter del plano publicable.** Un scanner/validador que detecte PII
  de terceros (NIT colombiano, razon social, rutas/payloads SQL de Budget) en el plano de protocolo, y/o
  un exporter que emita SOLO campos estructurados + hashes para el dataset publicable. Convierte la
  garantia "cero PII" de **disciplinaria** a **estructural**.
- **Condicion (regla 3.4):** DEF-PII **DEBE cerrar ANTES de la captura viva publicable** (#2/#3 contra el
  Core vivo / cualquier publicacion). **NO bloquea Carril A hoy** (la instrumentacion interna se sostiene
  por el control disciplinario + dos planos para el sujeto) y **NO se construye ahora** (anti
  meta-proyecto, regla 3.4).
- **Fecha:** se fija al promover, atada al hito "antes del primer franqueo de #2/#3 o publicacion".

## Alcance / No-alcance

- **En alcance:** base legal, minimizacion, dos planos (estructural para el sujeto + disciplinario para el
  predicado), DPIA-lite, verificacion de ToS, checklist de franqueo, registro de la tarea diferida
  DEF-PII; habilita capturar la coordinacion del modulo-app de forma interna y licita.
- **Fuera de alcance:** publicar/citar el dataset; correr #2/#3 en produccion; experimentos TFM (eso es
  GATE-INST + PRE-REG); gobernar la DB de Budget o su migracion (corte limpio); introducir reglas
  fiscales en el core (van al perfil, Carril B).

## Consecuencias

- La instrumentacion del modulo-app es licita sin consentimiento por evento porque la PII de terceros
  nunca entra al dataset (dos planos).
- Queda explicito que publicar/citar exige el checklist completo + gates institucionales: honestidad
  preservada (no se sobre-afirma).
- El invariante "sin PII en el event log" queda explicito y HONESTO: **estructural** para el sujeto
  (hash), **disciplinario** para el predicado/handoffs/mailbox hoy, con un **detector estructural
  DIFERIDO** (DEF-PII, tarea con fecha) como condicion previa a la captura viva publicable. No se
  sobre-afirma como ya-estructural.

## Alternativas consideradas

- **Capturar payloads completos (con datos de Budget) y anonimizar despues.** Descartada: introduce PII
  de terceros al log, viola dos planos y la minimizacion; reidentificacion residual; riesgo legal alto.
- **No instrumentar hasta tener aprobacion institucional plena.** Descartada para el uso INTERNO: el
  historial propio sin PII no requiere GATE-INST (solo la salida TFM lo requiere); bloquear todo seria
  desproporcionado y retrasaria T0 del dataset sin reducir riesgo real.
