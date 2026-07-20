# DISENO DE MEDICION - indexacion por grafo sobre la memoria hibrida (v0.1)

> Autor: Asesor, 2026-07-20. **Pendiente de REVISION ADVERSARIAL** (orden del Operador).
> Ejecucion: NO arranca hasta que cierre la tanda DECISION-0103 (orden del Operador:
> "no quiero dejar trabajo a medias").

## 0. DECLARACION PREVIA (se firma antes de mirar un solo numero)

- **Esto es DECISION-SUPPORT PRIVADO. NO CITABLE.** No es un estudio sellado, no alimenta
  publicacion ni TFM, y su resultado NO restringe el diseno de una eventual Fase B.
- **Firewall anti-HARKing:** hipotesis, brazos, metricas y **umbrales de decision** quedan
  fijados EN ESTE DOCUMENTO antes de ejecutar nada. Lo que se descubra fuera de lo
  pre-declarado se reporta como EXPLORATORIO y se etiqueta como tal, sin excepcion.
- **Proposito unico:** dar al Operador el dato que condiciona su firma de promocion de la
  memoria hibrida al master (DRAFT-DECISION-0104, R0: el checklist hace ELEGIBLE, la firma
  promueve).
- **No se ejecuta durante la ventana de medicion del N=6.** Introducir un indice que cambia
  el coste de exploracion mientras se mide Contabilidad invalidaria esa comparacion.

## 1. Pregunta e hipotesis

**Pregunta:** ?indexar la memoria hibrida con un grafo de aristas tipadas mejora la
recuperacion de contexto lo bastante como para justificar su coste?

**Hipotesis primaria (H-RANK):** el brazo con grafo mejora la POSICION de la entrada
correcta frente al ranking bm25 actual.

Fundamento medido, no supuesto: la celda B-bis del probe de memoria concluyo
**"hit 100 discriminante FUERTE; ranking bm25 no-informativo"** -- el retrieval encuentra
lo relevante pero no sabe ordenarlo, y empata familias enteras. Esa es la deficiencia que
este diseno ataca. Si no fuera por ese dato medido, no habria razon para tocar algo que
funciona.

**Hipotesis secundaria (H-TOK):** a fidelidad constante, el brazo con grafo necesita
INYECTAR MENOS TOKENS (basta traer top-K menor). Mecanismo distinto del que ya refutamos:
antes se pedia ahorro al ACTO DE GUARDAR (imposible: overhead-bound); aqui el ahorro
vendria de INYECTAR MENOS por mejor orden.

**No-hipotesis declaradas** (se miden, no se defienden): latencia, tamano en disco.

## 2. Brazos

| brazo | descripcion |
|---|---|
| **A - SIN (control)** | memoria hibrida tal cual esta hoy en el clon: retrieval + ranking bm25 |
| **B - CON grafo** | misma memoria + capa de grafo con aristas tipadas sobre las mismas entradas |

- **Mismo store, mismo contenido, misma consulta.** Lo unico que cambia es como se ordena
  y se navega. Cualquier otra diferencia entre brazos es un confusor y aborta la celda.
- **Baseline reutilizado:** el conjunto de consultas y el grading de B-bis se reutilizan
  cuando aplique, para que la comparacion sea contra un numero ya medido y no contra uno
  fabricado para la ocasion.

## 3. Corpus de consultas

- **Q1 - reutilizadas de B-bis** (las que produjeron el empate de familias): son las que
  exhiben el defecto; si el grafo no las arregla, no arregla nada.
- **Q2 - cross-agente**: consultas cuya respuesta correcta fue escrita por un agente
  distinto del que consulta (la capacidad que el probe demostro en ambos sentidos).
- **Q3 - distractoras**: consultas cuya respuesta correcta NO esta en el store. El brazo
  correcto responde NO-DERIVADO. Sirven para detectar que el grafo no fabrique conexiones
  plausibles donde no las hay -- el riesgo especifico de anadir aristas.

