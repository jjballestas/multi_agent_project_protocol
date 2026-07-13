---
name: arquitecto-guarda-estado
description: >-
  Checkpoint de cierre del Arquitecto: cuando el operador dice "guarda estado" (o "guarda el estado",
  "cierra sesion", "deja listo para la proxima", "checkpoint", "haz el handoff"), persiste TODO lo que se
  esta haciendo y COMO se hace, para que una sesion fria retome exactamente donde quedo, y al final ENTREGA
  el PRIMER MENSAJE de inicio de la proxima sesion (compacto, apuntando al prompt guardado). Actualiza:
  (1) la memoria/snapshot con el estado real verificado, (2) el prompt de arranque personal/Arquitecto/
  SESSION_START_PROMPT_<fecha>.md (supersede el anterior; watchdogs como paso OBLIGATORIO), (3) las skills
  cuyo PROCEDIMIENTO cambio. Frontera dura: SOLO archivos de memoria/personales/skills; NUNCA ledger, estado
  gobernado ni claims. Complementa la skill global session-checkpoint con la salida del primer-mensaje y la
  especificidad del Arquitecto (lease, watchdogs, gate-por-exit-code, F-NOVA-01). Trigger words: guarda estado,
  guarda el estado, guardar estado, cierra sesion, checkpoint, handoff, deja listo para la proxima, prompt de inicio.
---

# Arquitecto -- guarda estado (checkpoint + primer mensaje de inicio)

> Las sesiones mueren sin avisar (contexto, cierre, reinicio). Todo lo que solo vive en el chat se pierde.
> Este checkpoint hace que el conocimiento sobreviva a la sesion Y entrega el mensaje que el operador pega
> para arrancar la proxima. Prueba de calidad: el TEST DEL LECTOR FRIO -- alguien sin este chat retoma
> manana con solo los archivos que dejas.

## Frontera dura
Escribe SOLO: la memoria del harness (`memory/*.md`), el area personal `personal/Arquitecto/`, y las skills
del proyecto (`.claude/skills/`). **NUNCA** toca el ledger, `Area_comun/state/*`, claims, ni rutas gobernadas
que exijan coordinacion. El checkpoint es del agente, no es gobernanza. La memoria vive en el dir del harness
(NO se commitea al repo, persiste sola); el prompt y las skills SI se commitean al repo (pathspec explicito).

## Procedimiento

### Paso 0 - Reune el delta REAL (verifica, no asumas)
`git fetch` + `git merge --ff-only origin/main`; luego captura el estado real:
- `git log --oneline -30` (delta de la sesion) + `git rev-parse --short HEAD` (= origin?).
- Tareas en vuelo: status en `TASK_INDEX.json` + claims activos (los mios) en `CLAIMS.json`.
- Gates: `validate_collaboration_state.py` exit; sha8 de `protocol.config.json` (FONDO INTOCABLE = 2E35F26E).
- Lease: `personal/Arquitecto/.session-lease` (session_id mio).
- `open/`: que quedo vivo vs consumido; DECISIONes nuevas; hora UTC actual.
- Feedback/correcciones del operador de la sesion (oro: cambian el COMO, no solo el QUE).

### Paso 1 - Actualiza la memoria (snapshot)
- Reemplaza el bloque TOPE de `memory/project-state-snapshot.md` con un header nuevo fechado + una
  "ACCION INMEDIATA AL RETOMAR" que capture: HEAD/gates/config/lease, fase y foco, trabajo en vuelo con DUENO
  y estado, lo que espera respuesta de quien, decisiones nuevas y su porque, y la SIGUIENTE accion concreta.
  Corrige hechos obsoletos (un snapshot viejo que contradice la realidad es peor que nada). El detalle inferior
  queda como historia. Actualiza `memory/MEMORY.md` si hay una entrada nueva que indexar.

### Paso 2 - Regenera el prompt de arranque
- Escribe `personal/Arquitecto/SESSION_START_PROMPT_<YYYYMMDD>.md` con el estado REAL verificado (no lo que el
  plan decia). Marca el anterior como SUPERADO en el header del nuevo (no lo borres). Estructura fija:
  ROL / COLD-START / FONDO INTOCABLE / QUE ESTOY HACIENDO / COMO LO HAGO (loop) / LECCIONES CLAVE / CANAL DE
  ORDENES + PENDIENTES / SIGUIENTE ACCION.
