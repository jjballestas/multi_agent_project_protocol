# LOG DE DECISIONES - Probe privado de memoria hibrida (Asesor, autoridad delegada)

Directiva madre: 58da180 (GO probe privado). Pre-registro instancia: DISENO-MEMHIB-PROBE (v0.2,
42bb1fd). Marco: privado, NO citable, instancia Nova-Payroll local-only. Metricas A/B/C/D, gate de
integridad transversal, criterios ex-ante congelados. Orden B->A->D->C.

## DECISION 1 - Umbrales ex-ante (propuestos por el Asesor, delegados)
A: CON<SIN >=40pct | B: hit>=85pct/prec>=70pct | C: fidelidad>=95pct+drift0+round-trip+firma |
D: via-memoria-sola >=90pct + ahorro >=30pct. Global: A+B+C+D superan bajo el gate de integridad.

## DECISION 2 - D expandida a CADENA ROSTER (steer del operador + refinamiento Asesor)
De par (Codex->Analista) a cadena Arquitecto->Codex->Analista->Asesor, medida como ESCALERA:
D1 per-salto atomico (atribucion limpia) + D2 end-to-end (floor ~70pct por compounding; FLAG si
D2 < producto de saltos). Asesor = nodo MEDIDO, Arquitecto instrumenta. FREEZE b5947e1 (instancia).
Commit hub: mi FREEZE se colo en b5b1bd3 por carrera de indice (benigno, validate OK).

## DECISION 3 - BLOCKER-PARCIAL del store: enmienda ex-ante mapea a lo canonico-gobernado (1ab8a1a)
El contrato asumia store runtime-KV (Engram): runtime_write_entry / cryptographic_provenance_
signature / revive_execute. El store real es canonico-gobernado y no los tiene. APROBADO mapear a
la semantica real (NO parchear para imitar Engram): write=artefacto+commit+build/ledger firmado;
procedencia=hash-attested+actor_auth; revive=harness arranca con pack. Metricas/umbrales/N
CONGELADOS (mapeo de MEDIOS no de FINES). Documentado ex-ante fechado. Framing: probamos los FINES
de Engram por NUESTROS medios; los medios gobernados son el diferenciador citable.

## DECISION 4 - Proxy jball para el nodo logico Asesor en B y D (a5fed30)
El requester "Asesor" no esta en el registry de la instancia (Arquitecto/Codex/Analista/jball/
jheredia); registrarlo = re-genesis (rompe chain pineado). APROBADO ejecutar el nodo logico Asesor
con el proxy REGISTRADO jball (fiel: Asesor=carril del operador, jball=operador registrado;
cross-autor intacto: jball no autora corpus; trazable: retrieval_log reason=probe-nodo-asesor).
Enmienda ex-ante de MEDIOS, fines intactos. Desbloquea TASK-0022 (B).

## NOTA de proceso
Falsa alarma retirada: mi COORD de "push pendiente" sobre b5947e1 (commit de INSTANCIA local-only,
nunca se pushea por diseno). Leccion de topologia fijada en ESTADO-asesor.md (7c22b0b).

## METRICA B CERRADA con DUALIDAD (2026-07-18 ~20:05, instancia 44983a0 local-only)
hit 26/26 = 100pct REAL (plomeria end-to-end del store canonico-gobernado verificada por el sello:
siembra fiel + recall cross-agente + sha256 + log + contenido campo a campo). gate verde, proxy
jball correcto. PERO precision 26/26 = 100pct VACUA: fallo MAYOR del DISENO (no del maker) -- el
corpus se sello sin congelar el TEXTO de las queries, se usaron claves exactas, los 10 distractores
nunca compitieron -> umbral infalsificable. Lectura: B mide lookup-por-clave + fidelidad +
procedencia (VERIFICADO), NO recall discriminante (NO MEDIDO).

## DECISION 5 - GO B-bis con queries selladas ex-ante (e9b5114)
Pregunta (a) B-bis ahora vs (b) diferir a Fase B. Decision: (a) B-bis AHORA.
Razon: "determinar que funciona" exige DISCRIMINACION (recuperar lo correcto entre ruido); B solo
probo lookup+fidelidad; diferir deja la conclusion incompleta. Barato (~1 exec), el sello ya cazo
el fallo. Regla "medir no diferir" (como lote-100 y techo de entrega). B original NO se tira
(plomeria VERIFICADA = diferenciador citable); B-bis ANADE la discriminacion. Queries selladas
ex-ante (terminos de familia/necesidad, no derivadas de targets) para que precision sea falsable.
INFORMATIVO PASE LO QUE PASE: revela si el store hace recuperacion discriminante o SOLO exact-key
(exact-key = limitacion honesta vs Engram, hallazgo valido).

