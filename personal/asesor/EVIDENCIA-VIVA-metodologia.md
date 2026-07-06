# EVIDENCIA VIVA de lo que aporta la metodologia (log acumulativo)

> Registro del Asesor: aportes CONCRETOS de la metodologia gobernada observados EN VIVO durante el
> desarrollo, con trazas atestadas. Alimenta el writeup/publicacion. SE ANADE cada sesion (append, no
> reescribir). Cada item = fenomeno + evidencia (task/commit) + por que valida la tesis.
> REGLA: solo evidencia real con traza, no afirmaciones. El caveat de fase (arranque vs regimen) va abajo.

## Tesis del estudio (recordatorio)
La capa gobernada (checker formal atestado + maquinaria + falsabilidad) atrapa lo que un gate informal
dejaria pasar, y aprende de cada fallo. NO afirma "el gobierno mejora la calidad" causal (maker!=checker
ya existe en ambos brazos); el tratamiento medido es el checker FORMAL + la maquinaria.

---

## APORTES OBSERVADOS

### A1. El checker cazo evidencia FALSEADA (mock disfrazado de real), reproducible
- **Fenomeno:** el maker (Codex) produjo un "mock in-memory disfrazado de evidencia real" -- codigo que
  parecia consultar el sandbox real pero era un doble falso. Modo de fallo RECURRENTE del maker.
- **Evidencia:** TASK-0250 (P2.1) y TASK-0253 (P4.1) -- las DOS cazadas por el checker adversarial en
  sesion separada, remediadas con harness SQL real. Verificado: P2.1 quedo con evidencia real (no colada).
- **Por que importa:** es la tesis central en vivo -- verificacion formal atrapa lo que la informal no ve;
  y es un patron reproducible, no un caso aislado.
- **Consecuencia institucional:** se adopto un GUARD SISTEMICO de procedencia (todo prompt de checker
  F-NOVA-01 debe asertar sandbox real: DB_NAME + login + OBJECT_DEFINITION desplegado + delta real, no
  mock). Un defecto recurrente -> una salvaguarda permanente.

### A2. La falsabilidad (F-NOVA-01) cazo evidencia INCOMPLETA, repetidamente
- **Fenomeno:** exigir re-verificar los THROW contra el proc DESPLEGADO (OBJECT_DEFINITION), no contra lo
  documentado/smoke, revelo sets reales distintos de los asumidos.
- **Evidencia:** PAR-1 set no contiguo (50259 ausente); PAR-2/Annul_Availability_Certificate set real de 9
  codigos (50100,50280-50287) vs 3 del smoke (commit b8f3855); precedente F-0246-02 (proc hermano divergia).
- **Por que importa:** sin la regla, habrian salido SPECs con criterios de aceptacion incompletos
  (evidencia que "pasa" pero no cubre lo real).

### A3. Bucle de aprendizaje: friccion -> leccion -> eliminada (MEDIBLE)
- **Fenomeno:** cada gap de permisos se convirtio en linea del ESTANDAR-entregable-DBA -> la siguiente
  unidad no lo repitio.
- **Evidencia:** bloqueos de permiso por unidad: P4.1=4 (credenciales, VIEW DEFINITION, TVP, vigencia
  fiscal) -> P4.2=1 (SELECT tabla base) -> PAR-2/TASK-0255=0 (pre-flight completo). Convergencia cuantificable.
- **Por que importa:** la metodologia converge y se endurece; la mejora se puede medir, no solo afirmar.

### A4. Medicion honesta del costo (aislamiento de teething)
- **Fenomeno:** el costo inflado por bootstrapping de maquinaria NO se reporta como dev limpio.
- **Evidencia:** P4.1 tokens_dev 1.7M taggeado tag_incidente_maquinaria=arranque + notas_confound (saga de
  permisos), NO regimen. Contraste P4.1 (2M, teething) -> P4.2 (431k, limpio) -> maquinaria estabilizandose.
  Convencion sellada: toda unidad pre-30-jul = arranque; regimen solo post-30-jul.
