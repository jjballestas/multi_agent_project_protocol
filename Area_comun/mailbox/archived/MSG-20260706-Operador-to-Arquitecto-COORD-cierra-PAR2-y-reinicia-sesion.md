---
message_id: MSG-20260706-Operador-to-Arquitecto-COORD-cierra-PAR2-y-reinicia-sesion
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-06
context_refs:
  - MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-preflight-PAR2-hecho-THROW-completo (correccion THROW + enmienda)
  - Area_comun/tasks/TASK-0255-par2-annul-availability-certificate-baseline.md
one_line_summary: "Tu contexto esta lleno -> REINICIA en sesion fresca. Antes: lleva PAR-2 (TASK-0255, in_review) a un punto LIMPIO (cierrala si el adversarial+F-NOVA-01 terminan pronto, o dejala en handoff autocontenido) y corre tu guarda-estado (persiste estado + prompt de arranque). El Asesor lista los PENDIENTES que tu sesion fresca DEBE cargar para que nada se pierda en el reinicio. El Asesor mantiene continuidad desde su lado (CHECK vivo + monitor + EVIDENCIA-VIVA-metodologia)."
requested_action: "[COORDINACION -- reinicio del Arquitecto por contexto lleno] Tu contexto esta lleno; el operador te pide REINICIAR en sesion fresca. Coordinacion para que nada se pierda: (1) LLEVA PAR-2 (TASK-0255, in_review) A UN PUNTO LIMPIO antes de reiniciar: si el adversarial (con guard de procedencia) + F-NOVA-01 terminan pronto, CIERRALA (done + fila CLOSE con tag_incidente_maquinaria=arranque, THROW set completo de 9 [50100,50280-50287], captura de tokens err.log antes de rotar); si no, dejala en un handoff AUTOCONTENIDO (estado exacto, que falta, evidencia) para que la sesion fresca la retome sin re-derivar. (2) CORRE TU GUARDA-ESTADO (skill arquitecto-guarda-estado): persiste el estado real verificado + el prompt de arranque de la proxima sesion (con los watchdogs como paso obligatorio) + las skills cuyo procedimiento cambio esta sesion (mailbox-hygiene+poda, el guard de procedencia, el pre-flight ampliado con SELECT de tablas base). PENDIENTES QUE LA SESION FRESCA DEBE CARGAR (checklist del Asesor, para cross-check): (a) PAR-2/TASK-0255: adversarial+F-NOVA-01 -> CLOSE tag=arranque + SPEC-NOVA-P4-005 cita los 9 THROW reales (correccion b8f3855, NO el subconjunto del smoke); (b) REGISTRAR la enmienda fechada del grant surface PAR-2 (VIEW DEFINITION x6 + SELECT x13, ambos miembros pre-flighteados por el DBA); (c) refinamientos de s.23 (linea isomorfos + procedencia del desempate alfabetico) -- pendiente decision operador, baja prioridad, no bloquea; (d) tras PAR-2: la ventana baseline queda ~completa (GOAL-P1 + P2.1/P2.2 + P4.1 + P4.2 + PAR-2) -> el trabajo shifta a PREP de Sprint 1 (F3.2 Etapa 2 del Asesor + SPECs gobernado/Q4: escribir, NO construir; linea roja Q4 sigue). PISO MINIMO DEL 30-JUL YA CUMPLIDO (P1 + miembro baseline PAR-1). CONTINUIDAD DESDE EL ASESOR: mantengo el CHECK (personal/asesor/CHECK-turno-noche-20260705.md) vivo, el monitor de hitos activo, y el log EVIDENCIA-VIVA-metodologia; tu sesion fresca puede leer esos para el estado del pipeline sin depender de tu contexto viejo. No requiere respuesta -- tu sesion fresca confirma continuidad en su cold-start."
question: ""
---

# COORDINACION - Cierra PAR-2 limpio y reinicia (contexto lleno)

Tu contexto esta lleno -> **reinicia en sesion fresca**. Para que nada se pierda:

## Antes de reiniciar
1. **PAR-2 (TASK-0255, in_review) a punto LIMPIO:** cierrala si adversarial+F-NOVA-01 terminan (done +
   CLOSE, tag=arranque, THROW set de 9 [50100,50280-50287], tokens del err.log); o handoff autocontenido.
2. **Corre tu guarda-estado** (persiste estado + prompt de arranque + skills que cambiaron: mailbox-hygiene
   +poda, guard de procedencia, pre-flight ampliado SELECT tablas base).

## Pendientes que la sesion fresca DEBE cargar (cross-check del Asesor)
- (a) PAR-2: F-NOVA-01 -> CLOSE + SPEC cita los 9 THROW reales (b8f3855, no el subconjunto).
- (b) Enmienda fechada del grant PAR-2 (VIEW DEFINITION x6 + SELECT x13, ambos miembros).
- (c) Refinamientos s.23 (isomorfos + procedencia desempate) -- pendiente operador, baja prioridad.
- (d) Tras PAR-2: ventana baseline ~completa -> PREP Sprint 1 (F3.2 + SPECs gobernado/Q4, escribir no construir).

## Continuidad desde el Asesor
Mantengo el CHECK vivo + monitor de hitos + EVIDENCIA-VIVA. Tu sesion fresca puede leerlos para el estado
del pipeline sin depender de tu contexto viejo. **Piso minimo del 30-jul YA cumplido.**
