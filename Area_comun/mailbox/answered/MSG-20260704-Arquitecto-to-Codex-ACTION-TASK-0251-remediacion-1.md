---
message_id: MSG-20260704-Arquitecto-to-Codex-ACTION-TASK-0251-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0251-p22-reporte-ejecucion-presupuestal.md
  - Area_comun/handoffs/HANDOFF-TASK-0251-codex-to-arquitecto-1.md
one_line_summary: "TASK-0251 adversarial informal (sesion separada): GO en general (gateway SQL real confirmado, no es el fixture de TASK-0250), pero con 1 hallazgo a cerrar antes de ratificar: posible doble-paginacion (proc-side @page_size + Skip/Take en C# sobre el resultado ya limitado por el proc), sin ningun test que ejerza esa interaccion."
requested_action: "Cierra ANTES de que ratifique (fix-loop 1/2, tope antes de escalar al operador): en BudgetExecutionReportService.GetExecutionReportAsync (ExecutionReportQueries.cs) se pasa query.PageSize al proc via @page_size Y SEPARADAMENTE se hace .Skip((Page-1)*PageSize).Take(PageSize) en C# sobre las filas que YA devolvio el proc. Si @page_size limita filas del lado del proc (probable dado el nombre), la pagina 2+ hace Skip sobre un resultado YA truncado -> paginas posteriores devuelven vacio o filas incorrectas, y el conteo total (criterio 1 de la SPEC, 652 filas esperadas) podria reportarse mal si algo en el pipeline asume el total sin paginar. NINGUN test (StubExecutionReportGateway/TestBudgetExecutionReportGateway) ejerce esta interaccion -- ambos ignoran query.PageSize. NECESITO: (a) clarifica/confirma el contrato real de @page_size en el proc (via su definicion citada en la SPEC o comentario del DoR) -- si el proc YA pagina, ELIMINA el Skip/Take duplicado en C# (la paginacion es responsabilidad del proc, no se re-implementa); si el proc NO pagina (page_size es otro parametro, p.ej. un limite de otra naturaleza), documenta por que el doble mecanismo es intencional y correcto. (b) Agrega un test que ejerza la interaccion real (un stub que SI respete query.PageSize limitando su resultado, para que Skip/Take sobre un resultado ya limitado por el stub sea visible y falle si esta mal). Residual aceptado (NO bloqueante, ya declarado honesto): paridad de conteo en vivo (652/467/229/238 filas) contra DbsFinanciero sigue pendiente de quien tenga credenciales; el DTO dinamico Dictionary<string,object?> en vez de un contrato tipado de 50 columnas es una eleccion razonable mientras no se re-verifique el shape contra la BD desplegada (F-NOVA-01) -- no lo cambies ahora, solo cuando haya verificacion en vivo."
question: ""
---

# ACTION - Remediacion 1/2 TASK-0251 (posible doble-paginacion sin test)

El adversarial informal (sesion separada) dio GO en general -- confirmo que el gateway SI es SQL real
(no repite el fallo de TASK-0250) -- pero encontro 1 hallazgo concreto a cerrar antes de que ratifique:
posible doble-paginacion (proc-side `@page_size` + `Skip/Take` en C# sobre un resultado que el proc ya
pudo haber limitado), sin ningun test que la ejerza. Detalle y accion pedida en `requested_action`.

Fix-loop 1/2 (tope antes de escalar al operador si sobrevive la misma clase de hallazgo).
