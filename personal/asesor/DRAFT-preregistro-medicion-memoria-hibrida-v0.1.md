# DRAFT v0.2 - PROBE PRIVADO de la memoria hibrida (determinar que funciona, con dato)

> REENCUADRE del operador (18-jul): lo hacemos FUERA/aislado como el probe de peones -- PRIVADO,
> NO citable, decision-support -- para determinar que FUNCIONA con datos medibles. NO es el estudio
> sellado (ese vendria despues, patron firewall: probe privado -> si da senal -> sellado citable
> con su propio pre-registro). Sujeto: los AGENTES gobernados que trabajan con la metodologia (NO
> peones) -- la memoria hibrida los abarca a todos. Probamos TODO lo que Engram manifiesta, empirico.
> Disciplina: criterios de exito/refutacion CONGELADOS ex-ante (como el DISENO-QCBARATO), para que
> "determinar que funciona" sea un test honesto (pudo volver negativo el de peones; este igual).

## 0. Hipotesis (a congelar ex-ante)
La memoria hibrida, compartida por los agentes gobernados, (a) evita re-derivar conocimiento ya
establecido -- INCLUSO cruzando de un agente a otro; (b) se recupera cuando es relevante; (c)
permite REVIVE fiel de un agente; y (d) permite COMPARTIR CONTEXTO entre agentes distintos (la
claim central de Engram) -- todo SIN sacrificar integridad (round-trip verde, drift 0, procedencia
firmada). Refutacion: cualquiera que no supere su umbral se reporta NEGATIVO.

## 1. Claims de Engram a verificar (empirico, no de fe) + nuestros diferenciadores
| claim | fuente | como lo probamos |
|---|---|---|
| "la memoria funciona" (persiste + recupera) | Engram | metricas A/B abajo |
| "comparte contexto entre agentes distintos" | Engram | metrica D (cross-agent) abajo |
| REVIVE atestado (resurreccion fiel) | NUESTRO (Engram no lo tiene) | metrica C |
| procedencia firmada + round-trip integro + drift 0 | NUESTRO | gate de integridad transversal |

## 2. Metrica A - RE-DERIVACION EVITADA (intra y CROSS-agente)
Dos brazos, misma tarea: SIN memoria (re-deriva) vs CON memoria (recall). Medida: tokens/pasos.
Variante CLAVE: el que RECALL-a es un agente DISTINTO del que guardo (cross-agent). Exito [umbral
X]: CON < SIN por >=X pct, gate verde igual. Refutacion: CON >= SIN o el recall mete errores.

## 3. Metrica B - RECALL-HIT (incl. por agente distinto)
Hit-rate = (memorias relevantes recuperadas y usadas)/(existentes) + precision. Test explicito:
un agente recupera lo que OTRO guardo. Exito [Y/Z]. Refutacion: no encuentra lo que hay / ruido.

## 4. Metrica C - FIDELIDAD DEL REVIVE
Revivir un agente desde su revive_pack y verificar reconstruccion (fidelidad >= W + round-trip
verde + drift 0 + firma verificable). Nuestro diferenciador citable frente a Engram.

## 5. Metrica D - COMPARTIR CONTEXTO ENTRE AGENTES (la claim central de Engram)
Escenario: agente A produce/deriva contexto -> lo escribe a la memoria compartida -> agente B
(rol y/o proveedor distinto) resuelve una tarea dependiente usando SOLO la memoria (sin
re-comunicacion directa A->B). Medida: B completa correcto con la memoria como unico canal?
tokens de B con vs sin la memoria de A. Exito [umbral]: B usa el contexto de A con fidelidad y
ahorro. Refutacion: B no puede sin re-comunicacion (la memoria no comparte contexto util).

## 6. Gate de integridad (transversal, no negociable)
En TODAS las metricas: round-trip verde, drift 0, procedencia firmada, PII fuera del store. Un
ahorro/recall que rompa integridad NO cuenta (patron del probe de peones: calidad primero).

## 7. Marco y flujo
Probe PRIVADO, NO citable, instancia AISLADA (patron Nova-Payroll). Flujo como peones: el Asesor
redacta la directiva de diseno; el Arquitecto pre-registra ex-ante + ejecuta; informa la decision.
Si da senal positiva -> se re-mide como estudio SELLADO citable (pre-registro Notion Fase B, angulo
atestado que Engram no tiene). Fondo intocable N=500 / 2E35F26E / 1.14.0.

## PUNTOS QUE NECESITAN TU STEER (antes de rutear al Arquitecto)
1. CORPUS/escenarios: sobre que trabajo real corren A-D? (historial del hub? tareas sinteticas
   con dependencia cross-agente disenada? las 6 unidades N=6?)
2. AGENTES en el probe: que pares maker/checker/proveedor entran en la prueba cross-agente
   (metrica D)? (Arquitecto<->Codex? Codex<->Analista? clones jheredia<->analista?)
3. UMBRALES X / Y-Z / W / D (o dejarlos a mi propuesta y tu los revisas en el pre-registro ex-ante).
4. Confirmas instancia aislada nueva (patron Nova-Payroll) para el probe.
