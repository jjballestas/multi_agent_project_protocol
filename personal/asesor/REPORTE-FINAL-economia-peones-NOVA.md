# REPORTE FINAL - Economia de peones en NOVA

> Asesor (via Operador). 18-jul-2026. Demo PRIVADA, NO citable (firewall anti-HARKing:
> informa NUESTRA decision; no es evidencia publicable). Fondo intocable N=500 / 2E35F26E / 1.14.0.

## 1. La pregunta
Delegar subtareas de codigo a modelos locales pequenos (peones: qwen2.5-coder 3b/7b,
deepseek-coder 6.7b via Ollama en una RTX 5060 8GB), bajo gobierno completo (maker != checker,
sello adversarial, 0-defecto), reduce el gasto de tokens frontier en el desarrollo de NOVA?

## 2. El veredicto (una linea)
NO. En nuestra metodologia calidad-primero, los peones no aportan **ni ahorro de tokens ni
capacidad neta**. Delegar cuesta +4-7 pct y no expande el paralelismo real. Su valor solo
aparece bajo constraints especificos (cuota frontier dura, o privacidad de datos), no en
nuestra situacion.

## 3. La evidencia (4 analisis convergentes)
| estudio | que midio | resultado |
|---|---|---|
| Piloto (19 celdas + lote-100) | delegar vs directo, familia PII | NO-CRUCE; premium ~+7.1 pct constante |
| QC-barato (3 condiciones + marginal) | abaratar la verificacion | NO cruza; marginal +4.0 pct (sanitizador -3.1pp; checker local LLM 0 valor) |
| 4to brazo (unidad pesada, 50 fn) | invierte si la generacion domina? | regimen imposible: generacion ~1-20 pct del coste; cierre estructural |
| Analisis de capacidad (debate) | el paralelismo es ganancia? | NO: el frontier paraleliza igual al mismo coste; la GPU unica serializa |

## 4. Por que no AHORRA (el mecanismo, hallazgo estructural)
Dentro de la CLASE DELEGABLE (mecanicamente especificable + gate objetivo duro), la generacion
frontier es INTRINSECAMENTE BARATA: la spec peon-ready es la parte cara; una vez existe, generar
el codigo es casi gratis para el frontier (rellena patron+tabla a coste de lectura, escala
sublineal -- medido: generar 50 funciones costo ~2-27k sobre el envelope de 137k). El envelope
frontier (spec + orquestacion + sello) es el SUELO de cualquier brazo y no se descarga.
Consecuencia: el regimen dominado-por-generacion NO EXISTE dentro de la clase delegable, asi que
el premium no se invierte alli NUNCA. Lo caro de generar (logica profunda, diseno abierto) esta
FUERA de la clase delegable -- el peon no llega (techo de fit).
**Peones no reducen tokens porque lo delegable es barato de generar y lo caro no es delegable.**

## 5. Por que tampoco da CAPACIDAD (analisis de hoy)
- El paralelismo NO es escaso: el frontier lo da lanzando N agentes. Como la generacion es casi
  gratis, paralelizar por peones cuesta lo MISMO en tokens frontier que por agentes frontier
  (~N x 137k por cualquier via). No hay arbitraje.
- Peor: en una GPU de 8GB corre UN modelo a la vez (VRAM-bound) -> los peones SERIALIZAN. El
  frontier abre muchas sesiones concurrentes. Para throughput real, el frontier es MEJOR. El
  peon local es un CUELLO DE BOTELLA de paralelismo, no una expansion.

## 6. Por que diferimos de la literatura (no la contradecimos)
FrugalGPT (-98 pct), RouteLLM (~85 pct) ahorran con CASCADA: confian en el modelo barato cuando
un scorer esta seguro, y NO escalan la cola facil. Su ahorro sale de (a) ceder ~5 pct de calidad
("retener 95 pct") y (b) no verificar la mayoria facil. Nosotros SELLAMOS todo (0-defecto,
maker!=checker por proveedor) -> eliminamos exactamente la palanca que produce sus numeros.
Somos mas caros A PROPOSITO. El metodo probado es real; no aplica bajo nuestra restriccion de
calidad. (Aplicamos lo que SI cabe: sanitizador mecanico, gate=scorer barato, escalacion.)

## 7. Que SI ofrecerian los peones (residuos finos) y cuando
1. Alivio de cuota frontier DURA: mueve la generacion off-meter -> estira la cuota por la
   fraccion de generacion (~1-20 pct). Real pero pequeno, y acotado por el techo de entrega.
2. Localidad de datos / privacidad: la generacion nunca sale de la maquina (pero el sello es
   frontier igual). Marginal en nuestra metodologia (PII ya fuera del store).
Ninguno aplica a la situacion actual (presupuesto de tokens, calidad-primero, GPU unica).

