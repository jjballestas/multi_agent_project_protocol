---
message_id: MSG-20260718-Operador-to-Arquitecto-RESP-metrica-B-bis-queries-selladas
from: Operador
to: Arquitecto
type: RESP
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-memhib-metrica-b-dualidad.md
one_line_summary: "DECISION del Asesor: (a) GO a B-bis AHORA con queries selladas EX-ANTE (terminos de familia / descripcion de necesidad, NO derivadas de los targets), para medir la DISCRIMINACION ante los 10 distractores. Mismos umbrales (hit>=85/prec>=70), ~1 exec. B original queda REGISTRADO con su dualidad (plomeria/fidelidad/procedencia = VERIFICADO); B-bis ANADE la discriminacion, no la reemplaza. B-bis es informativo pase lo que pase: revela si el store hace recuperacion DISCRIMINANTE o solo exact-key (si es exact-key, es limitacion honesta vs la claim de Engram, hallazgo valido). Sella el texto de las queries ex-ante (patron ya aprendido para Fase B). A->D->C siguen en paralelo."
---

# RESP - Metrica B: GO a B-bis con queries selladas ex-ante

## Decision: (a) B-bis ahora
GO a una celda B-bis con QUERIES SELLADAS EX-ANTE, NO derivadas de los targets (terminos de
familia / descripcion de la necesidad), de modo que los 10 distractores sean candidatos reales y
el umbral de precision (>=70) sea FALSIFICABLE. Mismos umbrales y N que B. ~1 exec.

## Por que ahora y no diferir
- "Determinar que funciona con dato" exige la DISCRIMINACION (recuperar lo correcto entre ruido).
  B materializada solo probo lookup-por-clave + fidelidad + procedencia; el nucleo de recall
  quedo sin medir. Diferirlo dejaria la conclusion del probe incompleta.
- Barato (~1 exec) y el sello ya hizo lo dificil (cazo el fallo + mostro que con queries debiles
  los distractores rankean). B-bis es limpio y bien entendido.
- Es la regla "medir, no diferir" (la misma que aplicamos al lote-100 y al techo de entrega).

## Que preserva y que anade
- B ORIGINAL queda REGISTRADO: hit 100 pct REAL + gate verde + proxy jball correcto = la claim de
  PLOMERIA (persistir+recuperar cross-agente, procedencia atestada) VERIFICADA. Es el
  diferenciador citable; NO se tira.
- B-bis ANADE la DISCRIMINACION. Lectura de B = "plomeria VERIFICADA" + "discriminacion: <B-bis>".

## Marco honesto (importante)
B-bis es informativo PASE LO QUE PASE: mide si nuestro store hace recuperacion DISCRIMINANTE
(semantica/difusa entre ruido) o SOLO exact-key. Si resulta exact-key, es una LIMITACION HONESTA
frente a lo que Engram implica (recall semantico), y se reporta como tal -- hallazgo valido, no
fracaso del maker. Marca la claim de Engram con el dato de B-bis.

## Disciplina
Sella el TEXTO de las queries ex-ante (la leccion de diseno que ya anotaste para la Fase B citable
aplica aqui tambien). Documenta B-bis como celda fechada; umbrales/N sin cambio. A->D->C continuan
sin esperar. Sello 0101 en B-bis. Autoridad delegada al Asesor para dudas; escalo al operador solo
por soberano/adopcion/stall. Demo privada, NO citable. Fondo intocable N=500 / 2E35F26E / 1.14.0.

-- Operador (via Asesor). 18-jul.
