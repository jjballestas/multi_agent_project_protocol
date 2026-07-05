---
message_id: MSG-20260705-Arquitecto-to-Operador-RESPUESTA-integridad-mock-P2.1-guard
from: Arquitecto
to: Operador
type: HANDOFF
status: archived
requires_response: false
created_at: 2026-07-05
context_refs:
  - Area_comun/mailbox/answered/MSG-20260704-Arquitecto-to-Codex-ACTION-TASK-0250-remediacion-1.md
  - Area_comun/mailbox/archived/MSG-20260704-Codex-to-Arquitecto-TASK-0250-done-flip-done.md
one_line_summary: "(a) TASK-0250 evidencia_real_adjunta=true es CORRECTA -- el mock se cazo y corrigio ANTES del cierre (mi nota 'mismo patron' se referia al TIPO de defecto recurrente, no a que P2.1 quedara sin corregir). (b) Guard de procedencia adoptado para futuros checkers. (c) paridad=NA en P4.1 explicada. (d) recomendacion sobre cadencia de atestacion."
requested_action: ""
question: ""
---

# RESPUESTA - Integridad verificada: TASK-0250 esta limpia, guard adoptado

## (a) TASK-0250 (P2.1): evidencia_real_adjunta=true es CORRECTA, no hay dato falso en el journal
Revise los artefactos historicos (`MSG-...-remediacion-1.md`, `HANDOFF-...-done-flip-done.md`). Secuencia
real de P2.1: (1) primera entrega -- el checker adversarial (sesion separada) CAZO exactamente el mismo tipo
de defecto que P4.1: `InMemoryBudgetParametersGateway` (~10 filas hardcodeadas) registrado en
`DependencyInjection.cs` como implementacion de PRODUCCION (no un test double), mas un front que nunca
llamaba a la API. (2) Rutee remediacion-1 exigiendo un gateway SQL real que consultara las vistas `vw_*`
de la SPEC. (3) Codex reconstruyo con gateway SQL real + UI con fetch real. (4) Un SEGUNDO checker
adversarial (sesion separada, contexto limpio, no confio en la prosa del handoff) VERIFICO la remediacion
leyendo el codigo -> confirmo gateway SQL real -> GO. (5) Cierre: el UNICO residual declarado fue "paridad
de conteo en vivo contra DbsFinanciero pendiente de credenciales" (igual categoria que el residual de
F-NOVA-01 en TASK-0252/P4.1) -- NO un mock sobreviviendo al cierre.

**Mi nota de CLOSE ("mismo patron que TASK-0250") se referia al TIPO de defecto que RECURRE entre unidades
(mock in-memory disfrazado de implementacion real, cazado por el checker adversarial), NO a que la fila de
P2.1 tenga datos falsos.** Redaccion imprecisa de mi parte, la aclaro aqui. `evidencia_real_adjunta=true`
en TASK-0250 queda CONFIRMADA correcta -- no requiere correccion.

## (b) Guard sistemico de procedencia -- ADOPTADO desde ahora
De acuerdo: el patron recurre (2 veces ya cazado por checkers, nunca sobrevivio a un GO final, pero es un
riesgo real que vale la pena blindar). Desde este momento, TODO prompt de checker adversarial que yo lance
para F-NOVA-01/paridad debe incluir un punto EXPLICITO de procedencia: "confirma que la evidencia proviene
del sandbox REAL (DB_NAME=DbsFinanciero_SANDBOX + login nova_budget_verifier + OBJECT_DEFINITION del proc
DESPLEGADO + delta de saldo real), y no de un doble in-memory/mock -- busca especificamente si el test que
dice ejercitar los casos usa una implementacion Sql* real o un Recording*/InMemory* con resultados fijos
por caso". Ya lo aplique de facto en las ultimas 2 rondas de P4.1 (por eso se cazo); lo dejo como
checklist fijo para toda unidad futura (P4.2/P4.3/PAR-1 en adelante).

## (c) paridad_exec_vs_endpoint=NA en P4.1 -- explicacion honesta
F-NOVA-01 de P4.1 verifico: (i) el set real de THROW contra `OBJECT_DEFINITION` del proc desplegado, y
(ii) los 8 casos GWT ejecutando el proc DIRECTO via SQL real. Eso es distinto del contraste formal
"exec-vs-endpoint" (llamar el MISMO caso por la via directa Y por el endpoint HTTP y comparar resultado
byte-a-byte) que es el harness especifico de TASK-0252. Para P4.1 ese contraste puntual NO se corrio --
no es una degradacion declarada de antemano, es un alcance que F-NOVA-01 (tal como esta escrito en la SPEC)
no exigia explicitamente. Lo declaro como residual honesto (no lo maquillo): si quieres que sea criterio
duro para P4.2/P4.3, lo agrego a sus SPEC antes de GO-earlas.

## (d) Cadencia de atestacion -- mi recomendacion, tu decides
GOAL-P1 se atesto por-unidad porque era la unica unidad del piloto. Con el volumen actual (P2.1/P2.2/P4.1
ya cerradas, PAR-1 arrancando), recomiendo atestar por-CHECKPOINT (Sello Etapa 2 ~29-jul o la reconciliacion
26-29-jul), no por-unidad: el journal vive en `corpus/` (gitignored por diseno, no en el repo git) y el
sha256 se ancla al hub via `submit_intent` decision -- atestar cada cierre individual multiplicaria
intents de decision sin beneficio de integridad adicional (el CSV es append-only y ya lleva su propio
hash interno via `sha256`/`verificar` del script). Es mi recomendacion, no una decision unilateral --
confirmame si prefieres por-unidad y lo hago asi desde ya.

## Estado
P4.1 = **done** (Codex confirmo el done-flip). Arranco PAR-1 ahora (SPEC-NOVA-P4-002/003 citando los
THROW reales del preflight del DBA).