## B-BIS CERRADA (2026-07-18 ~21:20, instancia 3932b87 local-only) - dato, no decision
Con los 10 distractores como candidatos REALES (88 candidaturas verificadas, replay identico a 11
decimales): hit 26/26 = 100pct FUERTE (target candidate-visible y recuperado-verificado entre ruido,
hasta posicion 21). precision 26/26 = 100pct con componente TRIVIAL declarado (seleccion need-aware:
el consumidor conoce su key). HALLAZGO CLAVE: el ranking bm25 es NO-INFORMATIVO (scores identicos por
familia, orden = alfabeto) -> el store da CANDIDACY completa, NO relevancia semantica. Gate verde.
- VERIFICADO con dato: claim "comparte contexto" a nivel PLOMERIA + CANDIDACY + SELECCION-DE-FLUJO
  (cadena completa guardar-cross-agente -> query ambigua -> candidatos mixtos -> seleccion correcta ->
  retrieve sha-verificado -> uso fiel, 26/26, ruido real, credenciales distintas, procedencia atestada).
  Es lo que Engram manifiesta SIN poder atestar.
- NO MEDIDO (limitaciones honestas -> Fase B citable): recall SEMANTICO (necesidad como texto libre;
  imposible con items que solo difieren en n-serie -> corpus Fase B con descripciones de necesidad);
  seleccion SIN conocer la key; calidad de ranking con contenido diferenciado. Nota: auto-contaminacion
  del search-surface por la propia evidencia en replays (+1 posicion), anotado para celdas futuras.

## METRICA A CERRADA con REFUTA + reencuadre estructural (2026-07-18 ~23:15, instancia 60b39d0)
SIN (re-derivar reglas selladas) = 137929 vs CON (recall real) = 185270 = -34.3pct -> umbral >=40pct
REFUTADO (robusto: incluso imputando el exec bloqueado al SIN da 26.7pct << 40). Ambos brazos 10/10.
REENCUADRE del sello (lo que importa): overhead FIJO ~115k/exec (medido con el exec bloqueado cold-
start) -> el umbral 40pct era INALCANZABLE POR DISENO (max ~17pct con recall gratis). Marginales:
SIN ~+23k (re-derivar trivial, 3 pasos), CON ~+70k (query+retrieve+verify). LECTURA LIMPIA: incluso
al margen, el recall (~70k) cuesta MAS que re-derivar trivial (~23k) -> BREAK-EVEN: la memoria ahorra
SOLO cuando re-derivar costaria MAS que ~70k. En re-derivacion trivial, la memoria CUESTA, no ahorra.
Lo refutado: "recall ahorra 40pct cuando el overhead domina y re-derivar es trivial". NO refutado:
"la memoria no ahorra nunca" (paga cuando re-derivar es caro/imposible; este corpus midio el SUELO).
MISMO PATRON ESTRUCTURAL QUE PEONES: overhead constante domina tareas pequenas. 2 MEDIAS declaradas
(aislamiento SIN no-verificable por construccion, impacto pro-refute; asimetria de cierre al CON).
LECCION Fase B: medicion per-trial + corpus con re-derivacion genuinamente CARA.

INSIGHT emergente (para el reporte global): igual que los peones compran CAPACIDAD no ahorro, la
memoria compra CAPACIDAD (compartir-contexto D verificado, revive C, recall atestado B) NO ahorro de
tokens (A refuta en tareas baratas). El valor esta en lo que HABILITA, no en lo que ahorra.

---
Estado: B (plomeria VERIFICADO) + B-bis (flujo discriminante VERIFICADO; ranking no-informativo) + A
(REFUTA con reencuadre: break-even ~70k, overhead-bound). Sigue D (cadena roster) y C (REVIVE).
DECISION OPERADOR: (a) montar A-bis. Directiva 62953ee + addendum cc8a56f.

