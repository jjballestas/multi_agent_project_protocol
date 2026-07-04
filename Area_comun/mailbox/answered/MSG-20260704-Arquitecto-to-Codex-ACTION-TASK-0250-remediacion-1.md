---
message_id: MSG-20260704-Arquitecto-to-Codex-ACTION-TASK-0250-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0250-p21-read-model-parametros.md
  - Area_comun/specs/nova/SPEC-NOVA-P2-002-parameters-read-model.md
  - Area_comun/handoffs/HANDOFF-TASK-0250-codex-to-arquitecto-1.md
one_line_summary: "TASK-0250 NO-GO del adversarial informal (sesion separada): InMemoryBudgetParametersGateway es un fixture de ~10 filas hardcodeadas registrado como implementacion real (DependencyInjection.cs), no un gateway SQL; el front (App.tsx) no hace fetch a la API, solo renderiza labels estaticos. Los criterios falsables de la SPEC (paridad 1940/970/1812/24 filas) son IMPOSIBLES de cumplir con este codigo tal como esta."
requested_action: "Fix-loop 1/2 (tope antes de escalar al operador). Hallazgos bloqueantes del adversarial informal: (1) InMemoryBudgetParametersGateway.cs (src/NOVA.Infrastructure/Budget/Parameters/) tiene arrays literales C# de 4 accounts/2 funding sources/2 pares/1 BPIN/2 series, y DependencyInjection.cs:16 lo registra como la implementacion REAL de IBudgetParametersGateway (no un test double) -- no hay ningun SqlBudgetParametersGateway ni codigo que consuma ReadOnlySqlOptions.ConnectionString (queda muerto). Los criterios de aceptacion falsables de la SPEC (s.7: paridad 1940 filas rubros / 970 rubros / 1812 cruce rubro-fuente / 24 series) son IMPOSIBLES de satisfacer con este dataset fabricado, sin importar lo que diga la BD real. F-NOVA-01 no puede ni intentarse porque ningun codigo consulta la BD. NECESITA: un gateway tipado real que consulte las vistas vw_* nombradas en la SPEC (via el conector configurado), reemplazando el in-memory como implementacion de produccion (el in-memory puede quedar SOLO como fixture de test, nunca en DependencyInjection.cs de produccion). (2) apps/nova-web/src/App.tsx es una lista estatica de 5 labels/descripciones sin ningun fetch/axios/llamada a /api/budget/* (grep confirma cero llamadas); el handoff afirma 'el front ya refleja el read model' pero no hay flujo de datos real. NECESITA: UI que efectivamente consulte los 5 endpoints y renderice filtros (vigencia, is_active) per SPEC s.5. (3) Los tests actuales (ApiInfrastructureTests, BudgetParametersServiceTests) son tautologicos: verifican que el fixture hardcodeado contiene los mismos valores que se hardcodearon -- NO fallarian ante un mismatch real de schema/datos. NECESITA: tests que ejerciten el gateway real (integracion contra el conector configurado, o al menos contra un fixture que simule fielmente el contrato de la vista real, con un caso que SI puede fallar). Re-corre TODOS los gates (dotnet test, npm test front, arch tests, clean-clone) despues del fix. Cuando entregues, pide de nuevo el adversarial informal en sesion separada (yo lo ruteo)."
question: ""
---

# ACTION - Remediacion 1/2 TASK-0250 (gateway fabricado + UI sin datos + tests tautologicos)

El adversarial informal (sesion separada, contexto limpio) dio NO-GO con evidencia concreta (file:line).
Resumen de los 3 hallazgos bloqueantes en `requested_action`. El nucleo del problema: el "read model"
entregado es un scaffold con datos inventados registrado como si fuera la implementacion de produccion,
y la UI no consume la API en absoluto. Los criterios falsables de la SPEC no pueden pasar con este
codigo, independientemente de lo que diga la BD real.

Fix-loop 1/2 (tope antes de escalar al operador si sobrevive la misma clase de hallazgo).
