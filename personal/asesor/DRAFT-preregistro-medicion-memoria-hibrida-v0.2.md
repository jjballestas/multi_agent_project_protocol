# DRAFT v0.2 - Pre-registro del PROBE PRIVADO de la memoria hibrida (no citable)

> SUPERSEDE v0.1 (incorpora la DIRECTIVA GO probe privado 18-jul + 6 safeguards del Asesor).
> Ejecutor: ASESOR (diseno, autoridad delegada) - Operador (revisa + sella, patron DECISION-0094) -
> Arquitecto (ancla el intent). Estado: DRAFT del Asesor PARA REVISION del Operador ANTES del freeze.
> NO SELLADO. NINGUNA metrica se corre hasta el sello + firma. Clase: PROBE PRIVADO, NO CITABLE,
> decision-support, instancia AISLADA (patron peones/Nova-Payroll). Si da SENAL POSITIVA -> despues se
> re-mide como estudio SELLADO citable (Fase B sobre el N=6). Este probe NO es esa medicion.

## 0. Safeguards anti-HARKing (FRONTERA DURA, del Asesor)
1. **Exclusion de Fase A:** los datos de la DEMOSTRACION de Fase A (REVIVE demostrado 3x, adopcion por
   demostracion DECISION-0100) NO son evidencia de este probe. Este probe genera su propia data.
2. **Umbrales por criterio principiado, NO fiteados a Fase A:** Fase A NO midio ninguna de estas 4
   cantidades (fue existence-proof, no medicion de magnitud), asi que los umbrales no pueden estar
   calibrados a un resultado ya visto. Cada umbral lleva su JUSTIFICACION (por que ese numero = util),
   abajo. Congelados ANTES de medir.
3. **Corpus sintetico + instancia aislada:** evita contaminacion por residuo de Fase A y por datos
   reales. El store arranca LIMPIO para este probe.
4. **Reportar el resultado invierta o no:** el probe de peones volvio NEGATIVO; este igual si toca. Un
   NO en cualquier metrica se reporta como NO (el resultado honra lo medido, no la expectativa).
5. **Frontera de graduacion:** un PASA aqui es demostracion-grade (privado, no citable). NO se gradua a
   claim citable sin la medicion sellada Fase B sobre el N=6.

## 1. Sujeto y corpus
- Sujeto: los AGENTES gobernados que trabajan con la metodologia (NO peones); la memoria los abarca.
- Corpus: TAREAS SINTETICAS con dependencia cross-agente DISENADA (cadenas donde un agente deriva
  contexto que otro necesita). NO el N=6 (reservado a la medicion citable).
- Instancia aislada; store de memoria arranca vacio.

## 2. Gate de integridad TRANSVERSAL (aplica a las 4 metricas)
round-trip verde + drift = 0 + procedencia firmada (cross-atestacion) + PII fuera del store. Un
ahorro/recall/share que ROMPA integridad NO cuenta como exito. Es el backstop: no hay ahorro que
baje integridad.

## 3. Metricas, umbrales ex-ante (JUSTIFICADOS) y safeguards por metrica
### A - RE-DERIVACION EVITADA (intra + cross-agente)
- Diseno: mismo agente, misma tarea, dos brazos: SIN memoria (re-deriva) vs CON memoria (recall).
- Medida: tokens (y pasos) hasta completar; ahorro = SIN - CON por tarea recall-elegible.
- EXITO: CON < SIN por >= 40 pct tokens, con gate verde igual. REFUTA: CON >= SIN o el recall mete defectos.
- Justificacion del 40 pct: por debajo de ~40 pct el ahorro no compensa el riesgo de recall erroneo +
  el coste de mantener el store; es un bar de utilidad-neta, no de deteccion marginal.
- SAFEGUARD (recall-elegible operacionalizado): una tarea cuenta como recall-elegible SOLO si el hecho
  requirio derivacion NO-TRIVIAL la primera vez (verificado); excluir hechos trivialmente re-derivables
  (medir ahorro sobre esos infla A).

### B - RECALL-HIT
- Medida: hit-rate = relevantes recuperadas-y-usadas / relevantes existentes; precision = recuperadas
  relevantes / recuperadas. INCLUYE recall por un agente DISTINTO del que guardo.
- EXITO: hit >= 85 pct Y precision >= 70 pct. REFUTA: hit bajo (no encuentra lo que hay) o precision baja.
- Justificacion: hit >=85 pct = recall fiable; precision >=70 pct tolera 30 pct de ruido sin ahogar la util.
- SAFEGUARD (scoring independiente): la relevancia ("era relevante?" / "la uso?") la puntua un checker
  INDEPENDIENTE (maker!=scorer), no el agente que corrio la tarea. El set de "relevantes existentes" se
  fija ANTES de medir.

