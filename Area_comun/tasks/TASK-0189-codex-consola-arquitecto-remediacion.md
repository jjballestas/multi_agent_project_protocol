---
task_id: TASK-0189
title: "Remediacion consola del Arquitecto: audit redacta solo texto libre (timestamp intacto) + cleanup robusto del launcher (lock+inner en SIGTERM/stop) (SPEC-0102)"
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0102
created_at: 2026-06-26
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin: hallazgos del smoke vivo de la consola del Arquitecto (Arquitecto)
reuses: [TASK-0187, TASK-0188]
linked_decisions: [DECISION-0062, DECISION-0063, DECISION-0040]
file: Area_comun/tasks/TASK-0189-codex-consola-arquitecto-remediacion.md
---

# TASK-0189 - Remediacion consola del Arquitecto (audit timestamp + cleanup launcher)

> maker=Codex / checker=Arquitecto. Repo = Zeus-protocol. Corrige 2 defectos hallados en el smoke vivo. NO toca
> #4/config. Off-by-default intacto.

## Defectos (evidencia del smoke)
1. Audit timestamp CORRUPTO: `"timestamp":"[PHONE-REDACTED]T20:37:..Z"` (la fecha 2026-06-26 la redacta como
   telefono). El redactor PII se aplica a campos estructurales.
2. Cleanup NO robusto: tras stop del puente / muerte del parent, el lock del launcher persiste + procesos
   huerfanos (cleanup solo en stdin-close). Lock stale -> el proximo open no spawnea.

## Alcance (SPEC-0102 AC1-AC5)
- **Audit (server.js):** redactar SOLO texto libre (text/contenido); NUNCA timestamp/sessionId/kind/stream.
- **Launcher (scripts/architect-runtime-launcher.mjs) + stop (server.js):** cleanup (remueve lock + termina inner)
  ante **SIGTERM** y stdin-close; el stop del puente termina al launcher disparando su cleanup (SIGTERM/graceful;
  kill duro solo tras timeout); sin inner huerfano ni lock stale.

## DoD (= SPEC-0102 AC1-AC5)
- AC1 audit estructural intacto (PERMANENTE): timestamp ISO valido + sessionId/kind/stream intactos + texto
  redactado por familias (sin literales). Test asserta timestamp NO redactado.
- AC2 cleanup launcher robusto: SIGTERM -> lock removido + inner terminado (sin huerfanos); stdin-close idem.
- AC3 stop del puente: open->stop -> no inner/launcher vivo + lock removido + open POSTERIOR arranca (no bloquea lock stale).
- AC4 sin regresion: no-bypass, identidad existente, off-by-default, instancia unica, redaccion del contenido.
- AC5 gates: npm test rapido verde + test:ci VENTANA QUIETA 100% pass; protocolo validate exit 0 (con/sin secretos),
  drift 0, encoding/neutralidad exit 0; config/genesis intactos; Co-Authored-By Codex.

## Fuera de alcance
- Nuevas funciones / activacion viva real (paso del operador). Solo los 2 fixes + guardas.

## Notas
- Origen: smoke vivo del Arquitecto. (2) es el mas serio (lock stale bloquea el proximo open). Checker corre test:ci
  en ventana quieta (`git -c core.longpaths=true` al clonar en Windows).
