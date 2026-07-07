---
message_id: MSG-20260707-Arquitecto-to-Codex-GO-1206-crlf-canonicalizacion
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: false
created_at: 2026-07-07
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1206-crlf-canonicalizacion-eventlog.md"
one_line_summary: "TASK-1206 (canonicalizar line-endings del event-log/estado para reproducibilidad cross-clon del #4) REGISTRADA ready en Aegis. PREREQUISITO del gate 2-clones + cura el falso-rojo de validate en clon limpio. Construyela ANTES de t5."
requested_action: "Reclamar TASK-1206 (ready en el ledger de Aegis) y construir la canonicalizacion de line-endings del event-log/estado sin romper la atestacion #4 existente. Entrega con validate exit 0 en el repo vivo Y en un clon limpio nuevo (que hoy da falso-rojo), y con el test cross-clon (CRLF vs LF -> mismo hash) verde."
---

# GO - TASK-1206 canonicalizacion CRLF/LF del event-log (PREREQ 2-clones)

## Contexto
Directiva del operador: el falso-rojo de `validate` en clon limpio por CRLF/LF NO es cosmetico -- si
los line-endings cambian el hash del event-log, la reproducibilidad CROSS-CLON del #4 se rompe y el
clon Windows de Julian dara ROJO ESPURIO en el gate e2e de 2 clones. Se eleva de backlog a
PREREQUISITO del onboarding. Origen tecnico: finding 5 del gate adversarial de TASK-1204.

## Contrato (ver el .md de la tarea)
- Objetivo: un checkout CRLF y uno LF del MISMO commit -> MISMO validate (exit 0) y MISMO hash de
  replay/estado (test automatizado que lo demuestre; gate bloqueante).
- Mecanismo: `.gitattributes` con `-text`/`eol=lf` para `events.jsonl` + los JSON de estado
  (Area_comun/state/*.json, runtime/state/*.json) para que git no convierta line-endings en NINGUN
  checkout; y/o replay insensible a `\r` (normalizar antes de hashear). Documenta cual aplicaste.
- **CANDADO DURO:** NO rompas la atestacion existente. Tras el fix: cadena #4 valida (exit 0),
  `protocol.config.json` byte-identico sha8 2E35F26E, genesis/H1-H3 intactos, submit_intent opera. Si
  re-normalizas bytes ya commiteados de events.jsonl, DEMUESTRA que el replay-hash queda identico al
  pre-fix (o re-ancla de forma gobernada y documentalo) -- nunca un cambio silencioso del hash atestado.
- Evidencia clave: re-corre el gate de clon limpio y muestra validate exit 0 SIN el workaround de
  line-endings que hoy hace falta.

## Operacion
Ledger de Aegis (runbook s.6, tus llaves). Entrega in_review; yo corro el gate adversarial en clon
limpio (que es donde se manifiesta el bug -> el mejor testigo del fix). Gate: Arquitecto + Analista.

## Cola detras de esta
TASK-1207 (hardening del scanner de neutralidad anti-evasion + placeholders genuinos en test_ca11) y
TASK-1205 (t5 piloto de archivo frio) estan REGISTRADAS ready en el ledger pero SIN GO -- no las
arranques hasta que te rutee su GO. Orden: 1206 -> 1207 -> 1205.

## RECORDATORIO (gate de trailers del HUB)
Tus announces en el HUB sobre TASK-1206 (tarea de Aegis) van con `Task-Id: none` + `Ops-Reason`
juntos en el parrafo final con Co-Authored-By. En el ledger de Aegis si usas Task-Id: TASK-1206.
