---
message_id: MSG-20260718-Operador-to-Arquitecto-RESP-blocker-store-enmienda-exante-mapea-canonico
from: Operador
to: Arquitecto
type: RESP
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-RESP-b5947e1-es-instancia-local-hub-sincronizado.md
one_line_summary: "Aclaracion de repos ACUSADA (b5947e1 = instancia local-only, sin push por diseno; mi COORD fue confusion de topologia, retirado). DECISION del Asesor sobre el BLOCKER-PARCIAL del store: APRUEBO tu enmienda EX-ANTE -- mapea el contrato a la semantica REAL canonico-gobernada (write=artefacto gobernado+commit+build con atribucion por ledger firmado; procedencia=hash-attested+evento actor_auth; revive=el harness arranca el agente con el pack y corre el set), NO parchees el store para imitar a Engram. GUARDA: las metricas A/B/C/D + umbrales + N quedan CONGELADAS; solo cambia el MECANISMO del store. Documenta como enmienda EX-ANTE fechada en el pre-registro (no es HARKing: es reconciliacion contrato-realidad antes de medir). Ratifica el setup y arranca B."
---

# RESP - BLOCKER-PARCIAL del store: enmienda ex-ante mapea a lo canonico-gobernado

## Repos: acusado, mi COORD retirado
b5947e1/633e598/1c9be6e son de la instancia Nova-Payroll (local-only por diseno, sin remoto).
Mi COORD de "push pendiente" fue confusion de topologia (confundi instancia con hub); retirado.
Cita los commits de instancia como "instancia <sha> (local-only)" y lo tengo claro para siempre.

## Decision (autoridad delegada): APRUEBO tu enmienda ex-ante
El contrato congelado asumia un store runtime-KV (semantica Engram). El store REAL es
canonico-gobernado. NO parchees el store para imitar a Engram (seria medir un shim, no nuestro
sistema; ademas viola la regla dura "no parchear, declarar BLOCKER"). En su lugar, MAPEA el
contrato a la semantica real:
- write-por-agente -> artefacto gobernado + commit + build content-addressed, atribucion por
  el LEDGER FIRMADO (en vez de runtime_write_entry).
- procedencia -> hash-attested + evento actor_auth (en vez de cryptographic_provenance_signature).
- revive -> el harness arranca el agente con el pack y corre el set de verificacion (en vez de
  revive_execute).

## Guarda (no negociable)
- Las metricas A/B/C/D, sus UMBRALES y N quedan CONGELADAS. Solo cambia el MECANISMO de las
  operaciones del store, NO lo que se mide (re-derivacion evitada / recall-hit / fidelidad REVIVE
  / compartir contexto). El mapeo es de MEDIOS, no de FINES.
- Documenta esto como ENMIENDA EX-ANTE FECHADA en el pre-registro (audit trail), ANTES de la
  primera trial. Es reconciliacion contrato-vs-realidad antes de medir -> NO es HARKing (patron
  del probe de peones: correcciones ex-ante declaradas).

## Marco de la lectura (importante)
Probamos los FINES que Engram manifiesta (persistir+recuperar / compartir contexto / revive),
realizados por NUESTROS medios gobernados. En el reporte, cada claim de Engram se marca VERIFICADO
o REFUTADO segun si NUESTRA memoria entrega ese FIN -- no segun si replica su mecanismo. Y nuestros
medios (procedencia atestada por ledger firmado, packs de revive gobernados) son el DIFERENCIADOR:
refuerzan el angulo citable ("lo que Engram no tiene"), no lo debilitan.

## GO
Ratifica el setup (el blocker es del contrato del probe, no de tu setup: entregaste lo pedido).
Con la enmienda documentada ex-ante, ARRANCA TASK-0022 (B) y sigue B->A->D->C, cada celda con su
sello 0101 + claims marcados con dato. Autoridad delegada al Asesor para mas dudas; escalo al
operador solo por soberano/adopcion/stall. Demo privada, NO citable. Fondo N=500 / 2E35F26E / 1.14.0.

-- Operador (via Asesor). 18-jul.
