# Analista verdict -- TASK-0293 (pulido de los residuales accionables de TASK-0256)

- Reviewer: Analista (independent adversarial checker; maker != checker).
- Verdict: **OK-CLOSABLE (GO)** -- los 4 residuales accionables quedan cerrados por comportamiento,
  sin reintroducir SLIP-1 y sin tocar el sentido normativo de las 3 reglas de DECISION-0099.
  **3 residuales NUEVOS declarados (no bloqueantes) + 2 correcciones de registro**, una de ellas
  refuta la PREMISA de la pregunta (1) del Arquitecto aunque confirma su CONCLUSION.
- Emitted: 2026-07-24 05:30 local (UTC+0200).
- Relacion: cierra los accionables de `Analista-TASK-0256-roster-policy-remediation1-verdict.md`
  (POLISH/RES-5, RES-7, RES-3, RES-1). RES-2 / RES-4 / RES-6 siguen fuera de alcance por intake.

## Canonical anchor

- Repo bajo revision: multi_agent_project_protocol (hub de protocolo).
  **SIN producto en alcance -- no se corrio ningun npm test de producto.**
- Commit de implementacion: `130f63c`; base = `130f63c^` = `b7babed9`.
- La instruccion cita HEAD `273376c`; el `origin/main` real al momento del juicio es **`0047279`**
  (273376c + el commit de coordinacion que me rutea este review). Verifique que el delta
  `273376c..0047279` es **solo ledger/mailbox** (`CLAIMS.json`, `runtime/state/events.jsonl`,
  `runtime/state/snapshot.json`, 2 archivados de mailbox y el propio MSG de REVIEW): cero cambios
  del texto revisado. Anclo en **`0047279`** (mas conservador).
- Method: **CLON LIMPIO** de origin/main en `/d/ccv293`, `checkout 0047279`, gates corridos ALLI por
  EXIT code (nunca in-place, nunca por pipe a `head`/`tail`). Comportamiento probado por el
  **ENTRYPOINT REAL** (`scripts/new_instance.py`) generando instancias temporales en los **tres**
  tiers, mas una cuarta generacion para contrastar la muestra. Ninguna instancia viva tocada.

## El cambio auditado (no confiado)

`git diff 130f63c^ 0047279 -- AGENTS.template.md` (numstat real: **4 anadidas / 3 borradas**):

```
-This policy governs agent participants that execute code. It does not alter the human owner's
-approval authority or redefine the registry's `signer`/`worker` key-possession tiers.
+This policy governs the agent participants of the roster. It does not alter the human owner's
+approval authority or redefine `signer`/`worker` key-possession tiers where the registry defines them.
...
-   required in addition to key possession, and `maker != checker` remains mandatory.
+   required in addition to key possession, and `maker != checker` remains mandatory; otherwise,
+   a checker unable to refute the maker turns the gate into a rubber stamp.
```

`examples/generated_minimal_instance/AGENTS.md`: +18/-0 (el bloque `Roster policy` completo).
Las reglas **1 y 2 no aparecen en el diff**: son byte-identicas (esa es la prueba, no una lectura).
La regla 3 conserva integra su norma (`must always be a strong-capability agent`,
`required in addition to key possession`, `maker != checker remains mandatory`) y solo **anade**
una clausula de razon.

Diff no-ledger completo `130f63c^..0047279` con pathspec
`scripts runtime protocol.config.json AGENTS.md AGENTS.template.md examples profiles .github
Area_comun/protocol Area_comun/decisions skills`:

```
4  3  AGENTS.template.md
18 0  examples/generated_minimal_instance/AGENTS.md
12 0  runtime/state/events.jsonl      (ledger, append)
22 4  runtime/state/snapshot.json     (ledger, materializacion)
```

-> **cero** cambios en `scripts/`, `runtime/*.py`, `protocol.config.json`, el `AGENTS.md` VIVO,
`profiles/`, `.github/`, `skills/`. Ninguna instancia viva re-materializada (RES-2 sigue vivo, por diseno).

## Reproduccion (exit codes reales, clon limpio `/d/ccv293` @ `0047279`)

| Gate | Exit | Salida |
|------|------|--------|
| `python scripts/validate_collaboration_state.py` | **0** | "OK: collaboration state is valid." |
| `python scripts/scan_encoding.py` | **0** | "OK: encoding scan is clean." |
| `python scripts/scan_domain_neutrality.py` | **0** | -- |
| `python runtime/protocol_replay.py --check-drift --root .` | **0** | "PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=6358" -> **drift 0** |
| `python scripts/test_attested_instancing.py` | **0** | "OK: attested instancing golden checks passed" |
| `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` | **0** | "OK: runtime instantiation cases passed (8 + ps1 parity when available)." |
| `python scripts/validate_collaboration_state.py --root examples/generated_minimal_instance` | **0** | "OK: collaboration state is valid." |

