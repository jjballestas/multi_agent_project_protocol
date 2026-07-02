---
message_id: MSG-20260703-Operador-to-Arquitecto-ACTION-resolucion-dual-sesion
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Operador
created_at: 2026-07-03
context_refs:
  - MSG-20260703-Arquitecto-to-Operador-FYI-anomalia-dual-sesion-arquitecto
  - Area_comun/state/CLAIMS.json
one_line_summary: "Resolucion dual-sesion: QUEDA la sesion nueva (prompt 20260703); la anterior hace stand-down graceful; fix permanente = session-lease de instancia unica."
requested_action: "[DIRECTIVA] (1) DISCRIMINADOR: si tu sesion arranco 2026-07-03 ~00:42 con el prompt de sesion 20260703 -> CONTINUAS como unico Arquitecto. Si tu sesion es ANTERIOR a esa hora -> STAND-DOWN graceful al leer esto: concluye la operacion atomica en vuelo si la hay, no inicies coordinaciones nuevas, suelta tus claims activos, deja un FYI de cierre de 1 linea y finaliza el loop. (2) La sesion QUE QUEDA asume TODOS los carriles (0241 con su claim + coordinacion del 0242 ya en GO valido; el GO NO se re-emite). (3) FIX PERMANENTE anti-recurrencia: registra la leccion e implementa el guard de instancia unica: al arrancar como Arquitecto, escribe/verifica un lease de sesion en personal/Arquitecto/.session-lease (session_start_ts + nonce + heartbeat por turno); si al arrancar existe un lease FRESCO de otra sesion, NO coordinas y consultas al Operador. Anota el guard en tu prompt de arranque y en la skill arquitecto-monitor-coordina. (4) FYI de confirmacion al Operador cuando la dualidad quede resuelta."
question: "Confirmas stand-down de la sesion anterior + lease de instancia unica implementado?"
---

# ACTION - Resolucion de la anomalia dual-sesion (DECISION-0018)

El Operador ACEPTA la recomendacion del FYI: queda la sesion NUEVA (contexto
fresco del prompt 20260703), la ANTERIOR se retira. Bien detectada la anomalia y
correcta la particion por claims como mitigacion temporal.

Contexto del fix permanente: el hueco "sin guard de instancia unica" ya estaba
identificado en la familia de los crons (jams post-0235); esta anomalia demuestra
que tambien aplica a las SESIONES interactivas del Arquitecto. El lease de sesion
es el mismo patron exec-lease en miniatura: barato y cierra la clase entera de
colision silenciosa (dos actores con la misma firma no se ven entre si).

[RECOMENDACION] El diseno exacto del lease (campos, TTL del heartbeat, donde se
verifica) es tuyo; el requisito duro es: dos sesiones Arquitecto no deben poder
coordinar a la vez sin que la segunda lo detecte ANTES de escribir nada compartido.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
