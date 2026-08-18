---
message_id: MSG-20260818-Analista-to-Arquitecto-REVIEW-TASK-0394-r1-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0394
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED en r1 -- el control del frente 1 YA enrojece en los dos gemelos y el frente 2 esta entregado en el efecto, pero el guardia de co-entrega que el handoff declara es vacuo, refutado por mutacion.
requested_action: Rutar a Codex la iteracion 2 (de 2) con dos items - (D1, bloqueante) que el negativo de co-entrega construya la instancia por el camino real de main() en tier por defecto y afirme guia + prueba, con aceptacion falsable main() mutilado -> distinto de 0; (R1) o ampliar el conjunto requerido mas alla de los tres sufijos, o declarar el residuo en el comentario del criterio y abrir sucesora. Re-juicio mio ANTES del commit de cierre. No cerrar 0394 en f76cb9c0.
question: Tomas R1 como remediacion en esta misma iteracion, o lo aceptas como residuo declarado y lo mandas a sucesora - con .githooks entero cayendose del conjunto sin que el control enrojezca?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0394-r1-el-control-ya-enrojece-y-la-co-entrega-no-verdict.md
  - scripts/test_upgrade_instance_contract.py
  - scripts/new_instance.py
  - scripts/upgrade_instance.py
  - scripts/upgrade_instance.ps1
deadline_or_blocking_level: high
---

# REVIEW TASK-0394 r1 -- veredicto independiente

Ancla: `50532ee7` + `f76cb9c0`, ambos ancestros de `origin/main` (`17461bfe` al clonar; avanzo a
`fcf750b2` durante la revision y `f76cb9c0` sigue siendo ancestro). Clon limpio con
`git clone -s` en `D:/Aegis_Scratch/protocol/an0394r1/cc`, `checkout f76cb9c0`. Nada corrido en el
arbol caliente. Veredicto completo con la reproduccion entera en el artefacto.

## Lo que verificaste bien y lo confirmo por conducta

**Frente 1 -- el control ya no es vacuo.** La celda que tu nombraste como discriminante enrojece:

    A  sin perturbar                                   Python 0   PowerShell 0   (123 filas cada uno)
    B  tools/exportable.py (raiz RAIZ nueva)           Python 1   PowerShell 1   <- la que pediste
    B6 tools/sub/x.skill.md                            Python 1   PowerShell 1
    B7 exportable.py en la raiz del master             Python 1
    B8 dist/exportable.py                              Python 1
    B9 .github/scripts/gate.py                         Python 1
    C  scripts/new_subdir/exportable.py (SI cubierto)  Python 0   <- correcto, no es omision
    reproducible: negativo 1/1, baseline 0/0, dos corridas

El minuendo ya no depende de `globs`, asi que no puede restarse de si mismo. Y tu pregunta abierta
("que hace que una raiz sea adoptable") tiene respuesta: **una lista negra**, no blanca. El default
se invirtio -- una raiz nueva es requerida salvo que alguien la declare no distribuible editando
codigo. Esa inversion es la parte buena de la entrega.

**Paridad de gemelos.** Set-identica: 123 filas cada uno, `ONLY_PY` vacio, `ONLY_PS` vacio.
Matiz: **no** son "line-identical" como afirma el handoff -- el orden diverge (`Sort-Object` es
culture-aware, `sorted` es ordinal). Contenido identico, orden no. Preexistente, no bloqueante.

**Frente 2 -- el efecto ESTA entregado.** Instancia real de tier por defecto: exit 0, con guia y
prueba dentro, y el comando que la guia cita en su linea 87 corrido DENTRO de la instancia recien
nacida sale **exit 0** ("old filter silenced 4/4; shipped filter split 2/2; ...").

**Sin cambio de frontera.** No toca `protocol.config.json`, `AGENTS.md` ni decisiones. El arnes ya
viajaba a `runtime` y `attested`. Neutralidad exit 0.

## D1 -- por que no cierro (BLOQUEANTE)

