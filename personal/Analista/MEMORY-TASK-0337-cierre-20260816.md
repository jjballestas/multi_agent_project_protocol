# MEMORY -- TASK-0337 cierre (revert de H-1 + paridad del gemelo), 2026-08-16 14:42 local

**Veredicto: OK-CLOSABLE.** Commit `27a76b16` (pusheado a `origin/main`).
Artefacto: `Area_comun/artifacts/Analista-TASK-0337-cierre-revert-H1-y-paridad-gemelo-verdict.md`.
Mensaje: `Area_comun/mailbox/open/MSG-20260816-Analista-to-Arquitecto-REVIEW-TASK-0337-cierre-OK.md`.

## Anclas usadas

- HEAD revisado `cef48839` (re-anclado desde `60e365cf`: origin/main avanzo A MITAD de la revision).
- Controles historicos: `f2de3ad7^` = `db8759b9` (pre-H-1), `3d357a28^` = `231aa719` (pre-paridad),
  `623fb8b4` (lo que yo mismo acredite en r2).
- Clones: `D:/Aegis_Scratch/protocol/rev0337c` y `ctrl0337c` (`git clone -s`).

## Lo que aprendi y quiero repetir

**1. "Volvio al estado X" se prueba con identidad de blob, no con el mensaje del commit.**
`git rev-parse <commit>:<ruta>` para las mismas rutas en TRES anclas. Aqui salio algo mejor que lo
preguntado: no solo identico a `f2de3ad7^`, sino identico a `623fb8b4`, el estado exacto que yo ya
habia acreditado. Eso convierte "no re-pagar AC7/AC10" de una promesa del encargo en un hecho medido.

**2. Cuando el maker cita una coordenada, buscar al INSTRUMENTO que la emite.**
El Arquitecto dio 1502, Codex dijo 1515. No firme ninguno: corri el escaner en el estado PRE-FIX y el
escaner mismo emitio `scripts/harness/peer_mailbox_cron.ps1:1515: Codex`. La coordenada la nombra el
instrumento cuando falla, no la declaracion del entregable. A/B con control historico: pre-fix PS
exit 1 / post-fix exit 0, con el gemelo Python en 0 en ambos.

**3. Un gate que verifica DECLARACION no dice nada de EJECUCION.**
`check_falsification_contracts.py` salio 0 con 76/76/0 -- y aun asi el runner
`test_scan_domain_neutrality.py` estaba ROJO. El primero comprueba que las fronteras existan junto al
test; el segundo las ejecuta. Cruzar siempre los dos. Es mi leccion
`contratos-declarados-no-son-ejecutados` aplicada en vivo.

**4. NUEVA Y LA MAS IMPORTANTE -- un test que falla rapido oculta los defectos de detras.**
`NEG-NEUTRALITY-IDENTITY-INVENTORY-PARITY` fallaba en `:536` (`assertEqual(inventarios)`). El maker
declaro "Divergencias restantes: 1" y verifique que la cifra era CORRECTA como diferencia de
inventarios. Pero aplique la remediacion evidente en el clon y el test **siguio rojo**, ahora en
`:611`, sobre `runtime/context.py:16:Codex`. Detras del primer `assert` habia tres coordenadas
muertas mas y un censo 92-vs-91. **Ante un residuo declarado con un numero, aplicar el arreglo y
volver a correr: si el gate sigue rojo, el numero media otra cosa.** Un residuo declarado no es un
gate verde.

**5. NUEVA -- antes de prescribir una direccion de arreglo, medirla.**
Mi primera version del veredicto recomendaba "anadir el digest al `.ps1`". Lo medi y era EXACTAMENTE
al reves: el digest `c857d09d` es `claude`, que **no esta** entre los terminos de identidad
configurados (`Analista`, `Arquitecto`, `Codex`, `operador`, `operador humano`), asi que la
declaracion Python es MUERTA -- quitarla deja el escaner Python en exit 0. Anadirla al `.ps1` habria
igualado los inventarios concediendo una exencion sobre un termino que ese escaner ni vigila: verde
por construccion. Reescribi el artefacto antes de commitear. Prescripcion sin medicion = defecto.

**6. Coherencia entre rondas: la atribucion decide si bloqueo.**
En r3 bloquee H-3 porque el control probaba que la entrega lo INTRODUJO (`f2de3ad7^`=0, entrega=1).
Aqui el control prueba lo contrario: pre-H-1 el runner fallaba con DOS negativos y hoy falla con UNO
(`3d357a28` mato `NEG-NEUTRALITY-IDENTITY-EXEMPTION-PARITY`). Bloquear una mejora por deuda heredada
seria incoherente. Se declara como condicion de PUBLICACION, no de cierre, y se pide tarea propia.

**7. Negativo de paridad ejecutado por mi, no leido.** Inserte una linea antes de la ocurrencia
vigilada en la produccion copiada del clon: ambos gemelos exit 1, ambos emitiendo `...:1516: Codex`.
Restauracion byte a byte y `git status --porcelain` vacio despues. Siempre restaurar y comprobar.

## Estado que dejo

- TASK-0337 en `in_review`, owner Codex, 0 claims activos, drift 0. El flip a `done` es del Arquitecto.
- S-1 abierto y declarado: `NEG-NEUTRALITY-IDENTITY-INVENTORY-PARITY` rojo en
  `test_scan_domain_neutrality.py`, cableado en `.github/workflows/validate.yml:522`. Cuatro entradas
  muertas (3 en `runtime/context.py:16-17`, 1 en `peer_mailbox_cron.ps1:553`), censo 92 vs 91.
  No atribuible a 0337: `scan_domain_neutrality.py` y `runtime/context.py` son blobs identicos en los
  cuatro anclas.
- R-2 sin cambio: `test_exec_lease_harness.py` exit 1, 28/31, los mismos tres fallos de r2.
- H-1 abierto por decision del operador; su causa correcta es `message_scope_ambiguous`
  (`peer_mailbox_cron.ps1:1206`), no el guardia de residuo.
- Al commitear salto `PRUNE DUE: cold_start_tokens 23892 >= 20000`. La poda es del Arquitecto
  (capability orchestrator) y exige cero claims; yo no la corro, la senalo.
- Quedan en `open/` dos REVIEW mias pendientes: TASK-0409 y TASK-0378-r4.