Tamano y seleccion exacta: los fija el revisor adversarial junto con el sellado ex-ante
del set de verificacion (leccion de A-bis: el set se sella ANTES de cada tanda de brazos).

## 4. Metrica principal - FIDELIDAD POR TOKEN INYECTADO

Un solo numero que captura las dos formas legitimas de ganar:

- misma fidelidad con MENOS tokens -> ahorro;
- MAS fidelidad con los mismos tokens -> capacidad.

Definicion operativa: por consulta, `fidelidad_obtenida / tokens_inyectados`, donde
fidelidad se grada contra el set sellado ex-ante (mismo criterio de grading que el probe:
hechos correctos recuperados / hechos requeridos, con NO-DERIVADO contando como acierto en
las distractoras).

Se reporta ademas, desagregado y sin promediar entre trials:

- **precision@1** y **precision@3** (la hipotesis H-RANK en su forma cruda);
- **fidelidad a presupuesto constante**: fijado K de entradas, cuanto recupera cada brazo;
- **tokens a fidelidad constante**: fijada la fidelidad objetivo, cuantos tokens hace falta
  inyectar en cada brazo.

## 5. Los TRES costes (R5 de la DRAFT-DECISION-0104)

Obligatorios los tres. Medir solo el primero permitiria declarar victoria ignorando el
peaje -- que es el error de la celda A del probe ("REFUTADO, overhead-bound por diseno")
cometido del reves.

1. **Coste de USO** - tokens y latencia por consulta, ambos brazos.
2. **Coste de CONSTRUCCION** - construir el grafo desde cero sobre el store existente:
   tokens (si interviene un LLM), tiempo de reloj, tamano resultante.
3. **Coste de MANTENIMIENTO** - reindexado ante cambios: cada cuanto hace falta, que cuesta
   cada vez, y coste del drift si NO se reindexa (respuestas obsoletas).

El overhead fijo se reporta APARTE y sin diluir, igual que en A-bis (donde el overhead de
~115k por exec se declaro separado en vez de promediarse dentro).

## 6. Firewall de PII (desde el diseno, no anadido despues)

- La regla dura sigue vigente: **PII de nomina JAMAS entra al store**, y el grafo es parte
  del store a estos efectos.
- **Verificacion previa a construir**: escaneo del contenido a indexar con los mismos
  controles usados el 19-jul (IBAN con validacion de checksum mod-97, DNI/NIE, NSS,
  tarjetas, PEM, API keys), reportando CONTEOS Y RUTAS, nunca valores.
- **Dato conocido del clon**: existen 60 IBAN sinteticos en artefactos de probe y en
  `test_memory_db.py`; 58/60 fallan el checksum (fabricados) y los 2 restantes son
  consistentes con azar (~0.6 esperados sobre 60). Son fixtures de tests de deteccion de
  PII, no datos reales. **Aun asi el grafo NO los indexa**: entran a la lista de exclusion
  explicita, porque la regla no es "no indexes PII real", es "no indexes PII".
- **Verificacion posterior a construir**: 0 entradas prohibidas en el grafo, comprobado
  sobre el artefacto final, no sobre la intencion.

## 7. Guardas que NO pueden empeorar (si empeoran, el brazo B pierde aunque gane en ranking)

- Atestacion intacta: sha, procedencia, drift 0, round-trip.
- 0 entradas prohibidas (seccion 6).
- El grafo no puede convertirse en fuente de verdad: sigue siendo PROYECCION de las
  entradas atestadas. Si grafo y entrada discrepan, gana la entrada.

## 8. Umbrales de decision (PRE-DECLARADOS)

Propuestos por el Asesor, a ratificar o corregir por el revisor adversarial ANTES de
ejecutar. Una vez ejecutado, no se tocan.

