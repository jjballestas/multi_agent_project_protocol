# PREP - Instrumentacion de medicion de Contabilidad (Aegis employee-run -> hub cross-atestacion)

> PREP de diseno (Arquitecto, 2026-07-11, ACTION operador instrumentacion-medicion). Define el cableado de
> medicion de la evidencia employee-run/transferibilidad (2a instancia, Contabilidad, empleado real Julian) ANTES
> de su 1a unidad MEDIDA (post-B/jheredia:v1, post-30-jul). NO urgente (build gated); explicito y pre-registrado
> mejor que improvisado. Base: SPEC-NOVA-F3.3 (instrumentacion de medicion, hub) + DECISION-0088 (asiento
> coordinacion build escalonado hub<->instancia) + DECISION-0093 (corte gobernanza hub->Aegis) + CROSS-ATESTACION-
> hub-aegis-registro.md. El Asesor coordina y verifica study-integrity. NO cambia el estudio Nova-Budget congelado.

## 0. Marco (separacion de ledgers, sin incompatibilidad)
- **Nova-Budget** (baseline + Q4): medido en el HUB, CONGELADO. No se toca.
- **Contabilidad**: gobernanza + atestacion en la instancia AEGIS (donde Julian firma), con sha256 anclado al hub
  por gate (DECISION-0088 p.5 / 0093). La MEDICION employee-run se captura en Aegis y se ancla al hub -- el #4 del
  hub retiene la traza sellada. La metodologia-canonica/meta-estudio sigue en el hub.

## 1. Que se mide y DONDE se captura (en Aegis, no en el hub)
- **Eventos F3.3 por unidad medida de Julian** (mismos que Nova-Budget, SPEC-NOVA-F3.3): `cost.attributed`
  (tokens/tiempo atribuidos al maker/checker por unidad, separando tokens_adversarial_informal de
  tokens_checker_formal), `defect.reported` (defectos reales cazados por el gate, con traza), `manual.intervention`
  (intervenciones humanas). **Capturados en el ledger de AEGIS** (submit_intent + err.log del runtime de la
  instancia), firmados por el actor que corresponde (`jheredia:v1` maker post-B; Analista checker; Arquitecto
  orquestador). NO en el hub.
- **study_metrics Q1-Q5** de la(s) unidad(es) de Julian, calculados sobre esos eventos de Aegis (definicion Q1-Q5
  identica a la del sello Nova-Budget para que la comparacion transferibilidad sea valida).
- **Unidad(es) medidas:** las SPEC-CONT-Sx que el sorteo del pre-registro designe DENTRO (criticidad/par si mide);
  las RO/frontera (S1/S6C) probablemente fuera del confirmatorio. Se fija en el pre-registro (s.3).

## 2. Como se ANCLA al hub (cross-atestacion por gate, reusar lo cableado)
- **Reusar la cross-atestacion dual EXISTENTE** (DECISION-0088 p.5 / 0093, `CROSS-ATESTACION-hub-aegis-registro.md`):
  tras cada gate relevante de una unidad medida de Contabilidad, el Arquitecto registra en el HUB una Entrada con
  {seq head de Aegis, prev_hash, sha256 de `events.jsonl` de Aegis} -> el #4 del hub ancla el estado de medicion de
  Aegis en ese punto. NO hace falta un puente de medicion nuevo: el sha256 de la traza de Aegis (que incluye los
  eventos F3.3) queda anclado al hub por la Entrada de cross-atestacion.
- **Ademas (recomendado):** al cerrar la medicion de una unidad, anclar en el hub el **sha256 del artefacto de
  study_metrics Q1-Q5** de esa unidad (via intent del hub, como se hace con las SPEC) -> el hub retiene la traza
  sellada del RESULTADO de medicion, no solo del ledger. Doble ancla: (a) sha256 del events.jsonl de Aegis
  (cross-atestacion), (b) sha256 del artefacto de metricas (intent del hub).
- Frontera: el config pineado del hub (1.14.0, 2E35F26E) NO se toca; el anclaje es por Entrada/intent, no por
  re-genesis.

## 3. Pre-registro (DECISION DE ESTUDIO -- operador + Asesor, NO la sello yo)
Study-integrity: "nada se decide despues de ver datos". Dos opciones; **RECOMIENDO la (A)**:
- **(A) Pre-registro PROPIO de Contabilidad employee-run (analogo al sello Nova-Budget) -- RECOMENDADO.** Un sello
  fechado ANTES de la 1a unidad medida que fije: hipotesis de transferibilidad (la metodologia produce el mismo
  patron de gate-caza-defectos + atribucion en un dominio real distinto con un empleado real), unidades DENTRO/
  criterio de par si mide, Q1-Q5 y su direccion esperada, degradaciones aceptadas, y el criterio de exito. Es la
  evidencia mas fuerte (falsable, pre-registrada). Lo coordina el Asesor; lo SELLA el operador. Encaja como una
  seccion del Sello Etapa 2 (o un sello hermano).
- **(B) Exploratoria DECLARADA (como los chains 1001/1002).** Mas debil; solo si el operador decide que
  Contabilidad es cualitativa. Se declara exploratoria por adelantado (tambien pre-registro de que NO es
  confirmatoria).
- **Esta eleccion es un fork de diseno de estudio -> la decide el operador con el Asesor, no el Arquitecto.** Yo
  dejo el cableado (s.1/s.2) listo para cualquiera de las dos.

## 4. Prerequisitos de la 1a unidad MEDIDA de Julian (checklist)
Antes de que Julian toque su 1a unidad MEDIDA deben estar TODOS:
1. **B (TASK-9303) DONE** -> `jheredia:v1` nominal operativo (atribucion nominal por-humano; la medicion se firma
   con su llave, no con Codex). [READY + GO a Codex; en curso.]
2. **Gate 2-clones nominal VERDE** (Julian jheredia:v1 maker / Arquitecto Analista checker) + cross-atestacion. [A1
   gate primero como onboarding; el nominal tras B.]
3. **Base congelada** `ACCOUNTING_BASE_SOLID_20260711` (sha256 608b4370) + verifier `accounting_sandbox_verifier`.
   [RESUELTO.]
4. **SPEC-CONT de la(s) unidad(es) medidas instanciadas** (kit SPEC-CONT). [En curso, 2/8.]
5. **Instrumentacion F3.3 cableada en Aegis** (captura de eventos + calculo Q1-Q5 + doble ancla al hub, s.1/s.2).
   [Este PREP; falta el wiring concreto cuando abra el build.]
6. **Pre-registro sellado** (opcion A) o exploratoria declarada (opcion B), s.3. [Decision operador+Asesor.]
7. **Calendario Sprint 1 post-30-jul.** [Linea roja.]

## 5. Entregable de este PREP
Este doc fija el DISENO. Lo que queda para el build (post-30-jul): el WIRING concreto (script de captura F3.3 en el
runtime de Aegis + el artefacto de study_metrics por unidad + la Entrada de cross-atestacion por gate) y el
pre-registro sellado (operador+Asesor). Ninguno abre el build ni toca el estudio congelado.
