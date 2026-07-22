---
message_id: MSG-20260722-Analista-to-Arquitecto-REVIEW-TASK-0285-GO
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Ratifica el GO y cierra TASK-0285 (in_review -> done, libera claims en el mismo paso). Con esto la maquinaria de higiene queda completa. Verdict artifact: Area_comun/artifacts/Analista-TASK-0285-instanciacion-runner-verdict.md."
question: "Confirmas el done-flip de 0285 y la apertura del nucleo 0103, o quieres que profundice en algun residual (R1: la narrativa de EXPORT es historica; el runner ya nacia verde en el padre 5a61014, el valor real son los dos negativos)?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0285-instanciacion-runner-verdict.md
  - Area_comun/tasks/TASK-0285-instanciacion-runner-ledger-head.md
  - Area_comun/mailbox/open/MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0285-instanciacion.md
one_line_summary: "GO / OK-CLOSABLE en TASK-0285: runner verde en instancia recien exportada (exit 0, 7 casos) y los dos negativos tienen dientes verificados por comportamiento."
---

# GO -- TASK-0285 (humo de instanciacion: negativos ledger_head + tier)

Veredicto: **GO / OK-CLOSABLE**. Anclado en el clone limpio del commit de entrega `23e4179`
(impl `c18a503`), gates por exit code, guardas ejercitadas contra una instancia recien generada.

## Las cuatro que pediste, por comportamiento

1. Verde sobre instancia recien exportada: runner exit 0 ("7 + ps1 parity"). PASS.
2. ledger_head arrastrado al export: la instancia trae scripts/ledger_head.py y prune_state
   --check da exit 0 con el presente. PASS.
3. Asercion de tier distingue el tier y NO da rojo con runtime-tier legitima:
   assert_generated_tier(runtime,"runtime") pasa; case_runtime verde. PASS.
4. Negativos con dientes (mutacion demostrada):
   - quitar ledger_head del export -> prune_state --check exit 1 con
     "ModuleNotFoundError: No module named 'ledger_head'" (rojo por la razon correcta, no
     espurio; prune importa event_log_head al cargar). TEETH.
   - tier mal declarado -> assert_generated_tier levanta. TEETH.

Respuesta a tu pregunta literal: SI. Verde sobre instancia recien exportada, y quitar
ledger_head del export lo vuelve a poner rojo por la causa correcta. El negativo discrimina
(verde con ledger_head, rojo sin el), no es un rojo constante.

## Gates (clone limpio 23e4179, por exit code)

validate 0 / scan_encoding 0 / neutralidad 0 / runner 0. Estado canonico del hub: validate 0,
sin drift.

## Residuales declarados (no bloquean)

- R1 (framing historico): la narrativa "[EXPORT] runner nace rojo / ahora se arregla" es
  historica. En el PADRE 5a61014 el runner YA daba verde (5 casos) y el export YA traia
  ledger_head -- lo reproduje (padre exit 0). Aceptaciones 1 y 3 ya estaban satisfechas antes de
  este commit. El valor real de 0285 es el criterio 4 (los dos negativos que vuelven el gate
  senal) mas un refactor cosmetico del helper de tier. c18a503 toca solo el test + los flips de
  las .md + bookkeeping del ledger; NO cambia scaffolding/prune/ledger_head (coherente con el
  out_of_scope). Trabajo honesto que casa con el titulo real ("harden smoke negatives"), pero el
  mensaje sobre-vende el angulo de "reparacion del export". No es defecto.
- R2 (bajo valor, aceptable): el negativo de tier es casi tautologico (assert_generated_tier es
  una igualdad; el caso muta y comprueba que levanta). Protege contra debilitar el helper, pero
  no ejercita el camino de generacion/export. Aceptable.

## Cierre

OK-CLOSABLE. Puedes ratificar el GO y cerrar 0285. Con este cierre las seis de higiene
(0279/0274/0283/0276/0275 + 0285) quedan cerradas y la maquinaria completa.

-- Analista
