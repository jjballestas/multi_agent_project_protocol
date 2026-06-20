---
message_id: MSG-20260620-Analista-to-Operador-relay-veredicto-adversarial
type: REVIEW
task_id: none
from: Analista
to: Operador
status: open
requires_response: false
response_owner: none
one_line_summary: Voz externa adversarial sobre el RELAY del intake (anclado en canonico fc31bfe + Zeus 42e7931). 2 CAMBIOS CRITICOS (1 impersonacion ya en canonico, 3 accountability), 3 cambios, 2 PASA-con-nota. Recomiendo NO ratificar hasta cerrar #1 y #3.
requested_action: "Leer el veredicto antes de ratificar DECISION-0052/ext2/TASK-0134. Llevar los CAMBIOS a la SPEC del Arquitecto. No promueve, no autora SPEC, no muta estado."
context_refs:
  - Area_comun/artifacts/ANALISTA-intake-relay-veredicto-adversarial.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0052-operator-intake-relay-signer.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext2-intake-happy-path.md
  - personal/Arquitecto/carril_A/DRAFT-TASK-0134-intake-happy-path-relay.md
---

# Veredicto adversarial - RELAY del intake (anclado en CANONICO)

Pasada de voz externa (escepticismo: el diseno puede estar mal hasta probar lo contrario). Anclada en
canonico: drafts en fc31bfe, codigo del front en Zeus-protocol 42e7931 (el intake YA mergeado, TASK-0133).
Verifique yo mismo el codigo, no asumi los drafts. Detalle falsable en el artefacto.

CABECERA: el relay (firmar como Arquitecto en nombre del Operador) es razonable para el problema estrecho
(Operador no firmante, no tocar epoca pinned). PERO destapa un DEFECTO DE SEGURIDAD CRITICO que el relay no
cierra y que YA ESTA en el canonico.

- **1) SEGURIDAD/alcance - CAMBIO CRITICO.** El relay NO esta acotado y NO hay prueba negativa. El front
  canonico HOY (server.js): `actorId = action.actorId || payload.actorId || "Arquitecto"` (el cliente
  elige actor, o cae a Arquitecto) y para acciones no-intake los `intents` son ARBITRARIOS del cliente
  (solo se chequea el kind, no la forma). Endpoint en 127.0.0.1 SIN auth. -> un POST local puede forjar una
  decision/claim/task_status atestado FIRMADO COMO ARQUITECTO (el enforce no lo para: Arquitecto es firmante
  y el claim va en la misma tx). El "no-bypass" actual es string-match, no protege. Correccion: nunca confiar
  en payload.actorId; cada accion = builder server-side con forma estricta; relay-como-Arquitecto SOLO para
  la forma exacta del intake; PRUEBA NEGATIVA permanente (relayar otro intent como Arquitecto -> RECHAZADO).
  Es anomalia DECISION-0018: ya esta mergeado; remediarlo en TASK-0134, no solo "no empeorarlo".

- **3) ACCOUNTABILITY - CAMBIO.** El Arquitecto firma texto que no autoro ni reviso. "relayo != avalo" vive
  en un campo; la semantica #4 dice "Arquitecto firmo". Riesgo de lavado en el dataset de tesis. Correccion:
  relayed/endorsed first-class; DECISION-0052 declara "firma = origen+transporte, NO aval; el aval es la SPEC
  despues"; test que un relayado no cuente como autorado por el Arquitecto.

- **2) atribucion - PASA+cambio:** honesta en payload (author=Operador/relayed_by=Arquitecto); falta test de
  RENDER (firmante=Arquitecto, ningun verde "Operador firmo").
- **4) #4 intacto - PASA+cambio:** relay no toca config/genesis/keys (correcto, evita re-genesis); pero
  asertar genesis/keys/version byte-identicos, no solo drift 0 (drift 0 es necesario, no suficiente).
- **5) verificacion - PASA fuerte+cambio:** AC15 happy-path cierra el miss; exigir write REAL (no mock) +
  test de comportamiento permanente en CI.
- **6) PII - PASA+nota:** redaccion estructural real (NIT/razon social/SQL + ASCII), no depende de DEF-PII;
  PERO es por PATRONES best-effort, NO cero-PII garantizado (un nombre/email/telefono pasaria). No
  sobre-afirmar "PII-free"; DEF-PII (TASK-0118) sigue el gate.
- **7) neutralidad - PASA:** mecanismo generico, sin dominio en el core.

RECOMENDACION: NO ratificar hasta cerrar #1 (impersonacion) y #3 (accountability); los demas cambios van en
la SPEC/TASK-0134. No promovi, no autore la SPEC, no mute estado.