- **ADOPTABLE (recomendacion favorable al Operador):** precision@1 del brazo B supera al de
  A por un margen que el revisor fije como no atribuible a ruido, **Y** fidelidad por token
  no empeora, **Y** las guardas de la seccion 7 se mantienen.
- **NO ADOPTABLE:** el ranking no mejora, o mejora pero el coste de construccion +
  mantenimiento excede el beneficio de uso en el horizonte que fije el revisor.
- **INCONCLUSO:** los trials se parten (un trial a favor, otro en contra). **Se declara
  INCONCLUSO, no se promedia.** Precedente vinculante: la dimension AHORRO de A-bis se
  declaro inconclusa por split entre trials, y esa guarda impidio un claim falso de ahorro.

Recordatorio de R0: ninguno de estos resultados promueve nada. Producen una recomendacion;
la firma es del Operador y puede negarla sin causa tecnica.

## 9. Fuente externa: `github.com/DeusData/codebase-memory-mcp`

De ese repositorio se toma **la IDEA estructural**, no necesariamente codigo: grafo con
aristas tipadas, y su modelo de nodos/relaciones como referencia de diseno.

Advertencias para quien lo revise:

- **Ataca un problema DISTINTO al nuestro**: indexa estructura de codigo, que es
  RE-DERIVABLE (si el indice miente, abres el fichero). Nuestra memoria guarda contexto NO
  re-derivable (por que se decidio algo). Por eso ellos pueden permitirse no atestar el
  contenido y nosotros no.
- Su "atestacion" (SLSA-3, sigstore, VirusTotal, SHA-256) cubre **el binario**, no las
  respuestas. No confundir una con otra.
- Sus cifras (indexado en minutos, 120x menos tokens) son claims de README **sin verificar
  por nosotros**. No entran a este diseno como supuesto.
- Licencia MIT declarada: revisar compatibilidad antes de tomar codigo, no solo ideas.

## 10. Riesgos y confusores conocidos

- **Contaminacion por harness** (mordio dos veces: NO-GO de la serie C y H1 de A-bis). El
  volcado de cold-start del cron puede meter el payload en un brazo y no en el otro. Brazos
  homogeneos verificados ANTES de cada tanda, y cuarentena fisica de lo prohibido.
- **Aristas plausibles pero falsas**: el riesgo especifico de anadir un grafo es inventar
  conexiones. Para eso existe Q3 (distractoras).
- **Sobreajuste al corpus de B-bis**: si solo se mide sobre las consultas que ya sabemos
  que fallan, el resultado esta inflado. Por eso Q2 y Q3.
- **Falso verde por medir solo el uso**: cubierto por la seccion 5.

## 11. Entorno

- **Clon:** `D:/Aegis_Scratch/Nova-Payroll/memhib-graph-probe` (creado 20-jul, 279 commits,
  origin = la instancia local). Convencion de DECISION-0098 (scratch root por proyecto).
- **Sin `protocol-secrets`** (gitignored, 0 rastreados): el clon NO puede correr la
  ceremonia de firmas atestadas. **No hace falta**: la ceremonia produce evidencia
  publicable, y esto es privado. Lo que da validez aqui es la medicion, no las firmas.
- **Gobernanza:** el TRABAJO se gobierna en el clon (tareas con intake, claims, gate de
  entrega). Las DECISIONES y los reportes al Operador van por el mailbox del HUB, citando
  el sha del clon. Es el patron que ya funciono en el probe de peones y en el de memoria.

## 12. Lo que este diseno NO cubre (declarado)

- No mide el cruce decision<->codigo (la idea de enlazar una entrada de memoria con los
  nodos del codigo que explica). Eso es producto, no experimento, y se demuestra con un
  caso, no con una metrica. Va despues, si el ranking mejora.
- No evalua adoptar `codebase-memory-mcp` como herramienta para los agentes. Es otra
  pregunta, con otro diseno, y tiene su propia guarda: no durante la ventana del N=6.

-- Asesor, 20-jul-2026. v0.1, pendiente de revision adversarial.
