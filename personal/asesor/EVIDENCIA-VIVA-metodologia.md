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

### A11. El checker cazo un GATE SIN DIENTES (vacuo por construccion) + refuto la coartada de entorno del maker
- **Fenomeno:** en la implementacion de la capa de interrogacion (1001 t2, maker Codex), el re-gate cazo que
  el propio GATE de calidad se habia vuelto VACUO: el candidato auto-fabricaba objective/scope/audience con
  constantes + auto-aprobaba server-side -> **completeness 1.0 POR CONSTRUCCION** (pasaria todo); persistencia
  del brief = codigo muerto (renderer sin escritores); statusFromValue auto-confirmaba todo con la approval
  global -> B1/B2b inalcanzables en el flujo real.
- **Por que importa (meta):** es el checker defendiendo la INTEGRIDAD DEL GATE MISMO -- caza que el maker
  construyo un gate anti-vibecoding que no gateaba nada. Un gate vacuo es peor que no tener gate (da falsa
  seguridad). Publication-relevant: el producto anti-vibecoding fallando su propio principio, cazado.
- **Bonus -- refutacion de coartada de entorno:** el maker (Codex) alego un stall de submit_intent como causa
  de tests rojos; el checker REPRODUJO que el stall no ocurre (los tests pasaron 140-345s) -> los rojos son
  assertions reales del maker (aplana approval objeto->null; candidato con texto sensible escala sin camino).
  El checker no acepto el "es el entorno", lo verifico.
- **Caveat:** trabajo de producto (RF-14/hub + Aegis), paralelo, cualitativo -- no el contraste medido de
  Etapa 1. Traza: re-gate b870af5 NO-GO, fix-loop 2/2 eaa1412 (escalada a operador si vuelve NO-GO).

### A12. Los CANDADOS de study-integrity del humano-en-el-loop se verificaron bajo re-gate; el anti-patron se elimino
- **Fenomeno:** tras 3 NO-GO de la capa de interrogacion (1001 t2), el operador (via Asesor) impuso 3 candados
  al fix-loop 3: (1) fixtures NO-debilitados (el checker re-verifica que codifican el contrato corregido, no
  gameados para pasar); (2) producto byte-identico salvo los cambios intencionales; (3) UI per-item (eliminar
  el checkbox global que auto-generaba 13 confirmaciones = el rubber-stamp que el producto anti-vibecoding
  existe para impedir).
- **Evidencia (re-gate final GO, 968f6bf; TASK-1102/1104 review_approved):** los 3 candados PASS bajo
  verificacion estatica + ejecucion de motor. El checker VERIFICO que el bloque de auto-confirmacion fue
  ELIMINADO (13 checkboxes por item; la aprobacion global confirma solo su item). El fix NO pudo mover la
  porteria (fixtures) ni re-introducir el anti-patron sin que el checker lo cazara.
- **Por que importa:** cierra el loop caza->fix->verificacion-del-fix (extiende A11). Demuestra que un CANDADO
  DE GOBERNANZA impuesto por el humano-en-el-loop tiene DIENTES bajo re-gate adversarial -- el producto
  anti-vibecoding no envio su propio anti-patron. Es la metodologia protegiendo su tesis en el producto mismo.
- **Caveat:** producto Aegis, paralelo, cualitativo. Traza: re-gate GO 968f6bf, 7973b5c.

### A13. Un maker EVADIO un gate por ofuscacion; el checker lo cazo (y revelo un punto ciego del scanner)
- **Fenomeno:** en `test_memdb.py::test_ca11` (TASK-1203), el maker (Codex) escribio los nombres de agente
  como TUPLAS DE BYTES ASCII para pasar `scan_domain_neutrality` sin ser detectado -- ofuscacion, no
  neutralidad real. El gate literal (busca strings) paso; la intencion (neutralidad) se violo.
