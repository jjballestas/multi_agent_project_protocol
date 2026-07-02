# SPEC-F1-GATE-INTAKE - Gate de intake determinista (v0.1, base para F1.1)

Estado: DRAFT del Asesor para F0; el Arquitecto la refina y Codex la implementa en F1.
Objetivo: ninguna tarea entra a `ready` sin una definicion verificable (anti-vibecoding).
Cubre el item F1.1 del tablero. Neutral de dominio: la regla vive en el validador
generico y los templates, sin terminos de negocio.

## 1. Schema del bloque `intake` (frontmatter de TASK-XXXX-*.md)

```yaml
intake:
  type: feature | fix | infra | doc | research      # obligatorio, enum cerrado
  goal: "<1 linea, no vacia>"                        # obligatorio
  acceptance:                                        # obligatorio, >=1 item
    - "<criterio verificable por comando o gate>"
  verification_cmd:                                  # obligatorio, >=1 comando
    - "<comando o gate exacto que decide el criterio>"
  scope_routes:                                      # obligatorio, >=1 ruta
    - "<ruta permitida>"
  out_of_scope:                                      # obligatorio, >=1 item
    - "<que NO se toca>"
  risk: low | medium | high                          # obligatorio, enum cerrado
  estimate: S | M | L                                # obligatorio (anti-Goodhart:
                                                     #  el sizing queda registrado
                                                     #  ANTES de ejecutar)
```

Campo opcional de escape (liga con SPEC-F1-exception-trailers):

```yaml
intake_exempt: true
exception_ref: "<seq del evento exception.recorded que autoriza la exencion>"
```

## 2. Reglas de validacion (hard-gate en validador + runtime)

- R1: tarea con status en {ready, claimed, in_progress, in_review, done} SIN bloque
  `intake` completo y valido => `validate` exit != 0. `proposed` puede carecer de el.
- R2: campo vacio, placeholder ("TBD", "todo", "n/a", "...") o enum fuera de rango
  => invalido.
- R3: cada item de `acceptance` debe tener al menos un `verification_cmd` asociado
  (v0.1: |verification_cmd| >= 1 y la relacion se revisa en review; v0.2 puede
  exigir mapeo 1:1).
- R4: la transicion proposed->ready via submit_intent (task_status) valida el intake
  ANTES de aplicar; si falla, la transaccion se rechaza completa (mismo patron B.3).
- R5: `intake_exempt: true` requiere `exception_ref` valido (evento existente de tipo
  exception.recorded con kind=intake_exempt y task_id coincidente); si no, invalido.
- R6: los templates (`*.template.*`) incorporan el bloque intake vacio comentado;
  la instancia viva y `examples/minimal_instance` validan verde con la regla activa.

## 3. Estados

No se agregan estados nuevos al ciclo (proposed -> ready -> ... se conserva). El
"intake OK" NO es un estado: es una precondicion dura de `ready`. Esto evita tocar
el core del lifecycle (cambio compatible, no breaking).

## 4. Casos de prueba minimos (DoD de F1.1)

Positivos: (P1) proposed sin intake valida; (P2) ready con intake completo valida;
(P3) ready con intake_exempt + exception_ref valido valida.
Negativos: (N1) ready sin intake; (N2) goal vacio; (N3) acceptance con "TBD";
(N4) risk fuera de enum; (N5) intake_exempt sin exception_ref; (N6) transicion
proposed->ready via submit_intent con intake invalido (rechazo atomico).
