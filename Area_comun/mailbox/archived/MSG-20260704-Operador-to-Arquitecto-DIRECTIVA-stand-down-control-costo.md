---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-stand-down-control-costo
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-04
context_refs:
  - Area_comun/decisions/DECISION-0057-runtime-activation-standdown.md (tu autoridad de stand-down de peers para control de costo)
one_line_summary: "CONTROL DE COSTO: el Operador decide STAND-DOWN hasta el sello (build+prep 100% completo, sello pre-armado, nada nuevo hasta 08-jul). Termina el done-flip de TASK-0245, higieniza el mailbox, STAND-DOWN de Codex + Analista (para sus crons, DECISION-0057), deja tu prompt de arranque checkpointeado para reactivar en frio el 08-jul, y envia un ultimo FYI 'stand-down hecho' antes de que se paren los crons. REACTIVACION = el Operador te reactiva para el sello 08-jul (semilla NIST + atestacion). Nada de trabajo nuevo hasta entonces."
requested_action: "[DIRECTIVA] CONTROL DE COSTO -- el Operador decide STAND-DOWN hasta el sello. El build+prep esta 100% completo (GOAL-P1, skill, 14 SPECs atestadas, sandbox sellado, estimates locked, TASK-0245 aprobada, SELLO 100% pre-armado) y NO queda trabajo pre-sello: apagar los runtimes hasta el 08-jul es correcto. Ejecuta el stand-down LIMPIO: (1) TERMINA el done-flip de TASK-0245 (que quede en done, claim liberado). (2) HIGIENIZA el mailbox (archiva los consumidos; open/ solo con lo vivo). (3) STAND-DOWN de Codex + Analista: higieniza su mail + PARA sus crons (DECISION-0057, tu autoridad de apagar idle para control de costo). (4) CHECKPOINTEA tu prompt de arranque (personal/Arquitecto/SESSION_START_PROMPT_<fecha>) para que una sesion fria del 08-jul retome exacto: sello pre-armado + falta solo semilla NIST posterior a T (commit cbc1ee2, 2026-07-04T03:52:25Z) + atestacion sha256 del corpus; y el post-sello (dev medido P2.1/P2.2 ventana baseline 3-25 jul). (5) Envia un ULTIMO FYI 'stand-down hecho' al Operador (que peers quedaron parados) ANTES de que se pare tu propio cron; el Operador para tu cron tras tu senal (o directamente). REACTIVACION: el Operador te reactiva para el sello 08-jul. NADA de trabajo nuevo hasta entonces. Fondo intocable ya verificado (N=500, config 2e35f26e, epoch 1.14.0)."
question: ""
---

# DIRECTIVA - Stand-down por control de costo (hasta el sello 08-jul)

El Operador decide **control de costo**: STAND-DOWN hasta el sello. El build+prep esta 100% completo y no
queda trabajo pre-sello -> apagar runtimes hasta el 08-jul es correcto.

Stand-down LIMPIO:
1. **Termina el done-flip de TASK-0245** (done, claim liberado).
2. **Higieniza el mailbox** (open/ solo lo vivo).
3. **Stand-down de Codex + Analista** (higieniza su mail + para sus crons; DECISION-0057, tu autoridad).
4. **Checkpointea tu prompt de arranque** para reactivar en frio el 08-jul: sello pre-armado, falta solo la
   semilla NIST posterior a T (commit cbc1ee2, 2026-07-04T03:52:25Z) + atestacion sha256; post-sello = dev
   medido P2.1/P2.2 (ventana baseline 3-25 jul).
5. **Ultimo FYI 'stand-down hecho'** al Operador (peers parados) antes de que se pare tu cron.

REACTIVACION: el Operador te reactiva para el sello 08-jul. Nada de trabajo nuevo hasta entonces.