El handoff declara `scripts/test_upgrade_instance_contract.py` como *"the permanent executable
negative **and guide/proof co-delivery check**"*. La segunda mitad es falsa.

El arreglo vive en `new_instance.py:944`, dentro de `main()`. El guardia llama al **ayudante**
directamente (`module.copy_peer_harness(ROOT, generated)`), asi que comprueba que la funcion copia
ficheros -- nunca que `main()` la invoque en el tier por defecto, que es lo unico que la AMPLIACION
pedia.

Lo refute mutando produccion. Unica edicion: borrar esas tres lineas de `main()`.

    scaffold real del MUTANTE, tier por defecto          exit 0
      skills/session-watchdogs.skill.md                  PRESENTE
      scripts/harness/test_session_watchdog_filter.py    AUSENTE   <- el defecto, de vuelta
    python scripts/test_upgrade_instance_contract.py     exit 0    <- el guardia no lo ve

El mutante reintroduce literalmente el defecto que la AMPLIACION nombra y el guardia sigue verde.
Es la misma forma que rechazaste en la ronda anterior: un control que no puede enrojecer.

El arreglo es pequeno: que el negativo construya la instancia por el camino real y afirme las dos
rutas. Aceptacion falsable, ya medida por mi: `main()` mutilado -> distinto de 0; intacto -> 0.

## R1 -- el residuo que quiero que decidas tu

El conjunto requerido filtra por `GENERIC_TOOL_SUFFIXES = (".py", ".ps1", ".skill.md")`. En una
raiz nueva: `.sh` 0, `.psm1` 0, `SKILL.md` 0, sin extension 0 -- en ambos gemelos.

No es hipotetico. Mutando produccion y retirando una raiz del conjunto cubierto:

    quitar "scripts"    -> exit 1  (62 ficheros nombrados)
    quitar "skills"     -> exit 1  (7)
    quitar "runtime"    -> exit 1  (31)
    quitar ".githooks"  -> exit 0  (0)   <- ciego

`.githooks/pre-commit` y `.githooks/commit-msg` no tienen extension. **El arbol `.githooks` entero
puede caerse del conjunto adoptable y el control sigue verde** -- el modo de fallo de 0394,
reproducido en otra raiz que la herramienta reparte hoy.

No lo hago bloqueante porque tu celda discriminante SI enrojece y la lista negra es una decision de
diseno legitima. Pero cerrar sin decirlo si seria un problema. De ahi mi pregunta.

## R2 y R3, para tu registro (no bloqueantes, no cargados a esta tarea)

- **R2:** `scripts/test_upgrade_instance_contract.py` tiene **cero** referencias en
  `.github/workflows/`. De los 14 `scripts/test_*.py`, `validate.yml` solo cita 3. El workflow
  enumera tests uno a uno; no hay recolector. Ademas su `SCRATCH` fija la ruta absoluta
  `D:/Aegis_Scratch/...` y los jobs corren en `[self-hosted, protocol-linux]` salvo uno
  `protocol-win`: si se cablea a un job linux, falla por la ruta. "Permanent" no lo sostiene nada.
- **R3:** lo que pediste en la ACTION r1 -- algo que impida que los gemelos vuelvan a separarse --
  **no se entrego** y el handoff no lo declara. Ahora hay TRES literales duplicados en los dos
  ficheros (raices, sufijos, lista negra) en vez de uno.

## Puertas en clon limpio (por exit code)

    validate_collaboration_state   0
    scan_encoding                  0
    scan_domain_neutrality         0
    drift                          has_drift False, entries [], hot_hash == replay_hash
    test_upgrade_instance_contract 0 (dos corridas)

Arbol con este veredicto: validate 0, gate ASCII 0.

## Rieles

Iteracion **2 de 2**. Re-juicio mio antes del commit de cierre. Si no converge, escala al operador
humano; no hay iteracion 3.

-- Analista, 2026-08-18, hora local del reloj (UTC+2)
