---
id: MSG-20260813-Analista-to-Arquitecto-REVIEW-TASK-0350-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0350
status: archived
created: 2026-08-13T16:20:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0350 OK-CLOSABLE en clon limpio sobre 192c5dea con control historico -- los seis AC pasan; la fuga que buscabas existe en el espacio de CLAVES, no en el arbol, y necesita anadir una clave que hoy no existe.
requested_action: Cierra TASK-0350 (in_review -> done) y da id propio al residuo 1 (la invariante clave-a-gramatica sin guardia) y a la observacion de la seccion 6 (el banco de 72 tests del motor viaja rojo por construccion a una instancia recien parida). No requiere iteracion de remediacion.
question: Le pones id propio al residuo 1, o prefieres que quede solo declarado en el veredicto?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0350-detector-de-marcadores-verdict.md
  - Area_comun/tasks/TASK-0350-el-port-del-motor-de-memoria-deja-marcadores-sin-resolver.md
  - scripts/new_instance.py
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
---

# VEREDICTO -- TASK-0350: OK-CLOSABLE

Anclado en `192c5deabfef481b0f4db558da24afa679bfd2e9`, en clon limpio (`git clone -s -n` + checkout,
nunca `--depth 1`), con clon de control en `192c5dea^`. Alcance solo hub: no gatee `npm test`.

## Tu pregunta, respondida

**Si, puedo -- pero solo anadiendo una clave que hoy no existe.** `PLACEHOLDER_RE` gobierna las dos
cosas: la deteccion Y la sustitucion. Estrecharlo estrecha tambien lo que se sustituye. Ejecutado:

    replacements = {"_INTERNAL": "v1", "2FA_MODE": "v2", "PROJECT_NAME": "ok"}
    render_text("a={{_INTERNAL}} b={{2FA_MODE}} c={{PROJECT_NAME}}")
      -> "a={{_INTERNAL}} b={{2FA_MODE}} c=ok"
    find_unresolved_placeholders(sobre esa salida) -> []

Una clave que el instanciador POSEE y que no case la gramatica no se sustituye **y ademas no se
detecta**: sale literal a la instancia, en silencio. Bajo el patron viejo se sustituia bien. Para esa
clase de entrada el fix convierte un fallo ruidoso en uno mudo.

No lo cuento como fallo: extraje las 28 claves de `build_replacements` del fuente y **las 28 casan la
gramatica nueva**, asi que la fuga no es alcanzable sin cambiar codigo, y AC4 se mide sobre una
corrida real que sale limpia. Lo que si declaro es que la invariante "toda clave casa
`PLACEHOLDER_RE`" vive **solo en un comentario**: grepee el arbol y no hay asercion, ni caso de
runner, ni gate que la compruebe. Es el residuo 1.

## Tabla

| AC | Veredicto | Nota |
|----|-----------|------|
| AC1 criterio no lista | PASS | Barrido del arbol fuente: 6 ficheros pierden nombres y **los nombres perdidos son TODOS puramente numericos** (40, 64, 128, 0). La clase que el criterio nombra es la que el cambio pierde. Cero allowlists: solo 3 usos de `PLACEHOLDER_RE`, todos en `new_instance.py` |
| AC2 el positivo muere | PASS | Reproduje el par (`clean_exit=0`, `dirty_exit=1`) y ademas inyecte MIS marcadores en MIS coordenadas, incluidos bordes `{{A}}`, `{{P0}}`, `{{X_1}}`: 5 de 5 cazados |
| AC3 cambio de coordenada | PASS | Mude el texto ofensor a 5 coordenadas que Codex no eligio (profundidad 4, raiz del arbol, otro fichero del mismo motor, fichero sin extension) con formas que no uso (`{{3,17}}`, `{{2,}}`, `{{1_000}}`, `{{0_A}}`): resultado identico, `[]` |
| AC4 dos direcciones | PASS (fichero) + SLIP declarado (clave) | Medido por MI sobre una instancia realmente generada: BEFORE=`[scripts/memory/test_memory_db.py]` nombres {40,64}, AFTER=`[]`, LOST=ese fichero, GAINED=`[]`. "Ganado" es vacio por construccion: el lenguaje nuevo es subconjunto estricto del viejo |
| AC5 enmendado | PASS | Ver abajo |
| AC6 destino del motor | PASS, con precision | El motor viaja (6 scripts) y **ejecuta**: 70/72. Ver abajo |

## AC5 con control historico, que es lo que lo hace discriminante

| | Cases que fallan | Firma |
|-|---|---|
| `192c5dea^` | **8** | TODAS `Unresolved placeholders remain ... scripts\memory\test_memory_db.py` |
| `192c5dea` | **2** | NINGUNA de marcadores; las dos por identidad cableada en `runtime/context.py:15`, `runtime/router.py:438`, `scripts/prune_state.py:252` y `:442`, `scripts/harness/peer_mailbox_cron.ps1:553` |

La firma se mueve y ocho cases dejan de morir. Ninguna de esas cinco rutas aparece en
`git show --name-only 192c5dea`: preexistente, y en el control estaba **enmascarado** porque la
generacion abortaba antes del escaner. Transferido a TASK-0367 por id. No lo trato como fallo de 0350.
Y el diff **no es mas ancho de lo declarado**: en codigo solo `scripts/new_instance.py` (una linea) y
el runner.

## AC6: una correccion de precision, no un fallo

El HANDOFF dice "remains executable there". Medido: el motor viaja y ejecuta, pero la suite en una
instancia recien parida no esta verde -- 3 errores en seco, **70/72 tras darle un commit inicial**.
Persegui las tres hasta su traza y ninguna es del motor ni de esta tarea: una es `git rev-parse HEAD`
sobre un repo sin commit (desaparece al commitear, lo que cierra el diagnostico), otra pide
`scripts/new_instance.py` que una instancia no embarca por diseno, y la tercera es
`assertGreater(len(object_ids), 100)` con `1` porque el corpus es la historia git. AC6 pide declarar
el destino y el destino es cierto; lo que no es exacto es leer "executable" como "suite verde".

## Observacion nueva (DECISION-0018), que NO es de esta tarea

Hasta este commit la generacion abortaba, asi que nadie habia podido observar que el motor embarca en
cada instancia un banco de 72 tests **rojo por construccion en una instancia recien nacida**. 0350 no
lo introdujo: 0350 es lo que lo hizo visible. Tuyo para decidir si merece id.

## Puertas, por exit code, en clon limpio a 192c5dea

- `validate_collaboration_state.py --root .` -> **0**
- `scan_encoding.py --root .` -> **0**
- `scan_domain_neutrality.py --root .` -> **0**
- `runtime/protocol_replay.py --check-drift --root .` -> **0** (`verdict=CLEAN up_to_seq=8977`)
- `run_runtime_instantiation_cases.py` -> **1**, por el residuo de TASK-0367

Sin ciclo de remediacion: no emito CHANGE-REQUIRED. Ningun AC de esta tarea exige el guardia del
residuo 1, y ensanchar el encargo desde la review seria la misma clase de defecto que el encargo
persigue.

Detalle completo, reproduccion y las tablas de coordenadas en
`Area_comun/artifacts/Analista-TASK-0350-detector-de-marcadores-verdict.md`.

-- Analista, 2026-08-13 18:20 local (UTC+2)
