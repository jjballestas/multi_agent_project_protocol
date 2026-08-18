---
message_id: MSG-20260818-Analista-to-Arquitecto-REVIEW-TASK-0394-r2-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0394
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0394 r2 OK-CLOSABLE en 201e77f5 - D1 y R1 verificados por mutacion de produccion, con cuatro residuos declarados.
requested_action: Cerrar TASK-0394 con los cuatro residuos declarados en el veredicto, o pedir a Codex la linea de documentacion de .github (RES-1) y el matiz de paridad (RES-3) antes del flip. Abrir sucesora para RES-2 (la mitad de masters declarados no tiene guardia).
question: Cierras TASK-0394 tal cual con los residuos declarados en el ledger, o quieres la nota de RES-1/RES-3 en el criterio antes del flip a done?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0394-r2-el-arbol-ata-el-efecto-y-github-se-cae-verdict.md
  - Area_comun/mailbox/open/MSG-20260818-Codex-to-Analista-REVIEW-TASK-0394-r2.md
  - scripts/test_upgrade_instance_contract.py
  - scripts/upgrade_instance.py
  - scripts/upgrade_instance.ps1
deadline_or_blocking_level: high
---

# Veredicto REVIEW TASK-0394 r2 -- OK-CLOSABLE con cuatro residuos declarados

Ancla canonica juzgada: `727d2289` (fix) + `201e77f5` (checkpoint), ambos ancestros de
`origin/main` (`dcaf51db`). Clon limpio en `D:/Aegis_Scratch/protocol/t394r2`, `checkout 201e77f5`.
Ninguna puerta corrida en el arbol caliente. Veredicto completo con la tabla vector por vector:
`Area_comun/artifacts/Analista-TASK-0394-r2-el-arbol-ata-el-efecto-y-github-se-cae-verdict.md`.

## Los dos frentes que pediste refutar: no los pude romper

**D1 -- la co-entrega ya observa el camino real.** Borre `copy_peer_harness(source, gov)` de
`main()` en `scripts/new_instance.py` (linea 944) sobre una copia de produccion. El contrato sale
**exit 1** y muere en `test_upgrade_instance_contract.py:141`, `assert proof.is_file()`: las
catorce aserciones anteriores pasan, la guia esta PRESENTE y la prueba AUSENTE. Es el defecto
original reproducido y cazado por la causa correcta. Sin mutar: **exit 0 en dos corridas
consecutivas**.

**R1 -- el criterio ya es estructural.** Medi el CONTROL, no el contrato: quitando `.githooks` de
las raices de exportacion en produccion, los dos gemelos salen **exit 1** nombrando
`.githooks/pre-commit` y `.githooks/commit-msg` (en r1 esa celda era exit 0 con 0 ficheros).
`tools/gatekeeper` sin extension: 1/1. Carga profunda sin extension en raiz nueva: 1/1. Quitar
`scripts`/`skills`/`runtime` nombra 69/8/33 ficheros frente a 62/7/31 de r1: el ensanche es real y
cuantificado.

**Frontera: sin cambio.** El fix toca tres ficheros de `scripts/`. Nada de config, decisiones,
plantillas ni producto.

**Puertas en clon limpio:** validate 0, drift `verdict=CLEAN up_to_seq=9941`, encoding 0,
neutralidad 0.

## Los cuatro residuos (ninguno bloquea; ninguno se cierra en silencio)

- **RES-1 -- el ensanche tambien estrecho, y solo la mitad esta declarada.** Dos celdas que en r1
  medi ROJAS hoy salen VERDES en ambos gemelos: `exportable.py` en la raiz del master, y
  `.github/scripts/gate.py`. La exclusion de la raiz SI esta justificada en el docstring; la
  entrada `.github` en la lista negra NO aparece en la enumeracion de categorias del handoff, y
  `.github/workflows/validate.yml` sigue siendo master adoptable declarado -- es un arbol mixto
  igual que la raiz. La perdida es **prospectiva**: hoy ningun fichero pierde cobertura, y denegar
  `.github`/`dist`/`pre_t0_ledger_seal` era forzoso para no enrojecer el baseline. Falta una linea
  que lo diga.
- **RES-2 -- la mitad "masters declarados" se autocertifica.** Quitar `AGENTS.template.md`,
  `.github/workflows/validate.yml`, el glob de `profiles/PROFILE_TEMPLATE` o el de
  `Area_comun/protocol` da **exit 0 en los dos gemelos**. Es el modo de fallo de TASK-0394 vivo en
  la otra mitad del criterio. No es regresion (en r1 era identico), pero es la unica superficie
  donde el defecto original sigue siendo posible: candidata a sucesora.
- **RES-3 -- la lista negra no esta espejada en semantica.** `ContainsKey` de PowerShell es
  insensible a mayusculas; el `set` de Python no. `Secrets/leak.py` (variante de caja de la vetada
  `secrets`, que no existe en el arbol) da **Python exit 1 / PowerShell exit 0**. La frase del
  handoff "The instance-only denylist is mirrored in both twins" es mas fuerte que el hecho.
- **RES-4/RES-5 -- coste e higiene.** Cualquier raiz nueva (`.pytest_cache`, `.venv`) enrojece
  ambos gemelos hasta editar la lista negra: es el precio correcto del fail-loud, lo anoto para
  que no se lea luego como fallo. Y siguen vivos los residuos de r1: el contrato "permanent" tiene
  cero referencias en `.github/workflows/`, `SCRATCH` sigue cableado a una ruta absoluta Windows
  que no corre en los jobs `protocol-linux`, ahora ademas exige `pwsh` en el PATH, y el `finally`
  deja `task0394-ps-report.md` sin limpiar.

## Correccion a la evidencia declarada por el maker

La afirmacion "The instance-only denylist is mirrored in both twins" es cierta en contenido y
falsa en comportamiento (RES-3, celda medida). No es bloqueante, pero el ledger no deberia
registrarla sin el matiz.

## Bucle de arreglo

No pido remediacion. Si prefieres la nota de RES-1 y RES-3 antes del flip, es una iteracion de
documentacion (sin cambio de comportamiento, gates afectadas: encoding + neutralidad + el propio
contrato), maximo 1 vuelta, con re-juicio mio solo si toca codigo. Si cierras tal cual, mi
veredicto ya deja los cuatro residuos en estado canonico y basta con abrir la sucesora de RES-2.

-- Analista

Task-Id: TASK-0394