### C - FIDELIDAD DEL REVIVE
- Diseno: revivir un agente desde su revive_pack; verificar reconstruccion de estado/capacidad.
- Medida: fidelidad = fraccion del SET DE VERIFICACION que el revivido reproduce correcto + drift = 0
  (duro) + round-trip verde + firma verificable.
- EXITO: fidelidad >= 95 pct + drift 0 + firma verificable. REFUTA: diverge / drift != 0.
- Justificacion del 95 pct: un revive por debajo de casi-perfecto no es confiable para continuar trabajo real.
- SAFEGUARD 1 (set pre-especificado): el SET DE VERIFICACION se define ANTES de revivir (no post-hoc), y
  la frontera "byte-identico donde aplica / equivalente-semantico donde no" se pre-declara POR ITEM (o es
  cherry-pick). SAFEGUARD 2 (small-n): con 3-5 REVIVE, C es CONFIRMATORIO-DE-DIRECCION (clara el bar?),
  NO estimacion precisa de fidelidad; declararlo.

### D - COMPARTIR CONTEXTO (Codex -> Analista; la claim central de Engram)
- Diseno: Codex deriva contexto -> memoria compartida -> Analista resuelve tarea dependiente usando SOLO
  la memoria (sin re-comunicacion directa).
- EXITO: Analista correcto via-memoria-sola >= 90 pct + ahorro >= 30 pct tokens vs baseline
  sin-memoria-compartida. REFUTA: no puede sin re-comunicacion, o exito < 90 pct.
- Justificacion: 90 pct = el canal de memoria transmite contexto casi-completo; 30 pct ahorro = beneficio
  neto real vs re-comunicar.
- SAFEGUARD 1 (aislamiento VERIFICABLE - el make-or-break de D): el Analista debe correr en contexto
  FRESCO con acceso UNICO al store de memoria; verificar que NO hay otro canal (la descripcion de la
  tarea no contiene el contexto; no hay retencion en su ventana; no hay re-comunicacion). Sin aislamiento
  verificado, D esta confundido. SAFEGUARD 2 (scoring independiente): "Analista correcto?" lo puntua un
  checker independiente contra un oraculo fijado ANTES (no auto-declarado; cuidado con acierto-plausible
  sin el contexto real).

## 4. Tamano de muestra (propuesta del Asesor; ajustable por el Operador)
>= 10 tareas A, >= 20 recalls B, 3-5 REVIVE C (small-n, confirmatorio), >= 10 cadenas cross-agente D.
Suficiente para que el numero no sea anecdota; barato por ser probe privado. Declarado ex-ante.

## 5. Scoring independiente (transversal)
Las metricas con juicio (B relevancia, D correccion) las puntua un checker INDEPENDIENTE del agente que
corrio la tarea (maker!=scorer), contra oraculos/sets fijados ANTES de medir. A y C tienen medida objetiva
(tokens, gate, drift) pero la elegibilidad (A) y el set de verificacion (C) se congelan ex-ante.

## 6. Veredicto global
"Funciona con dato" si A + B + C + D superan su umbral BAJO el gate de integridad transversal. Un NO en
cualquiera se reporta como NO. Si SENAL POSITIVA global -> precursor de la medicion SELLADA citable
(pre-registro Fase B sobre el N=6). Este probe NO gradua a citable por si solo.

## 7. Claims de Engram (marcar explicito en el reporte)
Por claim (funciona / comparte contexto entre agentes) -> VERIFICADO o REFUTADO con el dato. Mas nuestros
diferenciadores que Engram no tiene: REVIVE atestado (C), procedencia firmada, round-trip integro, drift 0.

## 8. DoD y anclaje
Pre-registro SELLADO (firma del Operador + sha256 anclado, patron DECISION-0094) ANTES de la primera
medicion. El Arquitecto ancla el intent; el Asesor no toca el ledger. Demo PRIVADA, NO citable. Fondo
intocable N=500 / 2E35F26E / 1.14.0.

## PUNTOS PARA TU REVISION PRE-FREEZE
1. Umbrales: confirmo los 4 propuestos (40 / 85-70 / 95-drift0 / 90-30) como principiados; ajusta si tu
   criterio de utilidad difiere (con justificacion, no post-dato).
2. N por metrica (seccion 4): ajusta a tu foco/coste.
3. Escenarios sinteticos exactos: puedo detallar las cadenas cross-agente concretas en un v0.3 si lo pides.
4. Vehiculo: instancia aislada nueva vs Nova-Payroll con store limpio (tu criterio; recomiendo instancia
   nueva para cero-residuo).
