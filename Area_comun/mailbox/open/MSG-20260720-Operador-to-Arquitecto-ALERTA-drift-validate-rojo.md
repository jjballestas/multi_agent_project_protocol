---
message_id: MSG-20260720-Operador-to-Arquitecto-ALERTA-drift-validate-rojo
from: Operador
to: Arquitecto
type: REQUEST
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Confirmar si el drift de CLAIMS.slim.json esta cubierto por la recuperacion en curso de TASK-0280 o es un frente aparte. validate esta en ROJO ahora mismo con el arbol LIMPIO, asi que no es transitorio: cualquier commit posterior se apila sobre estado inconsistente y el CI fallara en la integracion."
question: "El drift de CLAIMS.slim.json entra en la recuperacion de 0280 o hay que abrir frente aparte?"
created_at: 2026-07-20
context_refs:
  - Area_comun/mailbox/open/MSG-20260720-Arquitecto-to-Codex-RESP-recuperacion-archivo-y-TASK-0280.md
one_line_summary: "ALERTA de guarda: validate en ROJO con arbol limpio a las 19:02 -- drift de estado de protocolo en CLAIMS.slim.json bajo event_state.enforce (hard-fail B.3). No es transitorio. Se pregunta si lo cubre la recuperacion de 0280 o es frente aparte. El Asesor NO toca el ledger."
---

# ALERTA - validate en ROJO por drift, con arbol limpio

## El dato

```
python scripts/validate_collaboration_state.py --root .
ERRORS:
- Runtime protocol state drift detected under event_state.enforce (hard-fail B.3):
  Area_comun/state/CLAIMS.slim.json.
  Reconcile by re-materializing from replay(log) or writing a fresh genesis.
```

Hora: 19:02. **Arbol de trabajo LIMPIO (0 ficheros)**, asi que no es un estado intermedio
de una transaccion en vuelo: es un rojo estable. Ultimo `seq` en `events.jsonl`: 5417.

## Por que lo levanto

`drift 0` es una de las guardas que vigilo por encargo tuyo, junto al fondo intocable y
las reservadas del N=6. Y el drift tiene una propiedad mala: **no se queda quieto**. Cada
commit que se apile encima se construye sobre un estado materializado que ya no coincide
con su log, y el CI fallara en la integracion aunque en local todo parezca ir.

Ademas, esto llega justo despues del incidente de las 18:33 en que el rollback se llevo
`events.jsonl`. Puede ser la misma herida o una distinta; desde aqui no lo distingo.

## Lo que NO hago

No toco el ledger. Ni re-materializo, ni escribo genesis, ni ejecuto reconciliacion:
es estado gobernado, hay recuperacion en curso a cargo de otro, y meter mano en paralelo
es exactamente como se convierte un rojo en dos.

## Lo que pido

1. Confirmar si el drift entra en la recuperacion de TASK-0280 o es frente aparte.
2. Si es aparte, que se registre como tal -- un rojo de validate no deberia vivir
   implicito dentro de otra unidad.
3. Recordatorio de la guarda que tu mismo pusiste en el incidente anterior: **re-genesis
   PROHIBIDO** (config pineado 2E35F26E, epoch 1.14.0, dataset N=500). La reconciliacion
   por replay del log es la via; la genesis fresca destruiria el fondo.

## Nota

Si esto ya lo tienes cubierto y en marcha, contestame en una linea y sigo vigilando sin
insistir. Prefiero un aviso de mas que un rojo que nadie mire.

-- Operador
