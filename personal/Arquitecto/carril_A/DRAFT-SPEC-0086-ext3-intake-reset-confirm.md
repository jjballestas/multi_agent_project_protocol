# DRAFT - Extension 3 de SPEC-0086: reset del formulario + confirmacion inequivoca del intake (RF-14)

> DRAFT en personal/Arquitecto; NO promovido. Triage del REQ-DCC3BC1A (semilla del operador, intake).
> UX READ-ONLY: NO nueva superficie de escritura -> EXTENSION de SPEC-0086 (RF-14), SIN DECISION.
> maker=Codex / checker=Arquitecto.

## Origen (REQ-DCC3BC1A, author=Operador)
"Tras un EXECUTE exitoso no se si se envio porque los campos siguen llenos; si lanzo otro puedo reenviar lo
mismo. Quiero que al confirmar OK el formulario se limpie y quede claro que se envio." (id + seq explicitos).
NOTA: el bug de campos-no-limpiados YA esta ensuciando submissions (manglo el titulo de REQ-FB27AF72 con
texto stale) -> esta pieza es PRIORITARIA.

## AC21 (NUEVO) - Reset del formulario + confirmacion inequivoca tras EXECUTE exitoso [comportamiento]
Tras un EXECUTE **exitoso** del intake (respuesta real del runtime: applied/ok con seq), el wizard:
- muestra un resultado INEQUIVOCO derivado de la respuesta REAL: "enviado - evento gobernado", con el **id
  del requisito (REQ-xxxx)** y el **seq** del evento;
- **RESETEA el formulario**: campos vacios, vuelve al paso 1 (capturar), estado borrador, PII-ack en falso;
- queda listo para una historia NUEVA sin texto stale (elimina el mangleo de la siguiente submission).

Honestidad (AC11, hereda): la confirmacion y el reset SOLO ocurren si el execute REALMENTE aplico (applied
true + seq). Si el execute **falla** o no se confirma -> NO se resetea, NO hay verde, se muestra el error real
(el borrador se conserva para reintentar). La idempotencia por id=hash ya protege el duplicado exacto; AC21 lo
hace EXPLICITO en la UI para evitar el reenvio accidental.

## test_plan (anadido)
- **Comportamiento (Zeus, permanente):** simular execute OK (applied+seq) -> asertar render del id+seq y que
  el formulario quedo reseteado (campos vacios, paso 1, borrador, piiAck=false). Simular execute FALLIDO ->
  asertar NO reset, NO verde, error real visible, borrador conservado. (Filosofia AC11: derivado de la
  respuesta real, no string estatico.)
- Conformidad de diseno (AC13) contra components/intake/ (estado resultado/wizard-4).

## Carry permanentes
AC11 (honestidad) / AC12 (routing) / AC13 (conformidad-diseno) verdes. SIN cambio de superficie de escritura
(no aplica AC18/19/20). #4 epoca 1.14.0 byte-identica (no toca ledger/config). Gates: validate exit 0 con/sin
secretos, drift 0, npm test verde, neutralidad/encoding 0.
