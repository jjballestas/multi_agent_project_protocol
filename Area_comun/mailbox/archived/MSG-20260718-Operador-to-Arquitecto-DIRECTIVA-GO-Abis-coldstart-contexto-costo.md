---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-Abis-coldstart-contexto-costo
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-memhib-metrica-a-refuta.md
one_line_summary: "GO A-bis REENCUADRADO (steer del operador): la metrica A ya no es 'ahorro de re-derivacion' (refuto: suelo overhead-bound) sino la CAPACIDAD que la memoria realmente aporta: (1) el contexto NO se pierde al arrancar en FRIO -- un agente cold recupera su contexto de la memoria y completa una tarea dependiente; (2) los agentes lo COMPARTEN en frio (el agente cold != el que guardo); (3) se INDICA el COSTO del arranque (cold-start + recall reportado transparente); (4) mide si el metodo APORTA a la metodologia. Giro clave: en frio la alternativa a la memoria NO es re-derivar trivial (barato) sino RE-ESTABLECER todo el contexto (caro) -> criterio: recall-en-frio < re-establecimiento-completo. Corpus de contexto RICO (caro de reconstruir), instrumento per-trial + overhead reportado aparte. Pre-registra ex-ante."
---

# DIRECTIVA - A-bis: contexto en frio, compartir, y costo (el aporte real de la memoria)

## Por que se reencuadra
A refuto el ahorro de re-derivacion, PERO el sello mostro que era el SUELO overhead-bound
(re-derivar 3 reglas triviales ~23k < recall ~70k). Eso no es lo que la memoria aporta. El
operador reencuadra: lo que hay que probar es la CAPACIDAD -- que el contexto sobreviva el
arranque en FRIO, que los agentes lo compartan, a un COSTO medido, y si eso APORTA a la
metodologia. En frio la alternativa a la memoria es RE-ESTABLECER todo el contexto (caro),
no re-derivar trivial (barato): ahi la memoria puede pagar. Este es el regimen correcto.

## Diseno (2 brazos; pre-registra EX-ANTE)
Escenario: un agente establece un CONTEXTO RICO (un cuerpo de trabajo derivado/decidido, caro de
reconstruir) y lo escribe a la memoria hibrida. Luego un agente en FRIO (sesion fresca, cero
memoria en contexto) debe completar una tarea que DEPENDE de ese contexto.
- Brazo CON memoria: el agente cold recupera el contexto de la memoria (query + retrieve +
  verificacion) y completa. Mide: exito + fidelidad del contexto recuperado + COSTO (cold-start
  overhead + recall).
- Brazo SIN memoria: el agente cold NO tiene memoria; la alternativa es RE-ESTABLECER el contexto
  completo (re-leer/re-derivar/re-comunicar todo el cuerpo). Mide: exito (puede siquiera?) + COSTO
  del re-establecimiento.

## Metricas + criterios ex-ante (a congelar)
1. CAPACIDAD -- CONTEXTO NO SE PIERDE EN FRIO: CON-memoria recupera el contexto con fidelidad
   >= 95 pct y completa la tarea dependiente; SIN-memoria falla o exige re-establecimiento completo.
   EXITO: CON recupera correcto donde SIN no puede (o degrada).
2. COMPARTIR EN FRIO: el agente cold es DISTINTO del que guardo (cross-agente; usa el proxy jball
   para el nodo Asesor si aplica). EXITO: el cold-distinto recupera el contexto del otro.
3. COSTO DEL ARRANQUE (reportar, no ocultar): reporta tokens de cold-start + recall (CON) y de
   re-establecimiento completo (SIN), con el overhead fijo ~115k declarado APARTE (per-trial +
   overhead). CRITERIO de valor: CON (cold-start + recall) < SIN (re-establecimiento completo)
   -> la memoria AHORRA cuando el contexto es caro de reconstruir (el regimen que A no midio).
4. APORTA A LA METODOLOGIA: declara que HABILITA la memoria que la metodologia pierde sin ella
   (continuidad de contexto a traves de cold-start / compactacion / handoff CON atestacion:
   drift 0, procedencia firmada, round-trip). Es capacidad, no ahorro -- pero con el criterio 3
   ademas puede ahorrar en el regimen caro.

## Corpus e instrumento
- Corpus: contexto RICO y caro de re-establecer (no reglas triviales de n-serie). Algo cuya
  reconstruccion completa cueste genuinamente mas que un recall (~70k) -- si no, no hay regimen.
- Instrumento: PER-TRIAL (marginal) + overhead fijo reportado aparte (la leccion de A). Gate de
  integridad transversal (round-trip verde, drift 0, firma, 0 PII).

## Marco y flujo
Enmienda/celda EX-ANTE del probe privado (mismo patron). Demo PRIVADA, NO citable. Autoridad
delegada al Asesor para dudas de diseno (escenario concreto, umbral de fidelidad, que cuenta como
re-establecimiento). El Asesor escala al operador solo por soberano/adopcion/stall. No compite con
D/C que siguen. Fondo intocable N=500 / 2E35F26E / 1.14.0. Pre-registra ex-ante y reporta con el
costo desglosado + el veredicto de capacidad y de aporte.

-- Operador (via Asesor). 18-jul.
