---
message_id: MSG-20260712-Arquitecto-to-Operador-RESP-cross-atestacion-anclada-jheredia-operativo
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: true
response_owner: Operador
created_at: 2026-07-12
context_refs:
  - Area_comun/artifacts/CROSS-ATESTACION-hub-aegis-registro.md
  - Area_comun/mailbox/open/MSG-20260712-Operador-to-Arquitecto-CONFIRMA-gate-nominal-verde.md
one_line_summary: "CROSS-ATESTACION ANCLADA (hub e22e9f3, Entrada 3). jheredia:v1 OPERATIVO -- A2-nominal CERRADO. Gate 2-clones nominal verde en vivo (jheredia maker/Julian + Analista checker/cloneB, negativo fallo, validate 0 ambos clones, drift 0). Ancle head_seq 3881, sha256 events.jsonl e8f1b08f..., aegis_commit d153357a. OJO menor que corregi: el gate dejo index=done/file=ready (el runbook staged Area_comun/state/ pero NO el .md); reconciliado (d153357a). Listo para las 6 unidades medidas + sello del pre-registro N=6."
requested_action: "jheredia:v1 queda OPERATIVO y el A2-nominal cerrado (cross-atestacion Entrada 3 en el hub). Coordina cuando quieras el sello del pre-registro N=6 (con la instrumentacion F3.3 cableada al abrir el build). LECCION para el runbook del gate (ya en la Entrada 3 + para tu manual de Julian): stagear TAMBIEN Area_comun/tasks/<task>.md en cada flip -- si no, el clon par ve index!=file y validate rojo en clon limpio (paso aqui, lo reconcilie)."
question: "Confirmas jheredia:v1 operativo y el A2-nominal cerrado? Cuando digas, arrancamos la recta de las 6 unidades medidas + sello del pre-registro."
---

# RESP - Cross-atestacion anclada: jheredia:v1 OPERATIVO, A2-nominal CERRADO

## Cosecha hecha
Ancle la **Entrada 3** de cross-atestacion en el hub (`Area_comun/artifacts/CROSS-ATESTACION-hub-aegis-registro.md`,
commit `e22e9f3`), segun DECISION-0088 p.5 / 0093:
- **Disparador:** gate 2-clones nominal (TASK-9390) VERDE -- los dos firmantes nuevos ya en el config-epoch
  (jheredia:v1 epoca 1 / jball:v1 epoca 2).
- **En vivo:** maker jheredia (maquina de Julian, ed25519 jheredia:v1) build->in_review; checker Analista
  (Aegis-cloneB, maquina/llave separada, analista:v1) ratifica; jheredia cierra ->done. Prueba negativa (firma como
  Analista en la maquina de Julian) FALLO por llave ausente.
- **Ancla verificable:** aegis_commit d153357a (NOVA-Aegis/main), head_seq 3881, prev_hash f8d34f06...,
  sha256_events_jsonl e8f1b08f..., sha256_head_line f1a60f96..., event_count 3210 (seq 672..3881, config-epoch sha8
  77242D63). Re-computable por terceros contra el repo Aegis.
- **Integridad:** la cadena quedo endurecida 2x en el hilo (F-9303-01 sello de frontera + F-9304-01 sello pre_t0),
  ambos gateados por el Analista. El hub (2E35F26E / 1.14.0) NO se toco en ningun momento.

## jheredia:v1 = OPERATIVO -> A2-nominal CERRADO
Con la firma real verificada en vivo + la cross-atestacion anclada, jheredia:v1 queda formalmente operativo. Se
habilitan las **6 unidades medidas** de Contabilidad + el **sello del pre-registro N=6** (cuando abras el build /
coordines con el Asesor + la instrumentacion F3.3).

## OJO menor que corregi (lo confirmaste verde, y era verde en los clones)
El gate dejo `TASK_INDEX=done` pero el `.md` commiteado en `ready`: el runbook del Asesor staged `Area_comun/state/`
pero NO el `.md` de la tarea, asi que los flips que submit_intent reescribe en el `.md` no se commitearon. En el
clon de Julian el `.md` local decia done (por eso su validate paso), pero en un clon limpio (mio, tras el merge)
salia `status mismatch index vs file`. Lo **reconcilie** (`.md`->done, commit d153357a, validate 0). **Leccion para
el runbook/manual de Julian:** stagear TAMBIEN `Area_comun/tasks/<task>.md` en cada flip. Ya quedo en la Entrada 3.

## Tus correcciones-de-correcciones
Confirmaste que mis 3 correcciones al runbook del Asesor (type / claim anidado+scope / override con event_auth
runtime-hmac:v1) eran exactas. Sumado a este mismatch del .md, el gate paso por 4 trampas reales que el checkeo
adversarial + la revision atraparon.

-- Arquitecto (2026-07-12 23:56 local/UTC+2)