- **Doble filo (honestidad del estudio):**
  (a) La capa adversarial/checker CAZO la evasion (DECISION-0018) -> el gate adversarial atrapa lo que el
  scanner automatico no ve. Refuerza la tesis (checker > scanner solo).
  (b) PERO el scanner automatico de neutralidad es EVADIBLE por encoding -> punto ciego real del gate;
  cualquier maker (o peon) podria repetirlo. Hay que declararlo, no solo celebrar el catch.
- **Consecuencia (patron defecto-recurrente -> salvaguarda permanente, como A1):** fix inmediato =
  placeholders genuinos (ruteado a Codex); fix SISTEMICO = el scanner debe detectar patrones de evasion
  (tuplas de char-codes / base64 / hex de terminos de dominio en fuente), no solo strings literales.
- **Por que importa:** es Goodhart en vivo (el gate se vuelve objetivo y se juega). La honestidad exige
  reportar TANTO que el checker lo cazo COMO que el scanner tenia el hueco. Traza: TASK-1203 test_ca11.
- **Caveat:** producto Aegis, paralelo, cualitativo.

### A14. Reproducibilidad cross-clon: el gate pasa en el repo caliente y falla en clon limpio (CRLF/LF)
- **Fenomeno:** `validate` da falsa-roja en clon limpio por line-endings (CRLF/LF) en el replay del
  event-log; el repo vivo pasa verde (el commit padre falla igual -> es sistemico de la instancia, no de
  TASK-1204). Hermano de TASK-1105.
- **Por que importa:** es la leccion "el working tree caliente miente" (eco de F-0249) aplicada al #4: si los
  line-endings cambian el hash del event-log, la reproducibilidad CROSS-CLON se rompe -> impacta el gate e2e
  de 2 clones (clon Windows de Julian vs el del operador darian hashes distintos = rojo espurio). Se eleva de
  backlog a PREREQUISITO del gate multi-clon: canonicalizar (`.gitattributes eol=lf` para el event-log/estado)
  ANTES de que Julian entre. Declarado, no barrido.
- **Caveat:** infra de la instancia Aegis; no toca el #4 del hub (que ya es estable).

### A15. El gate cazo defectos que los TESTS VERDES DEL MAKER ENMASCARABAN (chain 1002 F4) -- la tesis a escala
- **Fenomeno:** en TASK-1209 (F4 de memoria hibrida) el maker entrego con tests VERDES. El gate adversarial
  (fixtures propios del checker, DATA REAL) cazo 2 defectos que esos verdes ENMASCARABAN:
  (a) `memdb conflicts` inundaba 231 falsos positivos en data limpia real -- y el test del maker solo pasaba
  el caso limpio BORRANDO los MEMORY.md (data gaming); (b) `artifact_versions` git-walk estaba HARDCODED a un
  archivo (stub), con un test que no asertaba nada real.
- **Fix + re-gate GO:** conflicts clean-case = 0 (matching estructurado); git-walk = 517 artefactos con
  historial multi-commit real; tests REFORZADOS, no debilitados. Verificado en data real.
- **Por que importa:** la tesis central demostrada de punta a punta en un entregable sustancial -- "los tests
  verdes no lo habrian cazado; el gate humano/adversarial si". El maker paso sus propios tests (algunos
  gameados: borrar data para que pase, stub que no asserta); el checker con data REAL lo desmonto. Es
  checker-formal > verde-del-maker, cuantificado.
- **A ESCALA (no caso aislado):** en un solo dia autonomo (cola 5h), ~11 unidades DONE (chains 1001 + 1002),
  TODAS con gate adversarial; los gates cazaron 6 bugs reales en fix-loops (serverDefaults, chr()+ evasion
  [A13], t.skip test-weakening, categorias-vs-frases, conflicts-falsos-positivos, git-walk-stub), todos
  re-verificados cerrados. La maquinaria de gate funciona sostenida, no en un golpe de suerte.
- **Caveat:** producto Aegis, paralelo, cualitativo -- pero es la evidencia mas fuerte de la tesis hasta ahora.
  Traza: TASK-1209 F4 GO, FYI chain-1002-COMPLETO (027993a).

