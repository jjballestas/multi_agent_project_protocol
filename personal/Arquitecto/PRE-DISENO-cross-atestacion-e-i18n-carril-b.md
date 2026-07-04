# PRE-DISENO (solo doc, sin ejecucion) - cross-atestacion NOVA/Aegis + scoping i18n Carril B

> DIRECTIVA operador (profundiza-cola-sello-e-infra), item P3(c), relleno. Pre-diseno para discutir/
> aprobar despues; NO ejecuta nada, NO crea DECISION nueva, NO toca ledger ni epoch.

## 1. Mecanismo de cross-atestacion NOVA/Aegis (post-sello, DECISION-0088 #5)

DECISION-0088 fija la REGLA ("el journal de medicion del hub registra, en cada gate, el sha256 de la
atestacion de la instancia") pero no el MECANISMO concreto. Dos opciones evaluadas:

**Opcion A - columna nueva en el schema de medicion (mas simple, mas acoplada).**
- Anadir `instance_attestation_sha256` (y `instance_commit`) a `schema_medicion.json` v-siguiente (post
  freeze v1.0 del sello; NO se toca el schema congelado el 08-jul).
- Al cerrar cada fila del gate gobernado (post-migracion), el journal-ledger script del hub lee el
  commit HEAD de NOVA/Aegis en ese momento, computa/lee su sha256 de estado (o el hash que NOVA/Aegis ya
  publique de su propio #4), y lo escribe en la fila.
- Contras: acopla el schema del hub a la existencia de una instancia externa; instancias sin migrar
  dejarian el campo NA (aceptable, mismo patron que otros campos "sin artefacto-fuente").

**Opcion B - intent `decision` periodico de cruce (mas desacoplada, recomendada).**
- El hub NO modifica su schema de medicion. En vez de eso, cada gate gobernado post-migracion dispara un
  intent `decision` en el hub (tipo ya existente, sin necesidad de un intent nuevo) cuyo `.md` de decision
  registra: `hub_gate_id` (referencia a la fila del journal), `instance_commit` (hash de NOVA/Aegis),
  `instance_attestation_sha256` (sha256 que NOVA/Aegis ya calcula para su propio ledger/gate), y
  `verified_by` (quien lo comprobó, tipicamente el Arquitecto). Es un REGISTRO DE CRUCE, no una fila de
  medicion.
- El journal de medicion referencia el `decision_id` del cruce en una columna ligera existente/asimilable
  (o en `next_recommended`/notas de la fila, sin cambiar el schema congelado).
- Ventajas: no acopla el schema v1.0 sellado; el mecanismo de cruce es el MISMO patron ya usado para
  atestar SPECs/sandbox (submit_intent type decision); reutiliza infraestructura existente, cero codigo
  nuevo del validador.
- **Recomendacion de este pre-diseno: Opcion B.** Menor riesgo sobre el schema sellado, reutiliza un
  mecanismo ya probado (DECISION alimentando el ledger #4), y el acoplamiento hub<->instancia queda
  explicito y auditable en un artefacto propio en vez de una columna silenciosa.

### 1.1 Cuando se activa
Solo aplica DESPUES de que Nova migre a NOVA/Aegis (DECISION-0088 #4, trigger = sello + medicion de
Etapa 1 cerrados). Mientras el build se coordina en el hub (ventana actual), no hay cruce que registrar
(un solo asiento, sin costura). Este pre-diseno NO adelanta la migracion.

### 1.2 Verificacion por terceros
Cualquiera puede: (a) tomar el `decision_id` de cruce citado en una fila del journal del hub, (b) leer su
`.md` (instance_commit + instance_attestation_sha256), (c) clonar NOVA/Aegis en ese commit y recomputar su
sha256 de atestacion, (d) comparar. Sin secretos, sin autoridad especial requerida para verificar.

## 2. Scoping del programa i18n Carril B (DECISION-0087 s.7)

DECISION-0087 ya fijo la direccion: i18n = Carril B, POST-sello, acotado a la **superficie PUBLICADA**
(el dogfooding en espanol de este repo NO se publica). Este scoping enumera que cae dentro/fuera:

**DENTRO de la superficie publicada (candidatos a traducir a ingles):**
- Core neutral: `AGENTS.md`/`AGENTS.template.md`, `CLAUDE.md` (si se publica una guia generica),
  `Area_comun/README.md`/`README.template.md`, `Area_comun/protocol/TASK_PROTOCOL.md`.
- Los `*.template.*` (masters que se publican, DECISION del layering core/profiles/examples).
- `examples/minimal_instance/` (referencia publicable).
- La capa `skills/` neutral exportable (DECISION-0061) -- **YA esta en ingles** (verificado: `skills/
  codegen-triage.skill.md` y las recetas de instancia de ejemplo en Nova-Budget/docs/codegen-triage/ usan
  llaves de salida `codegen`/`boundary` en ingles, no en espanol). **No requiere trabajo de traduccion de
  output-keys** -- ya nacio neutral en ingles; el scoping aqui es solo confirmar que se mantiene asi al
  agregar mas skills a la capa neutral (gate de estilo, no de contenido).
- El spec de referencia del protocolo (si se publica uno consolidado fuera de AGENTS.md).

**FUERA (permanece en espanol, dogfooding no publicado):**
- Todo `Area_comun/` VIVO de esta instancia (tasks/specs/decisions/mailbox/reports/state): es la
  operacion real de este proyecto, no el master publicable.
  - `personal/<id>/` de cada participante (privado por diseno).
  - `Area_comun/specs/nova/` (namespaced instancia Nova, dominio real, nunca se publica).
  - Los reportes humanos (`Area_comun/reports/`) y decisiones (`Area_comun/decisions/`) del dogfooding.

**Item de trabajo (para cuando el Operador priorice Carril B):** traducir el core neutral +
templates + README + example + spec de referencia; verificar que la capa `skills/` neutral se mantenga
100% en ingles como gate de estilo (no de contenido) en el checklist de nuevas skills.

## 3. Que NO decide este documento
- No fija fecha de ejecucion de ninguno de los dos items (ambos son Carril B / post-migracion,
  explicitamente fuera de la ventana del sello).
- No crea una DECISION formal; si el Operador aprueba la Opcion B de s.1, se redacta una DECISION corta
  de implementacion cuando llegue el momento (post-migracion), no antes.
