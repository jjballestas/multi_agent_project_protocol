---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-onboarding-remoto-checklist-huecos
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/mailbox/open/MSG-20260706-Operador-to-Arquitecto-ACTION-corte-aegis-cola-reqs-contabilidad.md
  - D:/Agentes/Zeus/NOVA/Aegis/scripts/distributed_git_harness.py
  - D:/Agentes/Zeus/NOVA/Aegis/scripts/distributed_e2e_task_cycle.py
  - D:/Agentes/Zeus/NOVA/Aegis/protocol.config.json
one_line_summary: "Addendum a la directiva corte-aegis: onboarding de un participante REMOTO (empleado en Colombia, clon propio en su maquina) sobre la instancia Aegis. Checklist de 6 puntos verificado: 4 huecos con dueno asignado. El runbook del harness distribuido (TASK-0232/0233) se amplia con alta de participante, capabilities y requisito de pre-registro en el sello Etapa 2. Encargo DBA va al lote-pendiente-operador."
requested_action: "Integrar a la cola de la directiva vigente (mismo regimen no-idle): (1) runbook de onboarding remoto multi-clon que cierre los huecos 2/3/4 de abajo; (2) anadir el requisito del hueco 6 al item de diseno del sello Etapa 2; (3) registrar el hueco 5 (acceso BD remoto) como encargo DBA en el lote-pendiente-operador con su lead time marcado como camino critico. Confirmar integracion en la proxima senal de progreso, sin frenar la cola."
question: "Ves algun requisito adicional del modo enforce+authoritative de Aegis que el runbook deba cubrir y que no este listado abajo?"
---

# ACTION (addendum) - Onboarding remoto: huecos del checklist con dueno

Contexto: el Operador incorporara un empleado (Colombia, huso UTC-5) que trabajara Contabilidad
desde SU maquina con SU clon de la instancia Aegis. Arquitectura decidida: UN solo ledger (la
instancia Aegis existente), N clones coordinados via el remoto GitHub -- NUNCA una segunda instancia
independiente. El harness distribuido ya probado (TASK-0232/0233: ventana segura + ciclo e2e de
tarea desde clon limpio, solo-Git) es la base; esto lo convierte en procedimiento operativo.

Checklist de 6 puntos verificado hoy contra el estado real de Aegis:

## Hueco 1 - Remoto privado: CASI LISTO (dueno: Operador, tramite corto)
El origin de Aegis ya apunta a `github.com:jjballestas/Zeus-Aegis.git`. Pendiente del Operador:
confirmar visibilidad privada del repo + invitar al empleado. El repo de producto Nova-Accounting se
crea cuando el analisis de Contabilidad lo requiera (ya en tu cola).

## Hueco 2 - Alta del participante: FALTA (dueno: Arquitecto, runbook)
El `agent_registry` de Aegis solo tiene los 3 agentes actuales. El runbook debe cubrir: id del
participante nuevo, entrada en `agent_registry`, creacion de `personal/<id>/` (DECISION-0016), y
generacion de llaves Ed25519/HMAC EN SU MAQUINA via override gitignored -- patron exacto del
aprovisionamiento del tercer firmante en el hub: sin re-genesis, chain.genesis intacto, solo
material publico registrado. Su llave privada jamas viaja al repo.

## Hueco 3 - Capabilities maker/checker: FALTA (dueno: Arquitecto, runbook + propuesta)
Definir las capabilities del participante remoto y el reparto entre maquinas. Propuesta del
Operador como punto de partida (traela refinada en el runbook): sus agentes como implementer en
unidades de Contabilidad, el checker en la maquina del Operador (o cruzado por unidad), de modo que
maker != checker quede ademas separado fisicamente.

## Hueco 4 - Disciplina distribuida: PARCIAL (dueno: Arquitecto, runbook)
Los scripts del harness existen; falta el procedimiento. El runbook debe fijar: fetch + ventana
segura antes de toda escritura de ledger; push inmediato tras cada transicion (un flip sin pushear
es invisible desde el otro clon = FM-3.1); commits con pathspec y trailers. REQUISITO EXTRA
detectado: Aegis corre `event_state` con enforce+authoritative EN TRUE (escritor-unico duro) -- el
clon remoto DEBE rutear toda transicion por `submit_intent` desde el dia uno (una edicion manual
suya hard-falla el gate B.3), asi que el onboarding incluye runtime Python operativo + smoke de
`submit_intent` en su maquina, no solo git. El e2e de humo final corre ENTRE los dos clones reales
(maquina Operador + maquina empleado) antes de la primera tarea real.

## Hueco 5 - Acceso a BD sandbox: FALTA POR COMPLETO (dueno: DBA via lote-pendiente-operador)
No hay nada preparado: ni VPN, ni copia sandbox restaurada, ni grants de verificador remoto, ni
politica de sanitizacion. Las pruebas de paridad de Contabilidad lo necesitaran. Es el item de MAYOR
lead time del checklist (infraestructura, fuera del protocolo): registralo YA en el
lote-pendiente-operador como encargo DBA con las opciones (VPN al sandbox actual vs copia restaurada
local con grants minimos patron `budget_sandbox_verifier`) y la nota de confidencialidad: datos de
entidades publicas colombianas -> copia sanitizada si va a maquina ajena.

## Hueco 6 - Pre-registro en el sello Etapa 2: PENDIENTE POR DISENO (dueno: Arquitecto, sello)
Anade como requisito explicito al item de diseno del sello Etapa 2 (ya en tu cola): el sello nombra
a los participantes, sus maquinas/clones y roles ANTES de sellar. Un segundo humano es variable del
estudio; los exception events (`assist`/`manual_intervention`) y el journal registran quien hizo
que. Decidirlo antes de sellar es gratis; a mitad de ventana seria enmienda.

## Regimen
Mismo regimen de la directiva vigente: integra estos items a la cola sin frenarla ni pedir
confirmacion item a item; lo que requiera firma del Operador va al lote-pendiente-operador.

-- Operador