Entrypoint real, roster POR DEFECTO (sin `--roster`), instancias TEMPORALES generadas por MI en
`/d/i293` (no las del maker): `new_instance.py` exit **0** en los 3 tiers.

En los 3 `AGENTS.md` generados (`coordination/`, `runtime/`, `attested/Aegis/`), por `grep -c`:

| Comprobacion | coordination | runtime | attested |
|---|---|---|---|
| `Roster policy` | 1 | 1 | 1 |
| `the agent participants of the roster` (alcance NUEVO) | 1 | 1 | 1 |
| `participants that execute code` (alcance VIEJO) | **0** | **0** | **0** |
| `where the registry defines them` (exencion condicional) | 1 | 1 | 1 |
| ``the registry's `signer` `` (redaccion vieja, colgante) | **0** | **0** | **0** |
| `turns the gate into a rubber stamp` (razon regla 3) | 1 | 1 | 1 |
| regla 1 `A worker agent is a code executor subordinate to the maker` | 1 | 1 | 1 |
| regla 2 `The maker must be a strong-capability agent` | 1 | 1 | 1 |
| `maker != checker` | 1 | 1 | 1 |
| placeholders `{{...}}` sin sustituir | 0 | 0 | 0 |
| `agent_registry` en el `protocol.config.json` generado | **0** | **0** | **1** |
| orden: alcance (l.64) precede a regla 1 (l.67) y razon en l.78 | OK | OK | OK |

Gates de la instancia RECIEN NACIDA (`--root <instancia>`), los 3 tiers:
`validate` -> 0 / `scan_encoding` -> 0 / `scan_domain_neutrality` -> 0 (**9/9 exit 0**).
(Ver correccion de registro **C2**: ese 9/9 solo se sostiene con ids de agente que no sean
subcadenas de palabras inglesas; con `--human-owner Own` el neutrality de la instancia nacida es
exit **1** en los 3 tiers, por causa PREEXISTENTE y ajena a 0293.)

Falsabilidad del gate de neutralidad sobre las LINEAS NUEVAS del template (para que el verde no sea
vacio): inyectar un termino de negocio en la oracion de alcance -> exit **1**
(`AGENTS.template.md:61: trading`); inyectarlo en la clausula nueva de la regla 3 -> exit **1**
(`AGENTS.template.md:75: trading`); restaurar -> exit **0** y `git status --short` limpio en el clon.

## Vector por vector

| # | Vector pedido | Resultado |
|---|---------------|-----------|
| V1 | **RES-5/polish**: el alcance ya no dice "that execute code"; el checker read-only vuelve a caer dentro | **PASS con matiz** (grep 0/0/0 del viejo; el nuevo predicado no queda definido -> **RES-8**) |
| V2 | **RES-5**: no se reintroduce SLIP-1 (el human owner no queda atrapado por la regla 1) | **PASS**, pero **por otra razon**: la premisa "un humano no es un agente" es **FALSA** en el artefacto (ver C1 abajo). Lo que cierra SLIP-1 es la clausula de exencion, intacta |
| V3 | **RES-7**: "where the registry defines them" es exencion condicional y no cuelga en coordination/runtime | **PASS** (esos 2 tiers generan config **sin** `agent_registry` -> verificado por lectura del JSON; la frase vieja `the registry's signer` = 0 en los 3) |
| V4 | **RES-3**: la regla 3 lleva su razon | **PASS** ("turns the gate into a rubber stamp" = 1 en los 3 tiers; norma intacta, solo se anade) |
| V5 | **RES-1**: la muestra generada contiene la politica | **PASS por la letra** (bloque **byte-identico** al del template, 1160 chars, `IDENTICAL`) -- coherencia solo parcial -> **RES-9** |
| V6 | Las 3 reglas conservan su sentido normativo | **PASS** (reglas 1-2 byte-identicas: no aparecen en el diff; regla 3 conserva las 3 clausulas normativas y solo suma una razon) |
| V7 | Diff acotado: sin runtime/validador/config/instancias vivas | **PASS** (numstat arriba; el "+7" de la instruccion es "+4/-3", ver **C1**) |
| V8 | Neutralidad verde y **falsable** sobre el texto nuevo | **PASS** en el template (0 / 1 / 1 / 0). **NO cubierto** en la muestra -> **RES-10** |
| V9 | validate / encoding / drift / test_attested_instancing / run_runtime_instantiation_cases -> 0 | **PASS** (6/6 + el validate de la muestra) |
| V10 | **Escape buscado**: copia huerfana de la politica sin la aclaracion | **PASS** (la regla 1 aparece **1 sola vez** por instancia, en el mismo bloque; en el repo solo en `AGENTS.template.md` y en la muestra) |
| V11 | **Escape buscado**: restos de la redaccion vieja en el repo | **PASS** (`participants that execute code` y ``the registry's `signer` `` = 0 fuera de ledger/mailbox/artifacts) |

## Analisis de los dos puntos donde la instruccion pide confirmacion literal

### V2 -- la premisa de la pregunta (1) es falsa; la conclusion se sostiene

La instruccion afirma que el alcance nuevo "sigue excluyendo al human owner (un humano no es un
agente)". **Eso no es cierto en el artefacto**: la instancia attested generada emite

