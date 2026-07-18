---
message_id: MSG-20260718-Operador-to-Arquitecto-CONSULTA-conteo-sanitizador-directo-frontier
from: Operador
to: Arquitecto
type: CONSULTA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-CIERRE-4tobrazo-sintesis-serie.md
one_line_summary: "Consulta de dato (para cerrar con numero, no razonamiento): cuantas operaciones del sanitizador dispararon sobre la salida FRONTIER del brazo directo (TASK-0019 del 4to brazo)? Si 0 -> confirma que el sanitizador es no-op puro sobre salida frontier (limpia de fabrica via Codex CLI). Si >0 -> cuantas y de que tipo (fences/prosa/renames). Barato: sale de los logs del exec del directo ya corrido."
requested_action: "Reporta el conteo exacto de operaciones del sanitizador que dispararon sobre la salida del brazo DIRECTO (frontier/Codex) en TASK-0019: total + desglose por tipo (fences, prosa, renames, otros). Es un dato de los logs del exec ya corrido, no requiere re-correr nada."
question: "Cuantos disparos del sanitizador hubo sobre la salida frontier del directo (TASK-0019), total y por tipo? (0 = no-op puro sobre frontier; >0 = cuantos y de que clase)."
---

# CONSULTA - Conteo del sanitizador sobre la salida frontier del directo

## Motivo
Cerramos el item de si el sanitizador mecanico aporta cuando el maker es solo frontier. El
razonamiento dice: el frontier via Codex CLI escribe archivos directos (sin fences/prosa) ->
el sanitizador rara vez o nunca dispara -> aporte economico ~0 (aunque gratis e idempotente).
El operador quiere cerrar con DATO, no con razonamiento.

## Lo que pido
Del exec del brazo DIRECTO ya corrido (TASK-0019, 50 funciones, gate 250/250 a la primera):
el conteo EXACTO de operaciones del sanitizador que dispararon sobre la salida de Codex.
- Total de operaciones.
- Desglose por tipo (fences quitados, prosa quitada, renames mecanicos, otros).
- Lectura: 0 confirma no-op puro sobre frontier; >0 dice exactamente cuanto trabajo hizo.

Sale de los logs del exec ya corrido; no re-corras nada. Demo privada, NO citable. Fondo
intocable N=500 / 2E35F26E / 1.14.0.

-- Operador (via Asesor). 18-jul.
