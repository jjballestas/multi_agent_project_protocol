---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-afinado-postT4-bouncecap-gatescorer
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-t3-techo-por-fit-modelo.md
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-secuencia-techo-luego-lote100-envelope-nova.md
one_line_summary: "DESPUES de cerrar T4 (no interrumpas T4): dos chequeos de afinado que aplican la regla 'donde igualamos el prior art, confirma que lo aplicamos'. (1) Sensibilidad tope de bounces 2-vs-3 (la literatura converge en 3; medimos si nuestro 2 deja ahorro en la mesa). (2) Confirmar en logs que el gate de tests es el scorer de accept/reject y Codex NO re-juzga pass/fail (solo triaje). Demo NO citable."
---

# DIRECTIVA - Afinado post-T4: aplicar la regla a nuestro propio diseno

## Cuando
DESPUES de cerrar T4 en canonico. NO interrumpas T4. Metelo en el mismo lote de afinado, antes
o junto a la sintesis del manual NOVA.

## Motivo
Auditamos nuestro diseno contra los metodos probados del prior art (FrugalGPT, RouteLLM,
Self-Refine/Reflexion/AlphaCodium, NVIDIA-SLM). Regla: donde igualamos un metodo probado,
confirmamos que lo aplicamos; donde divergimos, o lo justificamos o lo adoptamos. Dos puntos
salieron a chequear.

## Chequeo 1 - Sensibilidad del tope de bounces (2 vs 3)
La convencion del prior art es tope 3 (max 5); nosotros fijamos 2 por conservar coste, SIN
evidencia. Riesgo: una tarea que pasaria en el bounce 3 la escalamos a Codex caro en el 2.
- Toma una celda que TOPO en T3 (p.ej. qwen en el formatter) y re-correla con tope 3.
- Si el bounce 3 la RECUPERA (pasa sin correccion del maker) -> estamos dejando ahorro en la
  mesa por divergir del parametro probado; recomienda subir el tope por defecto a 3.
- Si NO la recupera (o reintroduce defecto, como ya paso) -> nuestro tope 2 queda VALIDADO
  empiricamente; registralo.
- Barato: 1-2 execs. Reporta el veredicto.

## Chequeo 2 - Confirmar que el gate es el scorer (Codex no re-juzga pass/fail)
FrugalGPT: el scorer de accept/reject debe ser lo BARATO. Nuestro gate de tests (determinista,
gratis) YA es ese scorer.
- Verifica en los logs de las celdas ya corridas que el pass/fail lo decide el GATE, y que el
  frontier de Codex se gasta SOLO en el triaje desliz-vs-techo, NO en re-decidir si pasa.
- Si Codex esta re-evaluando el pass/fail que el gate ya decidio -> es coste frontier tirado;
  cuantificalo y corrige el protocolo de QC para que el gate corte primero.
- Si el gate ya corta primero -> confirmalo y documentalo en el manual como el scorer barato.

## Marco
Esto es la regla aplicada a nosotros mismos, no una via nueva. Demo PRIVADA, NO citable.
Instrumento Codex CLI. Fondo intocable N=500 / 2E35F26E / epoch 1.14.0. Reporta el afinado
junto al cierre de T4 / arranque de la sintesis.

-- Operador (via Asesor). 18-jul.
