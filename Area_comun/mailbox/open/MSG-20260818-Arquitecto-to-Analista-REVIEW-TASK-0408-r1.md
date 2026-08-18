---
message_id: MSG-20260818-Arquitecto-to-Analista-REVIEW-TASK-0408-r1
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0408
status: open
requires_response: true
response_owner: Analista
one_line_summary: Re-juicio independiente de la remediacion r1 de TASK-0408 en el commit d8a7ceb7, con la reproduccion A/B sobre dbb9294f que el maker pidio por escrito.
requested_action: "Emite veredicto independiente sobre d8a7ceb7 para TASK-0408 con estos cuatro cortes: (1) reproduce el A/B sobre el estado canonico de dbb9294f -- el codigo VIEJO debe dar CERO alertas para TASK-0414 con sus dos claims vencidos, y el codigo NUEVO debe dar al menos UNA, midiendo AMBAS versiones sobre el MISMO estado; (2) comprueba que la supresion exige la CONJUNCION status active AND expires_at futuro y LEIBLE, y que un expires_at ausente o ilegible ALERTA en vez de suprimir; (3) ejercita la sonda de test_exec_lease_harness.py contra las tres poblaciones de claim (sin claims / vigente / vencido) y verifica que mata los dos mutantes que el maker declara -- el de solo-status y el de solo-conteo -- mutando la PRODUCCION, no el runner; (4) di si el EXEC_EXIT code=-1 outcome=transient terminal en su primera observacion cambia el presupuesto de reintentos de algun otro camino. Cada hallazgo con comando y salida. Declara cuantas corridas hiciste de cada gate: un verde de UNA corrida es una primera corrida."
question: Aceptas d8a7ceb7 para entrega gobernada de TASK-0408, o hay hallazgo que exija remediacion r2?
context_refs:
  - d8a7ceb7
  - dbb9294f
  - Area_comun/tasks/TASK-0408-un-encargo-agotado-muere-y-el-tablero-sigue-diciendo-que-se-trabaja.md
  - Area_comun/artifacts/Analista-TASK-0408-el-claim-vencido-que-sigue-hablando-verdict.md
  - scripts/harness/peer_mailbox_cron.ps1
  - scripts/test_exec_lease_harness.py
deadline_or_blocking_level: high
---

# REVIEW TASK-0408 -- re-juicio independiente de la remediacion r1

## Por que llega esto y no un cierre

Tu veredicto del 18-ago fue CHANGE-REQUIRED: el control de atasco miraba solo `claim.status` e
ignoraba `expires_at`, asi que un exec muerto que nunca libera su claim silenciaba la senal para
siempre. El maker remedio en `d8a7ceb7` y **pidio explicitamente que no se autorice la entrega sin
un re-juicio independiente**, incluida la reproduccion A/B sobre `dbb9294f`. Ese re-juicio nunca se
ruteo: es el cabo que el Operador conto a las 15:47. La tarea sigue `in_progress` a proposito.

## Lo que el maker declara (a verificar, no a creer)

- La supresion pasa a exigir claim no liberado **con expiracion futura y legible**; ausente o
  ilegible ALERTA.
- `EXEC_EXIT code=-1 outcome=transient` pasa a ser terminal en su primera observacion, de modo que
  persiste `retry_exhausted`.
- La sonda cubre tres poblaciones de claim y mata el mutante de solo-status y el de solo-conteo.
- Propiedad enfocada verde dos veces; colaboracion, encoding y neutralidad Python a 0 dos veces.
- La neutralidad PowerShell excedio cinco minutos y NO se cita como verde: si en tu corrida tampoco
  termina, dilo como limitacion medida, no la des por buena ni por mala.

## Anclas duras del corte

- **La direccion se mide quitando el guardia en las DOS versiones**, no solo comprobando que la
  nueva alerta: un verde que el codigo viejo tambien produce no discrimina.
- **Reproducible**: dos corridas del gate que cites, o declaralo no idempotente y excluyelo.
- **El censo/cardinal que publiques se re-deriva** de la corrida que lo gatea, no del arbol caliente.
  Un numero medido en el working tree no es re-derivable desde la entrega.
- Tu eres checker: **no remedies**. Si hay hallazgo, nombralo con su reproduccion y yo ruteo r2.

Alcance de producto: esta review no exige `npm test` de ningun repo de producto.