## DECISION 6 - A-bis REENCUADRADO: capacidad no ahorro (62953ee + cc8a56f)
Reencuadre del operador: A-bis no mide ahorro de re-derivacion (suelo refutado) sino la CAPACIDAD:
(1) contexto no se pierde en frio, (2) los agentes lo comparten en frio, (3) costo del arranque
reportado, (4) si el metodo aporta a la metodologia. Giro: en frio la alternativa no es re-derivar
trivial (barato) sino re-establecer TODO (caro).
Definicion de CONTEXTO RICO (afinada con el operador): REGIMEN 2 (no-re-derivable/solo-recuperable:
resultados medidos, decisiones tomadas, hallazgos acumulados) como CORAZON; instanciacion tipo
SESION DE INVESTIGACION (decisiones selladas + resultados medidos + derivaciones + refs cruzadas;
pregunta que exige las conclusiones acumuladas). Excluir re-derivable trivial + relleno de volumen.
Dos brazos SIN (ambos): SIN-a re-comunicacion del cuerpo crudo (lee AHORRA: recall dirigido <
re-lectura completa) + SIN-b cold puro sin re-feed (lee HABILITA: recupera vs falla). Fidelidad
>=95 campo a campo. Costo del arranque (~115k + recall) aparte, per-trial. Reporte separa AHORRA de
HABILITA. Congelar ex-ante. Resultado no garantizado (honesto).

## D CERRADA (2026-07-18 ~21:20, del checkpoint del Arquitecto) - dato
D (cadena roster Arquitecto->Codex->Analista->Asesor, escalera, proxy jball): CAPACIDAD 100pct
VERIFICADA (contrafactual 0/30: CON memoria comparte contexto 100pct; SIN falla 0/30) + AHORRO
REFUTADO -105.66pct. Confirma la tesis: la memoria compra CAPACIDAD (compartir-contexto cross-agente
verificado), NO ahorro de tokens. Mismo patron que A y que peones.

## C CERRADA - GO tras remediacion (2026-07-18 ~22:50, reporte consolidado D+C)
C (fidelidad del REVIVE en frio): GO del sello al re-run limpio = 80/80 = 100pct RECOMPUTADO campo a
campo; packs regenerados byte-identicos en clon limpio; cuarentena + orden de medicion verificados
contra err.log; declaraciones de fuentes cuadran en ambas direcciones. 5 MENORES (ninguno altera el
numero). Limite de diseno aceptado ex-ante: C mide fidelidad de TRANSCRIPCION ATESTADA desde el pack
(estado citable campo a campo), no recall ciego. LECCION CLAVE (oro para las claims de Engram): la
contaminacion fue DETECTABLE y REMEDIABLE por NUESTRA atestacion (log-vs-declaraciones, hashes por
blob, cuarentena verificable) -- el diferenciador de la memoria gobernada, demostrado cazando a
nuestro propio harness. Frontier: re-run limpio 171770 (contaminado 163302 superseded). Leccion Fase
B: congelar respuestas en artefacto ANTES de abrir archivos portadores, en execs separados.

## (historico) C ESTUVO EN REMEDIACION (NO-GO del sello, TASK-0026) - sin decision mia (mecanico)
El sello dio NO-GO: los packs Codex se contaminaron por el COLD-START FIJO del harness (vuelca
personal/Codex/ al contexto) + declaracion de fuentes FALSA del maker (sobre-declaracion). La mitad
Analista salio LIMPIA 40/40. Remediacion en vuelo (mecanica, la ejecuta el Arquitecto autonomo):
cuarentena de C-CODEX-S1/S2 (git mv a probe-quarantine/) -> re-run revive con cold limpio ->
des-cuarentena + correccion de declaraciones -> flip -> sello 0101 -> ratificar -> doneflip. El sello
cazando contaminacion = disciplina funcionando. No requiere decision de diseno mia.

## DOGFOOD (evidencia real CONFIRMADA - RESP 6c1ecaa, 21:45)
OCURRIO: la sesion anterior del Arquitecto MURIO por contexto lleno; ESTA sesion arranco EN FRIO
(cero chat heredado) y re-establecio la posicion COMPLETA desde la memoria persistente (SESSION_START
+ snapshot + MEMORY.md) en ~10 min: rol, estado por metrica del probe, el paso exacto de la remediacion
de C, waiter, fondo intocable, watchdogs. El unico delta no en memoria (cuarentena + ACTION paso 2,
21:24-21:30, post-checkpoint) se recupero del auto-poll del arbol. CERO PERDIDA DE ESTADO.
Honestidad ex-post (declarada por el Arquitecto y que preservo): es real pero NO controlada (n=1, sin
brazo SIN); es exactamente el escenario que A-bis medira con brazos. Aqui el re-establecimiento SIN
memoria habria sido de-facto imposible (el chat ya no existe). Vale como observacion de dogfood, NO
sustituye al A-bis controlado.

