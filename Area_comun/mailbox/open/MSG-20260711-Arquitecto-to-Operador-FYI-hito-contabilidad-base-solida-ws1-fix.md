---
message_id: MSG-20260711-Arquitecto-to-Operador-FYI-hito-contabilidad-base-solida-ws1-fix
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-11
context_refs:
  - Area_comun/artifacts/PREP-CONTABILIDAD-esqueleto-spec-patron.md
  - Area_comun/mailbox/open/MSG-20260707-Operador-to-Arquitecto-ACTION-prep-post-chains-contabilidad-etapa2.md
one_line_summary: "Registre el hito design-source de Contabilidad (base solida + WS1 + THROW reales + fix de integridad) como ARTEFACTO atestado (#4) + este FYI, NO como DECISION ni task de build. Frontera confirmada: design-source PREP, NO abre el build gobernado, NO toca baseline/core pineado (2E35F26E, 1.14.0). Pubkey de Julian RECIBIDA y persistida; la re-genesis A2 de Aegis espera tu GO (reactiva agentes)."
requested_action: "GO o HOLD para la re-genesis A2 del config de Aegis (registrar pubkey jheredia:v1 + alta en agent_registry + gate e2e de 2 clones); esa via reactiva agentes. Sin tu GO queda en hold; el BUILD sigue gated aparte por (base promovida al hub/instancia + Sprint 1 post-30-jul)."
question: "Ejecuto la re-genesis A2 del config de Aegis ahora (registrar pubkey jheredia:v1 + alta en agent_registry + gate e2e de 2 clones, que reactiva agentes), o la dejo en hold hasta que tengas base promovida + ventana Sprint 1?"
---

# FYI - Hito design-source Contabilidad registrado + pubkey de Julian recibida

Reporto. Autonomo. Estado ~00:25 local (UTC+2), 2026-07-11. Registrado en el commit gobernado de esta
sesion (hub). NO abri el build gobernado.

## Disposicion gobernada (mi decision -- "no la predefino")
Registre el hito como **ARTEFACTO atestado + este FYI**, NO como DECISION ni como task de build:
- **Artefacto:** actualice `PREP-CONTABILIDAD-esqueleto-spec-patron.md` con el HITO 2026-07-11 (evidencia +
  THROW ranges + fix de integridad) -> queda atestado en el hub (#4) via el commit gobernado. El esqueleto
  SPEC-CONT (s.1) queda marcado INSTANCIABLE por unidad, sin promover ninguna tarea.
- **Por que NO DECISION:** no cambia protocolo/frontera/dominio; es evidencia design-source, no una politica.
- **Por que NO task de build en el hub:** las tareas de build de Contabilidad viven en el ledger de la
  INSTANCIA (DECISION-0050); crearlas aqui rozaria abrir el build gated. `submit_intent` del hub solo expone
  task/decision/claim/mailbox -- no hay intent de "artefacto"; el registro #4 correcto para evidencia
  design-source es el commit atestado del artefacto.

## Que quedo registrado (evidencia, en `D:/Agentes/Ingenas`, fuera del hub)
- **WS1:** 57 formularios legacy -> casos de uso por slice, con THROW por proc
  (`dictionary/accounting_ws1_base_solida.html`, verificado presente).
- **Base solida desplegada** en DbsFinanciero + DbsFinanciero_SANDBOX + SNJDC (smokes con ROLLBACK, residuo 0):
  CGN/CHIP trimestral `schema/027` (THROW 54400-54457), cierre anual `schema/028` (THROW 54460-54487).
- **F-NOVA-01:** THROW reales re-verificados contra OBJECT_DEFINITION en las 3 BD.
- **Fix de integridad (verificado estaticamente por tu asistente):** bypass de periodo cerrado del cierre
  anual acotado a la escotilla `SESSION_CONTEXT(N'accounting_annual_close')` que SOLO activa
  `Accounting.Close_Annual_Accounting_Period`; las 3 guardas (52204/52233/52512) la aplican con
  `AND NOT (item='annual_close' AND COALESCE(TRY_CONVERT(int,SESSION_CONTEXT(...)),0)=1)`; captura manual
  restringida a los 3 tipos manuales (52252), sin regresion (solo `source_module='accounting'` y not
  system_generated). Objetos: `schema/015`, `schema/023`, `schema/028`.

## Frontera confirmada (design-source PREP, NO abre el build)
- NO abre el build gobernado: sigue gated por (Julian onboardeado + base promovida al hub/instancia +
  calendario Sprint 1 post-30-jul).
- NO toca el baseline congelado ni el core pineado: config `2E35F26E` byte-identico, epoch `1.14.0`, dataset
  N=500 y genesis sin tocar (verificado esta sesion).
- No rutee build gobernado ni active SESSION_CONTEXT desde la API.

## Follow-up (backlog, no bloqueante -- registrado en s.4 del PREP)
Endurecer que la captura manual FIJE `source_module_code='accounting'` para que el THROW 52252 no sea
esquivable a nivel BD (hoy `Post_Voucher_Draft` lo lee del draft). El bypass de periodo cerrado NO depende
de esto -- lo cubre la escotilla `SESSION_CONTEXT` de forma independiente. Se instancia como hardening
cuando abra el build.

## Pubkey de Julian RECIBIDA (input (a)) -- re-genesis A2 espera tu GO
Recibi el pubkey ed25519 de `jheredia:v1` y lo persisti en su ruta canonica de onboarding
(`D:/Agentes/Zeus/NOVA/Aegis/git-key/jheredia-ed25519-public.pem`, staged, sin commitear). La re-genesis A2
del config de Aegis (registrar su pubkey) + alta en agent_registry + gate e2e de 2 clones NO la ejecuto
unilateralmente: reactiva agentes y es una operacion cripto gobernada de Aegis (nunca el hub). Es PREP valido
onboardearlo ahora (no abre el build; falta base promovida + Sprint 1), pero espero tu GO. Ver requested_action.

Fondo intocable intacto. Gates verdes. Watchdogs armados. A tus ordenes.
