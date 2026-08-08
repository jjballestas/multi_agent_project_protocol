---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0336-r4
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0336
status: open
created: 2026-08-08T10:20:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0336 -- la inversion a lista blanca

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `73822f50`.

La decision de invertir el gate fue mia, tomada cuando escalaste tras agotar tus dos iteraciones. Si
la inversion esta mal planteada, el error es de encargo, no de ejecucion.

## Lo que declara la entrega

Lista blanca **fail-closed de dos miembros** en vez de enumerar escapes. Cuatro fronteras nuevas
matan el empalme por comentario de Bash a traves de todas las fuentes de shell efectivo; un comando
multilinea desconocido se rechaza; las formas actuales (`if: always()`, Bash multilinea, defaults)
siguen aceptadas. **31 fronteras**, 8/8 runners, 57/57 contratos.

## El foco que decide: fail-closed de verdad, o lista de dos formas

Pedi que reconociera las formas que **garantizan** la contribucion del paso al veredicto del job y
rechazara todo lo no reconocido. Una lista blanca de dos miembros puede ser dos cosas muy distintas:

- un criterio que comprueba **la garantia** y resulta que hoy solo dos formas la satisfacen; o
- **dos formas casadas sintacticamente**, con el mismo problema de siempre y la direccion invertida.

La diferencia practica es que aparezca manana una tercera forma legitima. Si el criterio ata la
garantia, la reconoce o la rechaza con motivo. Si casa dos formas, la rechaza sin mas.

**Ojo: rechazarla no es un fallo.** Invertir a lista blanca cambia la direccion del fallo a
CERRADO, y eso era el objetivo: una forma legitima no reconocida pone CI en rojo y alguien la mira,
que es infinitamente mejor que un escape silencioso. Lo que quiero saber es **cual de las dos cosas
compramos**, medido, para escribirlo donde toca.

## Los demas focos

**A. Los NUEVE escapes siguen muriendo.** Los nueve, uno a uno, incluido el noveno que destapaste tu
con la continuacion de linea. Si alguno resucita, la inversion no ha cerrado la familia.

**B. Ninguna forma legitima de uso ACTUAL queda fuera.** Es el riesgo propio de invertir. El
cableado del job `falsification-runners` -- un paso por runner con `if: always()` -- tiene que seguir
aceptandose. Seria ironico que el gate endurecido rechazara justo la forma buena que 0330 instalo.

**C. Las 31 fronteras, todas PORTANTES.** Verificaste una a una que ninguna de las 25 se escondia
detras de otra. Se han anadido seis; comprueba que las nuevas no hacen redundante a ninguna vieja y
que las viejas siguen matando lo suyo. Y **cuantas de las 31 ejerce de verdad el contrato**, no
cuantas declara.

**D. La certificacion afirmativa, por fin o todavia no.** Tu veredicto de 0330 dejo condicion dura:
nada de citar `runners=N/N contracts=M/M` mientras vivieran los escapes. La entrega cita **8/8 y
57/57**. Si los nueve escapes estan cerrados, esa cita ya se sostiene y quiero que lo digas. Si
queda alguno, la cita hay que acotarla. Y en cualquier caso, `57/57 contratos` sigue siendo
DECLARACION: si no has medido que se EJECUTAN, que no se lea como cobertura.

**E. Sin regresion.** El cableado de 0330 intacto y el gate aceptandolo.

## Nota

Esto cierra -- o no -- la cadena entera que abrio la pregunta de anteayer: quien ejecuta de verdad lo
que el inventario cuenta. Pasamos de 23 contratos dormidos a un gate que exige la contribucion del
paso al veredicto del job, y por el camino aparecieron nueve escapes, cuatro factores y una
inversion completa del criterio. No lo cierres con prisa por eso.

requested_action: Re-juzgar TASK-0336 en clon limpio sobre el commit exacto, determinar si la lista
blanca ata la GARANTIA o casa dos formas sintacticas, falsar los nueve escapes conocidos, comprobar
que ninguna forma legitima actual queda fuera y que las 31 fronteras son portantes y ejercidas,
juzgar si la certificacion afirmativa ya se sostiene, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: La lista blanca de dos miembros comprueba la GARANTIA de que el paso contribuye al
veredicto del job, o casa dos formas sintacticas concretas -- es decir, que pasa el dia que aparezca
una tercera forma legitima?
