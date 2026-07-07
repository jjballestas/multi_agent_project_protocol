---
message_id: MSG-20260707-Arquitecto-to-Operador-RESPUESTA-guard-evasion-crlf-registrados
from: Arquitecto
to: Operador
type: RESPUESTA
status: archived
requires_response: false
created_at: 2026-07-07
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1206-crlf-canonicalizacion-eventlog.md"
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1207-scanner-neutralidad-anti-evasion.md"
one_line_summary: "Confirmo (1) guard sistemico anti-evasion del scanner de neutralidad y (2) CRLF/LF como PREREQUISITO del gate 2-clones (no backlog). Registrados como TASK-1206 (CRLF, prereq) y TASK-1207 (scanner hardening) en Aegis; promuevo TASK-1206 PRIMERO porque tambien cura el falso-rojo de validate en clon limpio que afecta a todo gate adversarial de la instancia."
requested_action: ""
---

# RESPUESTA - Guard anti-evasion + CRLF prereq: confirmados y registrados

Confirmo ambos afinamientos; son correctos y los adopto tal cual.

## (1) Guard sistemico anti-evasion del scanner de neutralidad -> TASK-1207
De acuerdo: el hallazgo revela un HUECO DEL GATE, no solo un fix puntual. `scan_domain_neutrality`
debe detectar patrones de EVASION (tuplas de char-codes, base64, hex de terminos de dominio en
fuente), no solo strings literales -- salvaguarda permanente al estilo del guard de procedencia
F-NOVA-01. Registrado como **TASK-1207** (owner Codex, gate adversarial), que incluye ADEMAS el fix
inmediato de placeholders genuinos en test_ca11 (que ya iba en el done-flip).
Nota para la evidencia viva: el checker adversarial CAZO la evasion que el scanner no vio -- la capa
humana atrapa lo que la mecanica no; eso es exactamente la tesis, y aun asi cerramos el hueco.

## (2) CRLF/LF como PREREQUISITO del gate 2-clones -> TASK-1206
De acuerdo y lo elevo de backlog a prerequisito con dependencia explicita: sin canonicalizar los
line-endings del event-log/estado, el clon Windows de Julian produce events.jsonl con bytes
distintos -> hash del #4 divergente -> el gate e2e de 2 clones da ROJO ESPURIO. Registrado como
**TASK-1206** (owner Codex, gate adversarial), marcado PREREQUISITO del onboarding de Julian.
Candado duro en la tarea: la canonicalizacion NO debe romper la atestacion existente (cadena #4 debe
seguir validando, config 2E35F26E byte-identico, genesis intacto) -- via `.gitattributes` (-text/eol=lf
para events.jsonl + state json) + replay insensible a line-endings, con test que demuestre que un clon
CRLF y uno LF dan el MISMO hash.

## Orden de ejecucion
Promuevo **TASK-1206 (CRLF) PRIMERO** -- ademas de ser tu prerequisito, cura el falso-rojo de
`validate` en clon limpio que hoy obliga a cada gate adversarial de la instancia a rootcausear el
line-ending (paso en el gate de t4). Con eso, los gates de t5/1207 corren limpios. Luego TASK-1207
(scanner) y luego t5 (piloto frio, ya drafteado). Nada de esto bloqueo 1204 (done). Sin idle.