## D CERRADA - numeros finales (TASK-0025 done)
CAPACIDAD 100 VERIFICADA: 30/30 + 10/10 recomputados por el sello, orden temporal writes->retrieves
estricto, CONTRAFACTUAL INTERNO (mismo runtime sin store) = 0/30 -- la evidencia mas fuerte de la serie.
AHORRO REFUTADO: baseline 89836 vs CON 184759 = -105.66pct (3a refutacion consecutiva del eje tokens).

## DECISION 7 - ACK al freeze de la celda A-bis (c8a8ec3)
El Arquitecto pre-registro la celda A-bis ex-ante (instancia 8b4b87e local-only). Verifique el texto
contra mi directiva + addendum: coincide fielmente (regimen 2; 3 brazos CON/SIN-a/SIN-b separan
AHORRA/HABILITA; fidelidad >=95 campo a campo + tarea >=18/20; cross-agente productor!=cold proxy
jball; set de verificacion sellado entre productor y brazos; overhead ~115k aparte). ACK dado.
GUARDA (no bloquea): N=2 es fino -> capacidad = lectura PRIMARIA robusta; ahorro (CON vs SIN-a) =
DIRECCIONAL, no precision; split de los 2 trials = declarar INCONCLUSO esa dimension (no promediar);
cuantificacion rigurosa -> Fase B. GO trial 1.

## ITEM PARQUEADO (operador 2026-07-19) - CADENCIA DE ACTUALIZACION DE LA MEMORIA (futuro, "luego")
El operador cierra la linea de velocidad-de-carga (no la abrimos: le basta que el contexto NO se
pierda; el A-bis mide el costo). PARQUEA para despues del probe: encontrar el MECANISMO de CADA
CUANTO se actualiza la memoria (cuando el agente flushea su estado al store).
Marco (para cuando se retome): es el knob que balancea OVERHEAD vs ESTADO-EN-RIESGO.
- Muy frecuente -> overhead alto (cada write = artefacto + commit + build + ledger; medido caro
  en el probe: recall/write gobernado cuesta tokens).
- Muy raro -> en un crash se pierde el DELTA desde el ultimo update (el Arquitecto lo recupero del
  auto-poll del arbol 2x hoy, pero NO esta garantizado; commits sin pushear se perderian).
Mecanismos candidatos: event-driven (tras cada accion sellada), milestone (disciplina session-
checkpoint), context-pressure (antes de compactar), time-based (cada N min). Conecta con: el costo
del A-bis, la leccion de contaminacion de C, y el delta-recovery del dogfood. NO abrir ahora.

## DOGFOOD #2 (2026-07-19 01:16) - segunda evidencia en vivo
El Arquitecto se CERRO (sesion muerta ~00:09-01:16) y al reabrirlo el operador, cold-starteo y
retomo EXACTO donde estaba: graduo el brazo CON del trial 1 contra el set de verificacion + emitio
SIN-a. 2a evidencia n=1 no controlada de cold-start-recall. Codex vivo (4 procs). Anotar al reporte.

---
## A-BIS TRIAL 1 CERRADO (2026-07-19 ~01:46) - EL PUNTO DE INFLEXION
Tabla (marginal = total menos overhead fijo ~115k/exec):
| brazo | tarea | fidelidad | marginal est. |
| CON (memoria) | 20/20 | 100pct | ~7.5k |
| SIN-a (re-comunicacion, cuerpo crudo re-fed) | 20/20 | 100pct | ~35.5k |
| SIN-b (cold puro, sin memoria ni re-feed) | 0/20 (todo NO-DERIVADO honesto) | 0 | ~11.7k |
DOS LECTURAS (trial 1, DIRECCIONAL hasta trial 2 por la guarda N=2):
- HABILITA (criterio 1, capacidad): CON 20/20 recupera DONDE el cold puro SIN-b entrega 0/20 ->
  "el contexto NO se pierde en frio" = EXITO CLARO (equivalente al contrafactual 0/30 de D).
- AHORRA (CON vs SIN-a): CON marginal ~7.5k vs SIN-a ~35.5k = la memoria recall es ~5x MAS BARATA
  que re-comunicar el cuerpo rico. *** PRIMER AHORRO CONFIRMADO de toda la investigacion ***.
