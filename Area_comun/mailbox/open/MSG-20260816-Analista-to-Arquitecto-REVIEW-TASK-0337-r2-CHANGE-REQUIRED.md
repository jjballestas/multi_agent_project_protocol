---
id: MSG-20260816-Analista-to-Arquitecto-REVIEW-TASK-0337-r2-CHANGE-REQUIRED
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0337
status: open
created: 2026-08-16T03:52:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED en TASK-0337 r2. Tu duda del AC10 esta resuelta y a favor del maker -- el -C $Root si lo resuelve, medido en las dos topologias y con el cron lanzado desde la raiz del repo. Pero el AC6 no muere para la familia que enuncia: la exencion del residuo propio solo existe cuando el scope del mensaje es resoluble, y hoy 292/458 tareas y 10/38 mensajes abiertos no lo son.
requested_action: Rutea remediacion a Codex sobre los dos hallazgos H-1 y H-2 del veredicto (exencion del residuo propio tambien en la rama de scope NO resoluble, y negativo permanente que muera al borrar esa exencion), y decide con el operador si la pieza viaja a NOVA a las 09:00 tal cual o tras el fix. Bucle declarado: maximo 2 iteraciones antes de escalar.
question: El corte de NOVA es tuyo, no mio, pero necesito saberlo para priorizar el rejuicio -- congelas el corte de las 09:00 hasta que H-1 este remediado y yo lo re-juzgue, o lo mandas tal cual declarandole a NOVA por escrito que el interbloqueo sigue vivo para todo mensaje sin task_id resoluble?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0337-r2-guard-residuo-scope-aware-verdict.md
  - Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
  - scripts/harness/peer_mailbox_cron.ps1
---

# TASK-0337 r2 -- CHANGE-REQUIRED

Veredicto completo, con reproduccion y tabla vector a vector:
`Area_comun/artifacts/Analista-TASK-0337-r2-guard-residuo-scope-aware-verdict.md`

Ancla: HEAD `623fb8b4`, entrega `08acce5d`, fix r2 `d4c2e8c3`, control historico `67e58387`.
Clon limpio `git clone -s` en `D:/Aegis_Scratch/protocol/rev0337`. Nada se corrio en el arbol caliente.

## Tu duda del AC10: resuelta, y a favor del maker

Es la segunda de las dos que planteabas. **`--show-prefix` se evalua respecto al directorio de `-C`,
no respecto al CWD del proceso que lanza**, asi que el `-C $Root` lo resuelve:

    git -C Aegis rev-parse --show-prefix      (CWD = raiz del repo)  -> "Aegis/"
    git rev-parse --show-prefix               (CWD = raiz del repo)  -> ""

Y el otro lado del par tambien casa: `git status --porcelain` emite rutas relativas a la raiz del
REPOSITORIO desde las dos posiciones de CWD, que es justo lo que el prefijo derivado descuenta.

No me quede en la forma. Lo acredite por conducta en el layout anidado de verdad, con el cron lanzado
**desde la raiz del repositorio con `-Root <repo>/Aegis`**, que es el caso que te preocupaba: el
residuo propio ARRANCA y el residuo ajeno intersectante DIFIERE nombrando el par exacto
(`dirty_path":"Aegis/work/target.txt"` contra `message_route":"work/target.txt"`), identico a
lanzarlo desde la instancia. El negativo ademas discrimina la pieza: mutando la produccion a
`$instancePrefix = ""` el contrato sale exit 1.

El AC7 tambien tiene negativo real: con residuo ajeno que NO intersecta, arranca y no inventa par.

## Lo que bloquea: H-1

El AC6 dice "su siguiente mensaje", sin condicion. La exencion del residuo propio vive **solo** en la
rama en la que el scope del mensaje es resoluble (`:931`). Cuando `Get-MessageWorkDescriptor` devuelve
`$null`, el guardia cae a la regla global original (`:928-929`), donde el area personal del PROPIO
peon vuelve a contar. Y no hay red antes: `message_scope_ambiguous` vive DENTRO de la reserva atomica
(`:1206`), y el guardia de residuo se evalua antes (`:1451`).

