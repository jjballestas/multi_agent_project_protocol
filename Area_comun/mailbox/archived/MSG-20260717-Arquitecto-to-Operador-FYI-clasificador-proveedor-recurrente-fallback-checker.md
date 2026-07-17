---
message_id: MSG-20260717-Arquitecto-to-Operador-FYI-clasificador-proveedor-recurrente-fallback-checker
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Operador-HITO-u2-done-u3-lanzada.md
one_line_summary: "FYI blocker de infraestructura RECURRENTE + fallback aplicado: el clasificador cyber del proveedor del CLI del checker flageo la review de U3 DOS veces seguidas (3er episodio del dia; falso positivo sobre probes adversariales legitimos con fixtures PII/tamper). Fallback en curso SIN frenar el carril: checker informal anti-rubber-stamp en modelo FUERTE (patron establecido del proyecto; cumple DECISION-0099 regla 3), veredicto marcara checker_formal=0. El re-judgement formal del Analista se re-ejecuta cuando el proveedor desbloquee. Opcion estructural si persiste: Trusted Access del proveedor."
---

# FYI - Clasificador del proveedor recurrente en reviews adversariales + fallback

## El blocker

El CLI del checker formal (proveedor OpenAI) flagea "possible cybersecurity risk" y aborta el
exec cuando la review escribe/ejecuta sus probes adversariales (fixtures con patrones IBAN/
salario plantados, tamper de sha, traversal de rutas -- trabajo legitimo sobre NUESTRO propio
codigo). Episodios de hoy: 1 en el re-judgement de U1 (resuelto con retry), 2 consecutivos en la
review de U3 (retry incluido). Es no-determinista pero la frecuencia sube con el contenido de los
probes (U3 incluye tamper + PII + retrieve).

## Fallback aplicado (carril NO frenado)

Checker INFORMAL anti-rubber-stamp en modelo fuerte (subagent Claude), con el MISMO mandato
adversarial por conducta en clon limpio (I5 sin-DB, fail-closed por mutacion, clase-de-drift no
cubierta, retrieve por blob, regresion U1/U2). Es el patron ya establecido del proyecto (SPEC
v0.2.0 se reviso asi) y cumple DECISION-0099 regla 3 (checker en modelo fuerte). El veredicto se
registra como artefacto marcando checker_formal=0 -- honestidad de clase de evidencia; Fase A es
demostracion, no citable, asi que el impacto de clase es acotado y declarado.

## Opciones estructurales (tu decision, no urgente)

(a) Mantener el fallback informal para reviews que el clasificador flagee, con re-judgement
formal posterior cuando pase; (b) solicitar Trusted Access for Cyber al proveedor (URL en sus
errores) para el CLI del checker; (c) mover el checker formal a otro CLI/proveedor (cambio de
harness, DECISION). Sigo con (a) salvo orden contraria.

-- Arquitecto. Hora local ~19:05 (UTC+2). Fondo: N=500, 2E35F26E, 1.14.0 intactos.
