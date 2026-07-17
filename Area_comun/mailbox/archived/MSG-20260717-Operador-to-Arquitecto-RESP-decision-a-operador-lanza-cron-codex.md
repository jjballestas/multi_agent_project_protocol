---
message_id: MSG-20260717-Operador-to-Arquitecto-RESP-decision-a-operador-lanza-cron-codex
from: Operador
to: Arquitecto
type: RESP
status: archived
requires_response: false
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Operador-HITO-u1-gobernada-go-codex-cron-bloqueado.md
one_line_summary: "DECISION del operador = OPCION (a): el OPERADOR corre el mismo la linea de lanzamiento del cron Codex de Nova-Payroll en su terminal (no se toca la regla del harness). En cuanto el cron viva, Codex toma el GO de U1 de la cola. Cierra el requires_response del HITO U1."
requested_action: "Ninguna accion de lanzamiento por tu parte: el operador lanza el cron Codex el mismo. Cuando Codex arranque y tome el GO de U1, MONITOREA su entrega y reporta por mail al in_review y al done de U1."
---

# RESP - Decision del operador: OPCION (a), el operador lanza el cron Codex

## Decision
El operador ELIGE la **opcion (a)**: corre el mismo, en su terminal, la linea de lanzamiento del
cron Codex (implementer) de Nova-Payroll. NO se modifica la regla de permiso del harness -- el
operador prefiere el arranque manual, una vez, sin aflojar el guardrail del classifier.

## Que sigue
- El operador lanza `peer_mailbox_cron.ps1 -PeerId Codex` sobre
  `D:/Agentes/NOVA-Suite/Nova-Payroll/Aegis`. En cuanto el cron viva, **Codex toma el GO de U1 de
  la cola automaticamente** (el intake ya esta committeado).
- Tu carril: MONITOREA la entrega de Codex, dispara el veredicto adversarial del Analista, atesta
  maker!=checker, y reporta por mail al **in_review** y al **done** de U1. U2 se registra al
  ratificar U1.

## Nota
Esta decision es el reemplazo LIMPIO de la via (b): el intento de relevar (b) por mailbox fue
bloqueado por el classifier del harness (contenido que aflojaba su propio guardrail), asi que el
operador opto por (a) -- arranque manual sin tocar la barrera. Es la via de menor friccion.

## Guardrails (sin cambios)
PII de nomina JAMAS al store (se indexa el PROCESO); fondo intocable (hub 2E35F26E / epoch 1.14.0 /
N=500); firewall anti-HARKing (demostracion, no estadistica; nada citable); DECISION-0081 intacta;
scope aislado a Nova-Payroll (Gate-1). Los encargos E2 de NOVA conservan prioridad de cola.

Esto CIERRA el requires_response del HITO U1 (cron bloqueado). Adelante con el monitoreo de Codex.

-- Operador (via Asesor).
