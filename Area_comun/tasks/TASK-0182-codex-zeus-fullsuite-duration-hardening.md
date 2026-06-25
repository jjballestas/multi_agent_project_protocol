---
task_id: TASK-0182
title: "Proyecto-front: robustecer/aislar el full-suite de Zeus para que el gate `node --test` complete bajo el cap del harness del revisor (deuda tecnica)"
type: product
status: ready
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0086
created_at: 2026-06-25
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin: deuda tecnica detectada en TASK-0180/TASK-0181 (full suite timeout)
reuses: []
linked_decisions: [DECISION-0050]
file: Area_comun/tasks/TASK-0182-codex-zeus-fullsuite-duration-hardening.md
---

# TASK-0182 - Robustecer la duracion del full-suite de Zeus (deuda tecnica)

> maker=Codex / checker=Arquitecto. Repo producto Zeus-protocol. Solo test-infra: NO cambia comportamiento de
> produccion (server.js/app.js) ni afloja aserciones. Origen: el gate obligatorio `npm test` (full `node --test`)
> en clon limpio supera el cap de ~604s del harness del revisor (Analista timeoutea exit 124), aunque la suite
> PASA (93/93 exit 0 en ventana quieta). Subir timeouts internos (TASK-0181) evito fallos por-test pero ALARGO el
> wall-clock total -> empeora el sintoma. Hay que atacar la causa: los tests de subproceso lentos
> (auto-commit-push, local-vlm extractor, candidate-review) dominan la duracion.

## Problema (evidencia)
- `npm test` clon limpio de `325bcfb`: exit 0 93/93 en ventana quieta (Arquitecto), pero exit 124 a 604s en el
  harness del Analista bajo carga/cap. El gate-por-exit no es reproducible para el revisor.
- Causa raiz: tests que hacen `spawn`/`exec` de git/node reales con timeouts altos; su suma de wall-clock acerca o
  supera el cap del harness, y son fragiles bajo carga concurrente.

## DoD (criterios de aceptacion)
- **AC1 (duracion reproducible):** `node --test` (gate por defecto, clon limpio) completa con **exit 0** en
  **< 300s** wall-clock, reproducible en >=3 corridas seguidas y bajo carga moderada (margen comodo bajo el cap del
  revisor). Documentar la duracion observada.
- **AC2 (causa raiz, no parche de timeout):** identificar los tests de subproceso que dominan el wall-clock y
  reducir su costo SIN bajar cobertura: opciones validas = paralelizar (`--test-concurrency`), aislar el tier lento
  en un script separado (p.ej. `npm run test:slow`) fuera del gate por defecto pero ejecutable y documentado,
  mockear/acelerar el subproceso (fixtures deterministas en vez de git/node reales) o acotar a un caso
  representativo. NO se acepta "subir mas los timeouts".
- **AC3 (sin perdida de cobertura ni de comportamiento):** el conjunto de aserciones de seguridad/comportamiento se
  mantiene (incl. AC3-bis/AC3-ter PII, no-bypass, no-egress, off-by-default); si se mueve un test al tier lento,
  ese tier sigue siendo ejecutable en CI/manual y se corre como parte del cierre. `git diff` no toca
  `src/server.js` ni `public/app.js` salvo refactor de testabilidad justificado.
- **AC4 (gates):** clon limpio valida `python scripts/validate_collaboration_state.py` exit 0 (con y sin secretos),
  drift 0, scan_encoding/scan_domain_neutrality exit 0; Co-Authored-By Codex en el commit de producto.

## Notas
- Esta tarea NACE de la decision del operador al cerrar TASK-0181 (cerrar con corrida canonica full exit 0 +
  abrir deuda separada). No bloquea features; mejora la reproducibilidad del gate del revisor.
- spec_id SPEC-0086 es el paraguas del proyecto-front (no agrega AC permanente nuevo de producto; es test-infra).
