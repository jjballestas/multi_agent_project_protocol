# BACKLOG F1 DESCOMPUESTO - Nucleo doctrinal v1.18.0 (paquete F0, parte c)

Estado: entregable del Asesor. El Arquitecto lo registra como tareas TASK-02xx
([VISION-NOVA][F1.x] + relates_to GOAL-VISION-NOVA-001) DESPUES de que F0.2
(DECISION-0083) este commiteada. Se promueve DE A UNA (regla vigente). Los ids
finales los asigna el Arquitecto con el siguiente numero libre del indice.

Auditoria previa (asesor): los PRDs son estrategicos, NO ejecutables; NO soltar
agentes contra PRDs directamente — solo contra estas tareas con DoD testable.

## Secuencia recomendada

F1-A -> F1-B -> F1-C (cadena Codex, de a una; B y C comparten runtime/validador)
en paralelo: F1-D y F1-E (Arquitecto/doctrina, no bloquean a Codex)
cierre: F1-F (mini-DECISION) + F1-G (release v1.18.0)
F1.6 (aprendizajes-externos, timebox 2d) SOLO si hay holgura; nunca camino critico.

---

## F1-A [F1.1] Gate de intake determinista

- Owner: Codex. Spec: SPEC-F1-gate-intake.md (v0.1 adjunta al paquete F0).
- Alcance: regla R1-R6 en validador (ps1 + python) y runtime (task_status hard-gate);
  bloque intake en templates; examples/minimal_instance actualizado.
- DoD (testable):
  1. Los 6 casos negativos y 3 positivos del SPEC s.4 implementados como tests; verdes.
  2. Transicion proposed->ready via submit_intent con intake invalido = rechazo
     atomico (exit != 0, sin drift).
  3. Los 3 gates (validate + encoding + neutralidad) verdes en CLON LIMPIO de HEAD.
  4. Cero terminos de dominio en core/templates (scan neutralidad exit 0).

## F1-B [F1.2] Evento firmado exception.recorded

- Owner: Codex. Spec: SPEC-F1-exception-trailers.md PARTE A.
- Alcance: intent `exception` en submit_intent + schema A.1 (enums cerrados, ASCII,
  sin PII) + doctrina U1-U3 en TASK_PROTOCOL.md (y template).
- DoD (testable):
  1. submit_intent acepta el intent y rechaza: kind fuera de enum, summary no-ASCII,
     exception_id duplicado, task_id inexistente (4 tests negativos).
  2. Round-trip: 2 eventos reales (assist + arbitration) emitidos en rama, replay
     drift=0, listables por task_id.
  3. Regla U2 (listado publicable) documentada en TASK_PROTOCOL; encoding gate verde.
  4. Gates verdes en clon limpio.

## F1-C [F1.3] Trailers bloqueantes Task-Id / Fixes-Task

- Owner: Codex. Spec: SPEC-F1-exception-trailers.md PARTE B.
- Alcance: escaneo de rango de commits en el validador (V1-V5), trailer_start_seq
  registrado, allowlist ops (`Task-Id: none` + `Ops-Reason`).
- DoD (testable):
  1. Los 8 casos B.3 (4 negativos + 4 positivos) como tests sobre repo fixture; verdes.
  2. El propio repo valida verde con commits historicos exentos (arranque declarado).
  3. Un commit de prueba en rama sin trailer hace fallar validate (demo reproducible);
     revertido despues de la evidencia.
  4. Gates verdes en clon limpio.

## F1-D [F1.4] Taxonomia de defectos D1-D4 ampliada + severidad del checker

- Owner: Arquitecto (doc) + Analista (gate adversarial). Codex no requerido.
- Alcance: doc versionado con subcategorias que cubren los 6 huecos del veredicto
  (requisito mal entendido, deuda de arquitectura, performance no testeada,
  UX/soporte, integracion externa, conciliacion tardia) + seccion explicita de
  SUBCONTEO ESPERADO (que defectos el estudio declara que NO capta). Adopta la
  severidad del checker CRITICAL / WARNING-real / WARNING-theoretical / SUGGESTION
  con la regla "si el uso normal lo dispara, es real" (cosecha gentle-ai).
- DoD (testable):
  1. Doc en Area_comun/protocol/ (o anexo del pre-registro) commiteado, ASCII.
  2. Prompt del checker (Analista) actualizado con la escala de severidad.
  3. Prueba de mesa: 10 defectos historicos del repo re-clasificados sin residuo
     (ninguno cae fuera de la taxonomia); anexada como evidencia.
  4. GO adversarial del Analista sobre la taxonomia.

## F1-E [F1.5-harness] Envelope de handoff 7 campos + fix-loop pre-commit

- Owner: Codex (harness de peers) + Arquitecto (doctrina). Cosecha gentle-ai nivel A.
- Alcance: schema de envelope (status / executive_summary / artifacts /
  next_recommended / risks + task_id + gates) en TASK_PROTOCOL + regla dura
  "el envelope es TEXTO FINAL del turno, nunca un tool call"; fix-loop: tras NO-GO
  del checker, remediacion + RE-JUICIO obligatorio antes del commit de cierre,
  tope 2 iteraciones y escalada al operador; opcional workload-guard N-lineas con
  size:exception (via exception.recorded kind=scope_change).
- DoD (testable):
  1. Schema y reglas en TASK_PROTOCOL.md (y template) commiteados.
  2. Prompts de cron de Codex y Analista actualizados con envelope + fix-loop.
  3. 1 handoff real conforme al envelope como evidencia (cita de commit/mensaje).
  4. Gates verdes en clon limpio.

## F1-F [F1.5] Mini-DECISION identidad anti-vibecoding

- Owner: Arquitecto (redaccion corta; ya existe draft en el area del operador,
  REQs Zeus-Aegis v0.2.0). Registra la identidad (interrogacion de requisitos +
  quality panel + excepciones auditadas via F1-B) como decision de doctrina.
- DoD: DECISION registrada via submit_intent, gates verdes, relates_to
  GOAL-VISION-NOVA-001 + DECISION-0083.

## F1-G [F1.7] RELEASE v1.18.0

- Owner: Arquitecto. Cierra F1: version SemVer + CHANGELOG + tag. Este tag es el
  que consume F2.1 (new_instance nova-budget).
- DoD: CHANGELOG actualizado; tag v1.18.0 sobre commit con los 3 gates verdes en
  clon limpio; templates sincronizados con las reglas nuevas (intake/exception/
  trailers/envelope); FYI al operador.

---

## Nota F2 (para la orden F2 posterior, NO ejecutar ahora)

La cosecha gentle-ai nivel B entra en F2: configs de agente COMMITEADAS en el repo
de instancia (Git es el adapter; NO construir adapters multi-IDE), dry-run +
write-atomico temp+rename en new_instance, y PROHIBIDO `gentle-ai install` en
maquinas Nova (inyecta Engram; reabriria DECISION-0081 y contamina el estudio).
Nivel C (merge por secciones, manifiesto, doctor) DIFERIDO a F5/agosto con DECISION.
