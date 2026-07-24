# Analista verdict -- TASK-0256 remediacion iter1 (SLIP-1: colision del token "worker")

- Reviewer: Analista (independent adversarial checker; maker != checker).
- Verdict: **OK-CLOSABLE (GO)** -- SLIP-1 CERRADO por comportamiento. Sin regresion. 3 residuales
  NUEVOS declarados, ninguno bloqueante (dos de ellos corrigen/afinan mi propio veredicto anterior).
- Emitted: 2026-07-24 04:13 local (UTC+0200).
- Supersede: `Analista-TASK-0256-roster-policy-born-operational-verdict.md` (CHANGE-REQUIRED) en lo
  relativo a SLIP-1; sus residuales RES-1..RES-4 siguen vivos y NO bloqueantes.

## Canonical anchor

- Repo bajo revision: multi_agent_project_protocol (hub de protocolo).
  **SIN producto en alcance -- no se corrio ningun npm test de producto.**
- Commit de remediacion: `26995a6` (Codex, "fix: disambiguate worker registry tier").
- La instruccion cita HEAD `0802ffa`; el `origin/main` real al momento del juicio es **`356ac5d`**
  (0802ffa + el commit de coordinacion que me rutea este re-juicio). Verifique que entre `0802ffa` y
  `356ac5d` no hay ningun cambio del texto revisado: el diff no-ledger `377bb20..356ac5d` es
  **exactamente `AGENTS.template.md` 3/0**. Anclo en `356ac5d` (mas conservador).
- Method: **CLON LIMPIO** de origin/main en `/d/ccv256r1`, `checkout 356ac5d`, gates corridos ALLI por
  EXIT code. Comportamiento probado por el ENTRYPOINT REAL (`scripts/new_instance.py`) generando
  instancias temporales en los **tres** tiers. Nada corrido in-place; ninguna instancia viva tocada.

## El fix auditado (no confiado)

`AGENTS.template.md` +3/-0: antes de la lista numerada del bloque "Roster policy", dos lineas de
aclaracion mas una linea en blanco:

```
This policy governs agent participants that execute code. It does not alter the human owner's
approval authority or redefine the registry's `signer`/`worker` key-possession tiers.
```

Las 3 reglas: **byte-identicas**. Prueba: extraje el bloque `Roster policy:`..`## 4.` en `377bb20` y en
`356ac5d`; el diff crudo es solo el +3 (2 lineas + blanco), y el diff tras retirar unicamente las 2
lineas nuevas es **vacio (exit 0)**. Ninguna regla fue reescrita al aplicar el fix.

Es la **opcion B** que yo mismo propuse, con reordenamiento menor de la redaccion (una frase en dos
oraciones en vez de una con punto y coma). Semanticamente equivalente a lo pedido.

## Reproduccion (exit codes reales, clon limpio /d/ccv256r1 @ 356ac5d)

Gates de protocolo, en el clon:

| Gate | Exit | Salida |
|------|------|--------|
| `python scripts/validate_collaboration_state.py` | **0** | "OK: collaboration state is valid." |
| `python scripts/scan_encoding.py` | **0** | "OK: encoding scan is clean." |
| `python scripts/scan_domain_neutrality.py` | **0** | -- |
| `python runtime/protocol_replay.py --check-drift --root .` | **0** | "PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=6334" -> **drift 0** |
| `python scripts/test_attested_instancing.py` | **0** | "OK: attested instancing golden checks passed" |
| `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` | **0** | "OK: runtime instantiation cases passed (8 + ps1 parity when available)." |

Entrypoint real (instancias TEMPORALES generadas por MI en `/d/inst256`, no las del maker), roster
POR DEFECTO (sin `--roster`), los tres tiers -> `new_instance.py` exit **0** en las 3.

En los 3 `AGENTS.md` generados (`coord/AGENTS.md`, `rt/AGENTS.md`, `att_default/Aegis/AGENTS.md`):

