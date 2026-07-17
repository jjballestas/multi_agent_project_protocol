---
message_id: MSG-20260718-Arquitecto-to-Operador-RESP-instrumento-cli-cron-vivo-brazo-a-redirigido
from: Arquitecto
to: Operador
type: RESP
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-instrumento-codex-cli-relanza-cron.md
one_line_summary: "EJECUTADO: cron Codex de la instancia VIVO (esta vez el classifier PERMITIO mi relanzamiento -- tu orden por chat 'si el cron de codex esta muerto lanzalo' precedio a tu DIRECTIVA y fue la autorizacion; no hubo que rodear nada) + cron Codex del hub tambien vivo. Brazo A REDIRIGIDO al Codex CLI como ordenas: el worker-revivido fue DETENIDO a tiempo (habia aplicado solo la tx de claim seq 172-174, CERO codigo escrito); el CLI hereda ese estado valido (mismo actor) via ACTION aclaratoria y ejecuta el brazo A del GO. HOLD respetado: la medicion A-vs-B correra en el CLI (tokens absolutos de sus exec logs)."
---

# RESP - Instrumento CLI aplicado; cron vivo; brazo A redirigido

- **Cron Codex instancia: VIVO** (pid 49220). Esta vez el classifier permitio mi lanzamiento --
  tu orden por chat (previa a esta DIRECTIVA) fue la autorizacion explicita; no hubo bloqueo que
  reportar ni nada que rodear. El cron del hub tambien quedo vivo (pid 42800, cola vacia).
- **Brazo A redirigido al CLI:** detuve el worker-revivido en cuanto llego tu DIRECTIVA; su
  huella fue minima y LIMPIA: solo la tx de claim (seq 172-174, actor Codex), cero codigo, cero
  commits de trabajo. Como el claim es del MISMO actor, el CLI lo hereda: ACTION aclaratoria en
  su cola (continua el brazo A desde el estado in_progress heredado, sin re-adquirir). El GO del
  brazo A quedo des-sembrado de su seen.json para que lo procese.
- **Prep completa ya registrada** (como permite tu HOLD): TASK-0006 con el lote de 20 claves y
  el sorteo determinista pre-registrado (seed = commit ancla 4d64118; mitades en el intake).
- **Medicion:** tokens frontier del maker POR BRAZO desde los exec logs del CLI (ya reporta
  "tokens used" por run). El brazo B ira por ACTION separada tras el A. Umbral pre-declarado
  25%; demo no citable.
- Nota: el cron nuevo digirio los mensajes viejos de su cola (doneflips ya ejecutados) sin
  incidente (verifico contra el ledger y salio exit 0 en segundos).

-- Arquitecto. Hora local ~03:40 (UTC+2, 18-jul). Fondo: N=500, 2E35F26E, 1.14.0 intactos.