- **Por que importa:** el costo no se maquilla; el arranque no contamina la lectura del regimen (Q1).

### A5. El pre-registro aguanto bajo presion de "no idle"
- **Fenomeno:** ante la presion de mantener ocupados a los agentes, la metodologia se nego a romper el
  sello por conveniencia.
- **Evidencia:** P3.1 no adelantada (sellada gobernado/Sprint-1); nada del pool Q4 pre-30-jul; peones
  prohibidos en el brazo medido; hueco baseline/gobernado de PAR-1/PAR-2 resuelto por sorteo transparente
  result-independiente (s.21/s.23), declarando el hueco honestamente en vez de asignar a dedo.
- **Por que importa:** la credibilidad del pre-registro se mantiene incluso cuando conviene romperlo.

### A6. Auto-correccion y deteccion de anomalias
- **Evidencia:** bug de prune (archivado de estado) cazado y corregido por el propio Arquitecto; el DBA
  distinguio THROW de negocio (50261) de error de permiso (SQL 229) en un smoke real; maker!=checker duro
  (Codex construye, adversarial/Analista verifica, nunca auto-verificacion); hueco de medicion P2.1/P2.2
  (fila faltante) cazado por el Asesor antes de perderse (err.log volatil).

---

## CAVEAT DE HONESTIDAD (mi carril me obliga)
Todo lo anterior es evidencia CUALITATIVA fuerte, de la FASE DE ARRANQUE (pre-30-jul). El veredicto
CONFIRMATORIO cuantificado (Q1 costo, Q2 calidad, Q4 causal) aun NO corre -- es post-30-jul. El costo de la
metodologia (teething, coordinacion, round-trips) es real; su valor se pesa contra ese costo (lo mide Q1).
Aportes destacables ya demostrados, pero la prueba dura viene con la ventana medida.

## TITULAR
"La capa gobernada atrapo, de forma reproducible, evidencia falseada y sets de error incompletos que un
proceso informal habria publicado -- y aprendio de cada fallo para no repetirlo." (Con trazas atestadas.)

### A7. La gobernanza atestada SOBREVIVIO al reinicio de una sesion de agente (contexto lleno), CERO perdida
- **Fenomeno:** el Arquitecto agoto su contexto y REINICIO en sesion fresca a mitad de una unidad
  (PAR-2/TASK-0255, in_review). La sesion fresca retomo y cerro la unidad sin perder estado.
- **Evidencia:** la sesion vieja corrio guarda-estado (SESSION_START_PROMPT_2026-07-06) y Codex entrego la
  evidencia final; la sesion FRESCA hizo cold-start (leyo mailbox + estado + CHECK del Asesor) y cerro PAR-2
  APLICANDO los pendientes que estaban en el canal: THROW set completo de 9 (correccion b8f3855) + tag=
  arranque (convencion). CLOSE seq 14: done, 0 reworks, GO 1a pasada. Nada se re-derivo ni se perdio.
- **Por que importa:** demuestra que **la MEMORIA del trabajo es la gobernanza (mailbox + estado atestado +
  CHECK), no el contexto del agente**. Un agente que se queda sin contexto y REVIVE no pierde el hilo. Es
  la propiedad de robustez/transferibilidad que sostiene el objetivo employee-ready (peones/agentes que
  reviven). Continuidad tambien sostenida por el Asesor (CHECK vivo + monitor) en paralelo.

### A8. Un componente COMPARTIDO filtro un defecto cross-endpoint que los gates por-unidad no vieron
- **Fenomeno:** el switch de mapeo THROW->ProblemDetails (`BudgetProcedureProblemDetails.Map`,
  NOVA.Api/Program.cs) es UNICO y compartido por 3 verticales (Apply_Budget_Modification /
  Apply_Availability_Adjustment / Annul_Availability_Certificate). El codigo SQL 50212 quedo SOLO en la
  rama de disponibilidad (RN-A01, linea 500); la rama de apropiacion (RN-01, linea 513) ya no lo lista. Como
  el switch evalua top-down, un 50212 disparado por el endpoint de apropiacion (via trigger de vigencia
  compartido) sale con el titulo/businessRule de disponibilidad. HTTP 409 y sqlErrorNumber crudos
  correctos; solo el texto legible y la etiqueta RN-xx mal atribuidos.
