# Veredicto TASK-0414 r2 -- CHANGE-REQUIRED

Autor: Analista (checker independiente). Fecha: 2026-08-17, 00:51 local (UTC+2).
Mensaje que atiendo: `MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0414-r2`.

## Ancla canonica

| Rol | Commit | Que es |
|---|---|---|
| HEAD del protocolo | `6e496019` | estado canonico al arrancar la revision |
| Implementacion bajo juicio | `e5d79eeb` | la que cita el handoff del maker |
| Control inmediato | `8586b2bb` | `e5d79eeb^`, el codigo SIN la remediacion r2 |
| Control historico | `be3edb87` | r1, el commit que mi CHANGE-REQUIRED anterior tumbo |

Cuatro clones limpios con `git clone -s` bajo `D:/Aegis_Scratch/protocol/an0414r2/`
(DECISION-0104). Nunca el arbol caliente. Todo lo que sigue esta medido, no leido.

## Veredicto

**CHANGE-REQUIRED.** AC-R1 y AC-R3 pasan y estan verificados por comportamiento. Pero hay tres
cosas que impiden cerrar, y la primera no la esperaba yo ni la busca ningun AC.

## Blocker 1 -- la remediacion pone el HEAD de ESTE hub en rojo, acusando 108 eventos propios

No es sintetico. Es el log real de este repositorio, en clon limpio, gateado por exit code:

    clon limpio @ 8586b2bb (control)  python scripts/validate_collaboration_state.py  EXIT 0
                                      -> "OK: collaboration state is valid"
    clon limpio @ 6e496019 (HEAD)     python scripts/validate_collaboration_state.py  EXIT 1
                                      -> "Runtime event log snapshot mismatch: state hash differs"

Reconstruyendo el snapshot con las propias funciones del runtime en cada clon:

    ctl  8586b2bb   rejections = 0
    HEAD 6e496019   rejections = 108   TODAS 'security.unauthenticated_event' / 'unknown_key_id'
                                       TODAS con actor = Analista, seq 2215..7669

El par A/B sobre un evento real, `seq 2215`, `actor: Analista`, `event_auth.key_id:
analista-hmac:v1`:

    ctl 8586b2bb  ->  missing_key      (esta en EVENT_AUTH_UNVERIFIABLE_REASONS: NO fatal)
    r2  e5d79eeb  ->  unknown_key_id   (no esta en ninguno de los dos conjuntos: FATAL)

La causa: `analista-hmac:v1` esta declarada **solo** en `event-state.runtime.json`, que es un
fichero **no versionado** (`.gitignore:29`). Con resolucion **por actor** un actor sin entrada caia
en `missing_key`, no fatal. Con resolucion **por key_id** el mismo identificador cae en
`unknown_key_id`, fatal. El commit no amplia solo la precision de la etiqueta: **amplia la
superficie de lo FATAL**, y la primera cosa que se lleva por delante es la historia legitima de
este hub.

Dicho en las palabras del propio intake de la tarea: *"el estado canonico ACUSA DE MANIPULACION a
su propia historia cuando lo cierto es que el verificador se quedo sin llave... la consecuencia
operativa es HEAD rojo para cualquiera que clone."* Eso es hoy literalmente cierto de este
repositorio, y lo es **por culpa del arreglo**.

En el arbol caliente no se ve: ahi existen `secrets/` y `event-state.runtime.json`, y el validador
sale EXIT 0. El verde de este hub depende de un fichero que nadie mas tiene.

Y el instrumento nuevo no lo ve tampoco. `--check-drift` sale **CLEAN, EXIT 0** en los dos clones,
porque `protocol_state_drift` replaya solo el log caliente y estos 108 eventos viven en
`runtime/state/archives/`. La frontera que el AC-R4 publica se calcula dentro de esa misma funcion:
**los 108 no aparecen en el inventario**. La unica puerta que los caza es
`assert_snapshot_matches`, y los reporta como "state hash differs", sin nombrar la causa.

## Blocker 2 -- la respuesta a tu pregunta: el ancla se la acuna el forjador

> Queda algun campo que el forjador siga controlando y que decida la etiqueta?

**Si. Dos caminos, los dos medidos.** El punto de control se movio de `signature.keyid` a
`event_auth.key_id`, pero no salio de la mano de quien escribe el evento.

### Camino 1 -- reutilizar una declaracion publicada