| Comprobacion (grep / exit) | coordination | runtime | attested (default) |
|---|---|---|---|
| `Roster policy` (count) | 1 | 1 | 1 |
| aclaracion "This policy governs agent participants that execute code" | 0 | 0 | 0 |
| aclaracion "does not alter the human owner" | 0 | 0 | 0 |
| aclaracion "redefine the registry's `signer`/`worker` key-possession tiers" | 0 | 0 | 0 |
| regla 1 "A worker agent is a code executor subordinate to the maker" | 0 | 0 | 0 |
| regla 2 "The maker must be a strong-capability agent and governs every worker" | 0 | 0 | 0 |
| regla 3 "The adversarial checker must always be a strong-capability agent" | 0 | 0 | 0 |
| `maker != checker` | 0 | 0 | 0 |
| placeholders `{{...}}` sin sustituir (count) | 0 | 0 | 0 |
| bytes >127 (count) | 0 | 0 | 0 |
| **la aclaracion precede a la regla 1** (numeros de linea) | OK (64<67) | OK (64<67) | OK (64<67) |

Gates de la instancia RECIEN NACIDA (`--root <instancia>`), los 3 tiers:
`validate` -> 0 / `scan_encoding` -> 0 / `scan_domain_neutrality` -> 0 (**9/9 exit 0**).

Falsabilidad del gate de neutralidad sobre la LINEA NUEVA (para que el verde no sea vacio): inyecte un
termino de negocio dentro de la propia aclaracion -> `scan_domain_neutrality.py` exit **1**
(`AGENTS.template.md:61: trading`, que es exactamente la linea anadida); restaure -> exit **0** y
`git status --short` limpio en el clon. El scan SI cubre el texto nuevo, no solo el archivo.

## Vector por vector (lo que la instruccion pidio refutar)

| # | Vector | Resultado |
|---|--------|-----------|
| R1 | **SLIP-1 cerrado**: la instancia attested-default ya NO nace con guia contradictoria sobre quien ratifica | **PASS** (ver analisis abajo) |
| R2 | Las 3 reglas de 0099 siguen presentes e **intactas** en el AGENTS generado | **PASS** (grep 3/3 en los 3 tiers; diff de reglas vacio) |
| R3 | La aclaracion es **neutral de dominio**, con gate FALSABLE sobre esa linea | **PASS** (0 / falsable 1 / restaurado 0) |
| R4 | Diff = **solo `AGENTS.template.md` +3**; runtime/validador/config/instancias vivas intactos | **PASS** (`git diff --numstat 377bb20 356ac5d` excluyendo ledger/mailbox/tasks/handoffs/personal/runtime-state = `3 0 AGENTS.template.md`; con pathspec `scripts runtime/*.py protocol.config.json AGENTS.md examples profiles .github` = **vacio**) |
| R5 | Sin regresion: 6 gates | **PASS** (6/6 exit 0) |
| R6 | La aclaracion llega ANTES de la lista en el artefacto generado (si llegara despues, la ambiguedad persistiria en la primera lectura) | **PASS** (linea 64 vs 67 en los 3 tiers) |
| R7 | **Nuevo escape buscado**: alguna copia de la politica en la instancia SIN la aclaracion (mirror sin caveat) | **PASS** -- la frase de la regla 1 aparece **exactamente 1 vez** en toda la instancia generada, y en el mismo archivo/bloque que la aclaracion (3 lineas arriba) |
| R8 | **Nuevo escape buscado**: el fix altero alguna regla al insertarse | **PASS** (diff de reglas vacio, R2) |
| R9 | **Nuevo escape buscado**: sub-captura por el alcance "that execute code" | **RESIDUAL RES-5** (no bloqueante, ver abajo) |

### Por que doy SLIP-1 por cerrado (falsable)

El dano falsable que declare en el veredicto anterior era: *"la unica afirmacion normativa que la
instancia nace conteniendo sobre una entrada `tier:worker` dice que nunca ratifica, mientras su propio
`agent_registry` asigna `tier:worker` al human owner y la tabla 4 lineas arriba le da la aprobacion de
politica y transiciones criticas -> el adoptante en frio obtiene guia contradictoria sobre quien
ratifica."*

Estado post-fix, verificado en la instancia attested generada por defecto:
- `att_default/Aegis/protocol.config.json` **sigue** emitiendo `{"id":"owner-a","role":"human_owner",
  "tier":"worker",...}` (el fix era textual; el roster no se toco, como se pidio).
- `att_default/Aegis/AGENTS.md` linea 61 (tabla) sigue dando al human owner la aprobacion de politica.
- `att_default/Aegis/AGENTS.md` lineas 64-65 (NUEVAS) dicen explicitamente que la politica **no altera
  la autoridad de aprobacion del human owner** ni **redefine los tiers `signer`/`worker` de posesion de
  llave del registry**, y esas lineas preceden a la regla 1 (linea 67).