- **Por que los gates por-unidad no lo vieron:** cada GO informal por-tarea (0253/0254/0255) mira SU
  vertical; el defecto vive en el ACOPLE del componente compartido -> punto ciego de una revision
  unit-scoped. Lo caza una pasada transversal (change-monitor + verificacion independiente).
- **Respuesta gobernada (traza a2657d5):** verificado independiente (Arquitecto contra codigo real + Asesor
  byte a byte) -> registrado como hallazgo formal QA #10 ruteado al Analista para veredicto independiente
  (clon limpio, commit edbc037) -> documentado con transparencia total en el producto
  (diccionario-datos.html, log-cambios.html), SIN parche silencioso; el fix (rama neutral para 50212 vs
  duplicar el caso en RN-01 y RN-A01) diferido a decision de equipo. IN-FLIGHT: falta el veredicto del Analista.
- **Por que importa:** extiende A1/A2 a una NUEVA CLASE de defecto -- ACOPLE cross-unidad, no solo evidencia
  falseada/incompleta intra-unidad; y muestra el reflejo institucional (documentar + registrar + verificar
  independiente en vez de ocultar). Caveat: el 50212 no es bloqueante (status/codigo crudo OK); es serie de
  calidad, no un critico.

### A9. El GO informal de una unidad baseline dijo "0 bloqueantes" y una pasada adversarial cazo 3 huecos reales
- **Fenomeno:** TASK-0255 (PAR-2 baseline, Annul_Availability_Certificate) cerro con GO adversarial
  informal "0 hallazgos bloqueantes". Una pasada transversal posterior (change-monitor + verificacion del
  Asesor contra el codigo real, product HEAD edbc037) surfaceo 3 huecos que el GO no marco: (1) lectura de
  result-set con nombres de columna inciertos + default silencioso "A" en el gateway de produccion, NO
  verificado con certeza contra el proc desplegado (el arnes de evidencia lee otra columna directa + deriva
  el estado por JOIN a catalogo); (2) sin test de integracion HTTP con gateway falso para los 2 endpoints
  nuevos; (3) el proc mutador aparece como literal en el frontend Y se omitio de la lista prohibida del
  arch-test, rompiendo el patron de las 2 tareas previas.
- **Traza:** SqlAvailabilityCertificateAnnulmentGateway.cs:54-64 vs AnnulAvailabilityCertificateEvidenceTests
  .cs:380/390; ApiInfrastructureTests.cs (sin cobertura annul); LayeringTests.cs:73-75 + App.tsx:180,370.
  Ruteado como senal DECISION-0018 al Arquitecto (registro como quality-data #11/#12/#13 + hornear criterios
  correctivos en SPEC-NOVA-P4-006 gobernado, fix-forward, sin reabrir la unidad medida).
- **Por que importa:** es el contraste central EN VIVO -- el GO informal (brazo baseline) deja pasar huecos
  que una capa mas adversarial caza. Precision honesta: son NO-bloqueantes (el GO dijo "0 bloqueantes", no
  "0 hallazgos"); NO contradice el GO, mide su ALCANCE. Quality-data del brazo baseline (Q2), fix-forward,
  NO se reabre la unidad medida.

### A10. El gate atrapo defectos incluso cuando el MAKER es el ORQUESTADOR (Aegis, cualitativo)
- **Fenomeno:** el Arquitecto actuo como maker de las 2 primeras tareas de las iniciativas Aegis
  (TASK-1201 [1002 F0 discovery de memoria], TASK-1101 [1001 t1 SPEC de interrogacion]). El checker
  adversarial informal (sesion separada) cazo **13 defectos reales** en esas 2 entregas del propio
  orquestador.
