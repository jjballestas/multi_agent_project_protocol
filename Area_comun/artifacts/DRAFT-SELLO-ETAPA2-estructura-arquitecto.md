# DRAFT - Estructura del SELLO ETAPA 2 (gobernada por el Arquitecto, lista para llenar + sellar)

> PREP autonoma 2026-07-07 (cola del operador, item 5). Estructura ARQUITECTO-GOBERNADA del sello Etapa 2:
> consolida los items REDACTABLES (no dependientes de la reconciliacion 26-29-jul ni de las DEC de dominio
> P3.x) y deja los dependientes como placeholders explicitos `[LLENAR-AL-SELLAR-E2 / BLOQUEADO: <input>]`.
> **NO SELLA** (no hay submit_intent/atestacion aqui): sellar exige (a) reconciliacion 26-29 cerrada, (b)
> DEC dominio P3.x cerradas, (c) aprobacion + firma del Operador. Insumos gobernados: DRAFT F3.2 del Asesor
> (personal/asesor/DRAFT-F3.2-...; el Arquitecto lo gobierna e incorpora, s.3 del propio draft),
> NOTA-DISENO peones (Area_comun/artifacts/NOTA-DISENO-peones-vs-tokens-sello-etapa2.md, Arquitecto), y el
> SELLO ETAPA 1 (DECISION-0091, atestado). NO toca el estudio medido, el genesis del hub, ni los resultados
> de Q4 (post-30-jul). Frontera de dominio neutral respetada: nada de esto entra al nucleo del protocolo.

## 0. Que SELLA Etapa 2 y que NO (marco, REDACTABLE)
- **SELLA (congela plan + reglas, no datos causales):** (a) la ARITMETICA del backlog reconciliada de la
  ventana baseline 3-25 jul + el pool Q4 comprometido al Sprint 1; (b) las reglas de CONDICIONALIDAD de Q4
  (pre-declaradas en Etapa 1, consolidadas aqui); (c) la REGLA DE ADOPCION (transferibilidad + migracion a
  la instancia Aegis, DECISION-0088); (d) el DISENO pre-registrado del contraste peones (Q-PEON) y su regla
  de apertura por completitud certificada; (e) el ROSTER de participantes (composicion del equipo).
- **NO SELLA (por calendario):** los RESULTADOS de Q4 (ejecuta post-30-jul, contemporaneo). Etapa 2 (<=29-jul)
  es ANTES de que abra el Sprint 1 (30-jul). Anti-sobreventa: Etapa 2 no afirma nada de Q4 todavia.

## 1. Aritmetica del backlog -- [BLOQUEADO: reconciliacion 26-29-jul, Analista read-only, s.10 Etapa 1]
- Marco REDACTABLE (fijo ahora): toda tarea de producto de la ventana debe tener fila en el journal v1.0;
  la reconciliacion mapea cada commit/rama/log de Nova-Budget contra `tarea_id`; sesiones sin fila =
  `abandonada` retro; huerfanos se PUBLICAN como metrica de integridad del estudio. GOAL-P1 (fundacion,
  sha256 d2a13216) EXCLUIDO del contraste (scaffolding sin dominio).
- Campos dependientes: `[LLENAR-AL-SELLAR-E2 / BLOQUEADO reconciliacion]` N_baseline_filas,
  N_abandonadas_retro, N_huerfanos_publicados, tokens_total del brazo baseline, defectos_post clase(b)
  paridad-true observados al corte.

## 2. Condicionalidad de Q4 + FRASE DE PODER EFECTIVO (REDACTABLE -- se sella ahora)
- **Sorteo ya sellado (Etapa 1 s.6, NO se re-sortea):** semilla NIST 1844242; `h=SHA-256(tarea_id+"|"+semilla)`,
  `h[0] mod 2`, por-unidad. Resultado: completo = NB-BRC3-4, NB-P2-3 (2/10); ligero = las otras 8. Por
  estrato: S (n=4) 1/3; M (n=6) 1/5 (desbalance 5-1 por azar, reportado sin corregir).
- **Frase de poder efectivo (se SELLA, redactable):** Q4 = evidencia causal DEBIL (cota, no puntual; ITT
  sobre <=2 completos y un cluster correlacionado). Tres degradaciones ACUMULATIVAS pre-selladas: (1) brazo
  completo delgado (2/10); (2) n efectivo < nominal (cluster BR-C3: 4 Get_*_List casi isomorfas = misma
  forma probada 4 veces; intra-cluster solo NB-BRC3-4 completo -> 1-vs-3); (3) dependiente de ejecucion (si
  Sprint 1 no ejecuta >=10, Q4 se reporta SUBPOTENCIADO, NO se rellena). NO invalida el estudio: Q1/Q2 son
  las confirmatorias fuertes; Q4 aporta direccion causal con incertidumbre declarada; el veredicto de compra
  se DIFIERE a la replica employee-run.
