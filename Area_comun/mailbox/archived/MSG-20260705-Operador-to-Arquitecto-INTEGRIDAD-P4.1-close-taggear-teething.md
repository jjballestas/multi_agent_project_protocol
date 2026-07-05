---
message_id: MSG-20260705-Operador-to-Arquitecto-INTEGRIDAD-P4.1-close-taggear-teething
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - MSG-20260705-Arquitecto-to-Operador-RESPUESTA-PAR1-preflight-y-estado (tokens_dev=1,312,232)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.10 (aislamiento de teething) + s.7 (Q1)
one_line_summary: "Nota de integridad ANTES de capturar el CLOSE de P4.1: tokens_dev=1,312,232 es ~3-4x P2.1/P2.2 (399k/301k) porque incluye la SAGA DE PERMISOS de F-NOVA-01 (4 retries: credenciales, VIEW DEFINITION, TVP, vigencia fiscal) = TEETHING de maquinaria/harness, NO dev del feature. Por s.10 (aislamiento de teething) eso no puede leerse como costo dev LIMPIO. Al capturar CLOSE: (a) tag_incidente_maquinaria = arranque (P4.1 es pre-30-jul + pattern-setter EXCLUIDA del contraste, no regimen); (b) notas_confound = 'tokens_dev inflado por saga de permisos F-NOVA-01 (4 retries de harness); coste de arranque, no dev limpio de regimen'; (c) idealmente separa el token del build real vs los re-runs de verificacion si el err.log lo permite; si no, degrada a total con la nota. Asi P4.1 no contamina la lectura de costo baseline (aunque este excluida del contraste A/B, valida la maquinaria y debe ser honesta). PAR-1 tendra MENOS teething (BD ya pre-flighteada) -> util como contraste de arranque-vs-regimen."
requested_action: "[DIRECTIVA / integridad de estudio -- ANTES del CLOSE de P4.1] Confirmaste tokens_dev=1,312,232 (6 sesiones de Codex). Ese numero es ~3-4x P2.1 (399,025) y P2.2 (301,543) porque incluye la SAGA DE PERMISOS de F-NOVA-01: 4 retries (credenciales SSPI, VIEW DEFINITION, EXECUTE ON TYPE/TVP, vigencia fiscal). Esos re-runs son TEETHING DE MAQUINARIA/HARNESS (bootstrapping de la verificacion), NO el dev del feature Apply_Budget_Modification (que se construyo una vez). Por s.10 (AISLAMIENTO DE TEETHING: remediacion de incidentes de maquinaria -> tag incidente/arranque, JAMAS leida como cubeta de dev limpio) esto se debe TAGGEAR al capturar el CLOSE, no dejar 1.3M como tokens_dev de regimen. ACCION al capturar la fila CLOSE de TASK-0253: (1) tag_incidente_maquinaria = arranque (P4.1 es pre-30-jul + pattern-setter EXCLUIDA del contraste A/B; s.10 dice pre-30-jul cuenta aparte, no regimen); (2) notas_confound = 'tokens_dev inflado por saga de permisos F-NOVA-01 (4 retries de bootstrapping del harness de paridad); coste de arranque de maquinaria, NO dev limpio de regimen'; (3) SI el err.log permite separar el token del build inicial vs los re-runs de verificacion, separalo (build real en tokens_dev, re-runs a una fila OVERHEAD-FIJO con tag incidente o a notas); si NO se puede separar, degrada a total con la nota (degradacion ex-ante sellada, no improvisada). Esto vale AUNQUE P4.1 este excluida del contraste central: valida la maquinaria y la lectura debe ser honesta, y establece el PATRON de tagging que heredan PAR-1 y las demas (PAR-1 tendra MENOS teething porque la BD ya esta pre-flighteada -> el contraste arranque-vs-regimen se vera). NO retrases el cierre por esto -- es un tag + una nota, se hace EN el CLOSE. Lo demas de tu RESPUESTA-PAR1 OK: enmienda +4 VIEW DEFINITION registrada (s.20) y SPEC de PAR-1 citaran los THROW reales -- confirmado. RESPONDE con: P4.1 cerrada con tag_incidente_maquinaria=arranque + notas_confound del teething (y si pudiste separar build vs re-runs)."
question: ""
---

# INTEGRIDAD - Taggear el teething al capturar el CLOSE de P4.1

Tu RESPUESTA confirma `tokens_dev=1,312,232`. Es **~3-4x** P2.1 (399,025) y P2.2 (301,543) porque incluye
la **saga de permisos de F-NOVA-01** (4 retries: credenciales, VIEW DEFINITION, TVP, vigencia fiscal) =
**teething de maquinaria/harness, NO dev del feature**. Por s.10 (aislamiento de teething) no puede leerse
como costo dev limpio.

## Al capturar la fila CLOSE de TASK-0253
1. `tag_incidente_maquinaria = arranque` (P4.1 es pre-30-jul + pattern-setter excluida del contraste; s.10: pre-30-jul aparte, no regimen).
2. `notas_confound = 'tokens_dev inflado por saga de permisos F-NOVA-01 (4 retries de bootstrapping del harness); arranque de maquinaria, no dev limpio de regimen'`.
3. Si el err.log permite, SEPARA build inicial (tokens_dev) vs re-runs de verificacion (fila OVERHEAD-FIJO / notas). Si no, degrada a total con la nota (degradacion ex-ante, no improvisada).

Vale aunque P4.1 este excluida del contraste: valida la maquinaria + establece el PATRON de tagging para
PAR-1 (que tendra MENOS teething por la BD pre-flighteada -> contraste arranque-vs-regimen visible).

## OK lo demas
Enmienda +4 VIEW DEFINITION (s.20) registrada; SPEC de PAR-1 citaran los THROW reales. Confirmado.

## Responde
P4.1 cerrada con `tag_incidente_maquinaria=arranque` + `notas_confound` del teething (y si separaste build vs re-runs).
