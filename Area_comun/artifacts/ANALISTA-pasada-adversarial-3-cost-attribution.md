# ANALISTA — Pasada adversarial acotada sobre #3 (cost-attribution por handoff)

> Voz analista independiente. Lente: INVESTIGACION / METODOLOGIA (no re-verificacion de ingenieria —
> eso lo cubren arquitecto + Codex con maker!=checker). UNA pasada, puntos falsables, sin re-arquitectura.
> Pre-GO de activacion en caliente (MINOR 1.6.0). Insumos leidos: DECISION-0033, SPEC-0079, golden
> `runtime_cost_attribution_cases` (6 casos), ordenes 02/03/04 del operador.
> Fecha: 2026-06-14.

## Veredicto de cabecera (3 lineas)

- **GO CON UN CAMBIO DE ESQUEMA, no GO liso.** El evento `cost.attributed` se captura sobre un log
  append-only (replay + #4 prev_hash/anclaje): el formato que actives AHORA es el formato que analizaras
  para H2 y que NO podras retro-corregir. Falta un tag de unidad/version y un contrato canonico de `subject`.
- Para el endpoint que pediste (Δtokens/handoff): el esquema **lo produce**, con dos condiciones falsables.
- Bajo GATE-DATASET: "sin texto libre" ≠ "anonimo". `subject_hash` es **seudonimo (RGPD/Ley 1581), no
  anonimo**. La afirmacion "publicable" debe reformularse antes del dataset.

---

## 1) Fitness para H2 (endpoint: Δtokens/handoff)

**PASA** — para el endpoint tal como lo definiste. Por handoff el esquema emite `cost_tokens` + un
`subject_hash = canonical_hash(subject)` determinista; como el hash es **invariante a la condicion** (no
incluye `seq`/`ts`), el MISMO handoff en el brazo A y en el brazo B comparte clave → da pares. Con N
handoffs apareados tienes N observaciones pareadas → test apareado (Wilcoxon/t pareado) construible.
`by_handoff` (sin agregacion cruzada) preserva la unidad observacional; no la colapsa.

**Metrica de H2 que el esquema NO puede producir (falsable, como pediste):** la **descomposicion
input/output (contexto ensamblado vs generacion) por handoff**. `cost_tokens` es un escalar opaco
inyectado por el orquestador. Si H2 ⊆ {Δtokens/handoff total} → ninguna metrica falta, PASA limpio. Si
H2 quiere atribuir el Δ al *mecanismo* (compaction reduce input, no output) o usar tamaño-de-contexto como
covariable → ese split no existe y, por ser el log inmutable, **no se recupera despues de un escalar**.

**CAMBIO REQUERIDO (concreto, falsable):**
(a) Fijar en SPEC un **contrato canonico de `subject`** por dimension (p. ej. handoff = `{handoff_id}`
exacto, nada de `to`/prosa variable). Hoy el propio golden usa formas inconsistentes — `{handoff,to}`,
`{h}`, `{decision,body_hash}` — luego dos emisiones del "mismo" handoff podrian hashear distinto y el
apareamiento (y el `idempotency_key`) se rompe en silencio. Test: dos emisiones logicas iguales ⇒ mismo
`subject_hash`.
(b) Fijar la **semantica de `cost_tokens`** (¿input+output?, ¿coste del PRODUCTOR o del consumidor del
handoff? — el golden carga el coste al actor emisor "Codex"): ambos brazos deben ser conmensurables.

**RIESGO DECLARADO:** si `subject` no se canoniza, el apareamiento de H2 falla de forma invisible (hashes
no casan) y lo descubres al analizar, no al capturar. Si solo guardas el escalar, cierras para siempre la
puerta a un H2 que distinga input/output.

---

## 2) Supervivencia a GATE-DATASET (RGPD / Ley 1581)

**NO confirmo "ninguno".** Nombro el campo (falsable):

- **`subject_hash` — seudonimo, NO anonimo.** Un hash de contenido es dato **seudonimizado**, no
  anonimizado, bajo RGPD (Considerando 26; WP29 5/2014) y bajo el principio de irreversibilidad de la Ley
  1581. Como el **plano de carga util se retiene** y es enlazable por ese hash, cualquiera con la carga
  util (o con un diccionario de `subject` de baja entropia, p. ej. ids de handoff predecibles) **re-identifica**.
  No filtra texto libre al plano de protocolo — eso es correcto — pero "auditable/publicable sin exponer
  carga util" describe el plano *en aislamiento*; publicar un dataset seudonimo enlazado a payload personal
  retenido sigue siendo tratamiento regulado.
- **`actor` — vector secundario.** Hoy son ids de agente (Codex/Claude). El esquema **no restringe** `actor`
  a vocabulario no-humano; si algun dia se usa un identificador del operador humano (usuario/correo), `actor`
  pasa a ser dato personal directo.

**CAMBIO REQUERIDO (falsable):**
(i) Reetiquetar en DECISION-0033 `subject_hash` como **seudonimo** (no "anonimo/publicable"); GATE-DATASET
trata el plano de protocolo como *regulado-pero-minimizado*. (ii) Para publicacion: o se **rompe el enlace**
(no retener `subject` en ningun lado, o salar por-publicacion y descartar la sal) o se acota explicitamente.
(iii) **Restringir `actor`** por esquema a un vocabulario controlado de ids de agente (no-humano). Test:
validador rechaza un `actor` fuera del vocabulario / detecta payload retenido enlazable.

**RIESGO DECLARADO:** publicar el dataset de la tesis como "anonimizado" seria una **declaracion de
cumplimiento falsa**. El encuadre honesto es "seudonimizado, carga util retirada".

---

## 3) Auditoria de honestidad

**NO confirmo "ninguno".** Excesos concretos (cada uno falsable):

1. **"medicion / captura en caliente" sobreestima un REGISTRO.** El codigo no *mide* tokens: *anota* una
   cifra que le pasa el orquestador (`attribute_cost(..., cost_tokens=N)`). El golden inyecta literales
   (120, 50, 30); nunca cuenta tokens reales. La promesa "capturar en caliente, no estimar" solo se cumple
   si esa cifra upstream es un conteo real y no a su vez una estimacion — y la fuente/unidad **no esta
   especificada**. *CAMBIO:* SPEC fija el contador y la unidad; añadir un caso EN CALIENTE que asierte que
   lo registrado == un conteo de tokens medido independientemente, no un literal.
2. **"event log byte-equivalente con flag off" probado solo en el caso trivial.** `case_disabled_byte_equivalent`
   verifica que *no existe fichero* en un dir nuevo. La instancia viva YA tiene log poblado; la propiedad
   relevante (append a un log existente con flag off ⇒ cero lineas `cost.attributed`, bytes identicos a un
   control) **no esta testada**. *CAMBIO:* caso de byte-equivalencia sobre log poblado.
3. **"auditable sin exponer carga util"** — cierto para el texto, pero cruza con §2: `subject_hash` es
   seudonimo, asi que "auditable/publicable con seguridad" esta parcialmente sobre-afirmado.

**Confirmo que NO se exceden (lo dejo explicito para no inflar el hallazgo):**
- No promete dolares ni "economia"; dice "tokens" / "imputacion generica de tokens" (correcto: coste de
  computo ≠ economia, y el texto se queda en tokens).
- No reclama una capacidad de seguridad (ocap): `applied:false` + replay omitido es una propiedad de
  **integridad**, y esa SI esta ttestada de verdad (`case_drift_unaffected`: `has_drift=False`, replay==hot).

**RIESGO DECLARADO:** el riesgo de honestidad no esta en el codigo (hace lo que hace) sino en la PROSA que
lo nombra "medicion": un revisor de tesis pedira la procedencia del numero y, hoy, el instrumento registra
lo que le den.

---

## 4) Riesgo de retrofit (regla 3.4) — ¿activar AHORA?

**CAMBIO REQUERIDO ANTES de activar (no GO liso).** El espiritu es correcto: capturar en caliente bate
retrofitar (estimar a posteriori es justo lo que quieres evitar). PERO el event log es **append-only e
inmutable** (replay; y #4 prev_hash/anclaje cuando se active sobre estos eventos): lo que captures queda
**congelado**. No re-corres el piloto para arreglar una unidad ambigua. Por tanto el listón sube: el esquema
debe estar bien *antes* de la primera emision en caliente, no "iteramos luego".

**UN cambio de esquema mas, antes de activar (falsable, como pediste):**
> **Añadir al payload de `cost.attributed` un tag explicito de unidad/version** — p. ej.
> `cost_unit: "tokens_total"` (o `tokens_io`) y `cost_schema: "1"`.
>
> Por que este y no otro: es el seguro mas barato contra el arrepentimiento mas caro. Si mañana cambias la
> semantica de `cost_tokens` (split input/output, o mueves la frontera productor↔consumidor), las filas
> historicas quedan **indistinguibles** de las nuevas y no hay forma de saber con que convencion se grabo
> cada una. Con un tag, la migracion futura es interpretable; sin el, el corpus en caliente es ambiguo para
> siempre. Test: toda emision lleva `cost_unit`+`cost_schema`; el summarizer rechaza filas sin ellos.

(Runner-up, misma familia: el contrato canonico de `subject` de §1 — pinearlo es igual de "formato que
lamentaremos". Si solo entra UN cambio, que sea el tag de unidad/version, porque protege el numero mismo.)

**RIESGO DECLARADO:** activar sin el tag = capturar el corpus de H2 en un formato auto-ambiguo que el log
inmutable no te deja re-anotar; si luego H2 necesita input/output o cambias la frontera de atribucion, el
dato caliente ya capturado no es comparable consigo mismo.

---

## Cierre (anti-meta-proyecto)

Una sola pasada. El minimo para tu GO en caliente, en orden:
1. **Tag `cost_unit` + `cost_schema` en el payload** (§4) — bloqueante: es inmutable.
2. **Contrato canonico de `subject` por dimension** (§1) — bloqueante para el apareamiento de H2.
3. **Reetiquetar `subject_hash` como seudonimo + acotar `actor`** (§2) — bloqueante para GATE-DATASET, no
   para el piloto; puede ir en la misma MINOR.
4. **Caso byte-equivalencia sobre log poblado + caso en-caliente con conteo real** (§3) — cierra la
   honestidad de "medicion".

Hecho 1 y 2 (y fijada la semantica de `cost_tokens`), **activar en caliente es correcto y oportuno**: el
resto (3, 4) endurece sin bloquear el piloto. No re-arquitectura; cuatro ediciones acotadas de esquema/golden.

> No consolido ni decido. No mute estado autoritativo. Artefacto para tu GO; el arquitecto entra por
> submit_intent si decides incorporarlo.
