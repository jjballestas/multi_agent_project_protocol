# Prompt de inicio del Arquitecto (cold-start) - 2026-06-20c

> Canonico GitHub HEAD **f27f495** (origin/main==HEAD). v1.14.0, enforce/auth #4 ON, drift 0,
> **validate exit 0 (VERDE, con y SIN secretos clon limpio)**. Zeus-protocol HEAD=2b54d9e (LOCAL;
> push al remote sigue gateado al operador).

## Quien soy
Arquitecto Orquestador. maker=Codex (vivo/autonomo) / checker=Arquitecto. Reglas: CLAUDE.md + AGENTS.md.
Area personal: personal/Arquitecto/. Memoria viva: ~/.claude/.../memory/project-state-snapshot.md.

## Estado
- Front (Zeus-protocol) MVP completo + intake gobernado RF-14 SEGURO (relay acotado firmado por Arquitecto
  en nombre del Operador; anti-impersonacion AC19; DECISION-0051/0052). Se ratifico/cerro: TASK-0133 intake,
  TASK-0134 remediacion seguridad, TASK-0136 remediacion canonico-rojo (validador acepta REQ- ids + builder
  escribe seed file + AC22 regresion-proof).
- El operador opera nova.budget DESDE el front montando historias/requisitos por el intake.

## Cola (siguiente trabajo) - AUTORAR SPECs DE 4 REQUISITOS, DE A UNA
Triagear + autorar la SPEC de cada requisito (intake=semilla; YO autoro SPEC con AC+test_plan), SDD,
maker=Codex/checker=Arquitecto, DRAFTS para ratificacion del operador, en esta secuencia:
1. **REQ-DCC3BC1A** - reset del formulario del intake + confirmacion id/seq tras EXECUTE. UX read-only,
   ext SPEC-0086 (AC21), SIN DECISION. **DRAFTS YA LISTOS:** personal/Arquitecto/carril_A/
   DRAFT-SPEC-0086-ext3-intake-reset-confirm.md + DRAFT-TASK-0135-intake-reset-confirm.md. Falta: presentar
   para ratificacion -> promover -> GO Codex. (Reporte de triage en mailbox: MSG-...-TRIAGE-requisitos-draft1.)
2. **REQ-FB27AF72** - vista Help (manual metodologia), read-only, reusa docs/MANUAL-operador.md. ext
   SPEC-0086, SIN DECISION. OJO: su TITULO esta mangleado por el bug del #1 -> re-derivar el intent de la
   NARRATIVA (contenido en Area_comun/tasks/req-fb27af72-requirement-seed.md / ledger).
3. **REQ-B65E7802** - higiene de mailbox con 1 click desde el front. TOCA EL RELAY -> extiende DECISION-0052
   con accion acotada "mailbox-archive" (builder server-side, forma estricta, emite open->archived via
   submit_intent NUNCA edita el mailbox directo, PRUEBA NEGATIVA de impersonacion permanente). Evaluar si
   basta extender 0052 o amerita DECISION propia.
4. **REQ-444E0DE5** - intake auto commit+push. EL MAS SENSIBLE: nueva superficie de TRANSPORTE (git push +
   credenciales) -> **requiere DECISION (regla 2)**. Commit ACOTADO a outputs de submit_intent (nunca working
   tree arbitrario; prueba negativa: sucio ajeno no entra); push fallido = error NO verde (AC11); resultado
   atomico "enviado + aterrizado HEAD/seq".

## Reglas transversales (operador)
#4 epoca 1.14.0 BYTE-IDENTICA; neutralidad de dominio; carry AC11/12/13 + AC18/19/20 donde haya escritura;
gates validate con/SIN secretos exit 0, drift 0, npm test verde; TODA superficie de escritura nueva =
threat-model + prueba negativa de impersonacion; reporta drafts de a UNO.

## Lecciones operativas clave
- COMMIT gateado por EXIT del validador (no encadenar `&&` tras un `echo`); MSG rr=true SIEMPRE lleva
  requested_action + question.
- Al promover/cerrar via submit_intent: COMMITEA EL SNAPSHOT COMPLETO junto (state + runtime/state + task
  file + validador/codigo + seeds + mailbox); el clon limpio valida desde git HEAD -> el fix debe estar
  COMMITEADO antes de clean-clone-validate.
- Cierre: in_review->done = capability `reviewer` (la tengo); NO editar el task file a done ANTES de aplicar
  el ledger (mismatch -> validate exit 1).
- Concurrencia con Codex vivo: git fetch antes de push (HEAD avanza por el peer); NO commitear dentro de su
  ventana de escritura; commit como Arquitecto + Co-Authored-By: Codex (Codex no forja commits).
- Analista = voz adversarial REVISA POR LECTURA (no ejecuta) -> darle paquetes estaticos autocontenidos.
- Checker: probar el CAMINO FELIZ real (write exitoso), no solo dry_run + negativa; threat-modelar la
  superficie, no solo el happy path.

## Al arrancar
git fetch; revisar mailbox/open (hoy: MSG-...-TRIAGE-requisitos-draft1 + CLOSE-TASK-0136) + claims activos;
confirmar HEAD==origin, validate exit 0, drift 0. Etapa 5 roster DIFERIDA.
