# VEREDICTO TASK-0344 -- la poda de mailbox y su caso de prueba discrepan

Revisor: Analista (voz adversarial independiente). Emitido 2026-08-10 11:26 hora local (UTC+2).

Recomendacion de cierre: **OK-CLOSABLE**.

## Ancla canonica

    ancla juzgada       6fb4ea952b7de4d96a8b87ea212a12367da794a9  (la que cita el encargo)
    HEAD / origin/main  0d143f3bd78b7feef98ba90b6aa1bb02b9ba4e59
    rutas en alcance    identicas entre 6fb4ea95 y 0d143f3b (diff vacio, verificado)
    clon limpio         D:/Aegis_Scratch/multi_agent_project_protocol/rev0344-analista/clone
    arbol del clon      git status --short vacio
    entrega juzgada     dc34ca39 (fix) + 205eea94 (entrega); diagnostico en
                        personal/Codex/DIAG-TASK-0344-before-fix-20260808.md

El diff de `6fb4ea95..0d143f3b` sobre `examples/mailbox_status_cases/`,
`scripts/prune_state.py` y el registro de contratos es **vacio**: lo juzgado en el ancla
describe tambien el HEAD de hoy.

## Reproduccion (clon limpio, gate por exit code)

    python examples/mailbox_status_cases/run_mailbox_status_cases.py   exit 0
        OK: mailbox status cases passed (5, including prune archive mutation).
    python scripts/prune_state.py --root . --check                     exit 0
        OK: prune not due (cold_start_tokens=15468).
    python scripts/validate_collaboration_state.py --root .            exit 0
        OK: collaboration state is valid.
    python scripts/scan_encoding.py --root .                           exit 0
    python scripts/scan_domain_neutrality.py --root .                  exit 0
    python scripts/check_falsification_contracts.py --root .           exit 0
        DECLARED NEG-MAILBOX-PRUNE-MUST-ARCHIVE boundaries=3
        runner=examples\mailbox_status_cases\run_mailbox_status_cases.py
    python examples/scratch_discipline_cases/run_scratch_discipline_cases.py
        --scratch-root D:/Aegis_Scratch                                exit 0

Los tres comandos del `verification_cmd` de la tarea salen verdes, y tambien los escaneos de
codificacion y neutralidad y el inventario de contratos.

## La pregunta central: se arreglo el lado correcto, y se acredita por medicion?

**Si, y lo he reproducido por mi cuenta sin apoyarme en el diagnostico del maker.**

Construi la fixture exacta dos veces, variando UNICAMENTE `cold_start_tokens_hard`, y medi
`assess()`, la rama `requires_unresolved_response()` de cada mensaje y el efecto real de
`prune --apply`:

    PRE-FIX (cold_start_tokens_hard = 999999)
      assess: due=False  reasons=[]  before_tokens=36
      requires_unresolved_response(MSG-001-old.md) = False
      requires_unresolved_response(MSG-002-new.md) = False
      prune --apply exit=0 -> mode=noop, no_op=true, mailbox_archived=0
      archived/MSG-001-old existe = False
      open/MSG-001-old existe     = False   <-- la rama sospechosa NUNCA se ejecuta

    POST-FIX (cold_start_tokens_hard = 0)
      assess: due=True  reasons=['cold_start_tokens 36 >= 0']
      prune --apply exit=0 -> mailbox_archived=1
      archived/MSG-001-old existe   = True
      answered/MSG-002-new sigue ahi = True   <-- keep_recent=1 se respeta en la corrida real

Dos consecuencias, ambas falsables:

1. **La hipotesis del enunciado de la tarea queda refutada por medicion.** El contrato de
   TASK-0344 y el GO culpaban a la rama `requires_unresolved_response` de `prune_mailbox`.
   Los dos mensajes de la fixture llevan `requires_response: false`, la rama devuelve `False`
   para ambos y `open/MSG-001-old` no llega a existir: esa rama no participa en el fallo. El
   fallo ocurria **antes**, en el guard de `apply_prune`. El maker no acepto el encuadre del
   encargo; midio y lo corrigio, que es exactamente lo que pedia el AC1.

2. **Produccion tiene razon y la fixture quedo obsoleta.** `scripts/prune_state.py` no aparece
   en el diff de la entrega (`dc34ca39` toca el runner, no produccion).

**La cita causal tambien la abri, no la di por buena.** El handoff atribuye el cambio de
comportamiento a TASK-0273, commit `3062214d`. `git show 3062214d -- scripts/prune_state.py`
muestra precisamente el bloque introducido al principio de `apply_prune`:

    +    assessment = assess(root)
    +    if not assessment.due:
    +        return { "mode": "noop", "no_op": True, ... "mailbox_archived": 0, ... }

La cita es exacta: ese commit, de esa tarea, es el que dejo la fixture sin alcanzar el codigo
que dice ejercitar.

## El AC5 SI se puede acreditar hoy -- el encargo lo daba por bloqueado y no lo esta

