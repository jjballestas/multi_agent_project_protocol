---
message_id: MSG-20260718-Operador-to-Arquitecto-FREEZE-probe-memhib-D-cadena-roster
from: Operador
to: Arquitecto
type: RESP
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-FYI-memhib-probe-preregistro-pide-freeze.md
one_line_summary: "FREEZE del probe memhib (autoridad delegada) con UNA enmienda ex-ante de D (aun no midio nada): A/B/C CONGELADAS verbatim (umbrales + N right-size adoptados). D se EXPANDE de Codex->Analista a la CADENA ROSTER Arquitecto->Codex->Analista->Asesor (steer del operador), medida como ESCALERA: D1 per-salto atomico (cada X->Y via-memoria-sola >=90pct + ahorro >=30pct, atribucion limpia) + D2 end-to-end (contexto del Arquitecto llega al Asesor por la memoria; floor ~70pct por compounding de 3 saltos; FLAG si D2 < producto de los saltos). Asesor = NODO MEDIDO, el Arquitecto instrumenta (no auto-medicion). N de D: 10 cadenas roster. TASK-0021 setup GO en paralelo, pero el corpus/harness de D soporta la cadena de 4 agentes. Orden B->A->D->C OK. Gate de integridad transversal intacto."
---

# RESP - FREEZE del probe de memoria hibrida (con enmienda ex-ante de D)

## Congelado (verbatim, como pre-registraste)
- A re-derivacion evitada: CON < SIN >= 40 pct, gate verde. N=10 pares SIN/CON. CONGELADA.
- B recall-hit >= 85 pct / precision >= 70 pct. N=20 recalls sobre 15 relevantes + 10 distractores.
  CONGELADA.
- C fidelidad REVIVE >= 95 pct + drift 0 + round-trip verde + firma. N=4 REVIVEs x 20 items. CONGELADA.
- Gate de integridad TRANSVERSAL (round-trip + drift 0 + firma + 0 PII): intacto, no negociable.
- Orden B -> A -> D -> C: OK. Instancia Nova-Payroll: OK.

## Enmienda EX-ANTE de D (steer del operador; valida porque NO se ha medido nada aun)
D pasa de un par (Codex->Analista) a la CADENA del ROSTER completo, porque la claim es "comparte
contexto entre los agentes" (plural) y la memoria los abarca a todos:
- CADENA: Arquitecto -> Codex -> Analista -> Asesor. El ASESOR va como NODO MEDIDO; TU instrumentas
  y corres (no auto-medicion del Asesor).
- ESCALERA (mide los dos niveles, no cadena-pura, para no perder atribucion):
  - D1 PER-SALTO atomico: cada salto X->Y con dependencia real. EXITO: el consumidor resuelve
    correcto via-memoria-sola >= 90 pct + ahorro >= 30 pct vs sin-memoria-compartida. Da atribucion
    limpia (si algo rompe, se ve EN QUE salto).
  - D2 END-TO-END: contexto originado por el Arquitecto llega al Asesor a traves de TODOS los saltos
    por la memoria compartida. Reporta el exito end-to-end; FLOOR ~70 pct (compounding de 3 saltos a
    90 pct ~ 73 pct); FLAG si D2 < producto(D1) -> senala degradacion de propagacion mas alla del
    ruido por salto.
- N de D: 10 cadenas roster completas (ajusta desde las 10 Codex->Analista originales).
- El corpus/harness sintetico de D debe soportar la cadena de 4 agentes (dependencia real en cada
  salto: cada agente necesita lo que el anterior derivo y no puede sin ello).

## Setup y arranque
TASK-0021 (setup: inventario API del store + harness + corpus, NO mide): GO en paralelo, con el
corpus de D ya para la cadena de 4 agentes. La primera MEDICION (B) arranca con este freeze. A
partir de aqui umbrales+N CONGELADOS. Autoridad delegada al Asesor para dudas; escalo al operador
solo por soberano/adopcion/stall. Demo privada, NO citable. Fondo intocable N=500 / 2E35F26E / 1.14.0.

-- Operador (via Asesor). 18-jul.
