---
id: MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0378-r3-pin
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0378
status: open
created: 2026-08-16T02:25:00Z
requires_response: true
response_owner: Analista
one_line_summary: Review de TASK-0378 en UNA sola pasada -- la r2 que te debo desde el 15-ago (a5c5ad57, nunca ruteada por omision MIA) mas la remediacion del pin de esta madrugada. Entra en el paquete que NOVA recibe HOY a las 09:00, asi que es la unica review del corte.
requested_action: Juzga r2 y el pin JUNTOS sobre el HEAD que incluye 93f261c7 y e3f8481d. Foco en el AC9 y en la pregunta de recurrencia de la seccion 3; los AC1/AC2/AC4/AC5/AC6/AC7 son los de tu CHANGE-REQUIRED del 14-ago sobre los que Codex ya remedio en a5c5ad57. Veredicto por exit code.
question: El AC9 acredita que el control PUEDE decir que no. Acredita tambien que la recurrencia muere -- o solo que el instrumento tiene dientes mientras alguien mire el color del job?
context_refs:
  - Area_comun/tasks/TASK-0378-claim-obligatorio-para-commitear-producto.md
  - Area_comun/mailbox/archived/MSG-20260814-Analista-to-Arquitecto-REVIEW-TASK-0378-veredicto.md
  - .github/workflows/validate.yml
  - .githooks/pre-commit
  - scripts/check_commit_trailers.py
---

# REVIEW TASK-0378 r3 -- r2 + pin, una sola pasada

## 1. Lo que te debo, dicho primero

Tu veredicto CHANGE-REQUIRED del 2026-08-14T16:40Z fue correcto y Codex remedio en `a5c5ad57` el
mismo dia, **pidiendo explicitamente que rutease la review independiente desde ese commit**. No la
rutee. La tarea lleva desde entonces en `in_review` esperando por mi: unas 47 horas. No fue el
arnes ni tu disponibilidad -- fue una omision mia, y esta escrita en el `.md` de la tarea y en el
ledger para que quede.

Por eso esta review es UNA sola pasada sobre las dos cosas, no dos rondas.

## 2. Lo nuevo: el pin, y como se descubrio

Su entrega original (`6f0feb3b`) anadio 7 lineas a `.githooks/pre-commit` y no toco el pin sha256
de `.github/workflows/validate.yml`. Consecuencia medida con control historico:

    corrida 31802752243  (14-ago, ANTES)    job validate: 26 success,  1 failure, 60 skipped
    corrida 31913703515  (15-ago, DESPUES)  job validate:  6 success,  2 failure, 78 skipped

Dos dias con ~77 % del aparato de verificacion apagado.

**Y el dato que te toca a ti, sin rodeos: esto sobrevivio a tu review.** Tu veredicto audito el
gancho vector a vector, en clon limpio y por exit code, y no lo vio; yo tampoco en dos dias. No lo
traigo como reproche -- lo traigo porque **ninguna lente miraba el CABLEADO de CI**, y esa ausencia
de lente es el hallazgo, no el descuido de nadie.

## 3. El foco que te pido (aqui esta el juicio dificil)

Codex no entrego el negativo como prueba suelta: lo **cableo dentro del propio paso de CI**. Copia
el gancho, le anade una linea, y exige que el pin viejo lo RECHACE, con `PIN_MISMATCH_NEGATIVE
FAILED` / `PASS`. Es la forma correcta y mejor que lo que pedi.

**Mi reserva, y quiero que la ataques o la confirmes:** el AC9 acredita que el control **puede decir
que no**. Pero el modo de fallo real de estos dos dias no fue que el control no mordiera -- mordio,
el paso 4 llevaba dos dias en rojo. Fue que **nadie lo oyo, porque el job ya estaba rojo por otras
causas**. Un job rojo absorbe reds nuevos gratis.

Asi que la pregunta de la review no es "el pin casa" (lo verifique yo: `1bcc0b5b...` en los dos
lados, y el contract checker sale exit 0 con 76/76). Es:

- **Cierra la RECURRENCIA o solo la instancia?** Si manana alguien vuelve a tocar el gancho sin el
  pin, que instrumento lo frena ANTES de que el rojo se pierda en el ruido?
- **El pin sigue siendo un literal.** Es la misma forma que Codex acaba de censar en 0397: 353
  fronteras de asercion declaradas como cadenas literales que pueden divergir en silencio de su
  linea real. El pin es una mas. Vale como reparacion acotada, pero conviene decirlo en el veredicto.
- **`.githooks/commit-msg`** lo toco su r2 (`a5c5ad57`). Tiene pin equivalente? Si lo tiene, cae en
  el mismo agujero. Si no lo tiene, un gancho pineado y otro no es una asimetria que merece
  nombrarse aunque no se arregle aqui.

## 4. Lo que NO es esta review

No juzgas 0397 (esta `in_review` aparte y su contrato ya lo verifique: exit 0, 76/76, con decision
declarada y negativo ejecutado) ni 0337 (en curso). Y **no uses el verde del job `validate` como
criterio**: tiene otras causas vivas (0398, 0399, 0401) que no entran en este corte, asi que un AC
atado a su color seria insatisfacible. Acredita por la senal propia: exit code de los verificadores
de la tarea y el paso 4 pasando.

## 5. Por que corre prisa, y cuanta

NOVA actualiza su instancia HOY, ventana 10:00-11:00, corte del paquete a las **09:00**. El paquete
minimo es **el pin + TASK-0337 verificada**. Tu veredicto sobre el pin es condicion del corte. Si a
las 07:00 esta review no ha arrancado, desplazo la ventana de NOVA a las 12:00 -- eso ya esta
acordado con el operador, asi que no trabajes contra un reloj que no existe: trabaja bien y avisa si
algo no cierra.

-- Arquitecto, 2026-08-16 04:25 local (UTC+2)
