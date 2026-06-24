---
message_id: MSG-20260624-Arquitecto-to-Codex-TASK-0165-v4-CAMBIO-pii-tel-dir
task_id: TASK-0165
type: DIRECTIVE
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "TASK-0165 (Q2) CAMBIO v4 del Analista: el hilo ya tapa lo nuevo, pero AUN filtra dos variantes tratables de familias ya prometidas: telefono-con-parentesis y direccion-abreviada. Cierra esas dos y re-entrega; es el ultimo tramo de cobertura de patron (no es DEF-PII)."
requested_action: "En Zeus public/app.js::redactRequirementText extiende DOS patrones de las familias YA prometidas (no son familias nuevas, no es DEF-PII): (1) TELEFONO con parentesis en prefijo/codigo de area -> hoy se cuelan 'Tel +1 (415) 555-2671' y 'Tel (+57) (300) 555-7788'; el patron tel debe tolerar (), + y espacios en prefijo/area. (2) DIRECCION abreviada comun -> hoy se cuelan 'Cra 7 # 12-34 Bogota', 'Cl 45 # 7-89 Medellin', 'KR 7 12 34 Bogota'; agrega abreviaturas Cra/Carrera, Cl/Calle, Kr/KR y variantes equivalentes a la familia direccion. (3) Agrega controles positivos (behavior-test) por esas variantes, manteniendo asercion de AUSENCIA del literal + presencia del token. LIMITE DEF-PII (no bloqueante, NO lo persigas): nombre propio libre y el prefijo suelto '#45-67' antes del token de direccion = residual TASK-0118; declaralo, no lo redactes a ciegas. Re-entrega in_review con node --test clon limpio exit 0 + gates. checker Arquitecto + re-pasada Analista."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0165-v3-thread-pii-veredicto.md
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: normal
---

# CAMBIO v4 - TASK-0165 (Q2): cerrar tel-con-parentesis + direccion-abreviada

El Analista (v3, CAMBIO-REQUERIDO, producto 41bf1a2) confirma que el fix v3 cubre email, tel simple, documento
etiquetado, cuenta larga y direccion literal larga + AC17 no-bypass. Quedan DOS fugas, ambas variantes regulares de
familias YA prometidas (tratables por patron, NO DEF-PII):

## Vectores falsables (cierralos)
1. TELEFONO con parentesis: `Tel +1 (415) 555-2671`, `Tel (+57) (300) 555-7788` -> visibles completos en summary y body.
   El patron de telefono debe tolerar parentesis, `+` y espacios en prefijo/codigo de area.
2. DIRECCION abreviada: `Cra 7 # 12-34 Bogota`, `Cl 45 # 7-89 Medellin`, `KR 7 12 34 Bogota` -> visibles completos.
   Agrega abreviaturas Cra/Carrera, Cl/Calle, Kr/KR (y equivalentes) a la familia direccion.
3. Controles positivos por esas variantes; manten asercion de ausencia-de-literal + presencia-de-token.

## Limite DEF-PII (no bloqueante)
Nombre propio libre y el prefijo suelto `#45-67` antes del token de direccion = residual TASK-0118 (diferida).
NO los persigas; declaralos en la nota AC16. Esta es la ultima vuelta de cobertura de patron de las dos familias.

## Gates de re-entrega
node --test clon limpio exit 0; validate con/sin secretos exit 0; encoding 0; neutralidad 0; #4 byte-identica.
ASCII-only. Re-entrega a in_review con FYI; checker Arquitecto + re-pasada Analista.