- **El COLD-START DEBE incluir, como PASO OBLIGATORIO NO-SALTABLE, armar los 3 watchdogs/monitores**
  (entregas con self-filter que ignora `Co-Authored-By: Claude (Opus|Fable|Sonnet)` -- LOS 3 modelos; exec-health;
  higiene). Es directiva permanente del operador: "asegurate que se carguen los watchdogs en la proxima sesion".
  Redactalo con la frase "si no los armas, no has completado el arranque".
- Captura el COMO (no solo el QUE): gate-por-exit-code antes de commit, ASCII puro en Area_comun, ventana
  segura (peers sin lock) para el ledger, gate de trailers (Task-Id en el parrafo final), fix-loop tope 2 iters,
  higiene en lote BACKGROUND, y la leccion F-NOVA-01 (citar la definicion REAL de la BD/artefacto por
  OBJECT_DEFINITION, distinguir THROW proc-directo de trigger/CHECK; el gate independiente caza lo que la
  generacion por-doc deja pasar).

### Paso 3 - Actualiza skills con procedimientos aprendidos (solo el COMO durable)
- SI un procedimiento durable y verificado cambio (ej. "el self-filter debe ignorar AND Fable, no solo Opus"),
  incorporalo a la skill correspondiente. NO metas anecdotas/datos/pids/fechas (eso va a memoria).
- Si el harness bloquea la auto-edicion de una skill, deja el texto propuesto en `personal/Arquitecto/` y avisa
  al operador para que lo apruebe (no la edites a la fuerza).

### Paso 4 - Commit (repo) + memoria (harness)
- Commit atomico al repo con pathspec EXPLICITO del prompt + las skills cambiadas:
  `git add <prompt> <skills...>` ; commit con `Task-Id: none` + `Ops-Reason: checkpoint de sesion` en el parrafo
  final junto a `Co-Authored-By`; push si verde. La memoria (dir del harness) persiste sola, no se commitea.

### Paso 5 - Auto-test del lector frio
Releete y responde honesto: (1) se entiende QUE y POR QUE? (2) esta clara la SIGUIENTE accion? (3) el trabajo
en vuelo tiene dueno y estado? (4) algo importante quedo solo en el chat? Si algo falla, completalo antes de cerrar.

### Paso 6 - ENTREGA EL PRIMER MENSAJE DE INICIO (la salida al operador)
Emite, en un bloque copiable, el PRIMER MENSAJE compacto que el operador pegara para arrancar la proxima
sesion. NO repitas el prompt entero (ya esta guardado); el primer mensaje solo APUNTA a el y exige el arranque.
Plantilla (rellena <YYYYMMDD> con la fecha del prompt que acabas de escribir):

```
Retoma como Arquitecto / Orquestador de multi_agent_project_protocol
(D:\Agentes\multi_agent_project_protocol). Codex=maker, Analista=checker-only,
operador(John)=aprueba. actor_id ledger="Arquitecto". DECISION-0038 narracion minima. HORA en cada informe.
LEE Y EJECUTA el cold-start completo de personal/Arquitecto/SESSION_START_PROMPT_<YYYYMMDD>.md:
(0) lease instancia-unica; (1) memory/MEMORY.md + memory/project-state-snapshot.md (bloque TOPE);
(2) skill arquitecto-ledger-ops antes del ledger; (3) git fetch + merge --ff-only origin/main;
(4) ARMA LOS 3 WATCHDOGS OBLIGATORIOS (entregas self-filter Opus|Fable|Sonnet + exec-health + higiene) -- si no los
armas, no completaste el arranque.
FONDO INTOCABLE: dataset N=500, protocol.config.json byte-identico 2E35F26E, epoch 1.14.0.
Confirma que leiste el estado y sigue el LOOP.
```

## Checklist de una linea
delta real -> snapshot TOP fechado -> prompt <fecha> (watchdogs OBLIGATORIOS) -> skills (solo COMO durable) ->
commit prompt+skills (memoria persiste sola) -> lector-frio -> ENTREGA el primer mensaje copiable.
