# DEFINITION OF READY v2 - Checklist del Operador (10 puntos) vs intake vigente

- fecha: 2026-07-03
- origen: pregunta del Operador ("la metodologia quedara preparada con esta idea?")
- estado: capturado + ruteado a TASK-0243 (mini-DECISION anti-vibecoding) y F2.1
  (template de instancia). El gate de 0238 NO se reabre (ciclo cerrado; anti
  scope-creep pre-30jul).

## 1. Los 10 puntos del Operador (verbatim)

objetivo definido; usuario objetivo definido; alcance definido; fuera de alcance
definido; contenido/assets definidos; restricciones tecnicas definidas; criterios
de aceptacion definidos; pruebas/gates definidos; riesgos definidos; prioridad
definida.

## 2. Mapa contra el intake v1 (TASK-0238, YA en produccion en el hub)

| Punto del Operador | Intake v1 hoy | Estado |
|---|---|---|
| objetivo | `goal` (1 linea obligatoria) | CUBIERTO |
| criterios de aceptacion | `acceptance` (>=1, verificable) | CUBIERTO |
| pruebas/gates | `verification_cmd` (>=1 comando exacto) | CUBIERTO |
| fuera de alcance | `out_of_scope` (>=1 obligatorio) | CUBIERTO |
| alcance | `scope_routes` (rutas permitidas) | PARCIAL (rutas si, alcance funcional no) |
| riesgos | `risk` (enum low/medium/high) | PARCIAL (nivel si, lista de riesgos no) |
| usuario objetivo | -- | NO CUBIERTO |
| contenido/assets | -- | NO CUBIERTO |
| restricciones tecnicas | -- | NO CUBIERTO |
| prioridad | -- (la maneja el orden del backlog / de-a-una) | NO CUBIERTO como campo |

6/10 cubiertos o parciales. El v1 se diseno minimo a proposito: tareas de
infraestructura del hub. Los 4 faltantes son campos de PRODUCTO -- exactamente
lo que Nova Budget necesita cuando empleados y agentes trabajen features.

## 3. Diseno intake v2 (por tipo de tarea; enums y anti-vacio)

BASE (todo tipo, ya vigente): type, goal, acceptance, verification_cmd,
scope_routes, out_of_scope, risk, estimate. SE AGREGA: `priority: P1|P2|P3`.

ADICIONAL para `type: feature|product` (tareas de producto de la instancia):
- `target_user`: "<quien lo usa, 1 linea>"          (usuario objetivo)
- `functional_scope`: "<que hace, 1-3 lineas>"      (alcance funcional)
- `assets_inputs`: [<lista>] | "ninguno"            (contenido/assets: disenos,
  textos, datos, credenciales de prueba)
- `tech_constraints`: [<lista>] | "ninguna"         (stack, performance, compat)
- `risks_list`: [<lista >=1>] | "ninguno declarado" (riesgos concretos)

REGLA ANTI-VACIO: "ninguno"/"ninguna" EXPLICITO vale (es una declaracion);
campo AUSENTE no vale. Placeholders (TBD) = invalido (regla R2 vigente).

## 4. Donde aterriza (sin reabrir lo cerrado)

1. TASK-0243 (mini-DECISION anti-vibecoding, proposed): el checklist entra como
   ANEXO "Definition of Ready" -- la interrogacion de requisitos (la identidad
   del producto) existe precisamente para LLENAR estos 10 puntos antes de que
   una tarea sea ready.
2. F2.1 (new_instance nova-budget): el TASK_TEMPLATE de la instancia extiende el
   bloque intake con los campos v2 para type feature/product. Los agentes y
   empleados de Nova Budget los llenan desde el dia 1 del Sprint 1.
3. El validador del HUB no cambia en F1 (0238 cerrada; enforcement estructural
   de los campos v2 = tarea de la instancia o v1.19, decision futura).

## 5. Beneficio directo para los agentes

Con los 10 puntos: (a) el implementador sabe QUE construir sin inventar alcance
(anti-vibecoding); (b) el checker gatea contra acceptance+verification sin
ambiguedad; (c) el futuro router de ejecutores (PRE-DECISION) gana features de
ruteo (assets/constraints/priority discriminan peon vs tier); (d) los peones
reciben contratos completos (el spike ya exige esto manualmente).
