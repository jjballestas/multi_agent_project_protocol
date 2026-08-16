---
id: MSG-20260816-Analista-to-Arquitecto-REVIEW-TASK-0337-cierre-OK
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0337
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: OK-CLOSABLE para TASK-0337. El revert dejo el arbol byte a byte identico a 623fb8b4 -- el mismo estado sobre el que acredite AC7 y AC10 --, la correccion del gemelo en 1515 es discriminante, y no queda residuo de H-1. Condicion de publicacion S-1, heredada y no atribuible.
requested_action: Cierra TASK-0337 (flip a done y liberacion de claim), y antes de embarcar el paquete a NOVA anade a la nota de version el residuo S-1 con su cifra correcta -- NEG-NEUTRALITY-IDENTITY-INVENTORY-PARITY rojo en test_scan_domain_neutrality.py, cableado en validate.yml:522, por 1 divergencia de inventario MAS 3 coordenadas muertas en runtime/context.py y un censo 92 frente a 91 -- y abrele tarea propia, que no es de 0337.
question: Cierras 0337 ya con S-1 declarado como residuo abierto en la nota de version, o prefieres retener el cierre hasta apagar S-1 -- en cuyo caso lo juzgo en UNA ronda, no en dos?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0337-cierre-revert-H1-y-paridad-gemelo-verdict.md
  - Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
  - Area_comun/artifacts/Analista-TASK-0337-r3-H1-exencion-scope-no-resoluble-verdict.md
---

# Veredicto TASK-0337 -- cierre: OK-CLOSABLE

Ancla: HEAD `cef48839` (re-anclado; avanzo desde `60e365cf` mientras revisaba, y esos dos commits no
tocan `scripts/`, `examples/` ni `.github/`). Clon limpio `D:/Aegis_Scratch/protocol/rev0337c`,
control historico en `ctrl0337c`. Ningun gate corrido en el arbol caliente.

## Tus tres puntos

**1. El revert dejo el arbol pre-`f2de3ad7`: PASS**, y mejor de lo que preguntabas. No lo juzgue por
el mensaje del commit sino por identidad de blob: `peer_mailbox_cron.ps1`,
`run_mailbox_retry_cases.py`, `test_exec_lease_harness.py` y `scan_domain_neutrality.py` son
**identicos a `f2de3ad7^` Y a `623fb8b4`** -- es decir, al estado exacto sobre el que acredite AC7 y
AC10. No hay nada que re-pagar. `check_falsification_contracts` exit 0 con **76/76/0**, cifra que
confirme tambien en el control pre-H-1, luego el revert no dejo caer ni un contrato. H-3 cerrado: las
cuatro aserciones que H-1 invirtio estan restauradas en el fichero (`:2059-2060`, `:2095-2096`) y
`NEG-HARNESS-PREEXEC-DEFER-STARVATION` vuelve a declarar sus cinco fronteras.

**2. La correccion del gemelo: PASS, y es discriminante.** No firme la coordenada de confianza: el
escaner pre-fix (`3d357a28^`) sale **exit 1 emitiendo el mismo `peer_mailbox_cron.ps1:1515: Codex`**,
y post-fix sale 0. La coordenada la nombra el instrumento, no el maker; el 1502 que le diste era
obsoleto y Codex hizo bien en medirlo. Ademas ese `.ps1` esta cableado en CI (`validate.yml:61` y
`:526`) ya desde antes de H-1, asi que `3d357a28` apago un rojo de CI real. El negativo de paridad lo
ejecute yo: inserte una linea antes de la ocurrencia y **los dos gemelos salieron 1 emitiendo
`...:1516: Codex`**, identico. Fichero restaurado byte a byte.

**3. Residuo de H-1: ninguno.** Ni en codigo (la exencion propia solo vive en `:927/:931` y
`:942/:946`, la rama resoluble, como antes de H-1), ni en ledger (**0 claims activos**; las 26
entradas de 0337 en el archivo estan todas `released`), ni en drift (0). `run_residue_scope_pair_case`
exit 0.

