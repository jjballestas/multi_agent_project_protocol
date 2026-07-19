---
message_id: MSG-20260719-Arquitecto-to-Operador-PLAN-0103-tabla-9-unidades
from: Arquitecto
to: Operador
type: REQUEST
status: open
requires_response: true
response_owner: Operador
requested_action: "Revisar la tabla del plan DECISION-0103 (9 unidades registradas, TASK-0257..0265) y dar OK explicito de arranque, o correcciones. Ninguna unidad arranca sin ese OK (gate manual de turno 0). Pronunciarse tambien sobre la nota de diseno N1 (carve-out de remediacion)."
question: "Apruebas el plan de 9 unidades tal como esta registrado? Y sobre N1: una unidad de remediacion nacida de un rechazo del checker, con el MISMO acceptance y scope de una unidad ya aprobada, queda cubierta por la aprobacion original o exige re-aprobacion?"
created_at: 2026-07-19
context_refs:
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "PLAN DECISION-0103 registrado: 9 unidades TASK-0257..0265 con intake DoR completo (unidad 1 = armar harness, PRIMERA). Gate manual de turno 0: nada arranca sin OK explicito. Incluye 4 notas de diseno (N1 pide decision tuya: carve-out de remediacion en C1)."
---

# PLAN DECISION-0103 - 9 unidades registradas (aprobacion de turno 0)

Hora local: 2026-07-19 19:07. DECISION-0103 formalizada (status active, firma tuya de
esta fecha) y sellada en el ledger (seq 4866-4877). Las 9 unidades estan REGISTRADAS en
status proposed con intake DoR completo. Por la paradoja de arranque declarada en la
decision, este mensaje es el gate manual de turno 0: NADA arranca hasta tu OK explicito
por esta via.

## Tabla del plan

Goal y acceptance van comprimidos; el detalle completo y vinculante esta en el .md de
cada tarea (ruta en la columna id).

| id | goal (compacto) | acceptance (compacto) | verification_cmd (nucleo) | required_capability | risk | estimate |
|---|---|---|---|---|---|---|
| TASK-0257 | C5: core.hooksPath -> .githooks/ + pre-commit invoca validate y falla en rojo; espejo born-operational | hooksPath cableado y repetible; hook aborta commit rojo y conserva checks previos; valida el snapshot (no el tree sucio); coste medido, modo acotado si lento, NUNCA desactivado; instancia nueva nace armada | git config core.hooksPath + prueba negativa/positiva en sandbox + validate | implementer | medium | M |
| TASK-0258 | C3: bloque obstacles[] en turn_schema.json | campo opcional con required what/root_cause/resolution/recurrence_risk (enum low/medium/high); SemVer minor del schema; suites verdes; forma canonica unica para ambos carriles | run_runtime_turn_cases + validate | implementer | low | S |
| TASK-0259 | C3: turn_validate condicional, obstacles obligatorio si friccion (gate_green false / attempt>1 / revert) | FAIL accionable si friccion y obstacles vacio; vacio legitimo sin friccion; 3 sensores documentados y testeados | run_runtime_turn_cases + validate | implementer | low | S |
| TASK-0260 | C1: vista de plan del conjunto (--plan-all) + gate de aprobacion turno 0 en orchestrator | tabla completa desde ficheros atestados (proyeccion, 0009); sin aprobacion registrada no arranca; cambio material invalida aprobacion; probado SOLO en scratch, jamas ejecutado en el hub | suites runtime + suite del gate + validate | implementer | medium | M |
| TASK-0261 | C3/C4: validate_mailbox exige obstacles + friction_count en type REPORTE | cruce friccion>0 y obstacles vacio = FAIL; vacio con friccion 0 pasa; GRANDFATHERING por fecha (historico NO se pone rojo); 4 cuadrantes en suite | validate exit 0 con historico intacto + suite mailbox | implementer | medium | M |
| TASK-0262 | C2/C4: plantillas de REPORTE de entrega y de reporte de ASIGNACION (unidad, agente, por que) | bloque obstacles IDENTICO al del schema; asignacion con datos ya emitidos por el routing; ejemplos completos; ASCII + neutralidad | validate + scan_encoding + scan_domain_neutrality | implementer (doc) | low | S |
| TASK-0263 | C3-bis: oferta de mejora (high o root_cause x2 -> propuesta YA redactada; registro durable acepta/rechaza/parquea) | deteccion determinista documentada; oferta con borrador concreto; rechazada no se re-ofrece; CERO auto-aplicacion | suite nueva del mecanismo + validate | implementer | medium | L |
| TASK-0264 | C1 (doc): regla de arranque, ningun conjunto sin plan aprobado | regla en TASK_PROTOCOL.md citando C1; espejo born-operational; FYI al Asesor (su prompt lo actualiza el) | validate + scans | implementer (doc) | low | S |
| TASK-0265 | gate: revision adversarial del conjunto por checker de proveedor diverso (0101) | veredicto por unidad en CLON LIMPIO; 5 pruebas adversariales (hook, friccion x2 carriles, grandfathering, no-re-oferta); residuales honestos | validate en clon limpio + suites + evidencia adversarial | reviewer | low | M |

Orden: 0257 PRIMERA (harness; las demas nacen ya exigidas por el hook). Luego
0258 -> 0259 (schema antes que validacion), 0260-0263 segun cola, 0264 con 0260,
0265 ULTIMA como gate del conjunto.

## Ejecucion (tus ordenes del 2026-07-19, ya recogidas en los intakes)

- Flujo gobernado NORMAL (cron/sesion + submit_intent), NO runtime orchestrator en el
  hub. maker = Codex (implementer); checker = proveedor diverso (DECISION-0101).
- Guardas en el out_of_scope de TODAS las unidades: reservadas N=6 intactas (R0-fuentes,
  R2-c, R3-b, R4-b, R4-c, R5-c), fondo intocable (2E35F26E / epoch 1.14.0 / N=500), sin
  encender supervised_autonomy ni real_invoker. validate verde antes y despues (baseline
  de hoy: verde).

## Notas de diseno (punto 8 de tu orden; ninguna bloqueo la firma tal cual)

- N1 (la unica que pide decision tuya, va en la pregunta de este mensaje): C1 dice que
  "unidades nuevas" re-aprueban. Leido estricto, cada rechazo del checker que genere una
  unidad de remediacion re-gatea contigo (y el bounce es frecuente: 4/5 en el piloto).
  Propongo el carve-out: remediacion con el MISMO acceptance y scope de una unidad
  aprobada queda cubierta por la aprobacion original; solo acceptance/scope/risk nuevos
  re-aprueban. Si lo apruebas, es una enmienda de una linea a la 0103 (o interpretacion
  registrada); TASK-0260 lo deja explicitamente fuera de alcance mientras tanto.
- N2: el hook debe validar el SNAPSHOT que se commitea, no el working tree sucio (el
  tree caliente miente; leccion clean-clone). Ya esta en el acceptance de TASK-0257.
- N3: el bypass local de hooks de git existe; el hook es primera linea, el enforcement
  duro sigue en CI + clean-clone + gates de cron. Declarado en TASK-0257, sin cambiar C5.
- N4: exigir obstacles en type REPORTE sin fecha de corte pintaria ROJO el historico del
  canal (validate barre open/answered/archived). Grandfathering por fecha/marker es
  acceptance obligatorio de TASK-0261, no opcional.

Higiene del canal en este mismo cierre: 6 mensajes consumidos de open/ (4 REPORTE + 2
RESP del 18-19 jul, todos terminales y ya recogidos en tus checkpoints) van a archived/
via mailbox_archive.