```
"agent_registry": {"agents": [..., {"id":"Own","role":"human_owner","tier":"worker",
                                     "llm_preset":"human","adapter":"human","capabilities":["human_owner"]}]}
```

es decir, el human owner **es una entrada del roster de agentes** con el vocabulario del propio
protocolo (`agent_registry.agents`), y ademas aparece en la lista de participantes del `AGENTS.md`
generado. Bajo la redaccion nueva ("the agent participants of the roster") el human owner cae
**dentro** del alcance declarado, no fuera.

Aun asi **SLIP-1 no se reintroduce**, y esto es lo que importa: la segunda oracion -- intacta desde
la remediacion de 0256 -- dice explicitamente que la politica *"does not alter the human owner's
approval authority"*, y que no redefine los tiers `signer`/`worker` de posesion de llave. La
proteccion nunca dependio de la palabra "agent": depende de la exencion explicita, que sobrevive
verbatim. Un adoptante en frio sigue sin obtener guia contradictoria sobre quien ratifica.

Consecuencia practica para el Arquitecto: **no se debe apoyar la defensa de la politica en "un
humano no es un agente"**; la defensa correcta es la clausula de exencion.

### V1 -- el predicado viejo se fue, pero el nuevo no tiene referente definido (RES-8)

`roster` aparece exactamente **2 veces** en el `AGENTS.md` generado, y ambas dentro del propio
bloque ("Roster policy:" y la oracion de alcance). **No existe** en la instancia ninguna seccion,
lista o clave llamada "roster". Los candidatos a referente y su efecto sobre la regla 3:

| Candidato a "the roster" | Contiene al checker? | Contiene al human owner? |
|---|---|---|
| lista de participantes (l.49-52 del AGENTS generado) | **si** (`Ana: Independent analyst / checker`) | si |
| tabla titulada "Suggested role model" | **NO** (la tabla del template trae 3 filas: architect, implementer, human owner; **no hay fila de analyst/checker**) | si |
| `agent_registry.agents` (solo attested) | si (tier signer) | si (tier worker) |

Bajo el referente mas literal *y titulado* de la pagina (la tabla), el sujeto de la regla 3 sigue sin
estar enumerado. Es la MISMA clase de sub-captura que motivo RES-5, entrando por otra puerta, y de
severidad **menor o igual** a la original: no lo hago bloqueante por las mismas tres razones
falsables que use en 0256 -- (i) las reglas 2 y 3 estan enunciadas de forma categorica y autonoma
("The adversarial checker **must always be** a strong-capability agent"), (ii) el bloque vive en la
seccion "Agent Roles" junto a la lista que si nombra al checker, (iii) el texto adoptado es
literalmente el que yo propuse. Neto frente al estado previo: **mejora** (el checker pasa de
"argumentablemente fuera por el predicado" a "dentro bajo 2 de 3 referentes"). No hay regresion.

## Residuales NUEVOS declarados (no bloqueantes)

- **RES-8 (nuevo, referente indefinido + tabla sin checker):** "the roster" no esta definido en el
  artefacto y la unica tabla titulada de roles **no trae fila para el analyst/checker** (el template
  emite 3 filas; `--analyst` solo puebla la lista de participantes). Pulido sugerido para un ciclo
  futuro, en una sola linea: **anadir la fila del analyst/checker a la tabla de roles** (arregla a la
  vez el referente y la sub-captura), o acotar el alcance a "the agent participants listed in this
  section". No bloqueante (ver V1).
- **RES-9 (nuevo, muestra hibrida):** el intake ofrecia dos salidas para RES-1 -- **regenerar** la
  muestra **o** anadir una **nota de snapshot congelado**. La entrega hizo una tercera cosa: inserto
  a mano el bloque actual en una muestra que sigue declarando `Last updated: 2026-06-05` (linea 7),
  con **0** ocurrencias de "snapshot" (no hay nota). Medida falsable: `diff` de la muestra contra una
  generacion fresca del tier coordination = **132 lineas**, y a la muestra le faltan **5 secciones
  completas** que hoy si emite el template: "Intake gate (Definition of Ready)", "Handoff envelope +
  fix-loop", "Commit trailers", "Audited exceptions", "Governed plan approval before execution".
  Resultado: la muestra ahora **senala falsa vigencia** (fechada en junio, con texto que solo existe
  desde el 24-jul). La aceptacion se cumple por la letra ("contiene la politica regenerada" +
  `validate` verde), por eso no bloqueo; pero la coherencia real pide **regenerar la muestra** o
  **fecharla como snapshot congelado**, en una tarea aparte.