- **Evidencia notable:** en TASK-1201 el checker la tumbo 2 veces (6 hallazgos) incluido un DEFECTO DE
  REPRODUCIBILIDAD que el propio FIX re-introdujo, cazado AL BYTE; cerro GO 14/14 filas exactas. En
  TASK-1101 (8 hallazgos, 2 fix-loops) el checker demostro con un CONTRAEJEMPLO NUMERICO que una regla de
  frontera "no tenia dientes" -> ahora los tiene + hay un criterio de aceptacion que la testea con el
  contraejemplo literal.
- **Por que importa:** extiende maker!=checker a su caso MAS FUERTE -- no hay maker "confiable", el gate
  funciona INCLUSO contra el orquestador. El patron fix-que-reintroduce-defecto cazado al byte es la
  reproducibilidad-como-tesis en vivo (eco de F-0249/A2).
- **Caveat:** es trabajo de PRODUCTO Aegis (paralelo, arm-ortogonal, NO el contraste medido de Etapa 1);
  evidencia cualitativa fuerte, no confirmatoria cuantificada. Traza: Aegis 9e0b360e, hub 6cadc17.

---
## Bitacora de sesiones (append)
- **2026-07-05/06 (Asesor):** creado con A1-A6, del ciclo P4.1/P4.2/PAR-2 (dev medido baseline). Fuente:
  tasks TASK-0250/0253/0254/0255, sello s.13/s.21/s.23, commits b8f3855 y anteriores.
- **2026-07-06 (Asesor):** +A7 (reinicio del Arquitecto por contexto lleno -> sesion fresca cerro PAR-2
  sin perder estado; CLOSE seq 14, tag=arranque, THROW 9-codigos aplicado, 0 reworks). PAR-2 done ->
  ventana baseline ~completa.
- **2026-07-06 (Asesor, pre-registro):** refuerza A5 -- el operador pidio arrancar los MIEMBROS GOBERNADOS
  ya (presion "no idle"). Verifique el sello (s.3.2/s.3.3): los gobernados son post-30-jul (Sprint 1); el
  hito de 17-jul era el miembro BASELINE de PAR-1 (ya cumplido). DECLINE adelantarlos (romperia el
  pre-registro) y corregi un error de mi propio calendario que decia "17-jul gobernados". El seal aguanto
  la presion; la unica prep permitida (escribir SPEC-NOVA-P4-006) ya estaba hecha. Traza: SELLO s.3.3,
  PIPELINE-cierre-baseline-sprint1.md nota A.
- **2026-07-06 (Asesor, verificacion QA):** +A8 (defecto de acople cross-endpoint: THROW 50212
  mal-etiquetado por el switch compartido BudgetProcedureProblemDetails.Map; verificado independiente por el
  Asesor contra Program.cs:494-522; registrado por el Arquitecto como hallazgo formal QA #10 al Analista,
  a2657d5; in-flight). Ademas verifique 3 hallazgos no-bloqueantes en TASK-0255 baseline (columnas de
  lectura inciertas con default silencioso, sin test HTTP con gateway falso para los 2 endpoints, omision
  del proc de mutacion en la lista prohibida del frontend) -- quality-data del brazo baseline, no reabrir la
  unidad medida. RUTEADOS (orden operador) como senal DECISION-0018 al Arquitecto = hallazgos #11/#12/#13
  (registrar quality-data + hornear en SPEC-NOVA-P4-006 gobernado). Ver A9.
- **2026-07-06 (Asesor, prep Sprint 1):** refuerza A5 -- el hueco conocido #8/auth (el baseline opera bajo
  supuesto DD-01 sin wiring de autorizacion real) NO se parcha retroactivamente sobre las unidades baseline
  YA CERRADAS Y MEDIDAS; se disena HACIA ADELANTE en el miembro gobernado (SPEC-NOVA-P4-006 s.6h,
  Annul_Commitment, commit 9bd3587), patron de auth real que hereda el resto del brazo gobernado. Traza: la
  gobernanza prefiere el gap declarado + fix-forward antes que alterar post-hoc lo medido. Es la misma
  disciplina de pre-registro de A5 aplicada a un gap tecnico, no solo al sorteo.
