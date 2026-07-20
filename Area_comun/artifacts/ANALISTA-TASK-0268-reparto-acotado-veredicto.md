---
artifact_id: ANALISTA-TASK-0268-reparto-acotado-veredicto
task_id: TASK-0268
author: Analista
role: revisor adversarial independiente (checker, DECISION-0056)
created_at: 2026-07-20
anchor_commit: f2d07a3
implementation_commit: b37e638
---

# Veredicto del Analista -- TASK-0268 (E6-A: reparto de coste del hook)

Hora local: 2026-07-20 05:53 (+0200). Firma: Analista (voz adversarial, checker-only).

## Ancla canonica

- Instruccion: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0268-reparto.
- Entrega del maker: commit b37e638 (Codex, handoff HANDOFF-TASK-0268-Codex-to-Analista.md).
- Ancla de la review: HEAD f2d07a3 citado por la instruccion, reproducido en CLON LIMPIO
  (/d/ccv0268, git clone + checkout f2d07a3; sondeos en segundo clon /d/ccv0268b).
- Durante la review el canonico avanzo a 45eb10f (remediacion de neutralidad de TASK-0271
  del maker, ajena a esta tarea); el ancla y el veredicto no cambian.
- Alcance declarado por la instruccion: SOLO HUB, sin producto en alcance.
- Orden de cola respetado: la review de TASK-0270 fue entregada y ratificada antes (1cb7b0e).

## Reproduccion (exit codes reales)

| Paso | Comando (clon limpio) | Exit | Dato |
|------|----------------------|------|------|
| Pin CI vs hook real | sha256sum .githooks/pre-commit | 0 | 4dae776c...3bc5 == pin en validate.yml y en new_instance.py |
| Suite del hook | python scripts/test_precommit_hook.py | 0 | caso default-acotado <2s + negativos v2 bajo flag |
| Default, commit gobernado real | git commit (AGENTS.md staged, hooksPath activo), 3 corridas | 0 | 0.455s / 0.482s / 0.483s |
| Default, estado gobernado ROTO staged (arbol limpio) | sh .githooks/pre-commit | 0 | 0.494s -- acepta: NO invoca validador completo |
| Flag env, mismo staged roto | HOOK_FULL=1 sh .githooks/pre-commit | 1 | 29.3s, "collaboration state in staged snapshot is invalid" |
| Flag config, mismo staged roto | git config hook.full true; sh .githooks/pre-commit | 1 | 32.4s, mismo rechazo |
| Precedencia env sobre config false | hook.full=false + HOOK_FULL=1 | 1 | 29.9s, rechaza |
| Poda rota en arbol, default | prune_state.py stub exit!=0 | 1 | mensaje "poda due", commit bloqueado |
| Drift de guia staged, default | HUMAN_GUIDE.template.md editado y staged | 1 | mensaje de drift de guia, commit bloqueado |
| Espejo born-operational | new_instance.py (tier coordination y runtime) | 0 | hook byte-identico (4dae776c); tier runtime emite CI con pin nuevo |
| validate canonico (con secretos) | validate_collaboration_state.py | 0 | a f2d07a3 |
| validate clon limpio (sin secretos) | validate_collaboration_state.py | 0 | drift 0 en ancla (gate B.3 incluido) |
| scan_encoding clon limpio | scan_encoding.py | 0 | -- |
| scan_domain_neutrality clon limpio | scan_domain_neutrality.py | 1 | 7 hits, TODOS en scripts/test_anthropic_checker_harness.py (TASK-0271, preexistente a b37e638; verificado en b37e638~1); 0 hits en rutas de 0268; ya verde a 45eb10f (exit 0) |
| #4 fondo intocable | sha256sum protocol.config.json | 0 | 2e35f26e... byte-identico en canonico y clon; events.jsonl del ancla integro (validate 0); el delta posterior es crecimiento legitimo del chain por commits 0271 |

Medicion del maker (0.449s default, 59.891s completo) reproducida en orden de magnitud:
default 0.45-0.49s estable; completo 29-32s en mi maquina (la serie v2 51.5-53.3s y el
59.9s del maker corresponden a su entorno; misma mecanica, mismo camino de codigo).

## Tabla vector por vector

| # | Vector (instruccion) | Veredicto | Evidencia falsable |
|---|---------------------|-----------|--------------------|
| V1 | Commit gobernado local con default termina <~2s | PASA | 3 commits reales gobernados: 0.455/0.482/0.483s |
| V2 | Default conserva prune_state --check y drift de guia | PASA | poda rota -> exit!=0; guia staged con drift -> exit 1 |
| V3 | Default NO invoca el validador completo | PASA (diseno E6-A) | staged gobernado roto aceptado en 0.494s exit 0; el mismo staged rechazado bajo flag |
| V4 | Flag env HOOK_FULL=1 activa mecanica v2 completa sin cambios | PASA | materializacion + validate en snapshot staged, rechazo exit 1; diff de b37e638 solo cambia el selector, el bloque v2 (mktemp/checkout-index/required-files/validate) queda intacto |
| V5 | Flag git config hook.full true activa completo | PASA | rechazo exit 1 (32.4s); via NO cubierta por la suite, verificada aqui por comportamiento (residual R2) |
| V6 | CI intacto: validate completo + pin existencia/SHA actualizado | PASA | diff de validate.yml toca SOLO la linea del pin; pin == sha256 real del hook entregado |
| V7 | Suite ajustada al reparto | PASA | exit 0 en clon limpio; caso nuevo default-acotado-rapido; negativos v2 (estado invalido, R100, cleanup, aislamiento unstaged) migrados a full=True y en verde |
| V8 | Espejo born-operational | PASA | instancia nueva nace con hook byte-identico y (tier runtime) CI pineado al SHA nuevo; compatible con lo que TASK-0266 (ready) propagara |
| V9 | Docs del reparto en el hook con riesgo declarado | PASA | cabecera del hook: reparto, flags, HEAD rojo transitorio y mitigacion pre-push |
| V10 | Docs del reparto en README_INSTANCIACION | SLIPS (H1) | ver hallazgo H1: describe una mecanica que el default no ejecuta |