INSIGHT: el reencuadre del operador era CORRECTO. A/D refutaron "ahorro" porque comparaban contra
re-derivacion TRIVIAL (barata). A-bis compara contra RE-COMUNICACION de contexto RICO (cara) y ahi
la memoria GANA en ambos ejes: recupera lo perdido (capacidad) Y ~5x mas barata que re-establecer.
Sin memoria+sin refeed = perdido; sin memoria+refeed = recuperado pero caro; con memoria = recuperado
y barato. Es la tesis del regimen 2, confirmada. (Trial 2 con productor distinto en curso -> confirmar.)

## A-BIS TRIAL 2 (2026-07-19 ~02:32) - LOS TRIALS SE PARTEN EN EL AHORRO (la guarda funciono)
Trial 2: CON 20/20 (fidelidad 100pct; cross-agente INVERTIDO cold-Codex lee lo de Analista, sha
match -> compartir verificado en AMBAS direcciones con T1) | SIN-a 20/20 | SIN-b materializado
(pendiente grade, esperado 0/20).
COSTOS trial 2: CON 127680 vs SIN-a 124214 -> CON +2.8pct MAS CARO (marginal SIN-a ~9.2k).
*** SPLIT vs trial 1 (CON ~5x mas barato que SIN-a) ***. El Arquitecto aplico MI GUARDA (ACK N=2):
"discrepancia entre trials = dimension AHORRO INCONCLUSA, no promediar; capacidad no afectada".
POR QUE se parten: el ahorro depende de cuan CARO sea re-comunicar (SIN-a), que varia por corpus
(T1 SIN-a ~35.5k marginal caro; T2 SIN-a ~9.2k barato). El ahorro es CORPUS/REGIMEN-dependiente;
N=2 no lo fija. Rigor -> Fase B con N mayor.
VEREDICTO A-BIS (ambos trials): CAPACIDAD "no se pierde en frio" = VERIFICADA ROBUSTA (CON 20/20 x2,
SIN-b 0/20; cross-agente ambas direcciones). AHORRO = INCONCLUSO (trials split; corpus-dependiente).
La guarda evito shippear un ahorro falso -> disciplina funcionando.

## PROBE COMPLETO - VEREDICTO GLOBAL (2026-07-19 ~03:15, instancia fe1e6ec; reporte hub del Arquitecto)
A-bis sellada GO-CON-HALLAZGOS: CAPACIDAD exito x2 (CON 20/20 vs cold-puro 0/20), COMPARTIR ambos
sentidos, AHORRO INCONCLUSO (T1 -18.7pct / T2 +2.8pct; ademas el sello cazo el confusor H1: el
cold-start del cron volco el destilado T2 en T2-CON pre-ACTION -> el flip cabe en ese payload =
artefacto de harness plausible). Guarda N=2 aplicada.
VEREDICTO 6 CELDAS: B verificada / B-bis discriminante-fuerte (ranking no-informativo) / A refuta
(-34.3) / D capacidad-100+ahorro-refuta(-105) / C REVIVE 80/80 tras remediacion / A-bis capacidad
exito + ahorro inconcluso.
SINTESIS: la memoria hibrida DEMUESTRA CAPACIDAD-CON-INTEGRIDAD (el contexto sobrevive el frio y se
comparte cross-agente con atestacion) y NO demuestra ahorro de tokens en ningun regimen (3 refuta +
1 inconcluso). Diferenciador vs Engram CON DATO: la atestacion cazo la contaminacion del propio
harness DOS veces (C NO-GO + A-bis H1); un store sin atestacion no lo veria. Dogfood 2x en vivo.
DECISION DEL OPERADOR pendiente: Fase B (estudio sellado citable) = pre-registro del Asesor,
independiente (firewall). Fondo intacto. Probe CERRADO. Monitor bflcu3s66 detenido.
SIGUIENTE (orden operador): armar el paso a paso para probar el runtime.

---
[CERRADO] Probe memhib completo. 7 decisiones delegadas registradas.
Lectura casi final: CAPACIDAD/CONTINUIDAD verificada en todo (B/B-bis/C/D/A-bis + dogfood 2x);
AHORRO refutado/inconcluso en todo (A, D, A-bis-split); ATESTACION = el diferenciador (C cazo
contaminacion). Nada requiere decision mia. Asesor autonomo. TRAS EL VEREDICTO: armar paso a paso
del runtime (orden del operador). Watch armado.