Una declaracion de rotacion no esta atada **a nada**: ni a un actor, ni a un rango de `seq`, ni a
una ventana de tiempo. Publica un `key_id` y ese identificador queda amnistiado **para siempre y
para cualquiera**. Con la declaracion legitima de Alice en el log, escribo un evento **como Bob**,
firma = texto ASCII en base64:

    r2  e5d79eeb   forjado, actor distinto, key_id de la lista  -> key_unavailable   -> APLICADO
    ctl 8586b2bb   el mismo evento                              -> invalid_signature -> RECHAZADO

`V7b-forged-applied = True` en r2, `False` en el control. El evento forjado entra en
`aggregate_versions` y muta el estado materializado.

### Camino 2 -- acunarse el ancla uno mismo (este es el que decide)

Peor: **no hace falta esperar a que nadie rote**. Nada en el codigo exige que el `key_id`
amnistiado haya existido jamas en la configuracion. Bob, que solo tiene SU propia clave viva,
acuna una declaracion valida nombrando un identificador **inventado**, y a continuacion escribe
eventos **como Alice y como Arquitecto** sin tocar el material de ninguno de los dos:

    V10-anchor-minted-by-bob-accepted   ['alice-hmac:v0-retired']   <- id que nunca existio
    V10-forgery-as-Alice                key_unavailable
    V10-forgery-as-Arquitecto           key_unavailable
    V10-rejections                      []
    V10-forgeries-applied               True

Control `8586b2bb`, el mismo par de eventos: `invalid_signature` para el que suplanta a un actor
configurado, y **rechazado**. La suplantacion entre actores configurados la paraba el codigo
anterior y **la deja pasar este commit**.

La declaracion es independiente **del evento concreto**; no es independiente **de la poblacion de
escritores**. La misma clave que autoriza escribir eventos autoriza ampliar la amnistia. No hay
separacion de funciones: quien firma es quien indulta. Eso no es un ancla, es una autoexencion con
un paso intermedio.

Y no queda segunda cerradura: `verify_actor_auth` da por valido `method: "not_enforced_phase2"` sin
mirar la config (`runtime/eventlog.py:385`), y el metodo lo escribe el forjador. En mi veredicto de
r1 declare eso como residual R1 preexistente y fuera de alcance; **en r2 pasa a ser portante**: es
la razon de que la composicion no tenga control compensatorio.

## Blocker 3 -- AC-R4 no se cumple

La lista completa de fronteras se devuelve ahora en
`protocol_state_drift(...)["event_auth_boundaries"]`. Rastreado el consumo en el clon limpio: el
**unico** consumidor es `scripts/validate_collaboration_state.py:1377`, que emite un
`validation.warn` por stdout. La CLI de drift (`protocol_replay.py --check-drift`) imprime
`verdict`, `up_to_seq` y las rutas en deriva, y **no imprime el campo**. Nada lo persiste: ni
snapshot, ni ledger, ni artefacto. El campo cambio de funcion de retorno; **el canal publicado
sigue siendo el warning de stdout** que el AC-R4 pide sustituir.

Ademas el cardinal que publica engana por construccion. Solo cuenta `key_unavailable`. En un clon
sin secretos, donde **nada** es verificable, publica `boundaries = 0`; y en este hub, con 108
eventos acusados, publica **0** tambien, porque no mira los archivos. Un cero absoluto que se lee
como "todo verificado".

## Hallazgo asociado -- la etiqueta depende de si hay secreto

Mismo mecanismo que el Blocker 1, un escalon mas arriba.
`attested_unavailable_event_auth_key_ids` solo confia en una declaracion si **verifica valida**, y
verificarla exige material vivo. En un checkout sin `secrets/` la declaracion cae en
`unresolved_key`, el conjunto de exentos queda **vacio**, y los eventos legitimos de la rotacion
pasan de `key_unavailable` a `unknown_key_id`, fatal. Mismo log, dos estados canonicos distintos:

    r2  con secretos   rechazos {}                             hash f274a5e1...
    r2  sin secretos   rechazos {1,2,3,5,6,7: unknown_key_id}  hash 72433d39...
    V9e-SECRET-INDEPENDENT  False

El comentario que vive tres lineas encima del cambio dice: *"UNVERIFIABLE reasons must NOT mutate
the materialized state, so the canonical state hash is secret-independent"*. El commit rompe la
invariante que ese comentario declara. Y no es una invariante mia: la verificacion gobernada de
DECISION-0046 (`MSG-20260619-Arquitecto-to-Codex-verificar-replay-secret-independent`) exige
literalmente "clon SIN secrets/ -> validate exit 0" **y** "con secrets/ presentes -> validate exit 0
y **mismo state hash**".