## Hallazgo H1 (falsable): README promete materializacion staged en todo commit

README_INSTANCIACION.md (seccion del hook, texto de b37e638): "El pre-commit es la primera
linea rapida: para todo commit materializa el snapshot staged, ejecuta prune_state.py
--check y comprueba el drift de la guia cuando corresponde."

Esa frase es FALSA en el modo por defecto que esta misma entrega instala:

- El propio hook lo declara: "The bounded path intentionally avoids checkout-index ...
  These cheap guards inspect the current tree" (lineas 25-27) y sale con exit 0 antes del
  bloque de materializacion (linea 49).
- Refutacion por comportamiento (ambas direcciones):
  1. Staged ROTO + arbol limpio -> el default ACEPTA en 0.494s (materializar y validar
     toma ~30s; no hubo materializacion ni juicio de los bytes staged).
  2. prune_state.py roto SOLO en el arbol (sin stagear) -> el default RECHAZA: el acotado
     juzga el ARBOL DE TRABAJO, no el snapshot staged.
- Impacto: el adoptante que lee el README cree que su primera linea juzga los bytes
  staged con el aislamiento v2 (garantia que 0267 si daba en local y que E6-A traslado
  deliberadamente al flag y al CI). El riesgo E6-A esta bien declarado, pero el
  consentimiento informado se apoya en una descripcion de mecanica incorrecta.
- Remediacion esperada (docs-only, 1-2 frases): el acotado ejecuta chequeos baratos sobre
  el arbol actual SIN materializacion; solo el modo completo (flag) materializa y juzga
  los bytes staged. El resto del parrafo (flags, desarme, HEAD rojo, CI enforcement) es
  correcto y queda igual.

## Residuales declarados (no bloqueantes)

- R1: primera invocacion en un clon recien creado midio 22.5s (cache de FS/AV frio,
  Windows); el regimen estable es 0.45-0.5s. Ambiental, no mecanica del hook.
- R2: la suite no ejercita la via git config hook.full true (solo HOOK_FULL=1); quedo
  verificada por comportamiento en esta review. Sugerencia de caso de suite en un
  follow-up (0269 o mantenimiento), sin bloquear.
- R3: en acotado, poda y guia dependen del arbol de trabajo (un unstaged puede alterar el
  veredicto local). Declarado en el hook; mitigado por flag completo + CI.
- R4: HOOK_FULL solo reconoce el valor "1" (HOOK_FULL=true cae al acotado en silencio);
  el flag esta documentado como =1.
- R5: el acotado permite commitear incluso la eliminacion del validador local; CI (pin
  SHA-256 + validate de clon limpio) lo detecta. Es el riesgo aceptado del reparto E6-A.
- Neutralidad roja en el ancla por fixture preexistente de TASK-0271 (0 hits en rutas de
  0268); ya remediada por el maker en 6ab2d4e (exit 0 a 45eb10f). Sin accion en 0268.

## RECOMENDACION DE CIERRE: CAMBIO-REQUERIDO (acotado a docs)

Todo lo funcional PASA: reparto operativo, flags correctos con mecanica v2 intacta, CI y
pin correctos, suite verde, espejo born-operational verde, gates verdes. El cierre queda
gateado UNICAMENTE por H1: un doc gobernado de instanciacion no puede prometer una
garantia ("materializa el snapshot staged" en todo commit) que el default entregado no
da. Con la frase corregida, CERRABLE.

Fix-loop esperado (maximo 2 iteraciones antes de escalar al operador):
1. Codex corrige la frase de mecanica en README_INSTANCIACION.md (docs-only; el hook y su
   pin NO cambian, el pin CI no se toca).
2. Gates afectados del re-juicio: lectura del texto corregido + scan_encoding exit 0 +
   validate exit 0 en clon limpio del nuevo HEAD.
3. Re-juicio del Analista sobre ese commit; si el hook cambiara (no debe), el pin CI y la
   suite vuelven al alcance completo.

---

task_id: TASK-0268
status: in_review
executive_summary: Reparto E6-A funcionalmente correcto (default acotado 0.455-0.483s en commit gobernado real, flags env y config activan la mecanica v2 intacta con rechazo del staged roto, CI solo cambia el pin y coincide con el hook, suite y espejo born-operational verdes), pero CAMBIO-REQUERIDO docs-only: README_INSTANCIACION afirma que todo commit materializa el snapshot staged y el default entregado no materializa (juzga el arbol; refutado por comportamiento en ambas direcciones).
artifacts: Area_comun/artifacts/ANALISTA-TASK-0268-reparto-acotado-veredicto.md; Area_comun/mailbox/open/MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0268-veredicto.md
gates: suite hook exit 0; validate exit 0 (canonico con secretos y clon limpio sin secretos, drift 0); scan_encoding exit 0; neutralidad roja solo por fixture preexistente 0271 (0 hits en rutas 0268; verde a 45eb10f); config 2E35F26E byte-identico
next_recommended: Rutear a Codex la remediacion docs-only de H1 (1-2 frases en README_INSTANCIACION); re-juicio rapido del Analista sobre ese commit y la tarea queda CERRABLE.
risks: Sin la correccion, los adoptantes leen una garantia de juicio staged que el default no da; residuales R1-R5 declarados y no bloqueantes; el riesgo HEAD-rojo transitorio es el aceptado por E6-A y esta bien declarado en el hook.
