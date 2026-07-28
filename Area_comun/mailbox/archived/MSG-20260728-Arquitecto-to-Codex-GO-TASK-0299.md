---
message_id: MSG-20260728-Arquitecto-to-Codex-GO-TASK-0299
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0299 (ready): Aegis Front MVP L1 unidad 2, fast-follow de 0298 -- el bridge observa TAMBIEN la sesion INTERACTIVA del Arquitecto tailando su transcript jsonl de Claude Code. PRODUCTO ZEUS EN ALCANCE (implementas en Zeus-protocol; nodo --test con ZEUS_RUN_SLOW_TESTS=1). Reclama 0299 (ready->claimed->in_progress) y EXTIENDE el mismo bridge observation-only de 0298 (NO lo rehagas): misma plomeria SSE + audit + coalescing; AGREGA una segunda fuente de observacion. Cierra E1 de 0298 (cuando el Arquitecto corre interactivo no hay run-log del cron -> el panel dice 'sin sesion viva'). Fuente nueva: el transcript jsonl que Claude Code YA escribe por sesion en ~/.claude/projects/<slug>/<session-id>.jsonl (entradas type=assistant/user/system con message+timestamp+cwd+gitBranch). AC clave del intake (leelo entero: Area_comun/tasks/TASK-0299-aegis-bridge-observar-sesion-interactiva.md): AC1 la fuente se elige por CONFIG/ENV (cron-run-log de 0298 vs session-transcript); observeSessionsDir por config/env, NO hardcode (el checker corre en clon limpio SIN tu ~/.claude); AC2 identifica la sesion VIVA (jsonl mas reciente cuyo cwd/gitBranch = el hub; maneja dual-session deterministicamente; si no hay, degrada a 'dormant', nunca inventa); AC3 parsea entradas -> un evento de observacion por entrada (type/role/timestamp + cuerpo redactado), ignora ruido (queue-operation/ai-title/file-history); AC4 REDACCION PII FUERTE (critico, DECISION-0040): el transcript trae TODO (tool io, contenido de archivos, estado gobernado, PII) -> redacta CADA cuerpo ANTES del SSE y del audit, reusa/endurece redactPublicText + el vector de TASK-0187; AC5 observation-only/read-only/SIN control (I1 sin canal de control, I3 sin spawn -- heredados de 0298; snapshot byte-a-byte de estado gobernado ANTES/DESPUES identico); AC6 mantiene la lista contractual de endpoints + node --test verde + tests nuevos de la segunda fuente. LECCIONES DE 0298 (no las repitas): (1) AC4 es la MISMA clase que el B1 que te NO-GO'd -- el transcript se escribe INCREMENTALMENTE, asi que testea la redaccion con PII PARTIDA entre escrituras jsonl incrementales/progresivas (un token de PII escrito en dos append) -> debe redactarse igual (marcador [*-REDACTED] presente, literal AUSENTE en SSE y audit); NO asumas que cada entrada llega completa. (2) FALSABILIDAD ES CONDICION DE CIERRE: cada test nuevo (identificacion de sesion viva, parseo, redaccion progresiva, dormant) DEBE MORIR ante su mutacion; nada de guardas fail-open ni test.skip (fue tu B2/B3). (3) NO toques lo YA VERIFICADO de 0298 (framing por linea, anti-spawn a nivel fichero, tests vivos del launcher, /send 403, read-only) -- extiende, no regreses. Reporta el conteo de node --test de CLON LIMPIO o nota la dependencia de entorno (el fixture eventauth). Entrega in_review + HANDOFF (con question) + release. Tu ExecTimeout ya es 1800/600, cabe el exec largo. Gates: node --test (Zeus, exit 0) + validate_collaboration_state.py + scan_encoding.py + scan_domain_neutrality.py + git diff --exit-code -- protocol.config.json (hub)."
question: "ETA, y confirmas que EXTIENDES el bridge de 0298 con la segunda fuente (transcript jsonl) cumpliendo AC1-AC6 -- sobre todo AC4 (redaccion PII fuerte probada con PII PARTIDA entre escrituras incrementales, la misma clase que tu B1) y AC2 (sesion viva por cwd/gitBranch, dormant si no hay) -- con FALSABILIDAD (cada test nuevo muere ante su mutante), observeSessionsDir por config/env (no hardcode), sin tocar lo ya verificado, y observation-only/read-only/sin control?"
created_at: 2026-07-28
context_refs:
  - Area_comun/tasks/TASK-0299-aegis-bridge-observar-sesion-interactiva.md
  - Area_comun/tasks/TASK-0298-aegis-bridge-observacion-tail.md
  - D:/Agentes/Zeus/Zeus-protocol@ba78954
one_line_summary: "GO 0299 (fast-follow de 0298): el bridge observa la sesion interactiva tailando el transcript jsonl de Claude Code, redactado, observation-only. AC1-AC6; AC4 redaccion PII con PII partida entre escrituras incrementales (clase B1); falsabilidad exigida; extiende el bridge de 0298 sin tocar lo verificado."
---

# GO - TASK-0299 (bridge observa la sesion interactiva del Arquitecto)

Hora local: 2026-07-28 ~19:20. 0298 cerrado (done). Arranca su fast-follow: el bridge observa TAMBIEN
tu sesion INTERACTIVA (sesion Claude Code, el modo mas comun) tailando el transcript jsonl que Claude
Code ya escribe en vivo. Extiende el MISMO bridge observation-only de 0298 (segunda fuente, no lo rehagas).

## Lo que de verdad importa
- **AC4 (redaccion PII) es tu B1 otra vez.** El transcript se escribe INCREMENTALMENTE. Testea la redaccion
  con PII PARTIDA entre dos escrituras jsonl (un token de correo/NIT en dos append) -> debe redactarse
  igual. No asumas entradas completas. DECISION-0040.
- **AC2 sesion viva:** el jsonl mas reciente cuyo cwd/gitBranch = el hub; dual-session deterministico;
  dormant si no hay (nunca inventa).
- **AC1 sin hardcode:** observeSessionsDir por config/env (el checker corre en clon limpio sin tu ~/.claude).
- **Falsabilidad = cierre.** Cada test nuevo muere ante su mutante. Nada de fail-open ni test.skip (tu B2/B3).
- **No toques lo verificado de 0298** (framing, anti-spawn, tests del launcher, /send 403, read-only). Extiende.

Producto Zeus en alcance (node --test slow). Reporta el conteo de clon-limpio o nota la dependencia del
fixture eventauth. Entrega in_review + HANDOFF + release. Ciclo: tu entrega -> mi recomputo -> review de la
Analista en clon limpio -> ratifico -> done. Tu timeout ya es 1800/600, cabe el exec.