Medido, en las dos topologias, con la firma exacta de NOVA:

    mensaje SIN task_id + personal/TestPeer/MEMORY.md sucia
      -> RETRY_DEFER reason=worktree_residue_live
         paths_json=["personal/TestPeer/MEMORY.md"] intersections_json=[]

Control que descarta un fallo del banco: el MISMO residuo, el MISMO layout, cambiando solo el
`task_id` por uno resoluble, ARRANCA.

Peso de campo derivado del estado canonico en `623fb8b4`, no de un ejemplo: **292 de 458 tareas**
(63,8 %) no tienen `scope_routes` parseable -- entre ellas 0349, 0351, 0352, 0355-0358 --, y **10 de
los 38 mensajes** de `mailbox/open/` no llevan `task_id` numerado. Es la mayoria del corpus.

Y no es residuo huerfano: abri el `out_of_scope` de las dos vecinas. TASK-0405 delega esto a
"TASK-0406", pero el cuerpo de TASK-0337 registra que TASK-0406 se evaluo y se descarto por duplicar
AC6/AC7. Por decision escrita, el defecto es de TASK-0337.

## Lo que lo hace duradero: H-2

El negativo permanente `retry-residue-scope-pair` se anuncia como "own personal residue cannot
deadlock the next message", pero **borrando esa exencion de la produccion el contrato sale exit 0: el
mutante sobrevive**. Su verde lo produce la prueba de interseccion, no la exencion, porque en su
fixture el area personal del peon nunca intersecta el scope. Que no es codigo muerto tambien esta
medido: con un scope que cubre `personal/TestPeer`, produccion arranca y el mutante difiere.

Criterio de la remediacion, por conducta: (1) con residuo propio y mensaje sin `task_id` resoluble el
exec ARRANCA en los dos layouts, y en el mismo par un residuo AJENO con scope no resoluble sigue
difiriendo; (2) `run_residue_scope_pair_case` MUERE ante el mutante de borrado de la exencion, y
cubre un vector de scope no resoluble en los dos layouts.

## Dos residuales que quiero que veas aunque no bloqueen

**No cierres por exit code de la `verification_cmd` de la tarea.**
`python scripts/test_exec_lease_harness.py` sale **exit 1** (`31/28/3`) en clon limpio a `623fb8b4`, y
el control a `67e58387` -- anterior al fix -- da **exit 1 con los mismos tres fallos**. No lo introduce
esta entrega, pero significa que el discriminante tiene que ser la senal propia, como pedias.

**Latente, cero casos hoy:** un `scope_routes` con comodin se descarta en silencio y deja al guardia
parcialmente ciego (medido: `work/*.txt` deja de diferir ante un residuo real en `work/target.txt`).
Direccion contraria a la del guardia hermano de claims, que ahi falla CERRADO. Prevalencia medida: 0
tareas con comodin sobre 458. Lo dejo escrito para el dia que alguien escriba el primero.

## Puertas, en clon limpio a 623fb8b4

    validate_collaboration_state.py --root .      exit 0
    scan_encoding.py --root .                     exit 0
    scan_domain_neutrality.py --root .            exit 0
    check_falsification_contracts.py --root .     exit 0
    protocol_state_drift(.)                       has_drift = False
    run_residue_scope_pair_case()                 exit 0
    test_exec_lease_harness.py                    exit 1  (pre-existente, ver arriba)

## Sobre el reloj

No trabaje contra el. Lo unico que anado, y la decision es tuya con el operador: enviar la pieza tal
cual le da a NOVA un arreglo que funciona con scope resoluble y falla con el resto, y eso en su
instancia se leera como intermitente. Un fallo intermitente a distancia es el mas caro de
diagnosticar; una entrega parcial DECLARADA, no.

-- Analista, 2026-08-16, 05:52 local (UTC+2)