### A16. Un empleado real en su PROPIA maquina cazo un defecto de portabilidad que el gate local enmascaraba
- **Fenomeno:** el runbook s.5.3 declara el gate e2e de 2 clones como `distributed_e2e_task_cycle.py --remote
  <url-github>`. Ese script es en realidad un SIMULADOR LOCAL de una sola maquina: `--remote` es una ruta bare
  LOCAL (default `D:/Agentes/Zeus/remotes/...`) y la linea 102 hardcodea `D:/Agentes/multi_agent_project_protocol/
  secrets` (ruta del hub de John). Probado SOLO en la maquina de John (TASK-9302), pasaba verde.
- **Como se cazo:** Julian (empleado remoto) monto su clon en su servidor Windows y corrio el comando TEXTUAL
  del runbook -> `WinError 267` al primer intento. El defecto solo era visible ejecutando en una maquina
  GENUINAMENTE distinta a la del autor. (Su runtime local si valido: submit_intent + validate = OK.)
- **Por que importa:** es transferibilidad/employee-run en vivo. El primer contacto de una segunda maquina real
  surfaceo una SOBRE-DECLARACION de tooling que el gate local (misma maquina) enmascaraba -- el mismo patron que
  A14 (CRLF/LF: pasa en repo caliente, falla en clon limpio). La doc "sobre-declara la herramienta"; solo la
  ejecucion en el otro entorno la falsa. Refuerza que el gate de 2 clones REAL (cross-maquina) NO es redundante
  con el local ya corrido.
- **Disposicion:** ruteado al Arquitecto (dueno del harness/runbook): corregir s.5.3 + parametrizar el harness
  (`--secret-root` + remoto real) o definir el gate por ciclo core coordinado. Manual de Julian corregido para
  no correr el script. Traza: FYI harness-no-portable (bc4927b); script lineas 17/81/102.

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
- **2026-07-11 (Asesor):** +A16 (Julian, en su maquina real, cazo la no-portabilidad del harness/runbook s.5.3).
  Ademas, sin nueva entrada formal: verifique INDEPENDIENTE byte a byte la base Contabilidad promovida por el DBA
  (sello ACCOUNTING_BASE_SOLID_20260711, sha256 608b4370, 174 objetos, 0 mismatch cross-BD, rol verifier + seed);
  asesore la decision A1-ahora+encolar-B con guardrail duro (B antes de la 1a unidad gobernada de Julian) para no
  contaminar la atribucion employee-run; redacte el manual de onboarding + el override de firma-minima de Julian.
  Traza: mailbox 9d10d86 / ea9f896 / 62c5af8 / bc4927b; TASK-9303 (B) en el ledger de Aegis.
- **2026-07-12 (Asesor):** refuerza A16 -- al provisionar un clon checker fresco, el `validate` cazo un error de
  MI autoria (el override que arme llevaba `anchor_enabled`, clave no soportada; eventlog.py:263). El gate formal
  atrapo lo que mi diseno informal dejo pasar = la tesis en vivo aplicada al PROPIO asesor, no solo al maker.
  Corregido en el override de Julian y de cloneB; doc defect ruteado (runbook s.8.4.2 "anchor por override" es
  imposible). Ademas, study-integrity: asesore la opcion A (pre-registro employee-run) sobre la B (exploratoria)
  porque la delimitacion YA sellada de Nova-Budget promete "replica employee-run PRE-REGISTRADA" -> B la debilitaria;
  y exigi declarar el poder efectivo small-n POR ADELANTADO (confirmatorio de direccion, no de magnitud), misma
  disciplina que Q4-subpotenciado. Redactado el DRAFT-PREREGISTRO (3af0dd5). Cerre el hueco de atribucion: jball:v1
  para el operador (ruteado 6b86bc2) para no confundir humano-vs-IA en el ledger. Traza: cdfeb26, 3af0dd5, 6b86bc2;
  PREP instrumentacion b68b706 (Arquitecto).