- **RES-10 (nuevo, texto gobernado en archivo exento del gate):** `examples/**` es un `exempt_glob`
  explicito de `scan_domain_neutrality`, de modo que las 18 lineas de politica que esta tarea mete en
  la muestra **no las cubre el gate de neutralidad**. Falsable: inyectar "for trading" dentro de ese
  bloque en la muestra -> exit **0** (no lo ve); la misma inyeccion en `AGENTS.template.md` -> exit
  **1**. Hoy es inocuo y lo verifique programaticamente: el bloque de la muestra es **byte-identico**
  al del template (que si esta gateado). El riesgo es de deriva futura: una edicion directa de la
  muestra no tiene puerta. (El `scan_encoding` tampoco cubre ese archivo, pero eso es su alcance
  declarado por diseno -- ASCII solo en `Area_comun/mailbox/**` y `Area_comun/state/*.json` -- no un
  hueco de esta tarea.)

Vigentes y **fuera** de esta tarea, sin cambio: **RES-2** (`upgrade_instance.py` propaga el template,
no re-materializa el `AGENTS.md` vivo), **RES-4** ("strong-capability" sin enforcement mecanico;
DECISION aparte), **RES-6** (correccion de registro, ya aplicada).

## Correcciones de registro

- **C1 (a la instruccion de REVIEW):** el mensaje declara `AGENTS.template.md (+7/-3)`. El numstat
  real de `130f63c^..0047279` es **`4 3 AGENTS.template.md`** (4 anadidas, 3 borradas; 7 es el total
  de lineas tocadas, no las anadidas). La muestra si es `+18/-0` como se declara. Ademas, la premisa
  "un humano no es un agente" de la pregunta (1) queda **refutada** por el artefacto (ver V2); la
  conclusion (no hay reintroduccion de SLIP-1) se **confirma**.
- **C2 (a mi propio registro de 0256, DECISION-0018 hacia el Arquitecto):** en aquel veredicto
  reporte "9/9 gates de instancias recien nacidas exit 0". Reproducible **solo** con ids de agente que
  no sean subcadenas de palabras inglesas. Con `--human-owner Own`, el `scan_domain_neutrality
  --root <instancia nacida>` da exit **1** en los **3** tiers, senalando el literal `Own` dentro de
  comentarios PREEXISTENTES (`runtime/submit_intent.py:817` "ITS OWN",
  `scripts/validate_collaboration_state.py:1406` "own path semantics", +2). Probe la causa: la misma
  generacion con `--human-owner Duenyo` da exit **0**. Es decir: **el escaneo de identidad de una
  instancia recien nacida es sensible a ids cortos que son subcadenas de palabras comunes**, lo que
  puede hacer nacer una instancia con su propio gate en rojo. **Nada que ver con TASK-0293** (probado)
  y no bloquea su cierre; lo dejo trazado por si el Arquitecto quiere una tarea de robustez
  (word-boundary en el escaneo de identidad, o validacion del id en `new_instance.py`).

## Recomendacion de cierre

**OK-CLOSABLE (GO).** Las 4 aceptaciones accionables del intake se cumplen por comportamiento,
verificadas en clon limpio por el entrypoint real en los 3 tiers, con 6/6 gates de protocolo en 0,
9/9 gates de instancias recien nacidas en 0, el `validate` de la muestra en 0, el gate de neutralidad
probado **falsable** sobre las dos lineas nuevas del template, el diff acotado y las reglas 1-2
byte-identicas. Los 3 residuales nuevos son de documentacion/cobertura, ninguno reabre SLIP-1 ni
altera la norma exportada.

Bucle de fix: **no solicito iteracion**. Si el Arquitecto quiere convertir RES-8/RES-9 en trabajo,
son una tarea de texto aparte (una linea de tabla + regenerar o fechar la muestra), no una
remediacion de esta.

Yo no cierro ni promuevo (checker-only): el flip `in_review -> done`, la liberacion de claims y el
archivado de mensajes son del Arquitecto.

Nada del fondo intocable fue tocado ni evaluado (config 2E35F26E, epoch 1.14.0, N=500, N=6).

-- Analista (checker adversarial independiente), 2026-07-24 05:30 (UTC+0200).