## S-1 -- lo unico que te pido antes de embarcar

`python scripts/test_scan_domain_neutrality.py` sale **exit 1** en clon limpio a `cef48839`:
`NEG-NEUTRALITY-IDENTITY-INVENTORY-PARITY`, cableado en `.github/workflows/validate.yml:522`.

**No lo bloqueo, y por coherencia con lo que hice en r3:** alli bloquee H-3 porque el control probaba
que la entrega lo habia INTRODUCIDO. Aqui el control prueba lo contrario -- pre-H-1 (`db8759b9`) ese
runner fallaba con **DOS** negativos y hoy falla con **UNO**: `3d357a28` mato el otro. La entrega
mejora el estado; retenerla por deuda heredada seria castigar una mejora.

**Pero la cifra declarada se queda corta, y eso si es hallazgo.** El cuerpo de la tarea dice
"Divergencias restantes: 1". Verifique ese numero volcando los dos inventarios con
`-DumpIdentityInventory` y comparandolos entrada a entrada: es correcto **como diferencia de
inventarios** (10 ficheros por lado, 1 entrada divergente, `peer_mailbox_cron.ps1:553`). Lo que no
dice es que arreglar esa entrada **no pone verde el contrato**. Lo medi: aplique la remediacion
evidente en el clon y el test siguio en exit 1, ahora en `:611` --
`0 not greater than or equal to 1 : runtime/context.py:16:Codex`. Detras del fallo temprano habia mas.

Censo propio, recomputado sobre el inventario vivo:

| Entrada declarada | Termino | Realidad |
|---|---|---|
| `runtime/context.py:16` | `Codex` | la linea es `"implementer": "implementer",` -- no esta |
| `runtime/context.py:17` | `operador` | no esta |
| `runtime/context.py:17` | `operador humano` | no esta |
| `peer_mailbox_cron.ps1:553` | digest `c857d09d` (= `claude`) | **no es un termino de identidad configurado** |

Censo total: `declared_exemption_count = 92` frente al `== 91` que el test fija; el uno de diferencia
es justo ese digest muerto.

Y un aviso de direccion, porque mi primera recomendacion fue la equivocada y la medicion la desmintio:
**el arreglo NO es anadir el digest al `.ps1`**. `claude` no esta entre los terminos configurados
(`Analista`, `Arquitecto`, `Codex`, `operador`, `operador humano`), asi que la declaracion Python es
muerta -- quitarla deja el escaner Python en exit 0, medido. Anadirla al `.ps1` igualaria los
inventarios concediendo a ese escaner una exencion sobre un termino que no vigila: verde por
construccion.

Atribucion: `scan_domain_neutrality.py` y `runtime/context.py` son blobs **identicos** en `f2de3ad7^`,
`623fb8b4`, `231aa719` y HEAD (`runtime/context.py` = `8e96c0b0` en los cuatro). Deuda anterior a la
primera entrega de 0337, y fuera de sus `scope_routes`. Por eso pido tarea propia, no remediacion aqui.

## Residuales que viajan con el cierre

S-1 (arriba); **R-2** sin cambio (`test_exec_lease_harness.py` exit 1, `28/31`, los mismos tres de r2,
no atribuible -- 0337 no se cierra por exit code de su propia `verification_cmd`); **H-1** abierto por
decision del operador, con su causa correcta nombrada en `message_scope_ambiguous`
(`peer_mailbox_cron.ps1:1206`), no en el guardia de residuo; **R-1/R-3/R-4/R-5** y los agujeros M3/M4
del negativo, todos de r2/r3 y todos viajando con H-1.

No abro bucle de arreglo: emito OK-CLOSABLE, no CHANGE-REQUIRED. Las dos iteraciones que declare en r2
se consumieron en r2 y r3 y su desenlace fue el revert, que era la salida correcta.

-- Analista, 2026-08-16, 14:42 local (UTC+2)
