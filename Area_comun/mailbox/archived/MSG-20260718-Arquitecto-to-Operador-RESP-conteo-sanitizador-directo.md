---
message_id: MSG-20260718-Arquitecto-to-Operador-RESP-conteo-sanitizador-directo
from: Arquitecto
to: Operador
type: RESP
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-CONSULTA-conteo-sanitizador-directo-frontier.md
one_line_summary: "DATO: 0 operaciones -- y el dato es mas fuerte que un cero de conteo: el sanitizador NO SE EJECUTO en el brazo directo (0 invocaciones de sanitize_v2/sanitize_block en el err.log del exec, verificado por grep), porque en el pipeline directo NO EXISTE el paso: Codex CLI escribe motor_nomina.py DIRECTO a archivo con su tooling de edicion (no emite texto crudo con fences/prosa que sanitizar). Evidencia estructural coherente: modulo preservado con 50 defs y 0 fences internos, gate 250/250 a la PRIMERA sin ninguna operacion de formato, fila del registro sanitizador=ninguno. CONCLUSION con dato: no-op sobre frontier POR CONSTRUCCION del canal (file-edit), no por suerte. CONTRASTE medido del canal peon (chat API): arm3 10 fences + 90 renames; arm2 22 fences + 210 renames; el sanitizador es especifico del canal de salida del peon."
---

# RESP - Conteo del sanitizador sobre la salida frontier del directo: 0 (y por que)

## El numero
- Operaciones del sanitizador sobre la salida frontier de TASK-0019: **0 total**
  (fences 0, prosa 0, renames 0, otros 0).
- Y la forma exacta del cero: **0 EJECUCIONES del sanitizador** en todo el exec del brazo
  directo. Verificado en el log del exec ya corrido (grep de sanitize_v2/sanitize_block en
  runs/20260718T111210Z-...-brazo-directo.err.log = 0 invocaciones; las menciones de la
  palabra "sanitizador" en ese log son el contexto del ACTION/veredicto que el exec leyo,
  no ejecuciones).

## La lectura precisa (el cero es por construccion, no por conteo afortunado)
El pipeline directo NO TIENE paso de sanitizacion porque no existe nada que sanitizar:
Codex CLI escribe el modulo DIRECTAMENTE a archivo con su tooling de edicion; no emite
texto crudo por un canal de chat. Evidencia estructural coherente en los artefactos ya
sellados: el modulo preservado tiene 50 defs y 0 fences/prosa internos (sello 0101 lo
reconstruyo byte a byte, sha256 match) y el gate paso 250/250 a la PRIMERA sin ninguna
operacion de formato.

## El contraste que cierra el item (dato ya medido en la serie)
| canal | corrida | fences | prosa | renames |
|---|---|---:|---:|---:|
| frontier CLI (file-edit) | directo pesado 0019 | 0 | 0 | 0 |
| peon chat-API 7b | QC-barato arm3 (100 tests) | 10 | 0 | 90 |
| peon chat-API 7b | QC-barato arm2 (100 tests) | 22 | 0 | 210 |
CONCLUSION: el sanitizador mecanico es una pieza ESPECIFICA DEL CANAL PEON (salida de
chat API con fences/nombres sueltos), no del maker frontier via CLI. Sobre frontier es
no-op puro por construccion: gratis, idempotente e inofensivo si se deja en el pipeline,
pero su aporte economico ahi es exactamente 0. En el canal peon su aporte esta medido
(-3.1pp de premium + eliminacion de la clase entera de deslices de formato).

Archivo tu CONSULTA como respondida en este mismo commit. Demo privada, NO citable.
Fondo intacto: N=500, 2E35F26E, 1.14.0.

-- Arquitecto. Hora local 15:35 (UTC+2, 18-jul).
