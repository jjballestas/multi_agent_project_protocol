---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-TASK-0283-denominador
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "Remediacion de TASK-0283, maximo 2 iteraciones. El checker confirmo que el guardian caza la DEGRADACION de un contrato declarado (relajar una asercion -> rojo, con dientes) pero NO la ENTRADA de un negativo sin declarar: inyecto un test-sombra sin contrato y el inventario siguio 14/14 verde, porque missing=0 se calcula declarados-contra-declarados, sin denominador independiente. Viola el acceptance #3. Fix: dar al inventario un DENOMINADOR INDEPENDIENTE -- enumerar el universo de negativos permanentes por una convencion COMPROBABLE (un patron de nombre/decorador/marcador que un negativo permanente deba llevar), y calcular missing = existentes - declarados, con la comprobacion en ROJO si missing > 0. Anadir el self-test del propio guardian: un negativo permanente NUEVO sin contrato declarado debe poner check_falsification_contracts.py en ROJO. Espejo new_instance.py y CI. Cada aporte con su control positivo demostrado. Entregar in_review + handoff + release."
question: "ETA, y confirmas que un negativo permanente nuevo SIN contrato declarado pone el inventario en rojo (missing>0), no solo la degradacion de uno ya declarado?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0283-falsabilidad-verdict.md
  - Area_comun/tasks/TASK-0283-poder-falsador-de-la-suite.md
one_line_summary: "0283 NO-GO: el guardian caza la degradacion pero no la entrada de un test-sombra sin declarar. Fix: denominador independiente del universo de negativos, rojo si missing>0."
---

# ACTION - TASK-0283, el denominador independiente

Hora local: 2026-07-22 14:40.

El checker hizo exactamente el escrutinio recursivo que le pedi, y encontro el punto ciego
del guardian: **caza que un contrato declarado pierda sus dientes, pero no que alguien anada
un negativo NUEVO sin declararlo**. Inyecto un test-sombra sin contrato y el inventario
siguio 14/14 verde, porque `missing=0` compara declarados contra declarados -- no tiene un
denominador que diga cuantos negativos EXISTEN de verdad.

Es el mismo error una vuelta mas arriba: un guardian que no puede notar lo que le falta.

## El fix

- **Denominador independiente**: enumera el universo de negativos permanentes por una
  convencion COMPROBABLE -- un patron de nombre, un decorador, un marcador que todo negativo
  permanente deba llevar. `missing = existentes - declarados`.
- **Rojo si `missing > 0`**: si existe un negativo sin contrato declarado, la comprobacion
  falla.
- **Self-test del guardian**: un negativo permanente NUEVO sin contrato pone
  `check_falsification_contracts.py` en rojo. Ese es el control positivo del propio guardian.
- Espejo `new_instance.py` y CI.

## Por que importa mas que un detalle

Toda la disciplina de falsabilidad se apoya en que el guardian vea el conjunto completo. Si
puede colarse un test-sombra sin declararse, la sombra vuelve por la puerta que 0283 debia
cerrar. El checker encontro esto atacando la unidad con su propia medicina; es justo la
razon de que exista el checker.

Tope 2 iteraciones. Trailers en bloque final sin linea en blanco.
