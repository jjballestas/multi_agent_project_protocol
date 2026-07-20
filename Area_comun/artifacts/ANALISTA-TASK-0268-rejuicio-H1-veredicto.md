---
artifact_id: ANALISTA-TASK-0268-rejuicio-H1-veredicto
task_id: TASK-0268
author: Analista
role: revisor adversarial independiente (checker, DECISION-0056)
created_at: 2026-07-20
anchor_commit: ab5a017
fix_commit: c06fbad
closure_commit: c2abc9c
prior_verdict: Area_comun/artifacts/ANALISTA-TASK-0268-reparto-acotado-veredicto.md
---

# Veredicto del Analista -- Re-juicio H1 de TASK-0268 (docs del reparto)

Hora local: 2026-07-20 06:27 (+0200). Firma: Analista (voz adversarial, checker-only).

## Ancla canonica

- Instruccion: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0268-rejuicio-H1.
- Fix del maker: commit c06fbad (remediacion H1 docs-only), cierre c2abc9c.
- Ancla de la review: HEAD ab5a017 citado por la instruccion, reproducido en CLON
  LIMPIO (/d/ccv0268h1, git clone + checkout ab5a017).
- Alcance: lectura de README_INSTANCIACION + invariancia de hook/pin, SIN producto en
  alcance (re-juicio de docs del hub; coherente con el alcance solo-hub del veredicto
  original).
- Atribucion verificada en el ledger firmado: los eventos de la remediacion H1
  (seq 5133-5140, intent.applied) estan firmados por Codex; maker != checker se
  conserva. El campo author de git es uniforme (config local del arbol compartido) y
  no es fuente de atribucion.

## Reproduccion (exit codes reales, clon limpio salvo indicado)

| Paso | Comando | Exit | Dato |
|------|---------|------|------|
| Alcance del fix | git show --stat c06fbad y c2abc9c | 0 | c06fbad: README_INSTANCIACION.md + churn de ledger (claim/status/eventos); c2abc9c: handoff/mailbox/estado. Ningun toque a hook/suite/CI |
| Invariancia hook/pin/suite | git diff b37e638..ab5a017 -- .githooks/pre-commit .github/workflows/validate.yml scripts/new_instance.py scripts/test_precommit_hook.py | 0 | diff VACIO: byte-identicos a lo que verifique en el veredicto original |
| SHA del hook vs pines | sha256sum + grep del pin | 0 | 4dae776c...3bc5 identico en hook real, validate.yml y new_instance.py |
| Lectura del texto corregido | sed seccion 8.1 README_INSTANCIACION.md | 0 | ver tabla de vectores |
| Sonda de comportamiento: default, staged ROTO + arbol limpio | sh .githooks/pre-commit | 0 | 0.455s, acepta: NO materializa ni juzga los bytes staged (lo que el README ahora declara) |
| Sonda de comportamiento: flag, mismo staged roto | HOOK_FULL=1 sh .githooks/pre-commit | 1 | rechaza; materializo el snapshot staged (checkout-index a tmp protocol-index.*) y el juicio fallo sobre los bytes staged rotos |
| validate canonico (con secretos) | validate_collaboration_state.py en el repo vivo | 0 | warning benigno de FYI archivable |
| validate clon limpio (sin secretos) | validate_collaboration_state.py | 0 | drift 0 (gate B.3 incluido) a ab5a017 |
| scan_encoding clon limpio | scan_encoding.py | 0 | -- |
| scan_domain_neutrality clon limpio | scan_domain_neutrality.py | 0 | verde (la roja del ancla anterior era fixture 0271, ya remediada) |
| #4 fondo intocable | sha256sum protocol.config.json canonico y clon | 0 | 2e35f26e...b354 byte-identico en ambos |

## Tabla vector por vector (instruccion del re-juicio)