El encargo me pedia declarar el AC5 bloqueado por el instrumento (facturacion caida desde el
09-ago). **Abri el run citado en vez de asumirlo, y esta vivo y es legible:**

    gh run view 31267480822 --json conclusion,headSha,status
      conclusion = failure   headSha = b1d7d5bd55baf340b48f81745627cb3a2c592ec7

    job "validate", paso 18 "Run mailbox status validation cases"  = success
    primer rojo del job: paso 24 "Run neutrality scan validation cases"
    job "falsification-runners": rojo en el paso 5 (retry falsification, TASK-0343)

El `failure` global del run NO es de este paso: el paso que exige el AC5 sale **success**, y
los dos rojos del run estan fuera del alcance declarado de TASK-0344 (neutralidad y
TASK-0343). Ademas comprobe que ese verde acredita el arbol que estoy juzgando: el diff de
`b1d7d5bd..6fb4ea95` sobre `examples/mailbox_status_cases/` y `scripts/prune_state.py` es
**vacio**. La cabecera del run corresponde al mismo codigo revisado.

Tampoco hay el hallazgo que me pedias buscar: el maker **no ofrece la corrida local como
sustituto de CI**. Cita el run real de Actions para el AC5 y lista las corridas locales por
separado como evidencia de clon limpio.

## Falsacion: mutar PRODUCCION, no los mutantes del runner

El negativo entregado muta el **sitio de llamada** (`mailbox_moved = prune_mailbox(...)` ->
`mailbox_moved = 0`). Eso ata la llamada, no necesariamente el efecto. Escribi mis propios
mutantes contra el **cuerpo** de `prune_mailbox` en el clon limpio y corri el runner entregado
contra cada uno:

    MUTANTE (produccion)                                         runner   resultado
    M1  move = []                (neutraliza el efecto,          exit 1   KILLED
        dejando la llamada intacta)                                       assert archived.exists()
    M2  move = eligible          (ignora keep_recent,            exit 0   *** SOBREVIVE ***
        archiva TAMBIEN el reciente)
    M3  set_mailbox_status(...) -> pass  (mueve sin normalizar)  exit 1   KILLED
                                                                          assert "status: archived" in ...
    M4  target = open_dir / name (destino equivocado)            exit 1   KILLED
    M5  requires_unresolved_response -> True siempre             exit 1   KILLED
    M6  requires_unresolved_response -> False siempre            exit 0   *** SOBREVIVE ***
    restauracion de produccion + runner                          exit 0   (control)

Cuatro de seis mutantes de produccion mueren, incluidos los dos que importan para el AC3: el
runner cae si la poda **deja de archivar lo que debe archivar**, tanto si se borra la llamada
como si se neutraliza el efecto dejandola en pie. La garantia esta atada al efecto, no al
helper.

**Y el negativo entregado no es verde por construccion.** Este era mi sospecha principal: el
bloque del mutante copia `scripts/` y `runtime/` a un temporal y corre con `cwd=temp`; si en
ese entorno copiado no se archivara nada **aunque no hubiera mutacion**, el
`assert not mutant_archived.exists()` seria vacuo. Replique el bloque verbatim con la mutacion
apagada:

    A: mutacion OFF (control)  exit=0  mode=apply  mailbox_archived=1  archived existe = True
    B: mutacion ON (entregado) exit=0  mode=apply  mailbox_archived=0  archived existe = False

El entorno copiado SI archiva cuando produccion esta intacta. El negativo discrimina de verdad.

## Tabla vector por vector

| AC | Que exige | Veredicto | Evidencia |
|----|-----------|-----------|-----------|
| AC1 | diagnostico medido ANTES del arreglo, declarando por que rama pasa cada mensaje y que lado esta mal | PASS (con residual R3) | DIAG committeado; contenido reproducido de forma independiente: `due=False/reasons=[]/mode=noop`, `requires_unresolved_response=False` en ambos, `open/` vacio |
| AC2 | arreglar el lado que esta mal y declarar que cambio lo dejo obsoleto y en que tarea | PASS | `scripts/prune_state.py` intacto en el diff; TASK-0273 / `3062214d` verificado abriendo el commit: introduce el guard `if not assessment.due: return noop` |
| AC3 | runner exit 0 y falsado que cae si la poda deja de archivar | PASS (con residuales R1, R2) | runner exit 0; M1/M3/M4/M5 mueren; negativo entregado no vacuo (control archiva 1) |
| AC4 | declarar que el runner no esta en ningun verification_cmd y proponer donde deberia estar | PASS (con residual R4) | handoff mide en `b726cce3^` que ningun task file lo contenia y propone la linea; el propio `verification_cmd` de TASK-0344 ya lo incluye |
| AC5 | paso verde en un run REAL de Actions, citando su id | PASS | run 31267480822, job `validate`, paso 18 `success`, headSha `b1d7d5bd`; rutas en alcance identicas `b1d7d5bd..6fb4ea95` |
| AC6 | poda real sigue funcionando y gates verdes en clon limpio | PASS | `prune --check` exit 0; validate/encoding/neutralidad/contratos exit 0; arbol del clon vacio |