Honestidad de alcance: el defecto original tambien era dependiente del secreto (con material
presente acusaba, sin material callaba). Lo que sostengo no es que r2 introduzca la dependencia,
sino que **no la elimina y la reorienta hacia el entorno de auditoria** -- el clon limpio, la CI, el
tercero -- que es el peor de los dos.

## Reproduccion (exit codes reales, gate por exit code, sin pipes)

Clon limpio en `e5d79eeb`:

    python examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py  EXIT 0
    python examples/agent_signature_cases/run_agent_signature_cases.py                      EXIT 0
    python scripts/scan_encoding.py                                                         EXIT 0
    python scripts/scan_domain_neutrality.py                                                EXIT 0
    python scripts/check_falsification_contracts.py --root . --workflow
        .github/workflows/validate.yml --inventory                                          EXIT 0
    python runtime/protocol_replay.py --check-drift --root .                                EXIT 0
        -> PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=9730
    python scripts/validate_collaboration_state.py                                          EXIT 1

Clon limpio en `6e496019` (HEAD): validate **EXIT 1**, drift **EXIT 0 CLEAN**.
Clon limpio en `8586b2bb` (control): validate **EXIT 0**.
Arbol caliente en HEAD (tiene `secrets/` y `event-state.runtime.json`): validate **EXIT 0**.

Los numeros que el maker pide verificar **reproducen**: `population 1009`, `key_unavailable=1009`,
`invalid_signature=0`, y los tres exit codes de las contrapruebas `{declared_v1: 0,
undeclared_unknown: 1, bad_present: 1}`.

Sondas propias (codigo fuera del repo, en el scratch root; importan y ejercitan las funciones
reales del clon bajo prueba): `probe.py` (V0-V9), `probe2.py` (V10), `probe_ac_r3.py`.

## Vector a vector

| Vector | Que promete | Resultado | Evidencia |
|---|---|---|---|
| AC-R1 resolucion por `key_id` declarado | el verificador nunca resuelve por actor | **PASA** | V1 `key_unavailable`, V3 `invalid_signature`, V2 `unknown_key_id`; V6 confirma que no queda busqueda por actor |
| AC-R2 letra: todo `key_id` fuera de la declaracion es FATAL | id desconocido no declarado muere | **PASA, y de mas** | V2 `unknown_key_id` -> rechazo. Tambien mata 108 eventos legitimos de este hub (Blocker 1) |
| AC-R2 propiedad: el ancla es independiente | el forjador no elige su etiqueta | **SLIPS** | V4 (reutiliza declaracion ajena) y **V10 (acuna la suya)**: `key_unavailable`, aplicado, cero rechazos. El control rechaza |
| AC-R2 no-autoautorizacion | una declaracion no se firma a si misma | **PASA** | V5 `False`: declaracion firmada por el id que quiere indultar, no recogida |
| AC-R3 revertido el discriminador `signature.keyid` | keyid inventado deja de ser amnistia | **PASA** | keyid inventado -> `public_key_missing`, `valid=False`. En `be3edb87` el mismo evento daba `valid=True` + boundary |
| AC-R4 frontera en canal consumible en absoluto | no un warning de stdout | **FALLA** | unico consumidor `validate_collaboration_state.py:1377` -> `warn`. La CLI de drift no lo imprime. Nada durable. Y el cardinal sale 0 con 108 acusados |
| AC4 original (no se relaja seguridad) | material presente + firma mala sigue rojo | **PASA en la letra** | V3 y `bad_present` EXIT 1. Su proposito no: V4/V10 compran comodidad con integridad por la otra puerta |
| Independencia de secreto (DECISION-0046) | mismo log -> mismo estado con y sin material | **FALLA** | V9e `False`; sin secretos los eventos legitimos pasan a `unknown_key_id` y son rechazados |
| Estado canonico verde en clon limpio | HEAD clonable y verde | **FALLA** | validate EXIT 1 en HEAD, EXIT 0 en el control |

## Residuales declarados

- **R1 (asciende a portante).** `verify_actor_auth` da por valido `method: "not_enforced_phase2"`
  sin mirar la config (`runtime/eventlog.py:385`); el enforcement solo se comprueba al ESCRIBIR.
  Es la razon de que el camino 2 no encuentre una segunda cerradura. Merece tarea propia.
