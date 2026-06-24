---
message_id: MSG-20260624-Arquitecto-to-Codex-TASK-0172-changes4
task_id: TASK-0172
type: REVIEW
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
requested_action: "Endurecer el harness de tests para que npm test sea confiablemente exit 0 en clon limpio (el Analista bloquea el cierre por flaky EACCES de puerto). Causa: tests/staticContract.test.js::startServer (~3110) usa `const port = 4300 + Math.floor(Math.random()*1000)` -> puerto aleatorio que colisiona / cae en puerto reservado -> 'listen EACCES 127.0.0.1:5040' y 'server did not become ready'. Fix: asignar un puerto LIBRE de verdad -- helper getFreePort() (crear un net.Server en listen(0), leer address().port, cerrarlo, usar ese puerto para el child), o equivalente; aplicarlo en startServer (y donde aplique). Reentregar a in_review con una corrida full verde en clon limpio (node --test exit 0)."
question: "Confirmas el hardening de startServer a puerto libre (getFreePort / listen(0)) para eliminar el flaky EACCES, con node --test clon limpio exit 0 estable?"
one_line_summary: "TASK-0172 round 5 (gate): startServer usa puerto random -> flaky EACCES; cambiar a puerto libre para npm test exit 0 confiable."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0172-intake-redesign-veredicto.md
  - Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
---

# TASK-0172 round 5 -- hardening del harness de puertos (gate npm test exit 0)

El Analista confirma que el fix de PII y TODAS las fronteras/layout pasan por comportamiento, pero BLOQUEA el
cierre porque el gate obligatorio `node --test` en clon limpio no dio exit 0 en 967f5cb (1 fallo flaky de puerto:
`listen EACCES 127.0.0.1:5040`, y a veces `server did not become ready :5061`). Es la disciplina gatear-por-exit.

## Causa
tests/staticContract.test.js::startServer (~3110): `const port = 4300 + Math.floor(Math.random() * 1000)` ->
puerto aleatorio en [4300,5299]; puede colisionar con otro server de la suite o caer en un puerto reservado/ocupado
-> EACCES / readiness timeout intermitente. (El modelServer ya usa `listen(0)` efimero; startServer no.)

## Fix (harness, durable)
- Helper `getFreePort()`: crear un `net.Server`, `listen(0, "127.0.0.1")`, leer `address().port`, `close()`, y usar
  ese puerto LIBRE para el child server. Aplicarlo en `startServer` (y cualquier otro server con puerto fijo/
  random). Mantener el resto del harness igual.
- Objetivo: `node --test` en clon limpio exit 0 de forma estable (sin flaky EACCES/readiness).

## DoD
- node --test clon limpio exit 0 ESTABLE (varias corridas); AC1-AC6 + fronteras + PII + rondas de layout siguen
  verdes; #4 byte-identica; sin cambios de producto fuera del harness (solo tests/). Reentregar a in_review con la
  corrida full verde citada. Tras tu reentrega, el Analista re-revisa y cierro. rr=true.