- **Doble rol Get_*_List (NO doble-conteo, redactable):** el cluster BR-C3 es miembro gobernado de PAR-D
  (Q3 descriptivo/cota) Y fabrica en Q4 (causal); contrastes pre-registrados DISTINTOS; su fase SPEC se
  excluye del delta (simetria con spec_prepagado de P2.2).
- Campo dependiente: `[LLENAR-AL-SELLAR-E2 / post-30-jul]` n realmente ejecutado en Sprint 1.

## 3. Regla de adopcion -- transferibilidad + migracion a Aegis (REDACTABLE -- se sella ahora)
- **Criterio de "adoptado" (sellable ahora):** una segunda instancia de dominio real (Nova-Budget) adopta
  cuando, verificable: (1) corre el PATRON BASELINE CONGELADO (P4.1 pattern-setter: aprobacion-via-proc +
  gateway tipado + saldo-de-vista) + maker!=checker DURO + gates atestados; (2) su governance operativa vive
  en su instancia `Aegis/` (DECISION-0085/0088), NO en el hub; (3) el hub registra la CROSS-ATESTACION (el
  journal del hub guarda el sha256 de la atestacion de Aegis por gate, regla dual DECISION-0088).
- **La migracion ES la evidencia (Q5):** HOY (hasta 30-jul) asiento = HUB (el brazo gobernado es el
  tratamiento medido; su atestacion en el MISMO #4). POST-sello migra a NOVA/Aegis; meta/estudio/metodologia
  canonica = hub SIEMPRE. Esa migracion pre-registrada ES la replica employee-run de Q5 (segunda instancia
  dominio real vs N=500 auto-dogfood). Etapa 2 sella el CRITERIO; la ejecucion es Carril B / post-sello.
- **Delimitacion (anti-sobreventa, se sella):** AFIRMA transferibilidad de la MAQUINARIA (instancia distinta,
  dominio real, protocolo con atestacion cruzada verificable). NO AFIRMA que el gobierno mejora la calidad
  (Q4 subpotenciado + maker!=checker ya en ambos brazos). El tratamiento medido es el checker FORMAL
  atestado + la maquinaria, no "separar maker de checker".

## 4. Contraste peones Q-PEON (REDACTABLE -- diseno pre-registrable, de la NOTA-DISENO del Arquitecto)
- **Pregunta:** bajo gobierno COMPLETO (mismo gate adversarial, SLA, aparato de medicion), delegar el
  drafting mecanico a peones (modelos no-frontera, keyless, fuera del ledger como makers-borrador) REDUCE
  `tokens_total_atribuibles` por unidad equivalente SIN degradar calidad (D1-D4 y reworks estables)?
- **Brazos:** A = mono-orquestado gobernado (identico a Etapa 1); B = peones bajo gobierno completo (peon
  draftea, firmante frontera revisa/firma; maker!=checker preservado; el peon JAMAS firma ledger).
- **Metrica:** primaria `tokens_total_atribuibles` (moneda confirmatoria ya probada) con cubetas Q1
  (regimen/arranque/overhead via `tag_incidente_maquinaria`); guardia no-inferioridad D1-D4 + `reworks_n`.
  Schema v1.0 ya incluye los 5 campos de peones (instrumentado desde F3.3; sin aparato nuevo).
- **Atribucion de tokens del peon (regla dura):** los tokens del peon van a sus 5 campos propios y JAMAS se
  restan de `tokens_total_atribuibles` del firmante; el ahorro se lee comparando el costo frontera entre
  brazos, no editando la moneda.
- **Apertura por completitud certificada (regla estructural sellada):** el contraste peones NO abre hasta
  certificacion READ-ONLY (tercero != maker) de (a) reconciliacion Etapa 1 completa, (b) analisis de
  Contabilidad con unidades enumerables, (c) sello Etapa 2 firmado. NUNCA por fecha. (Corrige el tiempo
  muerto endogeno de las ventanas por-fecha de Etapa 1.)
- **Tratamiento declarado (simetria):** la memoria hibrida forma parte del tratamiento de AMBOS brazos si su
  DECISION esta aprobada antes del sello E2; si no llega, corre sin ella EN AMBOS (nunca un brazo con
  memoria y otro sin). [ACTUALIZACION 2026-07-14: la DIRECTIVA del probe (answered/MSG-20260714-...-probe-
  memoria-hibrida) confirma que la memoria NO entra al tratamiento de E2: el probe corre AISLADO en
  Nova-Payroll, fuera de las instancias medidas -> ambos brazos SIN memoria, como preve esta regla.]
  Poblacion (unidades de Contabilidad): **DESBLOQUEADA 2026-07-14** -- corpus enumerable ENTREGADO por la
  instancia NOVA (commit NOVA `35a1b4e`, `docs/design-source-contabilidad/corpus-contabilidad-enumerable.md`,
  derivado del WS1 del hito 11-jul): **35 unidades CONT-U01..U35**, cada una con id estable + objeto
  Accounting.* + slice + form legacy + alcance 1-frase + verificacion de paridad FALSABLE (set real de THROW
  contra OBJECT_DEFINITION identico en 3 BD + negativo alcanzable + smoke con ROLLBACK, patron F-NOVA-01) +
  ancla de falsabilidad por unidad. `[LLENAR-AL-SELLAR-E2]` la seleccion final de poblacion del brazo B.
- Traza: TASK-0231 (F6.1) queda `proposed` en el hub, re-alcanzada a este contraste; no se activa antes del
  sello E2 (DIRECTIVA 30a4252 s.4). Diseno/pre-registro = capa ESTUDIO -> HUB; ejecucion brazo B sobre
  Contabilidad -> Aegis.

## 5. Roster de participantes (REDACTABLE -- estructura; nombres al sellar)
- Requisito estructural (addendum onboarding-remoto): el sello E2 DEBE NOMBRAR, antes de sellar, a los
  participantes, sus maquinas/clones y roles (maker/checker por unidad). Un segundo humano operando
  Contabilidad (empleado remoto) es VARIABLE del estudio; la composicion se pre-registra, no se descubre a
  mitad de ventana (a mitad seria enmienda).
- Plantilla por participante (llenar al sellar): `{id, identidad_firmante (propia|bajo-identidad-existente,
  ver bifurcacion runbook s.8.4), maquina/huso, reparto maker!=checker (separado FISICAMENTE por posesion de
  llave)}`. Participantes conocidos hoy: Arquitecto, Codex, Analista; Julian (DBA/empleado remoto):
  **DESBLOQUEADO 2026-07-14** -- onboarding COMPLETO y gate nominal 2-clones CERRADO con su firma
  (jheredia:v1 maker + done-flip; analista:v1 checker one-shot; cross-atest Entrada 2 del hub, commit
  `ffd2faa`; privada solo en su maquina). `[LLENAR-AL-SELLAR-E2]` maker/checker por unidad + cualquier
  participante adicional.

## 6. Condiciones de pertenencia del pool -- **DESBLOQUEADO 2026-07-14 (n=10 CONFIRMADO)**
> [ACTUALIZACION 2026-07-14 ~14:20: las DOS condiciones de esta seccion estan CUMPLIDAS.]
> (a) **BR-C4 = ENTREGADA Y DOBLEMENTE VERIFICADA -> n=10 CONFIRMADO.** Cadena completa: paquete P3.x
> resuelto por el Operador el 6-jul (opcion b) -> sembrado del DBA + verificacion EN VIVO del Arquitecto
> (enmienda s.27 del sello E1, 2026-07-06: 6/6 guardas, THROW 50320-50324, matriz 9x9 1:1 por celda) ->
> re-verificacion GOBERNADA Y FIRMADA en la instancia NOVA (enmienda s.28, 2026-07-14: TASK-9392 done,
> maker jheredia:v1 + checker one-shot analista:v1, smoke 30 casos 0 fallos + control negativo, drift 0;
> commits NOVA 8fd7e75..b984cd4). Hallazgo MENOR de s.27 (identidad cross-doc viva) sigue abierto, no
> bloquea (estructura 1:1 lo cubre). P3.2/P3.3/P3.4 CONSERVAN elegibilidad Q4.
> (b) **Hardening 15-jul (PAR-2/Annul_*) = SI, entregado ADELANTADO** (FYI de la instancia NOVA
> 2026-07-14: PAR-2 parity preflighted + los tres Budget.Annul_* existentes y guardados con
> Assert_Permission, verificado en vivo contra el sandbox; caveat declarado: procs viven en la BD, solo
> CDP-annul cableado en C#; commit de consolidacion a2333dc/TASK-0254).
> **=> El UNICO bloqueo restante del sello E2 es s.1 (reconciliacion 26-29-jul).**
- Marco REDACTABLE: pool Q4 nominal n>=10 (Etapa 1 s.5). Composicion por ESTIMATE: estrato M (n=6): NB-P2-3,
  NB-P3-2, NB-P3-3, NB-P3-4, NB-P4-4, NB-P6-3; estrato S (n=4): NB-BRC3-1..4 (cluster Get_*_List). P3.1 NO
  pertenece (pattern-setter, excluida del contraste central).
- Condiciones dependientes: `[LLENAR-AL-SELLAR-E2 / BLOQUEADO P3.x]` confirmar que la DEC de dominio de
  P3.2/P3.3/P3.4 esta CERRADA al 29-jul (si no, CAEN del pool y n baja -- subpotenciacion previsible ya
  declarada en s.2); items dependientes de hardening (PAR-2/Annul_*) entran SOLO por enmienda fechada con
  entrega comprometida (registrar si el hardening del 15-jul entrego los procs).
- **PRE-CHEQUEO 2026-07-14 ~19:45 (informativo, NO sustituye el chequeo del corte): VERDE.** (1) Scan de
  marcadores abiertos en SPEC-NOVA-P3-002/003/004 con word-boundary = 0 coincidencias (el patron SIN
  boundary da 3 falsos positivos por la palabra "independientemente" -- documentado para que el chequeo
  del corte no se asuste con ellos); (2) TASK-9392 (BR-C4) = `done` en el TASK_INDEX de NOVA (lectura
  read-only, origin fdeb99d). **Comando PRE-DECLARADO para el chequeo VINCULANTE al corte (29-jul),
  mismo criterio, ejecutar y pegar salida aqui:**
  `grep -rniE "\b(PENDIENTE|TBD|por resolver|decidir)\b" Area_comun/specs/nova/SPEC-NOVA-P3-002* Area_comun/specs/nova/SPEC-NOVA-P3-003* Area_comun/specs/nova/SPEC-NOVA-P3-004*`
  (esperado: 0 lineas) + status de TASK-9392 en el TASK_INDEX de NOVA (esperado: `done`). Un verde hoy
  NO liga el 29: la asercion del sello se fecha AL CORTE (disciplina de pre-registro); este pre-chequeo
  solo mecaniza el paso (2 min) y registra la linea-base.

## 7. Anexo de riesgos (REDACTABLE -- de la NOTA-DISENO)
1. Confusion arranque/regimen (peones agregan overhead propio) -> separar con cubetas Q1; degradacion
   ex-ante si el runtime no permite el desglose.
2. Curva de aprendizaje asimetrica (brazo B estrena tooling) -> primeras unidades como teething tagueado
   (`tag_incidente_maquinaria=arranque`), igual que el baseline.
3. Fuga de trabajo entre brazos -> el peon no toca unidades del brazo A; aislamiento de par con verificacion
   mecanica.
4. Atribucion de tokens del peon -> ver s.4 (campos propios, nunca restar de la moneda del firmante).

## 8. Plan de atestacion (REDACTABLE el plan; la EJECUCION es al sellar)
- Al sellar: `submit_intent` (intent `decision`) del sha256 del doc Etapa 2 final + manifiesto -> #4 (mismo
  patron que Etapa 1, DECISION-0091 seq 3831). El sello lo ejecuta el ARQUITECTO (submit_intent); el Asesor
  no toca el ledger; la reconciliacion empirica es del Analista read-only.
- Precondiciones de sellado (checklist de cierre): [ ] s.1 reconciliacion incorporada; [ ] s.6 condiciones
  P3.x cerradas; [x] s.2 frase de poder efectivo; [x] s.3 criterio de adopcion + regla dual; [x] s.4 diseno
  peones + apertura por completitud; [x] s.5 estructura de roster (nombres pendientes de Julian); [x] s.7
  anexo de riesgos; [ ] aprobacion + firma del Operador.

## 9. Frontera (recordatorio duro)
Nada aqui toca el estudio medido, el genesis del hub, la config pineada (2E35F26E, epoch 1.14.0), ni los
resultados de Q4 (post-30-jul). Esto es ESTRUCTURA/redaccion pre-registrable, no ejecucion. El BUILD
gobernado de Contabilidad y la apertura del contraste peones esperan DOS inputs del Operador: (a) Julian
onboardeado (pubkey + gate 2-clones), (b) la base de BD de Contabilidad (DBA). Tras esta PREP, el desarrollo
de producto entra en PAUSA NATURAL hasta esos inputs. El Asesor coordina el sello.
