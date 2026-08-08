---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0332
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0332
status: open
created: 2026-08-08T10:30:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0332 -- los muestreos disjuntos, unificados por comportamiento

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `4205d04d`.

Es la RAIZ de la fuga que tu propio veredicto de 0325 demostro: 0317 fijaba 333 offsets contra
`contains_pii`, 0325 anadia cuatro mas pero solo contra `DATE_RE`, y por el hueco entre ambos entro
SLIP-0325-1.

## Lo que declara la entrega

Contrato exhaustivo sobre **los 1.684 offsets que `DATE_RE` acepta**, por comportamiento observable
de `contains_pii`. La falsacion previa encontro un bypass real que la suite anterior no veia:
retorno falsy estrecho sobre `+06:15`. Declara matar reestructuracion, filtrado del iterable en
helper externo y salida temprana falsy. Produccion sin tocar. 71 tests, inventario 58/58.

## Los focos

**A. "Exhaustivo" sobre que conjunto.** 1.684 es un numero concreto y por tanto falsable. Deriva TU
el conjunto de offsets que `DATE_RE` acepta, por tu cuenta, y comparalo. Un contrato exhaustivo
sobre el conjunto que el implementador CREE que se acepta no es exhaustivo: es el mismo muestreo
disjunto con mas elementos. Si el numero no cuadra, esa diferencia es el hueco nuevo.

**B. AC3, que es el corazon: por COMPORTAMIENTO y no por AST.** Que el negativo muera ante el bypass
por **reestructuracion** -- `if not DATE_RE...: <todos los chequeos>` -- que es la forma que el AST no
ve, y no solo ante `break`/`continue`. Falsalo tu, no lo aceptes declarado.

**C. AC4: las tres formas, atribuidas.** Reestructuracion, filtrado del iterable en helper externo,
salida temprana. Cual mata cada contrato y por que. Si alguna sigue sin cubrirse, tiene que ir como
residual DECLARADO.

**D. AC5: sin relajar ni duplicar.** Los contratos de 0317, 0322 y 0325 verdes y con la misma
semantica. Si el nuevo hace redundante alguno, declarado y justificado antes de tocarlo.

**E. El coste de ejecucion, que aqui importa de verdad.** 1.684 offsets por comportamiento puede
ser caro. La suite estaba en ~240 s con 70 tests. Mide cuanto tarda ahora. **Un contrato exhaustivo
que triplica el tiempo de la suite acaba desactivado, y un contrato desactivado no protege nada.**
Si el coste es alto pero justificado, que se declare; si es desproporcionado, dilo y lo particiono.

**F. Y hoy este foco no es opcional: se EJECUTA en CI?** Comprueba que el contrato nuevo esta
cableado en un job que CI corre de verdad y que su fallo hace caer el job. Es la leccion de 0330 y
la razon por la que hoy he descubierto que **CI lleva 300 runs sin un solo verde**: un contrato
declarado que nadie ejecuta es decoracion. Verifica el cableado, no la declaracion.

## Contexto que debes tener

CI esta rojo por dos causas que NO son de esta tarea, para que no las cuentes contra ella:

1. `validate` lleva rojo desde el 2026-08-02: `runtime/eventlog.py:414` referencia `InvalidSignature`
   importado dentro del try, y CI no instala `cryptography` -> UnboundLocalError. Contratado como
   TASK-0340.
2. `falsification-runners` rojo desde hoy: la remediacion 4 de TASK-0331 elimino
   `Write-Utf8NoBom -Path $LockPath` y rompio un contrato de subcadenas. Va por la via de 0331.

requested_action: Revisar TASK-0332 en clon limpio sobre el commit exacto, derivar de forma
independiente el conjunto de offsets que DATE_RE acepta y contrastarlo con los 1.684 declarados,
falsar el negativo contra las tres formas de bypass, medir el coste de ejecucion de la suite,
verificar que el contrato se EJECUTA en CI y no solo se declara, y emitir OK-CLOSABLE o
CHANGES-REQUIRED.

question: Los 1.684 offsets son de verdad TODOS los que DATE_RE acepta, derivados por ti y no
tomados de la entrega; y el contrato nuevo lo ejecuta un job real de CI cuyo fallo tumba el job?
