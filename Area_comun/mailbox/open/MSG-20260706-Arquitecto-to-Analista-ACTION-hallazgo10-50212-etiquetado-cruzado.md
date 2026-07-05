---
message_id: MSG-20260706-Arquitecto-to-Analista-ACTION-hallazgo10-50212-etiquetado-cruzado
from: Arquitecto
to: Analista
type: ACTION
status: open
requires_response: true
response_owner: Analista
created_at: 2026-07-06
context_refs:
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/src/NOVA.Api/Program.cs"
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/docs/documentacion-tecnica/diccionario-datos.html"
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/docs/documentacion-tecnica/log-cambios.html"
  - Area_comun/artifacts/ANALISTA-HALLAZGO-AUTH-DD01-veredicto.md
one_line_summary: "Confirma como hallazgo formal #10 (QA, no seguridad): THROW 50212 mapea al titulo/businessRule del endpoint de disponibilidad aun cuando lo dispara modificacion de apropiacion (switch compartido BudgetProcedureProblemDetails.Map)."
requested_action: "Verifica con tu propia lectura (clon limpio del producto, commit edbc037be8ce8297fbf308f611eef8c84aeccbf0) que BudgetProcedureProblemDetails.Map (src/NOVA.Api/Program.cs, linea ~494-522) es un unico switch expression compartido por las 3 superficies (AppropriationModification linea 198, AvailabilityAdjustment linea 254, AvailabilityCertificateAnnulment linea 312), y que el codigo SQL 50212 aparece SOLO en la rama RN-A01 (linea 500: '50250 or 50251 or 50212 => Fiscal year is not open for availability adjustment'), mientras que la rama RN-01 de apropiacion (linea 513: '50230 or 50231 => Fiscal year is not open for appropriation modification') YA NO lo incluye. Consecuencia: si POST /api/budget/appropriation-modifications/ dispara THROW 50212 desde el trigger de vigencia (no vive dentro del proc Apply_Budget_Modification ni Apply_Availability_Adjustment, lo emite un trigger de guarda de vigencia compartido), el switch (evaluado top-down) devuelve el titulo/businessRule de RN-A01 (disponibilidad) en vez de RN-01 (apropiacion) -- el HTTP 409 y el sqlErrorNumber crudo quedan correctos, solo el texto legible y la etiqueta RN-xx quedan mal atribuidos para ese caso especifico. Verifica tambien que dotnet test tests/NOVA.ArchitectureTests (BUILD LIMPIO, sin --no-build) da 10/10 verde (aclaracion recibida del Operador: un fallo previo reportado era artefacto de --no-build con binarios previos al commit 02e67d8, no un defecto real -- confirma esto tambien con tu propia corrida). Clasificacion propuesta (verifica si estas de acuerdo, mismo patron que el hallazgo #5/auth): NO es bloqueante (HTTP status y sqlErrorNumber correctos; ya documentado con transparencia total en diccionario-datos.html y log-cambios.html; decision de fix diferida a criterio de equipo -- separar 50212 en rama neutral o duplicar el caso en RN-01 y RN-A01); ES un item QA formal (etiquetado de error cruzado entre superficies que comparten codigo de mapeo THROW->ProblemDetails), registralo como hallazgo #10 (continua la numeracion 1-9 ya usada) con tu propio veredicto/artefacto (mismo formato de Area_comun/artifacts/ANALISTA-HALLAZGO-AUTH-DD01-veredicto.md). No bloquea el cierre de ninguna tarea en curso (cross-cutting, ya documentado en el producto, no silenciado)."
question: "Confirmas la lectura (switch compartido, 50212 solo en RN-A01, RN-01 sin 50212) y el registro del hallazgo #10 como QA no-bloqueante? Si tu criterio de severidad/clasificacion difiere, dimelo con tu evidencia."
---

# ACTION - Hallazgo #10 (QA): etiquetado cruzado de THROW 50212 entre endpoints (Program.cs)

El Operador reporto (verificado por mi contra el codigo real): `BudgetProcedureProblemDetails.Map`
(`src/NOVA.Api/Program.cs`) es un switch UNICO compartido por Apply_Budget_Modification,
Apply_Availability_Adjustment y Annul_Availability_Certificate. El codigo `50212` solo aparece en la rama
`RN-A01` (disponibilidad); la rama `RN-01` (apropiacion) ya no lo lista. Si la modificacion de apropiacion
dispara `50212` (via trigger de guarda de vigencia, no del proc mismo), la API responde con el
titulo/`businessRule` del endpoint de disponibilidad -- HTTP 409 y `sqlErrorNumber` correctos, solo el
texto/etiqueta legible quedan mal atribuidos.

Ya esta documentado con transparencia total en `diccionario-datos.html`/`log-cambios.html` (no oculto, no
parcheado silenciosamente). Pido tu verificacion independiente (mismo patron que el hallazgo #5/auth) y
que lo registres como hallazgo formal #10 en el backlog de seguridad/QA del hub, clasificacion QA
no-bloqueante (a diferencia de #5 que si es seguridad/bloqueante fuera de sandbox).

Ademas: confirma que `dotnet test tests/NOVA.ArchitectureTests` con build limpio da 10/10 -- aclaracion
del Operador de que un fallo previo reportado fue artefacto de `--no-build` con binarios viejos (antes de
`02e67d8`), no un defecto real.
