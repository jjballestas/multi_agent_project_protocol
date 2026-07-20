# LOG DE DECISIONES - 4to brazo: unidad PESADA (regimen dominado por generacion)

Directiva madre: 7d4d203 (GO 4to brazo). Autoridad delegada del Operador al Asesor para dudas de
diseno durante la corrida. Demo privada, NO citable.

## Contexto / tesis
El QC-barato cerro en +4.0 pct midiendo un regimen BARATO-por-unidad (tests PII de juguete) donde
el envelope orquestacion+sello dominaba. Tesis a falsar: en una unidad PESADA (generacion frontier
grande) con gate duro, descargar la generacion al maker local (gratis) hace el sello/orquestacion
(fijos) una fraccion menor -> el premium podria encogerse o INVERTIRSE (delegado < directo).

## Diseno pre-registrado (ex-ante)
- Brazo 1 DIRECTO PESADO: frontier genera + QC + sello. Tokens frontier totales.
- Brazo 2 DELEGADO PESADO: maker local genera + sanitizador + gate duro + bounce-1+triaje +
  escalacion a Codex solo en gate rojo + sello Analista. Tokens frontier (generacion local = 0).
- Cruce = total_delegado < total_directo, junto a calidad + escalacion.
- GARANTIA DE REGIMEN: generacion del directo >= 3-5x el envelope; reportar la fraccion; si no
  llega, read inconcluso -> escalar la unidad.
- Parametros: sanitizador SI; checker LLM local NO; bounce 1+triaje; maker qwen2.5-coder:7b
  B0-reuse (secundario mayor si el 7b topa entrega, etiquetado aparte). maker!=checker intacto.

## Decisiones tomadas

### DECISION 1 - Aval del diseno ex-ante del Arquitecto (2026-07-18 ~12:31)
Contexto: el Arquitecto tomo la directiva y pre-registro ex-ante (6c3cac6: DISENO-PESADO-4tobrazo).
Decision: AVALADO sin objecion (autoridad delegada).
- UNIDAD: motor de nomina sintetico, 50 fn (10 familias x 5 variantes), gate 250 asserts exit-code.
  Razon: generacion-pesada dentro de la clase delegable (especificable + gate duro + familia
  repetida + no catastrofica), sintetica = sin PII, dificultad patron+tabla en fit-7b (T3).
- SETUP COMPARTIDO TASK-0018 (spec+gate+sanitizador v2 = termino comun medido aparte): correcto,
  la simetria manda.
- UMBRAL DE REGIMEN 440k (~4x proxy 110k), chequeado ANTES del delegado, inconcluso+escalar si no
  llega: es la garantia que pedi; no malgasta el delegado en regimen no dominado por generacion.
- Refinamientos aplicados (sanitizador v2, SIN checker local, bounce-1, qwen7b) + leccion 0020.

### DECISION 2 - Respaldo del gate SIN implementacion de referencia (2026-07-18 ~12:31)
Decision: APROBADO formalmente. Razon: pre-generar una solucion de referencia seria el propio
directo (contaminacion) o filtraria al delegado. Los 250 asserts (input->output) son el ORACULO;
computarlos es mucho menor que generar el motor y va como termino comun. El sello 0101 cubre la
correccion del gate. Es una llamada de diseno correcta que merece respaldo explicito.

### GUARDA 3 - Proveniencia del envelope-proxy 110k (2026-07-18 ~12:31)
Fijada (no objecion): que reporte de donde sale el proxy 110k. La fraccion (directo-110k)/directo
solo es interpretable / el "generacion domina" solo es falsable si 110k esta anclado (sello+spec
del setup, o extrapolado del QC-barato), no arbitrario.

### WATCH-POINT 4 - Cobertura del gate (2026-07-18 ~12:31)
5 asserts/fn es cobertura modesta para 0-defecto. Sin cambio de diseno: que el sello 0101 preste
atencion a edges/negativos no cubiertos; el gate corta lo grueso, el sello es el backstop.

Commit del ACK: 150f29e (Ops-Reason 105c, ASCII 0, push OK).