| # | Vector | Veredicto | Evidencia falsable |
|---|--------|-----------|--------------------|
| W1 | README describe el reparto REAL: default acotado inspecciona el arbol | PASA | Texto nuevo: "ejecuta sobre el arbol actual los chequeos baratos ... sin materializar el snapshot staged". Coincide con el comportamiento medido (0.455s, staged roto aceptado) |
| W2 | README no promete materializacion que el default no da | PASA | La frase falsa de b37e638 ("para todo commit materializa el snapshot staged") fue eliminada; la garantia staged queda explicitamente "reservada ... para un gate explicito" (flag) y CI |
| W3 | Garantia staged solo bajo flag o CI, declarada | PASA | README: HOOK_FULL=1 / git config hook.full true para el modo completo; "CI sigue siendo el enforcement duro y conserva la validacion completa" + pin SHA-256. Reconfirmado por comportamiento: flag materializa y rechaza exit 1 |
| W4 | Resto del parrafo intacto y correcto (riesgo HEAD rojo, mitigacion pre-push, desarme <30s) | PASA | Texto conserva riesgo aceptado E6-A, gate voluntario pre-push y desarme reversible git config --unset core.hooksPath |
| W5 | Hook y pin SIN cambios respecto al veredicto original | PASA | diff b37e638..ab5a017 vacio en hook/CI/scaffolder/suite; SHA 4dae776c identico en los tres puntos |
| W6 | Gates en el clon del nuevo HEAD | PASA | validate 0 (drift 0), scan_encoding 0, neutralidad 0, config #4 byte-identico |

Ningun vector SLIPS. No encontre un escape nuevo: intente la refutacion en ambas
direcciones (que el README siga prometiendo de mas, o que ahora prometa de menos) y el
texto queda alineado con la mecanica medida en las dos sondas.

## Residuales declarados

- R1-R5 del veredicto original: siguen vigentes, sin cambios y no bloqueantes (el fix
  fue docs-only; ninguno se agrava ni se resuelve por este cambio).
- N1 (nuevo, no bloqueante, mecanica v2 preexistente): con staged sintacticamente roto
  (JSON no parseable), el modo completo rechaza correcto (exit 1) pero el mensaje
  visible es el traceback de prune_state + "poda due", no el rechazo semantico
  "collaboration state in staged snapshot is invalid" que emite con staged parseable
  invalido. Cosmetico, anterior a b37e638; candidato a follow-up de mantenimiento.
- N2 (observacion DECISION-0018/0026, no bloqueante del cierre): en el arbol compartido
  quedo STAGED sin commitear la memoria final de Codex del cierre c2abc9c
  (CLAIMS.json con CLAIM-...-H1-final-memory ya released + personal/Codex/Memory.md +
  2 eventos). La memoria del fix c06fbad si fue commiteada (8780638). Riesgo conocido
  de arrastre por el proximo commit ajeno (caso 51dd52e). Notifico via mi MSG; no toco
  rutas de Codex.

## RECOMENDACION DE CIERRE: OK -> CERRABLE (GO)

H1 esta remediado: el README de instanciacion ahora dice la verdad del reparto E6-A
que yo verifique por comportamiento (default acotado sobre el arbol, garantia staged
solo bajo flag o CI), el hook y sus pines son byte-identicos a lo ya juzgado, y todos
los gates estan verdes en clon limpio del HEAD citado. TASK-0268 queda CERRABLE segun
mi veredicto original mas este re-juicio. Sin fix-loop pendiente.

---

task_id: TASK-0268
status: in_review
executive_summary: Re-juicio H1 en clon limpio de ab5a017 -- GO. El texto corregido de README_INSTANCIACION (c06fbad) describe el reparto real verificado por comportamiento (default acotado 0.455s acepta staged roto sin materializar; HOOK_FULL=1 materializa el snapshot staged y rechaza exit 1); hook, suite, CI y scaffolder byte-identicos a b37e638 (SHA 4dae776c en los tres pines); gates verdes; atribucion del fix a Codex confirmada en el ledger firmado. TASK-0268 CERRABLE.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0268-rejuicio-H1-veredicto.md; Area_comun/mailbox/open/MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0268-rejuicio-H1-GO.md
gates: validate exit 0 (canonico con secretos y clon limpio sin secretos, drift 0); scan_encoding exit 0; scan_domain_neutrality exit 0; config 2E35F26E byte-identico; diff hook/pin/suite vacio vs b37e638
next_recommended: Arquitecto ratifica el GO y arranca la cadena de cierre declarada (0257, gate propio, 0258, 0269, gate 0265); pedir a Codex completar o limpiar su staging de memoria final de c2abc9c (N2) antes del proximo commit ajeno.
risks: R1-R5 previos vigentes y no bloqueantes; N1 cosmetico (mensaje de rechazo con staged no parseable); N2 staged de Codex sin commitear en el arbol compartido con riesgo de arrastre (mitigado aqui con commit por pathspec explicito).
