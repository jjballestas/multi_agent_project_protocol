---
message_id: MSG-20260720-Arquitecto-to-Operador-RESP-ventana-N6-adelantable
from: Arquitecto
to: Operador
type: RESP
status: open
requires_response: false
created_at: 2026-07-20
context_refs:
  - Area_comun/mailbox/open/MSG-20260720-Operador-to-Arquitecto-REQUEST-ventana-N6-julian-entregables-previos.md
one_line_summary: "RESP ventana N=6 (08:25 local): SI SE PUEDE ADELANTAR -- los DOS entregables previos ya estan CERRADOS y VERIFICADOS en NOVA (corpus E2: 35 unidades enumeradas, commit 35a1b4e del 14-jul; BR-C4: TASK-9392 done con gate firmado y review independiente GO, maker jheredia). Cero dependencia futura de Julian en previos. La unica puerta real es TU GO. Un riesgo que anado: CONGELAR la propagacion 0266 hacia NOVA hasta post-medicion (no cambiar el entorno sellado a mitad de ventana)."
---

# RESP - la ventana del N=6 es adelantable; la unica puerta es tu GO

Hora local: 2026-07-20 08:25. Verificado en el arbol de NOVA (watch read-only,
dos-trios), no de memoria. Tus 4 preguntas en orden:

## 1. Estado real de los entregables previos: AMBOS CERRADOS

- **Corpus E2** (objetivo <=25-jul): ENTREGADO el 14-jul -- commit 35a1b4e
  "docs(corpus): Encargo 2 -- corpus Contabilidad enumerable (35 unidades) + FYI al
  hub". Once dias antes del objetivo.
- **BR-C4** (deadline duro <=29-jul): ENTREGADO Y VERIFICADO -- TASK-9392 en su ledger:
  review independiente GO ratificada (ab64a5d, analista:v1), gate firmado cerrado
  (b984cd4), done-flip por jheredia (22c8ed8), FYI de cierre "VERDE para el sello
  Etapa 2" (6e6c3d1) y smoke fresco del maker (2a5ba92). Con control negativo, como
  exigia el encargo.

El "gated post-30-jul" era secuencia operativa sobre estos dos entregables, y ambos ya
no existen como espera. Tu lectura es correcta: no queda restriccion cientifica ni
operativa de fecha.

## 2. Dependen de Julian? YA NO

BR-C4 SI consumio tiempo de jheredia -- pero ya esta entregado. El corpus fue del
Arquitecto de NOVA. Adelantar la medicion NO desplaza ningun previo: no hay previos
vivos.

## 3. Que hace falta operativamente para abrir manana

1. **TU GO del build-open** -- es lo unico que falta. El resto ya existe: TASK-9401..
   9406 en ready y reservadas (freeze intacto, commit dc8f0e9 de NOVA), WIRING-F33 de
   medicion por unidad, RUNBOOK de Julian escrito, jheredia:v1 operativo.
2. **Checker de la ceremonia**: la del N=6 usa el trio DE NOVA (su Analista one-shot
   con firma analista:v1, el mismo que acaba de cerrar BR-C4) -- NO compite con el
   checker del hub que sostiene la cola 0103. Verificado el patron en el cierre de
   9392. Si algo de la ceremonia s.11 exigiera al checker del hub, se secuencia: la
   segunda mitad de la 0103 no tiene fecha y es pausable.
3. Nada mas. La ceremonia de clones esta descrita en el runbook.

## 4. Riesgos de adelantar que yo veo y tu no mencionaste

- **EL IMPORTANTE -- congelar la propagacion 0266 hacia NOVA**: la 0103 esta
  propagando harness nuevo (hook, upgrade_instance) y TASK-0266 esta en ready para
  llevar eso a instancias. NOVA debe medir con SU entorno SELLADO tal como esta --
  propagarle el harness nuevo entre el sello y la medicion cambiaria el entorno
  preregistrado. Propongo: 0266 queda EXPLICITAMENTE excluida de NOVA hasta
  post-medicion N=6 (lo anoto en su intake si das el GO del adelanto).
- Menores: el checker del hub esta cargado con la 0103 (mitigado por el punto 3.2);
  y conviene que el primer build medido de Julian no coincida con ventanas de
  mantenimiento del hub (coordinacion trivial de horario).

## Resumen

Adelantable en cuanto firmes. Nada arranca sin tu GO, como ordenas. Si lo das: (a)
anoto la exclusion de NOVA en 0266, (b) confirmo con el Arquitecto de NOVA la
disponibilidad de su checker one-shot para la ceremonia, y (c) Julian puede construir
la primera unidad MEDIDA en su proxima ventana.

## Guardas

Reservadas N=6 intactas hasta tu GO; fondo intocable (2E35F26E / epoch 1.14.0 /
N=500); firewall anti-HARKing intacto (el sello previo es justo lo que hace seguro el
adelanto); sin supervised_autonomy ni real_invoker.
