---
message_id: MSG-20260720-Arquitecto-to-Operador-RESP-0273-registrada-medicion-poda
from: Arquitecto
to: Operador
type: RESP
status: archived
requires_response: true
response_owner: Operador
requested_action: "Decidir el GO de TASK-0273 con la medicion ya en mano: prune_state --apply tarda 86.7-89.1 s INCLUSO SIN poda vencida (vs --check 0.31-0.61 s). El dato refuerza tu reparto y anade una pieza al acceptance (camino no-op barato). Nada arranca sin tu GO."
question: "Con --apply en ~87-89s (y ~87s de ellos evitables en el camino no-op), das GO a TASK-0273 tal como esta registrada?"
created_at: 2026-07-20
context_refs:
  - Area_comun/mailbox/open/MSG-20260720-Operador-to-Arquitecto-DIRECTIVA-deadlock-poda-reparto.md
  - Area_comun/tasks/TASK-0273-deadlock-poda-claim-reparto.md
one_line_summary: "RESP + MEDICION (12:20 local): TASK-0273 registrada con tu reparto (aviso local / poda coordinada en checkpoint / CI exige) y el numero que pediste ANTES del GO -- prune_state --apply = 89.055s y 86.732s en dos corridas, con poda NO vencida; --check = 0.31-0.61s. El apply paga el ciclo transaccional completo aunque no haya nada que podar: ~87s evitables. Anadido al acceptance el camino no-op barato."
---

# RESP - TASK-0273 registrada + el numero que pediste

Hora local: 2026-07-20 12:20. Registrada en proposed con intake DoR completo, priority
high, con tus tres piezas tal cual (aviso local que no bloquea / poda coordinada en el
checkpoint / CI la exige) y sus limites (claim-como-lock, validate y drift NO se
relajan; espejo born-operational y conjunto adoptable por la leccion .githooks).

## La medicion, antes del GO como pediste

Ventana quieta, cero claims activos, arbol gobernado limpio, dos corridas:

| comando | tiempo | |
|---|---|---|
| `prune_state --check` | 0.307 s / 0.612 s | barato, ya lo tenias |
| `prune_state --apply` | **89.055 s** / **86.732 s** | **con la poda NO vencida** |

El hallazgo que no esperaba: **el `--apply` cuesta ~87-89 s aunque no haya NADA que
podar**. No es que podar sea caro por el volumen: es que ejecuta la maquinaria
transaccional completa (claim acquire -> intent -> release -> materializacion) antes de
constatar que no procede. La mayor parte de ese minuto y medio es evitable.

## Que cambia en el diseno (ya anotado en el acceptance)

1. **Tu reparto sale reforzado.** Con ~87 s por invocacion, dejar que el gate dispare la
   poda en medio del trabajo de cualquiera es peor de lo que parecia: no es solo el
   bloqueo, es minuto y medio de latencia sobre un commit ajeno. Atarla al checkpoint
   (una vez por ciclo, en quietud) es claramente correcto.
2. **Anadi una pieza al acceptance**: el camino no-op debe salir barato (comparable a
   `--check`) cuando no hay nada que podar. Sin eso, la poda coordinada seguiria
   costando ~90 s por checkpoint sin razon, y la tentacion de saltarsela volveria.
3. La coordinacion **no es gratis**, asi que la barrera explicita a los peers se queda
   como excepcion (tal como la planteaste), no como rutina.

## Estado de la tanda

DONE: 0257, 0267, 0268, 0270, 0271. E6 resuelta (E6-A permanente). 0258 in_review con su
re-juicio de lectura ruteado. En ready esperando GO: 0272 (seen-burn, ya con tus dos
aportes en el acceptance) y ahora 0273. Cola pendiente: 0259-0264 + gate 0265.

Pendientes tuyos: GO de 0273, GO del build-open N=6 (respondido ADELANTABLE con evidencia
verificada en NOVA), y 0272 ya tiene tu GO y esta en cola del maker.
