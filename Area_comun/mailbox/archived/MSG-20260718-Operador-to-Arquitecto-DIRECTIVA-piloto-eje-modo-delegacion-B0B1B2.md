---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-piloto-eje-modo-delegacion-B0B1B2
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-piloto-benchmark-peones-privado.md
  - Area_comun/artifacts/PROBE-COSTE-tabla-AvsB.md
one_line_summary: "REFINA el piloto con un eje nuevo -- MODO DE DELEGACION -- porque el 2x de TASK-0006 pudo ser artefacto del modo mas caro (B0). Anade: B0 (spec fresca, lo medido), B1 (extractiva: Codex reenvia {patron + contrato I/O + criterio de aceptacion} de la intake SIN spec nueva), B1-literal (verbatim, control), B2 (triage + B1). Metrica nueva CLAVE: added-spec-tokens (spec NUEVA que Codex escribe; ~0 = intake ya peon-ready). Registra el coste SUNK Arquitecto->Codex. PRIMERO: re-run del T1 de TASK-0006 en B1 para ver si el 2x colapsa."
requested_action: "[DIRECTIVA] (1) Re-run INMEDIATO del T1 (misma sub-tarea de TASK-0006, 10 tests NEG PII) en modo B1-extractivo: compara tokens frontier vs B0 (169881) y vs arm A (84121). (2) Anade MODO DE DELEGACION como eje del piloto (B0/B1/B2 + B1-literal control) con la metrica added-spec-tokens y el coste sunk Arquitecto->Codex registrado. Ejecuta tras cerrar TASK-0006. Sigue siendo DEMO privada, NO citable."
question: "Confirmas las definiciones de B0/B1/B2 y la regla dura de B1 (extraer, no generar)? Puedes instrumentar added-spec-tokens de forma limpia?"
---

# DIRECTIVA - Piloto: eje MODO DE DELEGACION (B0/B1/B2) + metrica spec-anadida

## Por que (el 2x pudo ser artefacto de B0)
En TASK-0006 el brazo B midio B0: Codex escribio una spec-contrato NUEVA para el peon -> 2x. Pero
la regla anti-vibecoding hace que la tarea llegue a Codex YA CLARA desde el Arquitecto (coste SUNK,
pagado delegue o no). Si esa spec ya es peon-ready, Codex puede REENVIARLA sin re-escribirla, y la
ceremonia de abajo colapsa. Hay que medir los modos que reutilizan la spec sunk.

## Los modos (nuevo eje)
- **B0 -- spec fresca:** Codex escribe spec nueva para el peon (lo medido; 2x). Peor caso.
- **B1 -- extractiva:** Codex EXTRAE de la intake del Arquitecto {patron/ejemplo + contrato I/O
  (claves, tipos, valores) + criterio de aceptacion (el test que gatea)} y lo reenvia al peon.
  **REGLA DURA: reformatear/quitar el envoltorio de gobernanza SI; anadir especificacion NUEVA NO.**
  Si Codex tiene que escribir spec nueva, eso se registra como added-spec-tokens (y la celda ya no
  es B1 puro -> senal de que la intake no era peon-ready).
- **B1-literal (control):** Codex reenvia la intake VERBATIM (con ruido de gobernanza). Solo purity
  check: ver si el 7b maneja la intake cruda o el ruido lo confunde.
- **B2 -- triage + B1:** Codex evalua peso/fit; si es peon-ready reenvia extractivo (B1); solo
  aumenta la spec si NO lo es. Paga ceremonia solo cuando hace falta.

## Metricas nuevas
- **added-spec-tokens** (la clave): contenido de spec NUEVO que Codex escribe al delegar. ~0 =>
  la spec anti-vibecoding ya era peon-ready => delegar barato => confirma la tesis. Mucho => spec
  calibrada-para-Codex => B0 necesario.
- **coste SUNK Arquitecto->Codex:** registra (del ledger/logs, o declarado) los tokens que costo
  producir la intake clara -- para separar SUNK de MARGINAL en la contabilidad.

## Orden de ejecucion
1. **YA (alto valor, barato): re-run del T1 en B1-extractivo** (la misma sub-tarea de TASK-0006).
   Reporta tokens frontier B1 vs B0 (169881) vs arm A (84121). Si B1 colapsa hacia/por debajo de
   arm A, el 2x era artefacto de B0.
2. Folding de B0/B1/B2 en el piloto ya montado; ejecuta el grid completo tras cerrar TASK-0006.

## Guardrails (sin cambios)
Demo NO citable (anti-HARKing); PII fuera; fondo intocable (2E35F26E/1.14.0/N=500); instrumento
maker = Codex CLI; gate duro por celda; DECISION-0099 (spec al peon = artefacto).

-- Operador (via Asesor).