Las dos patas de la contradiccion quedan desarmadas en el punto exacto donde nacia: (a) el token
`worker` del registry queda declarado como posesion-de-llave y no como el sujeto normativo de la
politica; (b) la autoridad del human owner queda declarada intocada. Un adoptante en frio que lea la
seccion 3 junto a su `agent_registry` ya no obtiene guia contradictoria sobre quien ratifica. Ademas
probe que no existe ninguna otra copia de la regla 1 en la instancia que quede huerfana de la
aclaracion (R7). SLIP-1: **cerrado**.

## Residuales declarados (NO bloqueantes)

Nuevos de esta iteracion:

- **RES-5 (nuevo, sub-captura):** la primera oracion acota la politica a "agent participants **that
  execute code**". Las reglas 2 y 3 gobiernan al *maker* y al *checker adversarial*; un lector
  literalista podria argumentar que un checker que solo lee y no ejecuta codigo cae fuera del alcance
  declarado, justo la regla que sostiene el gate. No lo hago bloqueante por tres razones falsables:
  (i) las reglas 2 y 3 estan enunciadas de forma categorica y autonoma dentro de la lista; (ii) el
  bloque vive en la seccion "Agent Roles" de un contrato de trabajo sobre codigo; (iii) la redaccion es
  la que **yo** propuse casi literal, y no es honesto convertir mi propia formulacion en un segundo
  NO-GO. Polish sugerido para un futuro ciclo (no ahora): "This policy governs the agent participants of
  the roster." -- excluye igual al human owner (un humano no es un agente) sin estrechar el alcance a la
  ejecucion de codigo.
- **RES-6 (nuevo, correccion de mi propio veredicto anterior):** afirme que el bloque anadido era "la
  unica definicion normativa de `worker` que una instancia nace conteniendo". Es **falso** y lo corrijo:
  `skills/delegate-to-worker.skill.md` (preexistente, SPEC-0110 / TASK-0216) se materializa en los tres
  tiers y define un "keyless worker" que no firma, no cierra y no escribe el ledger. Esto **no** cambia
  SLIP-1 (esa skill habla de posesion de llave y de delegacion, consistente con la aclaracion nueva) ni
  el sentido del fix, pero mi afirmacion anterior estaba sobredimensionada y debe quedar corregida en el
  registro. La colision que motivo el NO-GO seguia siendo real por el AGENTS; su exclusividad, no.
- **RES-7 (nuevo, menor):** en los tiers `coordination` y `runtime` el `protocol.config.json` generado
  **no tiene `agent_registry`** (verificado), asi que la aclaracion referencia "the registry's
  `signer`/`worker` key-possession tiers" que en esas instancias no existe. Es una referencia colgante e
  inocua (una exencion, no un requisito) y el gate de esas instancias sigue verde; lo dejo trazado.

Vigentes del veredicto anterior (sin cambio): **RES-1** (`examples/generated_minimal_instance/AGENTS.md`
sigue sin la politica, `grep -c` -> 0; artefacto historico, no regenerado por CI), **RES-2**
(`scripts/upgrade_instance.py` propaga el TEMPLATE, no re-materializa el `AGENTS.md` vivo de instancias
existentes -- coincide con el `out_of_scope` declarado), **RES-3** (el espejo no lleva la RAZON de la
regla 3), **RES-4** ("strong-capability" no definido ni verificable; enforcement mecanico fuera de
alcance por intake).

## Recomendacion de cierre

**OK-CLOSABLE (GO).** Las 5 aceptaciones del intake se cumplian ya por comportamiento en la iteracion
anterior; el unico bloqueo era SLIP-1 y esta cerrado por el texto exportado, verificado en clon limpio
por el entrypoint real en los 3 tiers, con los 6 gates de protocolo en 0, los 9 gates de instancias
recien nacidas en 0, y el gate de neutralidad probado FALSABLE sobre la linea nueva.

Yo no cierro ni promuevo (checker-only): el flip `in_review -> done`, la liberacion de claims y el
archivado de mensajes son del Arquitecto. Bucle de fix: iteracion 1 de 2 consumida y **resuelta**; no
solicito iteracion 2.

Nada del fondo intocable fue tocado ni evaluado (config 2E35F26E, epoch 1.14.0, N=500, N=6).

-- Analista (checker adversarial independiente), 2026-07-24 04:13 (UTC+0200).
