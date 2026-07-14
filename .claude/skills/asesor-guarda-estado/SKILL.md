---
name: asesor-guarda-estado
description: >-
  Checkpoint de cierre del ASESOR: cuando el operador dice "guarda estado" (o "guarda el estado",
  "cierra sesion", "deja listo para la proxima", "checkpoint", "haz el handoff", "actualiza la memoria"),
  persiste TODO lo que se esta haciendo y COMO se hace, para que una sesion fria del Asesor retome
  exactamente donde quedo, y al final ENTREGA el PRIMER MENSAJE de inicio de la proxima sesion (compacto,
  apuntando al prompt guardado). Actualiza: (1) el snapshot canonico personal/asesor/ESTADO-asesor.md
  (bloque TOPE fechado, supersede lo de abajo), (2) el prompt de arranque personal/asesor/PROMPT-INICIO-ASESOR.md
  (nueva version, supersede la anterior; auto-poll + re-armar monitor como paso OBLIGATORIO), (3) la memoria
  .claude (memory/*.md + MEMORY.md), (4) las skills cuyo PROCEDIMIENTO cambio. Frontera dura: SOLO archivos de
  memoria/personales(asesor)/skills; NUNCA ledger, estado gobernado, claims ni el area de otro agente.
  Complementa la skill global session-checkpoint con la salida del primer-mensaje y la especificidad del Asesor
  (canal mailbox firmado Operador, gate ASCII, pathspec en arbol compartido, trailers OPCION A). Es el espejo de
  arquitecto-guarda-estado para el rol Asesor. Trigger words: guarda estado, guarda el estado, guardar estado,
  cierra sesion, checkpoint, handoff, deja listo para la proxima, prompt de inicio, actualiza la memoria.
---

# Asesor -- guarda estado (checkpoint + primer mensaje de inicio)

> Las sesiones mueren sin avisar (contexto, cierre, reinicio). Todo lo que solo vive en el chat se pierde.
> Este checkpoint hace que el conocimiento del ASESOR sobreviva a la sesion Y entrega el mensaje que el operador
> pega para arrancar la proxima. Prueba de calidad: el TEST DEL LECTOR FRIO -- alguien sin este chat retoma
> manana con solo los archivos que dejas. Es el espejo de `arquitecto-guarda-estado`, para el rol Asesor.

## Frontera dura (identidad del Asesor)
El Asesor es participante NO-FIRMANTE (DECISION-0086): cero capabilities de ledger, canal = mailbox firmado
Operador, area `personal/asesor/`. El checkpoint escribe SOLO: la memoria del harness (`memory/*.md`), el area
`personal/asesor/`, y las skills del proyecto (`.claude/skills/`). **NUNCA** toca el ledger, `Area_comun/state/*`,
claims, el area de otro agente (`personal/Arquitecto/` etc.), ni rutas gobernadas. El checkpoint es del agente, no
es gobernanza. La memoria vive en el dir del harness (NO se commitea al repo, persiste sola); el prompt y las
skills SI se commitean al repo (pathspec explicito + gate ASCII + trailers OPCION A).

## Procedimiento

### Paso 0 - Reune el delta REAL (verifica, no asumas)
Auto-poll: `git fetch` + `git pull --ff-only origin/main`; luego captura el estado real:
- `git log --oneline -20` (delta de la sesion) + `git rev-parse --short HEAD` (= origin?).
- Mailbox: `ls Area_comun/mailbox/open/` -- que quedo vivo (esperando MI respuesta o la del Arquitecto) vs consumido.
- Gates de higiene: `validate_collaboration_state.py`/scan si aplica; sha8 de `protocol.config.json`
  (FONDO INTOCABLE del hub = 2E35F26E, epoch 1.14.0). Cross-atestacion/epoca de Aegis si hubo movimiento.
- Trabajo en vuelo: que espera respuesta de quien (yo->Arquitecto o Arquitecto->yo), DECISIONes nuevas, hora UTC.
- Feedback/correcciones del operador de la sesion (oro: cambian el COMO, no solo el QUE).

### Paso 1 - Actualiza el snapshot canonico (ESTADO-asesor.md)
- Anade/reemplaza el bloque TOPE de `personal/asesor/ESTADO-asesor.md` con un header nuevo fechado (marca que
  SUPERSEDE lo de abajo) que capture: HEAD/gates/config, foco actual, trabajo en vuelo con DUENO y estado, lo que
  espera respuesta de quien, decisiones nuevas y su porque, y la SIGUIENTE accion concreta. Corrige hechos
  obsoletos (un snapshot viejo que contradice la realidad es peor que nada). El detalle inferior queda como historia.

### Paso 2 - Regenera el prompt de arranque (PROMPT-INICIO-ASESOR.md)
- Reescribe `personal/asesor/PROMPT-INICIO-ASESOR.md` con el estado REAL verificado (no lo que el plan decia).
  Sube la version en el header (vN -> vN+1) y marca la anterior como SUPERADA (no borres el historico si es util).
- El COLD-START DEBE incluir, como PASO OBLIGATORIO NO-SALTABLE: (a) leer ESTADO-asesor.md (bloque TOPE) +
  la memoria .claude; (b) **AUTO-POLL** (git fetch/pull, git log, ls open/) = red primaria; (c) **RE-ARMAR EL
  MONITOR** sobre origin/main con self-filter **SOLO por `Ops-Reason: coordinacion-asesor`** (mi marcador
  inequivoco) = respaldo. **NO filtres por `Co-Authored-By` / modelo (Opus|Fable): el Arquitecto TAMBIEN corre
  esos modelos y ese filtro lo CEGABA a sus commits (leccion 14-jul).** (d) verificar ledger limpio antes de
  commitear. Redactalo con la frase "si no haces el auto-poll y no re-armas el monitor, no has completado el arranque".
- Captura el COMO (no solo el QUE), reglas duras del Asesor: canal = SOLO mailbox firmado Operador (NUNCA
  submit_intent); GATE ASCII pre-commit bloqueante (aborta si bytes>127; acentos/em-dash son mi vicio);
  PATHSPEC en el commit (arbol compartido con el Arquitecto: `git commit -- <pathspec>`, NUNCA `git add`+commit
  pelado; ventana segura si hay peer-state a medio escribir en state/decisions); trailers OPCION A
  (`Task-Id: none` + `Ops-Reason: coordinacion-asesor-mailbox: ...` <=120 chars + Co-Authored-By, sin blank line
  entre trailers); heredoc bash (`git commit -F -`), NUNCA `@'...'@` (es PowerShell, mete `@` literal); debate =
  drafts en mi area, NO rutear/sellar hasta orden explicita; proactividad sin preguntar (preparo el siguiente
  entregable). Verificar POST-commit con `git show -s --format=%B` antes del push.

### Paso 3 - Actualiza la memoria .claude + skills (solo el COMO durable)
- Actualiza `memory/*.md` con hechos durables verificados (no anecdotas/pids/fechas efimeras) + `memory/MEMORY.md`
  si hay entrada nueva que indexar. SI un procedimiento durable cambio, incorporalo a la skill correspondiente.
- Si el harness bloquea la auto-edicion de una skill, deja el texto propuesto en `personal/asesor/` y avisa al operador.

### Paso 4 - Commit (repo) + memoria (harness)
- Commit atomico al repo con PATHSPEC EXPLICITO del prompt + ESTADO + las skills cambiadas. Gate ASCII bloqueante
  ANTES. Trailers: `Task-Id: none` + `Ops-Reason: coordinacion-asesor-mailbox: checkpoint de sesion` en el bloque
  final junto a `Co-Authored-By` (sin blank line). Push si verde (verifica POST-commit). La memoria (dir del
  harness) persiste sola, NO se commitea.

### Paso 5 - Auto-test del lector frio
Releete y responde honesto: (1) se entiende QUE y POR QUE? (2) esta clara la SIGUIENTE accion? (3) el trabajo en
vuelo tiene dueno y estado (yo<->Arquitecto)? (4) algo importante quedo solo en el chat? Si algo falla, completalo
antes de cerrar.

### Paso 6 - ENTREGA EL PRIMER MENSAJE DE INICIO (la salida al operador)
Emite, en un bloque copiable, el PRIMER MENSAJE compacto que el operador pegara para arrancar la proxima sesion.
NO repitas el prompt entero (ya esta guardado); el primer mensaje solo APUNTA a el y exige el arranque. Plantilla
(rellena <vN> con la version del prompt que acabas de escribir):

```
Eres mi ASESOR (no el Arquitecto -- corre en otra sesion). Proyecto:
D:\Agentes\multi_agent_project_protocol.
LEE Y EJECUTA el arranque completo de personal/asesor/PROMPT-INICIO-ASESOR.md (<vN>):
(1) ESTADO-asesor.md bloque TOPE + memoria .claude; (2) AUTO-POLL (git fetch/pull, git log, ls open/) = red
primaria; (3) RE-ARMA EL MONITOR con self-filter SOLO por Ops-Reason coordinacion-asesor (NO por modelo Opus|Fable);
(4) verifica ledger limpio antes de commitear. Canal = SOLO mailbox firmado Operador (NUNCA submit_intent);
gate ASCII + pathspec + trailers OPCION A. Si no haces el auto-poll y no re-armas el monitor, no completaste el arranque.
Confirma que leiste el estado + responde lo que este esperando en open/, y continua con el bloque vigente.
```

## Checklist de una linea
delta real (auto-poll) -> ESTADO-asesor TOP fechado -> PROMPT-INICIO vN+1 (auto-poll + monitor OBLIGATORIOS) ->
memoria/skills (solo COMO durable) -> commit ESTADO+prompt+skills con pathspec+ASCII+trailers (memoria persiste
sola) -> lector-frio -> ENTREGA el primer mensaje copiable.