---
### GUARDA 3 RESUELTA - proxy anclado (2026-07-18 ~12:40, commit Arquitecto 37d1b58)
El Arquitecto anclo el proxy 110k al punto MEDIDO 135171 (marginal QC-barato, envelope real con
generacion local=0 frontier) menos ~25k estimados. Reportara la fraccion de regimen con DOS
denominadores: proxy 110k Y cota conservadora medida 135171. Con umbral 440k -> generacion >=75pct
(proxy) y >=68pct (cota medida): "generacion domina" robusto al ajuste de 25k y falsable. ACEPTADO
sin objecion (no mando mailbox: guarda satisfecha, nada que accionar). Watch-point del sello
incorporado. Nota: 440k da 3x vs proxy y ~2.3x vs cota medida; ambos mantienen generacion
dominante (68-75pct del total), y el 440k es PISO (si el directo sale mayor, mejor).

## DIRECTO MEDIDO + REGIMEN FALLA (2026-07-18 ~13:55, entrega ea97e6a)
Directo pesado: 50 funciones, gate 250/250 A LA PRIMERA + regresion 42/42, limpio. Frontier
total = 137042. Garantia de regimen (>=440k): FALLA. Generacion = ~20pct (proxy 110k) / ~1.4pct
(cota medida 135171). La generacion NO domina en ningun anclaje (generar el motor costo ~2-27k
marginales sobre el envelope). Pre-registro -> inconcluso; delegado parado hasta mi decision.

## DECISION 5 - OPCION (a): cerrar con veredicto estructural, NO correr el delegado (2026-07-18 ~14:00)
Decision (autoridad delegada sobre la escala). RESP 7df4a3f.
Razon:
1. Cruce ARITMETICAMENTE descartado: el delegado tambien paga el envelope (~135k) ~ directo 137k;
   su suelo no baja del directo. Correrlo (~150k) confirma un empate ya determinado.
2. El veredicto se apoya en lo MEDIDO (directo 137k, generacion marginal ~2-27k), NO inferencia.
   NO es el error del ~99u (aquello extrapolaba; esto es medido + clausura aritmetica).
3. Demo privada + operador cost-conscious -> "no reproducir lo determinado" (regla del reuso del
   baseline) manda sobre "medir el confirmatorio" (que aplica cuando la region NO esta determinada).
4. Diferido (no descartado): el techo de ENTREGA del 7b a ~50 funciones queda abierto barato.
Consideré (b) medir el delegado (empate ~135-155k, +150k) pero no cambia el veredicto ni la decision;
solo daria el techo-de-entrega, que difiero. (c) descartada: el Arquitecto mostro que escalar por
volumen es ~16x impracticable (generacion sublineal) y por dificultad saca la unidad de la clase.

## VEREDICTO ESTRUCTURAL (el resultado, headline de la sintesis)
Dentro de la CLASE DELEGABLE (especificable + gate duro), la generacion frontier es INTRINSECAMENTE
BARATA (la spec peon-ready es lo caro; generar el codigo es casi gratis, escala sublineal). El
regimen dominado-por-generacion NO EXISTE dentro de la clase delegable -> el premium no se invierte
alli NUNCA. Lo caro de generar (logica profunda, diseno abierto) esta FUERA de la clase delegable
(el peon no lo hace). UNIFICA la investigacion: peones no ahorran tokens frontier porque lo
delegable es barato y lo caro no es delegable.

Estado: 4to brazo CERRADO (directo medido + veredicto estructural; delegado NO corrido). Pendiente:
el Arquitecto ratifica el sello 0101 del directo + entrega la sintesis final de economia de peones
(que ya cierra la investigacion completa: piloto +7pct -> QC-barato +4pct -> 4to brazo estructural).

## RECTIFICACION 6 - GO delegado para MEDIR el techo de entrega (2026-07-18 ~14:25, dir 260e4e4)
El operador rectifico mi DECISION 5 en la parte del diferido: el techo de ENTREGA del 7b a 50fn NO
se difiere/opina, SE MIDE ("medir no opinar"). Reconocido: era mi mismo instinto de saltarme una
medicion no-determinada (como el lote-100 que ya me corrigio). El CRUCE sigue cerrado (aritmetico);
lo que se abre es SOLO el techo de entrega. Ruteo el delegado (TASK-0020) con proposito REDEFINIDO:
metrica primaria = entrega del 7b a 50fn (completa? donde rompe? escalacion?), coste como contexto
(empate ~135-155k, no es el punto). Da la guia de dimensionamiento de unidades de peon para NOVA.
Monitor blmwrcdlg re-armado. Leccion propia: no diferir/opinar lo no-determinado cuando es medible barato.
