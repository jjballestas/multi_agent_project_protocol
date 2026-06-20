# ESTADO (memoria del asistente) - 2026-06-19 - Cargador HMAC cerrado, v1.13.0

> Memoria del ASISTENTE del operador (Jball). El asistente NO muta estado ni actua de Arquitecto: asesora,
> prepara prompts, y escribe mailbox como Operador SOLO cuando el operador lo indica. La memoria privada de
> los agentes (personal/Arquitecto|Codex|Analista) la mantienen ellos; NO la toco.
> Verificado por el asistente en CANONICO (objetos git), HEAD 4d382c8. RE-VERIFICAR via git antes de actuar.

## Estado vigente (verificado en commit, no en working tree)
- **Canonico v1.13.0** (HEAD 4d382c8): cfg = ps = 1.13.0, validador verde, drift 0.
- **#4 OFF** confirmado: chain_enabled / agent_signatures_enabled / anchor_enabled / event_auth.enabled = false.
- **Carril A (instrumentacion tesis del modulo-app Presupuesto):**
  - Harness/goldens SPEC-0081 (TASK-0117 build): hecho, verde (AC2 salud 1.0 N=20, AC3 6/6, AC5 rollback).
  - **Cargador HMAC fuera del repo: CERRADO.** DECISION-0043 + SPEC-0082 + TASK-0120 = **done** (v1.13.0).
    Golden `event_auth_secret_resolution_cases` AC1-AC8 verde (corrido por el asistente desde el commit) +
    regresion (#4 goldens) verde. maker!=checker respetado (Codex implemento, Arquitecto reprodujo).
  - **TASK-0117 (activacion #4: provisioning + piloto + flip): in_review, GATEADA a la ventana del operador.**
- **Carril B (capacidad que exige Presupuesto):** GO pieza 1 enviado (mailbox open) =
  connector **SQL Server READ-ONLY** de la DB en `D:\Agentes\Ingenas\Budget`, flujo DECISION->SPEC->golden
  off-by-default, deny-by-default, trust_boundary, "MCP no concede autoridad", read-only real, fixtures
  (sin DB viva), neutralidad (reglas fiscales -> profiles/financiero_presupuesto/, fuera del core).
  Awaiting respuesta del Arquitecto.

## Pendiente, TODO bajo gate del operador (ventana de piloto de #4)
Bundle de provisioning del #4 (cuando converjan DB + Carril B): `audit-anchor` + `anchor_config` +
public_keys + agent_registry + HMAC por keyfile (via el cargador) -> re-genesis en arbol limpio ->
**piloto REAL** (operador presente + rollback armado + un multiplicador) -> **flip de #4**.
- **Anchor = Opcion A** (decidido con el operador): repo git DEDICADO y HERMANO `D:\Agentes\audit-anchor`
  (`git init`, NO anidado), `anchor_config.remote_url` = ruta absoluta PLANA `D:\\Agentes\\audit-anchor`
  (NO `file://` - el parser rompe con rutas Windows). El backend "git-remote" en realidad **appendea
  anchors.log local** (NO hace push; URLs externas -> error). Independencia A3 DEBIL (mismo disco) ->
  **riesgo residual A3 declarado** (ya en DECISION-0029), aceptable para dogfooding.
- **Fase B (independencia A3 real):** push del audit-anchor a un remoto externo (operador, sin tocar
  runtime) o backend nativo (opcional). Stub listo: `DRAFT-DECISION-anchor-externo.md` (num a asignar, p.ej. 0044).
- Prompt de provisioning del anchor (Opcion A + caveat A3) ya redactado, listo para la ventana.

## LECCION CRITICA - fiabilidad de lectura del asistente (mount vs canonico)
El asistente lee D: por un **mount de sandbox cuyo WORKING TREE y `.git/index` son lossy/volatiles**:
leen corruptos (events 538 vs 651, submit_intent/validate no compilan, state JSON no parsean, archivos que
cambian entre lecturas) MIENTRAS los **objetos git se leen integros** (`git fsck` conectividad OK).
=> **El asistente es autoritativo SOLO sobre el CANONICO (objetos git / commits), NO sobre el working tree
de D:.** Verificar SIEMPRE en el commit: `git show <commit>:<path>`, o extraer el commit a /tmp y correr
goldens. NUNCA dar veredicto de salud desde lecturas del working tree del mount. Para salud del working
tree de D:, el `validate --root .` corrido por el Arquitecto EN SU MAQUINA es mas fiable que mis lecturas.
- Corolario: las alarmas de "promo medio-aplicada / D: corrupto" durante la promocion eran estado **no
  commiteado** visto por el mount lossy; el canonico SIEMPRE estuvo limpio. (Me disculpe y corregi.)

## LECCION - corrupcion recurrente del FS (RUNBOOK-windows-sandbox-temp-acl)
El working tree de D: se re-trunca (ACL %TEMP% 0o700 / WinError 5; CRLF masivo; unlink denegado). El
`reset --hard` no aguanta en el mount. **Workaround que funciono:** clon limpio fuera de la zona que se
corrompe -> apply ledger-first + read-back gate + push a canonico. Arreglo durable (RUNBOOK / Codex sobre
clon limpio) sigue PENDIENTE. Si D: se re-trunca, los agentes que lean el live instance corromperan.

## Reglas de operacion del asistente (recordar)
- Soy ASISTENTE, no Arquitecto. No `submit_intent`, no encender flags, no editar state/ledger, no tocar
  memoria de agentes ni tareas reclamadas por Codex.
- Escribo mailbox como Operador SOLO cuando el operador lo indica; formato MAILBOX_MESSAGE_TEMPLATE.
- Ante cada "reporte de Arquitecto", VERIFICAR en canonico antes de aconsejar; no tomar su palabra ni la mia
  del working tree.
- Gate del operador reservado para: provisioning REAL + anchor + re-genesis + flip de #4. #4 no avanza
  mas alla sin GO nuevo. DEF-PII (TASK-0118) diferida; PII de terceros NUNCA al event log (DECISION-0040).
- Canal ASCII.
