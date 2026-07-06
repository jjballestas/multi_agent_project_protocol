---
message_id: MSG-20260706-Operador-to-Arquitecto-RESPUESTA-pendientes-vivos-brc4-orden-1001-1002
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/mailbox/open/MSG-20260706-Operador-to-Arquitecto-ACTION-brc4-opcion-b-dba-encargo.md
  - personal/asesor/DRAFT-ENCARGO-DBA-BR-C4-hardening.md
  - Area_comun/mailbox/open/MSG-20260706-Operador-to-Arquitecto-ACTION-corte-aegis-cola-reqs-contabilidad.md
one_line_summary: "Respuesta a tus pendientes vivos: (1) BR-C4 YA resuelto = opcion (b) NO (a), tu reporte precede mi mensaje; (2) gate 2-clones confirmado antes de Contabilidad; (3) orden de promocion 1001->1002 fijado (per DIRECTIVA e749c0a); (4) veredictos Analista = su cola, ack."
requested_action: "Actualiza tus pendientes: (1) BR-C4 = opcion (b), no (a) -- consume MSG-...-brc4-opcion-b-dba-encargo (commit 09ec410): trackea deadline 29-jul + auto-fallback n=7; el encargo del DBA ya esta redactado. (2) Corre el gate e2e-humo-2-clones ANTES de la primera tarea real de Contabilidad (firmantes ya provisionados). (3) Promueve las primeras tareas en el orden de abajo. (4) Veredictos #10/#11-13 siguen en la cola del Analista, sin accion tuya."
question: "Confirmas el orden de promocion 1001->1002 y el resto? Si tu lectura de capacidad Codex sugiere otro interleaving pre-30-jul, proponlo (respetando prioridad dura Sprint 1 desde 30-jul)."
---

# RESPUESTA - pendientes vivos

## 1. BR-C4 = opcion (b), NO (a) -- tu reporte quedo desactualizado
Tu reporte de pendientes precede a mi mensaje `MSG-...-brc4-opcion-b-dba-encargo` (commit 09ec410). El
Operador TIENE DBA y eligio la **opcion (b)**: sembrar BR-C4 en sandbox <=29-jul para preservar Q4 **n=10**,
con **auto-fallback a n=7** si no llega. El encargo del DBA ya esta redactado por el Asesor
(`personal/asesor/DRAFT-ENCARGO-DBA-BR-C4-hardening.md`; el Operador se lo entrega a su DBA). Tu parte:
trackea el deadline 29-jul; al entregar verificado registra la enmienda fechada + confirma n=10; si pasa el
29-jul sin entrega, ejecuta la caida sellada -> n=7. Actualiza tu pendiente de "recomendacion opcion a".

## 2. Gate de 2 clones del runbook -- confirmado, buen sequencing
Si: corre el e2e-humo entre 2 clones ANTES de la primera tarea real de Contabilidad. Los firmantes ya estan
provisionados (el Operador corrio `provision_local_signers.py`; secrets/ + override presentes), asi que el
gate ya es ejecutable. Correcto encadenarlo antes de abrir Contabilidad.

## 3. Orden de promocion 1001 / 1002 -- FIJADO (per DIRECTIVA e749c0a seccion 2)
El orden ya esta sellado en la DIRECTIVA original: anti-vibecoding -> intake -> memoria-hibrida. Como
DECISION-1001 fusiona anti-vibecoding+intake y DECISION-1002 es memoria-hibrida:
- **Primero DECISION-1001**, empezando por su tarea 1 (SPEC de la capa de interrogacion; owner Arquitecto,
  review Analista).
- **Luego DECISION-1002**, empezando por F0 (discovery/inventario; owner Arquitecto).
- Interleaving pre-30-jul a tu criterio de capacidad de Codex; **desde el 30-jul manda la prioridad dura del
  Sprint 1** (SLA del sello) sobre ambas iniciativas y sobre Contabilidad.

## 4. Veredictos del Analista sobre #10 / #11-13
Ack -- son su cola, monitor armado, sin accion tuya. El Asesor los vigila y coordina cuando lleguen.

## Higiene
Los 4 vivos de open/ estan revisados por el Operador; esta respuesta + la de BR-C4 consumen las que aplican.
Archiva las consumidas en tu proximo checkpoint de higiene.

-- Operador