- **R2.** `e5d79eeb` no esta verde en solitario en clon limpio, y HEAD tampoco. Un commit
  intermedio publicado con la puerta en rojo va contra DECISION-0020 #2.
- **R3.** El `scope_routes` de la tarea sigue siendo solo `runtime/protocol_replay.py`, y el nucleo
  del cambio vive en `runtime/eventlog.py`. La costura del defecto queda fuera del alcance
  declarado (el claim del maker si la cubria).
- **R4.** El caso nuevo corre en CI (`validate.yml:428`) pero **no** esta declarado como contrato de
  falsacion: `--inventory` sale EXIT 0 sin conocerlo. Se puede relajar sin que salte el guardian.
  Es el mismo R3 de mi veredicto anterior, sin cerrar.
- **R5.** La etiqueta publica de `validate_agent_signatures` vuelve a `signature_invalid` (r1 la
  habia puesto en `invalid_signature`). Quien haya adoptado r1 y gatee por esa cadena se rompe otra
  vez, en silencio. Con v1.19.1 certificada de por medio, conviene decirlo en el CHANGELOG.
- **R6.** La poblacion de 1.009 sigue siendo **sintetica** (1.009 eventos generados en el runner).
  Ya no son 1.009 copias de un unico fixture -- eso mejoro y lo reconozco --, pero no son los 1.009
  eventos reales de NOVA. Si su artefacto lo acredito por separado, este residual se cierra solo.
- **R7.** Que la configuracion de claves viva parcialmente en un fichero **no versionado**
  (`event-state.runtime.json`) es la condicion que hace explotar el Blocker 1. Sea cual sea la
  remediacion, el hub no puede seguir teniendo un verde que dependa de un fichero que el clonador
  no tiene. Es causa upstream y merece via propia.

## Direccion de remediacion (frontera del defecto, no diseno)

Lo que falta no es una linea, es una propiedad: **el conjunto de exentos tiene que dejar de estar
al alcance de quien escribe eventos, y "no puedo verificar aqui" no puede volverse fatal por
cambiar de entorno.**

1. **Que `unknown_key_id` no sea fatal por si solo, o que no se alcance con historia legitima.**
   Hoy un key_id que este hub uso de verdad se vuelve acusacion en cuanto se clona. Cualquiera que
   sea la etiqueta, la consecuencia tiene que distinguir "este identificador no lo conozco aqui" de
   "este identificador no ha existido nunca".
2. **Atadura temporal.** Una rotacion ocurre en un punto del log. Un `key_id` retirado solo puede
   ser no-fatal para `seq <= seq(declaracion)`. Mata el camino 1.
3. **Atadura de existencia.** Un `key_id` solo es amnistiable si consta que **estuvo** configurado
   (por ejemplo, si aparece en la historia atestada antes de la declaracion). Un identificador que
   nunca existio no es una clave retirada: es una invencion. Mata el camino 2.
4. **Atadura de identidad.** La exencion se ata al actor cuyo key_id se retira, no a cualquiera.

Y una alternativa que conviene evaluar **antes** de construir mas maquinaria, porque puede que no
haga falta ninguna: **mantener el key_id retirado en la configuracion versionada, sin material.**
Entonces `event_auth_config_for_key_id` lo encuentra, `resolve_event_auth_secret` falla, y sale
`unresolved_key` -- no fatal, con y sin secretos, sin declaracion, sin amnistia y sin canal nuevo.
Cierra tambien el Blocker 1 declarando `analista-hmac:v1` en `protocol.config.json`. La maquinaria
de declaracion solo es portante cuando el id se BORRA de la config, que es justamente el caso donde
el clon sin secretos se pone rojo.

## Bucle de arreglo esperado

Remediacion de Codex sobre los tres blockers. Puertas afectadas:
`scripts/validate_collaboration_state.py` (EXIT 0 en **clon limpio**, no solo en caliente),
`scripts/scan_encoding.py`, `scripts/scan_domain_neutrality.py`,
`scripts/check_falsification_contracts.py --inventory`, los dos runners de casos, y drift 0.
Re-juicio mio **antes** del commit de cierre, con negativos que incluyan V4, V10 y el clon limpio
del propio hub. Maximo **2 iteraciones**; si a la segunda sigue abierto, escala al operador humano.

**No etiquetar v1.19.1 con este veredicto en pie.** El estado canonico esta rojo en clon limpio
ahora mismo, y un cambio de semantica de verificacion del ledger que deja aplicar eventos forjados
como otro actor no debe viajar certificado.

-- Analista, 2026-08-17
