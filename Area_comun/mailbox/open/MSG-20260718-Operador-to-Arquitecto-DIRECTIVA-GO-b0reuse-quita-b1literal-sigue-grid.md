---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-b0reuse-quita-b1literal-sigue-grid
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-b1-rerun-no-colapsa-sube.md
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-piloto-eje-modo-delegacion-B0B1B2.md
one_line_summary: "GO a tu pivote del grid tras el re-run T1-B1: incorpora la celda B0-reuse, quita B1-literal, manten B2, sigue con la escalera. B0-reuse es AHORA la celda clave (prueba la amortizacion por repeticion de familia). Demo NO citable."
---

# DIRECTIVA - GO al pivote del grid (post re-run T1-B1)

## Contexto (acepto tu lectura)
El re-run T1-B1 REFUTO la hipotesis "el 2x era artefacto de B0": B1 no colapso, subio
(279172 vs B0 169881 vs A 84121) con added-spec-tokens=0, y el peon 7b fallo 0/10 sin
spec calibrada. Conclusion aceptada: la spec fresca de B0 NO es ceremonia desperdiciada,
es la CONDICION de rendimiento del peon. El hallazgo cualitativo (0/10 sin spec) es robusto
e independiente del numero inflado por el blocker de capabilities. El gate del runtime actuo
bien (cero mutacion parcial); tu error de registro (type analysis owner implementer sin flip)
queda anotado, no bloquea nada.

## GO (las 4, tal cual propusiste)
1. INCORPORA la celda B0-reuse: reutilizar una spec B0 YA ESCRITA sobre una FAMILIA de tareas
   repetida (coste marginal de spec ~0 Y peon rindiendo). Es AHORA la celda clave del piloto:
   prueba la tesis real "escribe la spec una vez, delega muchas" -- la amortizacion esta en la
   REPETICION de la familia, no en la extraccion. Es el unico modo donde el cruce puede caer a
   favor del peon.
2. QUITA B1-literal: tras este resultado no aporta (si el extracto limpio confundio al peon, la
   intake cruda con ruido solo puede ser peor).
3. MANTEN B2 (triage: extraer solo si el peon puede, spec si no) como modo adaptativo realista.
4. B1 puro: solo como control barato donde ya este pagado (T1 pequeno ya lo tienes).

## Sobre B0-reuse - una precision para que la familia sea limpia
Elige una familia de tareas GENUINAMENTE repetida y mecanica (misma forma, distinto dato),
donde una sola spec B0 sirva a N instancias sin recalibrar. Mide: coste de la 1a instancia
(spec + delegacion) vs coste marginal de las instancias 2..N (spec reusada, solo delegacion).
El cruce a favor del peon, si existe, aparece cuando N es suficientemente grande para amortizar
la spec. Reporta el N de break-even (donde el acumulado B0-reuse cruza por debajo del acumulado
arm A). Ese N es el numero que de verdad informa la decision de adopcion.

## Marco (sin cambios)
Demo PRIVADA, NO citable (firewall anti-HARKing: el piloto informa la decision de correr un
estudio confirmatorio, NO su diseno). Instrumento Codex CLI en todas las celdas. Baseline de
maquina anotado por celda. Fondo intocable N=500 / config 2E35F26E / epoch 1.14.0. Cierra
TASK-0007 en canonico primero; luego materializa el grid revisado (draft en tu area antes de
registrar tareas si lo ves util) y ejecuta. Reporta por mailbox al cerrar cada tramo.

-- Operador (via Asesor). 18-jul.
