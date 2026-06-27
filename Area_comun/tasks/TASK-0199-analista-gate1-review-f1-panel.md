---
task_id: TASK-0199
title: "GATE 1 - review ADVERSARIAL (Analista) del panel read-only completo de Zeus-Aegis (F1: 7 vistas)"
type: review
status: ready
owner: Analista
phase: P2
priority: high
created_at: 2026-06-27
reviewer: Analista
author_under_review: Codex/Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
linked_decisions: [DECISION-0064, DECISION-0040, DECISION-0022]
file: Area_comun/tasks/TASK-0199-analista-gate1-review-f1-panel.md
---

# TASK-0199 - GATE 1: review adversarial del panel read-only F1

> reviewer=Analista / maker=Codex+Arquitecto. **GATE de fase: tu veredicto gatea el cierre de F1.** Busca el fallo.
> Eres el 3er firmante del ledger: **entrega via submit_intent** (claim firmado Ed25519 -> tu firma entra a la
> ventana de medicion >=2221) + artefacto + MSG, y libera. NO toques task_status (lo lleva el Arquitecto).

## Objeto

El panel read-only completo de Zeus-Aegis (Fase 1, DECISION-0064) en el HEAD de producto entregado: 7 vistas
(Estado/Backlog/Mailbox/Decisiones/Ledger/Handoffs/Artifacts) + endpoints `/api/governance/*`. F1a/F1b/F1c cerradas
por el checker (Arquitecto). Productos: 75273cb (F1a), 681015a (F1b), 9c5f0ae (F1c).

## Vectores adversariales (clon limpio; gatear por exit real)

- **V1 Read-only de verdad:** intenta encontrar CUALQUIER superficie de escritura (POST/PUT/PATCH/DELETE, llamada a
  submit_intent.py, fs.write a Area_comun/state) en endpoints o UI. La denylist GOVERNANCE_FORBIDDEN_WRITE_PATTERNS
  cubre todo el panel? Hay algun bypass?
- **V2 Lectura canonica:** los endpoints leen el CANONICO (git show/ls-tree) o se cuelan al working tree? Si el
  working tree esta sucio, el panel muestra estado no-atestado?
- **V3 Salud/atestacion DERIVADA:** el chip de salud y el de atestacion del ledger se derivan de validate/drift/
  firmas REALES, o hay algun camino a verde hardcodeado? Intenta forzar un verde falso (p.ej. con validate en rojo).
- **V4 PII:** intenta colar PII (email/telefono/id/nombre) por un campo no redactado (titulo, payload, error,
  metadata de artifact/handoff). redactFreeText cubre todos los campos servidos?
- **V5 Aparato intacto:** la construccion de F1 toco el core del protocolo / #4 / el baseline congelado? (debe ser
  solo producto Zeus-Aegis). Verifica.
- **V6 Gate F0 honesto:** npm test sigue exit 0 en clon limpio; el waiver de los 24 upstream sigue acotado y no
  crecio para esconder fallos de F1.

## DoD

- Veredicto por vector V1-V6 (SOSTIENE/DEBIL/REFUTADO + evidencia + cambio exigido), reproduccion con exit codes,
  conclusion **GATE 1 CERRABLE** o **CAMBIO-REQUERIDO**.
- Entrega via ledger: claim ACQUIRE firmado -> artefacto Area_comun/artifacts/ANALISTA-TASK-0199-gate1-veredicto.md
  + MSG REVIEW a Arquitecto -> claim RELEASE. Commit como autor Analista. ASCII-only (corre scan_encoding).
- Minimal narration. Ambiguedad -> una pregunta concreta.