## Residuales declarados (ninguno bloquea el cierre)

**R1 -- la direccion contraria no esta cubierta: sobre-archivar sobrevive.** M2 (`move = eligible`,
ignorando `keep_recent`) archiva **los dos** mensajes y el runner sale verde. Nada asegura que
`MSG-002-new.md` siga en `answered/`, y `mailbox_keep_recent: 1` es literalmente la configuracion
que define la fixture. El AC3 solo pide la direccion "deja de archivar", asi que la entrega cumple
la letra; pero el limite `keep_recent` queda sin atar. Reparacion falsable en una linea:
`assert (fixture / "Area_comun/mailbox/answered/MSG-002-new.md").exists()` en el caso positivo. La
corri en las dos direcciones antes de proponerla:

    assercion propuesta + produccion INTACTA   runner exit 0  (sigue verde, no es falso positivo)
    assercion propuesta + M2 (sobre-archiva)   runner exit 1  (ahora si muere)

Sugiero tarea de seguimiento, no vuelta de esta.

**R2 -- la rama de reapertura no tiene caso positivo.** M6 (`requires_unresolved_response` siempre
`False`, es decir correo sin responder que se archiva en vez de volver a `open/`) sobrevive. La
rama solo esta cubierta en un sentido (M5 muere porque desvia de mas). Fuera del alcance de los AC
de TASK-0344; va al mismo seguimiento que R1.

**R3 -- el orden "antes de tocar nada" del AC1 esta atestiguado, no evidenciado.** El diagnostico y
el arreglo entran en el MISMO commit `dc34ca39`, asi que el ledger no distingue si el DIAG se
escribio antes o despues. Lo doy por bueno porque he reproducido su contenido y es correcto, y
porque la conclusion contradice la hipotesis del encargo -- algo que no se escribe a posteriori
para justificar un arreglo comodo. Para futuras tareas con un AC de orden temporal, el DIAG
deberia ir en un commit propio anterior.

**R4 -- la propuesta del AC4 es prosa en area personal, no cableado.** Vive en
`personal/Codex/HANDOFF-TASK-0344-20260808.md`, que no es documento gobernado: nada impide que el
siguiente cambio de `prune_mailbox` vuelva a entregarse sin correr este runner. Es el defecto
sistemico que ya esta contado en TASK-0346 (35 de 66 runners de CI fuera de todo `verification_cmd`),
no una deuda que deba pagar esta entrega.

**R5 -- el negativo se ancla a una linea literal de produccion.** `prune_source.replace('    mailbox_moved = prune_mailbox(root, int(cfg["mailbox_keep_recent"]))', ...)`
se rompe con un simple reformateo. Falla **ruidosamente** (`assert mutant_source != prune_source`),
no en silencio, asi que es fragil pero no falso-verde. Mis mutantes M1/M3/M4 muestran que la
garantia sobrevive al cambio de coordenada aunque el negativo declarado no.

**R6 -- nota de convencion, no defecto de la entrega.** `scratch_parent()` deriva el paraguas de
scratch de la letra de unidad del checkout (`{ROOT.drive}/Aegis_Scratch/<repo>/<proposito>`) y deja
el directorio padre creado y vacio al terminar. Lo mire como posible violacion de DECISION-0104 y
**no lo es de esta entrega**: es la convencion que define el propio nucleo
(`scripts/new_instance.py`: "per-disk umbrella, `<drive of target>/Aegis_Scratch/<project_name>/`
en Windows, `~/Aegis_Scratch/<project_name>/` fuera"), identica en forma a
`examples/encoding_gate_cases/run_encoding_gate_cases.py`. Los casos del detector de disciplina de
scratch salen exit 0. Si el paraguas por-disco incomoda, es debate de convencion en el nucleo, no
correccion de TASK-0344.

## Lo que NO he verificado

- El resto del run 31267480822 (neutralidad, TASK-0343): fuera de alcance declarado.
- Producto: el encargo declara **sin producto en alcance**; no corri nada de Zeus ni npm.
- El validador PowerShell dentro del runner solo corre si hay `pwsh`/`powershell` en PATH; en mi
  corrida estaba disponible y el runner no reporto discrepancia, pero no lo aisle como gate propio.

## Recomendacion

**OK-CLOSABLE.** Los seis AC pasan, incluido el AC5 que el encargo daba por bloqueado. El arreglo
esta en el lado correcto, la eleccion de lado esta medida y no argumentada, la cita causal
(TASK-0273 / `3062214d`) resiste que se abra el commit, y la garantia sobrevive a mutantes de
produccion que el negativo entregado no contempla.

Lo unico que pediria enrutar aparte, sin retener este cierre, es una tarea con R1 y R2: el limite
`keep_recent` y la rama de reapertura son las dos mitades que hoy pueden romperse con el gate en
verde.

-- Analista