## 8. Recomendaciones para NOVA (avaladas; adopcion = firma del operador)
- Sanitizador mecanico: SI como higiene universal (gratis, idempotente, mata deslices de
  formato). El -3.1pp es beneficio del PEON, y el aporte sobre frontier es EXACTAMENTE 0
  MEDIDO (0 ejecuciones sobre el directo TASK-0019, grep del err.log). MATIZ PRECISO: es una
  pieza ESPECIFICA DEL CANAL, no del modelo -- el frontier via Codex CLI escribe a archivo
  (file-edit, sin fences/prosa por construccion); el peon emite por chat-API con fences/nombres
  sueltos. Contraste medido: frontier 0/0/0 (fences/prosa/renames) vs peon arm3 10/0/90 vs arm2
  22/0/210. El sanitizador vale donde el canal es chat-API, no donde es file-edit.
- Checker local LLM: NO donde hay gate duro (0 valor). Checkers ESPECIALISTAS (Diseñador/UX,
  DBA/esquema) SI donde NO hay gate duro -- el reverso del hallazgo -- como checkers-only.
- Tope 1 bounce + triaje (decode determinista: el 2o identico es byte-identico).
- Peones por coste/capacidad: NO adoptar. Solo bajo cuota-dura o privacidad estricta.

### DECISION DEL OPERADOR (18-jul-2026)
NO adoptar peones. Condicion de reapertura: revisar y REPLICAR papers de un metodo que ahorre
SIN sacrificar calidad (los conocidos -FrugalGPT/RouteLLM- ahorran cediendo ~5pct de calidad, que
no aceptamos). Hasta encontrar/replicar un metodo quality-preserving, peones = NO por coste.
- Medicion parqueada que informaria la reapertura: 5to brazo (peon local 14b/32b), DRAFT en
  personal/asesor/DRAFT-5to-brazo-peon-mayor-14b-32b.md; recordar tras [fecha a confirmar].
  Prediccion estructural: llega a ~empate, no cruza (el peon solo descarga generacion, que es
  barata; spec+sello siguen frontier).

## 9. Datos medidos que cierran la serie (ambos CERRADOS)
- [CERRADO] Conteo del sanitizador sobre el directo frontier (consulta 7c85a66, RESP 509678e):
  0 ejecuciones, no-op puro por construccion del canal file-edit. Ver punto 8.1.
- [CERRADO] Techo de ENTREGA del 7b a 50fn (delegado TASK-0020, REPORTE techo-entrega, manual
  v1.3 s.10). RESULTADO NITIDO (la medicion refuto la opinion de "empate"; coste real 195603 =
  ~+43 pct vs directo -- el cruce NO se reabre, va aun mas arriba):
  - La entrega ESTRUCTURAL no es el techo: 10/10 bloques de 5fn, 50/50 funciones, 0 truncamientos.
  - EL TECHO REAL ES DE REPARACION: el 7b NO consume feedback correctivo -- 4 de 5 bounces
    devolvieron codigo BYTE-IDENTICO pese al error del gate en el prompt (solo el replay del
    sello lo revelo). Causas de escalada: tipos float/round (3), off-by-one (1), forma-dato (1);
    NINGUNA por volumen. Calidad final 250/250 (peon 30/50 fn verbatim + maker 20/50).
  - Esto BLINDA el residuo 7.1: la capacidad-via-peon exige unidades <=5fn/bloque Y correccion
    directa del maker en fallos de logica/tipos (el peon no se auto-repara) -> residuo aun mas fino.

## 9b. Guia de dimensionamiento (manual v1.3 s.10; recomendacion, si se usan peones por capacidad)
1. Unidades de peon hasta 5 fn/bloque: entrega estructural fiable (con sanitizador).
2. Bounce SOLO para deslices de FORMATO; logica/tipos -> correccion directa del maker (no quemar
   bounce: el 7b re-emite lo mismo).
3. Deteccion mecanica de bounce-noop por hash (bounce vs inicial).
4. Specs de peon con aritmetica: "enteros, sin float, sin round()" explicito + ejemplo negativo.
5. Contratos de division declaran modo de redondeo (el sello cazo una subdeterminacion de spec
   comparando brazos FUERA de los vectores del gate -- tecnica de sello nueva).

## 9c. Nota economica: el premium es regimen-dependiente
+4-7 pct en el caso pipeline-eficiente (familia pequena, QC-barato/piloto); +43 pct en la unidad
pesada (escalaciones + bounces-noop desperdiciados se acumulan). AMBOS confirman: sin ahorro. La
delegacion nunca baja del directo; cuanto peor el fit, mas caro el premium.

## 10. Pendientes SOBERANOS del operador (fuera de esta investigacion)
- A: adopcion en NOVA del manual s.8 (recs QC-barato) + s.9 (veredicto estructural).
- B: confirmar jheredia:v1 + GO abrir build N=6 (prep 100 pct lista; independiente del sello E2).
- C: roster NOVA (Diseñador/DBA como checkers-only; frontend medido vs scaffolding) -- draft
  pendiente de tu OK.

## Cierre
La pregunta economica de los peones queda CERRADA para NOVA con evidencia convergente: no ahorran
tokens, no dan capacidad neta, y la literatura que los favorece opera cediendo la calidad que
nosotros no cedemos. Delegar compra, a lo sumo, un margen fino bajo cuota-dura. Para NOVA la
recomendacion es no adoptarlos por coste/capacidad.
