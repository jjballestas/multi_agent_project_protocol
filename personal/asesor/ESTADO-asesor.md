# ESTADO del Asesor - fuente de verdad canonica (leer al arrancar)

> Reemplaza al snapshot compartido de .claude (memory/project-state-snapshot.md), DEPRECADO para
> el Asesor. El Asesor mantiene SU estado aqui. Historial completo en git.
> Ultima actualizacion: 2026-07-14 ~23:09 local Madrid (CIERRE DE SESION; ver bloque TOP 15-jul arriba). Lo de abajo es historia. **SELLO ETAPA 1 EJECUTADO Y ATESTADO**
> (DECISION-0091, #4 seq 3831; corpus congelado + schema v1.0 + sorteo pre-registrado corrido con semilla NIST
> pulso 1844242 -- VERIFICADO independiente por el Asesor byte a byte: 2 completo / 8 ligero). Se construyo
> Nova-Budget de cero: GOAL-P1 (done+medido+atestado sha256 d2a13216) + skill codegen-triage (viva) + 14 SPECs
> baseline atestado + sandbox mutadores sellado (P4.x READY) + estimates Q4 locked + TASK-0245 aprobada.
> HALLAZGO CLAVE: el sorteo 8/2 hace Q4 SUBPOTENCIADO (se declara poder efectivo, no se fuerza). CAMINO OPTIMO
> routado (NO stand-down): F3.3 instrumentacion (Codex) + F3.2 diseno (yo) + dev medido P2.1/P2.2 (3-25 jul) +
> PAR-2 condicional. >> BLOQUE DE TRABAJO DE LA PROXIMA SESION: ver seccion ">> PROXIMA SESION - BLOQUE DE TRABAJO".

## >> ESTADO ACTUAL 2026-07-15 (LEER PRIMERO; supersede TODO lo de abajo, incl. el bloque 14-jul)
**Foco proxima sesion: DESARROLLAR LA MEMORIA HIBRIDA (Fase A sobre Nova-Payroll) -- directiva del operador al cierre del 14-jul ("manana vamos a desarrollar la memoria hibrida"). Dia 14-jul CERRADO end-to-end: DECISION-0097 (Gate-1) + DECISION-0098 (scratch-root) SELLADAS; Nova-Payroll NACIDA (local) + anclada Entrada 0; hardening 15-jul/PAR-2 cerrado (s.29 firmada, PAR-2 FUERA); skill notion-spec-mirror viva + retroactiva a Contabilidad. HEAD=origin 2d1ff24. FONDO 2E35F26E / epoch 1.14.0 / N=500 INTACTO. (Cierre ~23:09 local Madrid UTC+2.)**

- **>> DIRECTIVA PROXIMA SESION -- MEMORIA HIBRIDA (el bloque de trabajo).** El operador quiere DESARROLLAR la
  memoria hibrida = Fase A de `Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md` (v0.2.0) sobre **Nova-Payroll**. CONTEXTO
  DURO antes de arrancar:
  - **DECISION-0097 (SELLADA)** AUTORIZA implementar REQ v0.3.0 / SPEC v0.2.0 **SOLO en Nova-Payroll**, alcance
    **Fase A** (F1 indexador read-only + round-trip + drift + revive_pack s.5.5; F2 minimo si el probe lo pide;
    **F3+ NO** -- exigen su propia DECISION).
  - **Clausula 4 "Contabilidad gana":** el BUILD de Fase A arranca TRAS el sello E2 **o con ventana ociosa
    DECLARADA por el operador**, y necesita su **GO especifico de Fase A**. => AL ARRANCAR: confirmar con el
    operador si declara ventana ociosa / da el GO de Fase A (el operador ya dijo "manana desarrollamos", pero el
    GO formal de Fase A conviene explicito para no romper el freno).
  - **Firewall anti-HARKing (cl.3):** el probe es SOPORTE A DECISION del operador, **NO evidencia**; nada entra al
    corpus citable. El go/no-go se decide por **DEMOSTRACION** (round-trip verde + cold-start recall + **REVIVE
    demostrable** + drift 0), no por estadistica. Medicion rigurosa/citable exigiria pre-registro previo (Fase B).
  - **Un solo DDL master** (SPEC s.3) via export born-operational (DECISION-0096); port del `memdb.py` (hallazgo
    M6). PROHIBIDO tercer esquema. **PII de nomina JAMAS al store** (frontera dura ya en el AGENTS de Nova-Payroll).
- **Nova-Payroll (el vehiculo, YA EXISTE):** repo **LOCAL** en `D:/Agentes/NOVA-Suite/Nova-Payroll`. Genesis
  `0e01cb3`; Entrada 0 anclada en el hub (commit `262a541`); **`payroll_commit 95af2a4` LOCAL-ONLY por tu orden**;
  config-epoch git-blob **4229BDBC** / canonical **0345B5D9**; 5 firmantes con pubkeys reales (Julian firmante
  desde el genesis); `scratch_root` declarado. **Remoto GitHub = NO crear/pushear hasta GO explicito (post-E2).**
- **DECISION-0098 (scratch-root, SELLADA):** regla todos-los-proyectos `D:/Aegis_Scratch/<proyecto>/<proposito>/`
  (`~/Aegis_Scratch` POSIX); campo OPCIONAL `scratch_root` (configs pineados EXENTOS, sin re-genesis); cableado
  ACTIVO (template/new_instance/validador py+ps1/gitignore). Raiz del disco LIMPIA; 3 dirs `nova-*` reapeados; 2
  residuales en `D:/Aegis_Scratch/NOVA-Suite/residue/` (`nova-9310-tx.json`, `nova-a2-events.bak`; reap final tuyo,
  por ahora NO reap). Anomalia `TASK-SANDBOX` movida a `personal/operador/` (opcion b).
- **Sello E2:** `s.6` (pool **n=10 CONFIRMADO sin PAR-2**) CERRADO + **hardening/s.29 CERRADO** (checkpoint 15-jul
  cumplido EN PLAZO, evidencia declarada honesta; **PAR-2 = FUERA del pool**). Numero smoke **citable = 30** (no 36;
  la anomalia 36-vs-30 es DECISION-0018 para el Arquitecto de NOVA). **UNICO bloqueo restante de E2 = `s.1`
  reconciliacion 26-29-jul.** Contabilidad MEDIDA sigue gated post-30-jul (ruta critica real).
- **Skill `notion-spec-mirror`** (la creo el Arquitecto sobre mi DIRECTIVA): viva + master exportable + aplicada
  RETROACTIVO a las 9 SPEC-CONT. Espeja SPEC/DONE -> Notion con pasos-dentro; Notion = read-model del ledger,
  disparo post-commit. IDs Notion en memoria `[[notion-workspace-nova]]`.
- **Manual de Julian** (`D:/Agentes/Ingenas/MANUAL-onboarding-julian-contabilidad-aegis.html`, mi area, SIN commit):
  **v4**. Esta sesion += seccion **2-B "Nuestros artefactos frente al spec-driven (SDD / Spec Kit)"** (referencia
  SDD/Spec Kit como metodologia CONOCIDA, SIN la palabra "tutorial" -- correccion del operador; 2 tarjetas + mapeo +
  capa de gobernanza) + diagrama "vista de pajaro" convertido de ASCII-consola a **HTML grafico** (3 nodos push/pull)
  + caja repo-org en PRESENTE (sin "antes/ahora"). (Los otros `<pre>` son comandos reales, se quedan.) Preview:
  `python -m http.server 8791` en `D:/Agentes/Ingenas` (matar si sigue vivo).
- **>> FIX del MONITOR (COMO durable, importante):** el self-filter del monitor **NO debe incluir**
  `Co-Authored-By: Opus|Fable` -- el **Arquitecto TAMBIEN corre Opus/Fable** y ese filtro lo **CEGABA** a sus
  commits. El monitor correcto filtra **SOLO `Ops-Reason: coordinacion-asesor`** (mi marcador inequivoco). YA
  corregido en el PROMPT v11 y en la skill `asesor-guarda-estado`.
- **open/:** 5 RESP del Arquitecto->Operador (0098-sellada, s29-sellada, skill-notion, cross-atest 12-jul,
  secuencia-probe); **NINGUNO espera MI respuesta** (FYI/cierres que el Arquitecto archivara).
- **SIGUIENTE ACCION:** arrancar el desarrollo de la memoria hibrida -- confirmar con el operador ventana ociosa /
  GO de Fase A (freno "Contabilidad gana") + recordar el firewall anti-HARKing; el vehiculo Nova-Payroll YA existe.

## >> ESTADO ACTUAL 2026-07-14 (historico; ver bloque 15-jul arriba)
**Foco: la recta de medicion de Contabilidad sigue gated post-30-jul (E2: corpus <=25-jul, BR-C4 <=29-jul). Sesion 14-jul = onboarding Julian a NOVA COMPLETO + reorg 2.A cerrado + DEBATE memoria (Engram/gentle-ai) + coordinacion del PROBE de memoria hibrida sobre Nova-Payroll. HEAD=origin b699996, fondo 2E35F26E/1.14.0 INTACTO.**

- **INSTANCIA re-nacida como NOVA 2.A (dos-trios) + A2-nominal RE-DEMOSTRADO EN VIVO.** NOVA es instancia
  INDEPENDIENTE (genesis fresco, config-epoch **git-blob C2DE91F9**, canonical genesis **C157FE00**; el `5679362F`
  de Entrada 0 fue artefacto CRLF -> ERRATUM append-only; leccion: hashear el BLOB de git, no el working copy).
  Gobernanza ENCAPSULADA en subfolder `Aegis/` (retrofit sin re-genesis; NOVA HEAD 5518b5a). Cross-atest Entradas
  0/1/2 en el hub. **Gate 2-clones nominal NOVA (TASK-9391) cerro VERDE**: maker!=checker demostrado bajo el genesis
  REAL, 3 firmantes ed25519 en maquinas separadas (jheredia maker / Analista checker / jheredia done). Frontera:
  el hub-Arquitecto SOLO LEE NOVA para atestar; el trio de NOVA escribe su ledger.
- **DECISION-0095** (topologia 2.A sellada, enmienda 0050) + **DECISION-0096 / release v1.19.0** (instancias
  born-operational). El **epoch pineado 1.14.0 sigue intacto** (release != epoch, dos ejes por diseno).
- **JULIAN (jheredia) ONBOARDED A NOVA COMPLETO + OPERATIVO como firmante:** deploy key en NOVA.git + ed25519
  `jheredia:v1` + **HMAC PROPIO `jheredia-hmac:v1` / `protocol-secrets/jheredia-eventauth.key`** (verificado en el
  config vivo de NOVA). OJO: el `codex-hmac:v1` que se dijo antes era el plan A1 pre-onboarding, SUPERADO -> jheredia
  tiene HMAC propio. Manual + receta corregidos a jheredia-hmac.
- **PRE-REGISTRO N=6 SELLADO + s.11.5 CERRADA** (historico, sigue vigente): DECISION-0094, sha256 28fd963b, cadena #4
  seq 4659; Analista OK-ATESTADO (ADDENDUM, commit 6582325). Ceremonia s.11 completa. Kit SPEC-CONT 8/8.
- **DEBATE metodologia vs Engram/gentle-ai (para debatir; conclusiones):** objetivo = **evidencia citable** (ancla =
  Contabilidad). Engram = motor de memoria (SQLite/FTS, MCP/HTTP/TUI, agent-agnostic, ~4.6k stars, bus-factor-1);
  gentle-ai = "ecosystem configurator" que su propio doc declara **NO ser** gobernanza/atestacion. Estamos por delante
  en gobernanza/atestacion/maker!=checker/pre-registro; FLACOS en memoria-enviada. PERO ya hay
  **`SPEC-MEMORIA-HIBRIDA v0.2.0`** (commit 9376bb4, adversarialmente revisada; 3 planos hot/cold/DB-SQLite; importador
  round-trip = "el gap que mato a Engram"; REVIVE de peon employee-ready). Ruta unica memoria = DECISION-0081
  (Engram CERRADO; DECISION-0071 superseded). `engram_*` en runtime = 0 hits (specified-no-merged).
- **>> COORDINACION VIVA -- PROBE de memoria hibrida (mi carril como asesor):** el operador quiere saber **si la
  memoria hibrida aporta valor a la metodologia** (para DECIDIR adoptarla). Diseno acordado (debate 14-jul):
  - **Probe de VALOR ahora** = Fase A de la SPEC (round-trip verde, cold-start recall, **REVIVE demostrable**,
    drift 0) + observacion cualitativa. Objetivo = decision del operador, **NO evidencia** -> **firewall duro del
    corpus citable** (probe disfrazado de resultado = HARKing). Un go/no-go se decide por DEMOSTRACION, no estadistica.
  - **Vehiculo = `Nova-Payroll`** (modulo Nomina), instancia born-operational PROPIA (base+store propios), **NO
    cableada** a Budget/Contabilidad medidos. **Slice ACOTADO** (nucleo de liquidacion: empleados/contratos/conceptos +
    cabecera DbsNom002t/detalle 007t/bases 028t + FindBaseTra + %concepto + consecutivo + control periodo + reporte RO).
    Nomina es **greenfield** (sin SDD/base/procs; solo legacy VB6 + 42 tablas). PII de nomina fuera del store (firewall).
  - **Secuencia:** Gate-1 (DECISION que autoriza implementar, scope AISLADO a Nova-Payroll, OFF estructural en
    hub/medidas) -> nacer Nova-Payroll -> PREP slice -> Fase A build+probe. **Timing:** papel/ceremonia AHORA;
    Fase A build TRAS el sello E2 salvo ventana ociosa, freno "Contabilidad gana". Post-30 y SOLO si el probe da
    indicios: medicion RIGUROSA (pre-registro del Asesor O folded en metricas Q1-Q5).
  - **Estado de ruteo:** DIRECTIVA marco (9b02e23) -> Arquitecto CONFIRMO con 4 precisiones (RESP 64d5c5e: Gate-1
    ACTIVA citando 0081 no re-supersede / OFF estructural / un DDL master via export born-operational / build tras E2).
    **GO Gate-1 + roster ruteados (b699996)** -> Arquitecto entrego el draft -> **operador FIRMO (8e669fc) ->
    Gate-1 SELLADO: `DECISION-0097` accepted** (sello b13e090, tx seq 4688-4690 drift 0; fondo INTACTO). Autoriza
    implementar la **Fase A SOLO en Nova-Payroll** (repo NOVA-Suite/Nova-Payroll; trio Arquitecto/Codex/Analista +
    jball + jheredia firmante desde el genesis; PII de nomina fuera del store; OFF estructural+vinculante en
    hub/medidas; firewall anti-HARKing). **Nova-Payroll NACIDA local** (97b2eeb; genesis 0e01cb3 verificado
    clean-clone; aislada, fondo hub intacto). **Nova-Payroll remoto = queda LOCAL hasta un GO** (decision del operador,
    133f5c1; no se crea repo GitHub aun). La **Fase A build** queda gated por su GO especifico + sello E2 ("Contabilidad gana").
- **NOTION:** Contabilidad POBLADA (9 menus + 25 opciones option_id/menu + raiz + Fecha->date + fila proyector
  TASK-9310). Creada DB **"Tareas de metodologia"** en METODOLOGIA (ds 61f88150-e0be-497b-8d8d-acb4e4ae31c2) con
  **6 tareas del probe** (Gate-1/nacer-instancia/Fase-A/slice/pre-registro/Fase-B), zona Planeacion, is_governed NO.
  IDs canonicos en memoria `[[notion-workspace-nova]]`.
- **Manual de Julian** (`D:/Agentes/Ingenas/MANUAL-onboarding-julian-contabilidad-aegis.html`, mi area, sin commit):
  esta sesion += recuadro HMAC (2 capas ed25519/HMAC), seccion vibecoding, anatomia SPEC (T-001), instalar OpenSSL
  (4.9), generar llave git ssh-keygen (5.1), HMAC->jheredia-hmac, frase-mision "Para desarrolladores profesionales --
  y para profesionalizar a quien construye con IA sin serlo".
- **open/:** nada espera MI respuesta. Vivo: mi GO Gate-1 (b699996, espera draft del Arquitecto). Stale candidato a
  higiene del Arquitecto: RESP-cross-atestacion 12-jul.
- **NUEVO 14-jul tarde:** **DECISION-0098 (scratch root unico) SELLADA** (firma operador, tx seq 4691-4693, cableado
  ACTIVO; template/new_instance/validador host-independiente). TASK-SANDBOX movido a personal/operador (opcion b). **Nueva DIRECTIVA/skill `notion-spec-mirror`**
  (operador 14-jul): espejar SPEC/DONE -> Notion con los PASOS DENTRO de la pagina, post-commit, upsert idempotente
  por spec_id/task_id (Notion = read-model, nunca fuente). El Arquitecto poblo la DB "Tareas de metodologia"
  (14 tareas con pasos + seccion "Ruta de convergencia"). Boundary reforzado (skill Arquitecto + safety): **el Asesor
  NO firma DECISIONes por el operador** -- la firma es acto humano genuino; yo solo RELEVO.
- **SIGUIENTE ACCION:** vigilar la ceremonia de nacimiento de Nova-Payroll (Arquitecto) + el GO de la Fase A (tras E2).
  Mantener projector-ready + monitor armado + EVIDENCIA-VIVA + espejo notion-spec-mirror. Contabilidad medida gated post-30-jul.

## >> ESTADO ACTUAL 2026-07-13 (historico; ver bloque 14-jul arriba)
**Foco: la recta de medicion de Contabilidad queda GATED SOLO por el build-open (post-30-jul). Pre-registro N=6 SELLADO + ceremonia s.11 COMPLETA (verif independiente cerrada). Notion Contabilidad POBLADO. Agentes STOPPED (pausa natural).**

- **PRE-REGISTRO N=6 = SELLADO Y ANCLADO (DECISION-0094, 13-jul ~00:38 local).** El Arquitecto congelo el diseno
  (hipotesis H-TRANSFER, muestra N=6, metricas, criterio exito/refutacion) ANTES de construir/medir ninguna unidad
  (build-open post-30-jul; ninguna existe -> cero HARKing). Artefacto
  `Area_comun/artifacts/SELLO-PREREGISTRO-contabilidad-employee-run-N6.md` (17189 bytes, ASCII),
  **sha256 = 28fd963b2472b1b6277b45e38e3bdf92686f022b0c41de4ab6a1338597d45828**, anclado via intent `decision`
  (cadena #4 seq 4659, commit 86e5ce5). SIN re-genesis: hub 2E35F26E/1.14.0 + dataset N=500 INTACTOS. **VERIFICACION
  INDEPENDIENTE s.11.5 CERRADA (OK-ATESTADO):** el Analista (analista:v1, LLAVE SEPARADA) recomputo el sha256 en clon
  limpio de HEAD -> match exacto; ADDENDUM en DECISION-0094 (commit 6582325), REQUEST/REVIEW archivados. **Ceremonia
  s.11 COMPLETA** (sello + verif independiente por segundo firmante con llave separada). El cableado F3.3 + las 6 unidades medidas
  (R2-c/R3-b/R4-b/R5-c/R0-fuentes/R4-c) siguen gated post-30-jul (prereq de la 1a unidad MEDIDA, no del sello del DISENO).
- **A2-NOMINAL CERRADO + INSTANCIA RE-NACIDA COMO NOVA (modelo 2.A, 2026-07-13 tarde).** Gate 2-clones nominal
  corrido en vivo (jheredia firmo build/done [jheredia:v1] maquina Julian; Analista ratifico [analista:v1] clon
  SEPARADO; prueba negativa fallo) demostro maker!=checker POR POSESION DE LLAVE. Luego el operador reorganizo a
  **modelo DOS TRIOS (2.A):** NOVA es instancia INDEPENDIENTE con su propio trio + **genesis FRESCO** (repo NOVA.git,
  carpeta `D:/Agentes/NOVA-Suite/NOVA`; gobernanza ENCAPSULADA en el subfolder constante `Aegis/`; config-epoch
  reproducible git-blob **C2DE91F9**, canonical del genesis **C157FE00**, cadena seq 1..4, 5 firmantes ed25519:
  arquitecto/codex/analista:v1 + jheredia:v1 + jball:v1). **Cross-atest NOVA anclada:** Entrada 0 (hub f23ec3e) +
  Entrada 1 tras encapsular (nova_commit 5518b5a, events.jsonl 4f69a3dc, sello byte-preservado SIN re-genesis).
  **ERRATUM (integridad):** la Entrada 0 registro `5679362F` = artefacto CRLF del working copy; el reproducible
  desde clon limpio es `C2DE91F9`; **el sello NUNCA estuvo afectado** (el genesis liga el canonical C157FE00).
  Leccion: hashear el BLOB de git, no el working copy. **A2-nominal NOVA CERRADO.** El hub-Arquitecto SOLO LEE NOVA
  para atestar (no escribe su ledger). SUPERSEDE la epoca-2 Aegis 77242D63 (Entrada 3). **jheredia:v1 OPERATIVO.**
  Nota integridad (Asesor): maker!=checker se preserva bajo el genesis fresco porque registra las MISMAS llaves ya
  demostradas en vivo, y se re-demuestra live con la 1a unidad medida bajo NOVA 2.A (post-30-jul) -> sin hueco.
  Topologia 2.A SELLADA como **DECISION-0095** (enmienda DECISION-0050, gobernanza encapsulada bajo Aegis/; fondo hub
  intacto). Crons Codex/Analista recableados a `D:/Agentes/NOVA-Suite/NOVA` (mi DIRECTIVA DECISION-0018 -> fix 3699714).
- **KIT SPEC-CONT COMPLETO 8/8** (commit 3ba9e2d): S1-S6A + S6B (cierre anual, Close_Annual_Accounting_Period,
  annual_close atomico + reserva legal privada) + S6C (spec-FRONTERA causacion ingresos/CxC, contrato una-via
  fuente->Accounting via Post_Voucher, sin harness SQL propio). Diseno/PREP: NO se construye antes del 30-jul.
- **WORKSPACE NOTION = BACKBONE COMPLETO + CONTABILIDAD POBLADA (2026-07-13, Asesor).** HECHO: (1) **9 Menus**
  (menu_id MENU-CONT-R0..R8; menu = slice funcional del SDD/SPEC-CONT, NO taxonomia inventada -- no existe menu en el
  SDD); (2) las **25 Opciones** con `option_id` (extraido del titulo: R0-cuentas/tercero/estructura/usos/fuentes,
  R1-reportes, R2-a..d, R3-a..c, R4-a..c, R5-a..c, R6-a..d, R7-a, R8) + Menu vinculado por slice; (3) raiz NOVA
  actualizada (checks marcados + link a METODOLOGIA + nota de poblacion); (4) `Artefactos.Fecha` text->date; (5) fila
  proyector TASK-9310 en Tareas. **PENDIENTE decision operador:** (a) relacion **Agentes<->Tareas CONTRADICE la
  doctrina de la raiz** ("puente = task_id, no relacion cross-espacio") -> NO resuelta en silencio, escalada (Tareas ya
  liga agentes via el select Ejecutor; anadi link nav a METODOLOGIA); (b) llaves gobernadas restantes
  (object_id/test_id/evidence_id) las llena el proyector. SQL query_data_sources = plan gratuito AGOTADO (usar
  notion-search; create/update SI funcionan). IDs canonicos en memoria `[[notion-workspace-nova]]` (rehidratada 13-jul).
- **PROYECTOR = RUTEADO -> TASK-9310** (Aegis, proposed/backlog, owner Codex maker / Analista checker FORMAL,
  integridad ALTA, contra SPEC-NOTION-PROJECTOR). El Arquitecto lo AGENDO al build-open (no compite con Sprint 1).
  **Trazado en la base Tareas de Notion:** fila proyector (Backlog, Ejecutor Codex, task_id TASK-9310). FALTA (lo crea
  el BUILD): metadata de gobernanza completa (source_event_seq/hash/commit/actor/projector_version).
- **Manual de Julian v2** (`D:/Agentes/Ingenas/MANUAL-...html`): 5 trampas de PowerShell + receta verificada
  (`personal/asesor/COMANDOS-julian-gate-nominal-7b.md`). **Skill `asesor-guarda-estado` viva** (espejo de la del Arquitecto).
- **open/:** NADA espera MI respuesta. REQUEST verif-sha256 CONSUMIDO+archivado (Analista OK-ATESTADO). Fix del cron
  de Codex: AUTORIZADO (dbe7abe). **Crons apagados / agentes STOPPED** (Arquitecto checkpoint 682f722, pausa natural;
  el operador reactiva al abrir el build).
- **SIGUIENTE ACCION:** Contabilidad en Notion POBLADO + s.11.5 cerrada. Solo queda: (a) decision operador sobre la
  relacion Agentes<->Tareas (doctrina) + llaves gobernadas via proyector; (b) al build-open (post-30-jul): cablear F3.3 +
  arrancar las 6 unidades medidas + el Arquitecto promueve TASK-9310 a ready+GO. Mientras: monitor armado + EVIDENCIA-VIVA.

## >> ESTADO ACTUAL 2026-07-12 (NOCHE) (historico; ver bloque 13-jul arriba)
**Foco actual: (A) recta de medicion de Contabilidad + (B) construccion del workspace NOTION para control del proyecto.**

> **ACTUALIZACION 2026-07-12 (tarde-noche) -- supersede lo de abajo en lo que toca:**
> - **A2-NOMINAL CERRADO, VERDE.** Gate 2-clones nominal corrido EN VIVO (TASK-9390 en Aegis): jheredia (maquina de
>   Julian) firmo build->in_review [ed25519 jheredia:v1], Analista (Aegis-cloneB, maquina/llave SEPARADA) ratifico
>   review_approved [ed25519 analista:v1], jheredia cerro done; PRUEBA NEGATIVA fallo como debia (jheredia no puede
>   firmar como Analista); validate exit 0 en ambos clones, drift 0 (HEAD Aegis 4054e3ae). **maker!=checker por
>   posesion de llave demostrado en vivo.** Config-side previo: epoca 2 de Aegis con jheredia:v1 + jball:v1 (TASK-9303
>   frontera + TASK-9304 pre_t0, chain_cases 40/40; hub 2E35F26E/1.14.0 INTACTO). **jheredia:v1 OPERATIVO** (pendiente
>   SOLO que el Arquitecto ancle la cross-atestacion en el hub; confirmacion ruteada 9592cfe). Al anclarla -> arrancan
>   las 6 unidades medidas + sello del pre-registro N=6.
> - **APRENDIZAJE DURO del gate (para replicar):** submit_intent en PowerShell exige intent POR ARCHIVO (--intent),
>   campo `type` (no kind), --timestamp UTC obligatorio, override de jheredia CON event_auth->runtime-hmac:v1
>   (secrets/eventauth-runtime.key), claim ANIDADO con scope de 4 fragmentos (TASK_INDEX/PROJECT_STATE/.md/CLAIMS#id),
>   git identity + stagear Area_comun/state + runtime/state/{events.jsonl,snapshot.json}. Todo en la receta verificada
>   `personal/asesor/COMANDOS-julian-gate-nominal-7b.md` + horneado en el manual de Julian v2.
> - **WORKSPACE NOTION = BACKBONE COMPLETO.** NOVA: Modulos/Opciones/Tareas(+8 Budget congeladas)/Specs SDD(25)/
>   Objetos BD/Objetos Legacy/Casos de Prueba/Artefactos/Decisiones de dominio -- todo con vista Por Modulo. METODOLOGIA:
>   Agentes/Unidades Medidas(6)/Decisiones de metodologia/TFM/Norma. IDs en memoria [[notion-workspace-nova]]. Falta solo
>   cablear el proyector (SPEC-NOTION-PROJECTOR) que llena task_id/Staleness/M-Q1/M-Q2/rollups.
> - **Manual de Julian v2** (D:/Agentes/Ingenas/MANUAL-onboarding-julian-contabilidad-aegis.html): 5 trampas PowerShell
>   + receta verificada + jheredia operativo + gate marcado hecho. **Fix del cron de Codex: AUTORIZADO** (ruteado dbe7abe).

- **B (TASK-9303 en Aegis) = DONE.** El re-anclaje de cadena (config-epoch para jheredia:v1) esta construido y
  gateado adversarialmente. El Analista cazo un bug CRITICO real **F-9303-01** (`validate_chain` aceptaba tamper del
  sello de frontera: sealed_segment sha256/event_count/seq_range, boundary_id, old_config_hash = el registro que
  declara la historia sellada era modificable sin detectarse). Codex remedio (validate_chain falla cerrado + recomputa
  el sello contra las lineas reales 672..N; chain_cases 26/26). B done-flip. GUARDRAIL CUMPLIDO: NUNCA se provisiono
  la privada de jheredia a la maquina de build; hub intacto (2E35F26E/1.14.0).
- **A2-NOMINAL de B = SEPARADO y PENDIENTE (sin mas codigo).** El Arquitecto registra jheredia:v1 + jball:v1 en el
  config-epoch (una re-genesis; ambas pubkeys ya en su mano, `personal/Arquitecto/A2-nominal-pubkeys.md`) + Julian
  corre la e2e 7b jheredia-live + el gate 2-clones NOMINAL en su maquina. **PENDIENTE OPERADOR: decidir CUANDO se
  ejecuta** (pasos de Julian: pull nuevo config-epoch -> override Codex->jheredia -> validate -> gate; ver detalle en
  bloque manana). Al cerrar A2-nominal -> jheredia:v1 operativo -> las 6 unidades medidas se pueden construir bajo medicion.
- **PRE-REGISTRO (opcion A) = REDACTADO COMPLETO** (`personal/asesor/DRAFT-PREREGISTRO-contabilidad-employee-run.md`).
  Debate resuelto: (1) **TFM = SI** (operador quiere las mediciones). (2) **Plan de medicion DESACOPLADO**: el producto
  NOVA NO se congela; se RESERVA una muestra pequena de unidades de Julian y se mide temprano (frontload) -- el enemigo
  no es la fecha 30-jul, es el DRENAJE (no se mide retroactivo; reservar unas pocas). (3) **Muestra N=6 FIJADA** (s.3):
  R2-c/R3-b/R4-b/R5-c/R0-fuentes/R4-c (mutadoras de Julian, mezcla dificultad facil->alta). (4) **s.4 mapeo HONESTO**:
  M-Q2 (defectos, VERBATIM del sello Nova-Budget) + M-Q1 (costo DESCRIPTIVO no marginal) APLICAN; **Q3/Q4 = N/A** (Q4
  ligero-vs-completo y Q3 pares PAR-D son contrastes INTERNOS que Contabilidad NO tiene); M-ATRIB/M-MANUAL propias.
  SELLA tras A2-nominal (jheredia operativo) + instrumentacion F3.3 cableada. CORRECCION del operador confirmada en el
  sello: N=500 auto-dogfood = **Zeus-Protocol** (NO Nova-Budget). Escalera de transferibilidad: Zeus-Protocol(N=500 auto)
  -> Nova-Budget(dominio real, equipo) -> Contabilidad-Julian(dominio+empleado reales).
- **jball:v1 (identidad del operador) DADA + pubkey ENVIADA:** `pSGHuZPbQQF4aJn4dBhyRSiCUn1DKrMwhAUjjLVyWd0=` (ed25519,
  capability implementer). El Arquitecto la tiene para el A2-nominal. Razon: John dirige agentes + revisa + corrige a
  mano la MAYORIA; su trabajo se firma como jball, no Codex. maker!=checker (sus unidades las gatea el Analista).
- **WORKSPACE NOTION = CONSTRUIDO (andamiaje + primeras DBs).** El operador quiere Notion para control (planeacion/
  visibilidad HUMANA: "que me toca" + "como avanza"). Consenso de los 3 firmantes: **Notion = read-model AUDITADO del
  ledger #4, NUNCA fuente**; sync una-via ledger->Notion via proyector; campos de gobernanza (seq/hash/actor/commit/
  staleness); **SPEC-NOTION-PROJECTOR ESCRITA** por el Arquitecto (`Area_comun/specs/SPEC-NOTION-PROJECTOR.md`, con los
  5 tests + 2-workspaces + dimension estudio). El proyector se cablea CUANDO el workspace este construido.
  **IDs de Notion (workspace del operador, john.ballestas@gmail.com):** ver memoria `notion-workspace-nova.md`.
  Construido hoy: espacios **NOVA** + **METODOLOGIA** (paginas raiz); DBs en NOVA: **Modulos**(8), **Opciones/Casos de
  Uso**(25 = R0-R8 Contabilidad, con estado de migracion del DBA + tipo objeto + relaciones a Modulo y Tareas),
  **Tareas**(6 reservadas sembradas; kanban "Mis tareas" + "Reservadas para medicion" + "Por modulo"). Jerarquia
  Modulos<-Opciones<-Tareas relacionada. Insight de diseno: el Estado de tarea cruza 2 zonas (Planeacion nativa Notion
  Backlog..Listo <-submit_intent firmado-> Ejecucion espejo del ledger En-desarrollo..Hecho).
- **kit SPEC-CONT: 6/8** (S1-S6A; el Arquitecto sigue con S6B cierre anual + S6C frontera).
- **PENDIENTE OPERADOR (4):** (1) decidir CUANDO el A2-nominal de B; (2) autorizar FIX DURABLE del prompt del cron de
  Codex (sus announces del hub sobre tareas de Aegis salen sin `Task-Id: none` -> gate rojo, grandfather manual 3x hoy);
  (3) invitar a Julian a Notion (para "Mis tareas = Yo" con persona) o usar filtro por `Ejecutor`; (4) seguir el build
  de Notion (siguiente DB sugerida: Specs SDD, o poblar METODOLOGIA con Unidades Medidas + Agentes).
- **Yo (Asesor) tengo el conector MCP de Notion vivo** (puedo search/fetch/create/create-database/create-view). Retomo
  el build de Notion directamente. Monitor: re-armar.

## >> ESTADO ACTUAL 2026-07-12 (MANANA) (historico; ver bloque NOCHE arriba)
**Pipeline vivo: `personal/asesor/PIPELINE-cierre-baseline-sprint1.html`. Onboarding de Julian casi cerrado; el foco pasa a la RECTA DE MEDICION de Contabilidad (pre-registro + jball:v1 + gate nominal tras B).**

- **ONBOARDING DE JULIAN -- casi cerrado, todo lo del operador HECHO:**
  - BD RESTAURADA en su server de desarrollo (`WIN-UUTF2NRPI8V\INGENAS`, SQL Server 17): DbsFinanciero_SANDBOX
    con rol `accounting_sandbox_verifier` + 358 objetos Accounting. (El `.bak` ya no es pendiente.)
  - BUNDLE de firmante entregado en `D:/Agentes/Zeus/NOVA/NOVA-Aegis/secrets/`: `codex-ed25519-private.pem` (A1)
    + los 4 `eventauth-*.key`. **maker!=checker verificado:** NO estan las ed25519 de analista/arquitecto.
  - Override A1 de Julian VALIDADO 5/5 por el Arquitecto (solo-Codex, sin event_auth por HMAC pineado, anchor por
    operacion). Runtime local de Julian VERDE. Falta el smoke firmado + el gate 2-clones coordinado.
- **BUG DE OVERRIDE cazado y corregido (mio):** mi plantilla incluia `anchor_enabled:false`, clave NO soportada
  (validate la rechaza; eventlog.py:263 solo permite `actor_auth_enforce`/`actor_auth_config`/`event_auth`).
  Corregido en el override de Julian y en cloneB. **Doc defect ruteado:** runbook s.8.4.2 ("anchor deshabilitado
  por override") es imposible -> es canonico-solo por OPERACION. (EVIDENCIA: el validate cazo mi error de autoria.)
- **CLON CHECKER (Aegis-cloneB) RE-PROVISIONADO:** apuntaba por error a `Zeus-Aegis` (fork product-front) y estaba
  stale -> BORRADO + re-clonado fresco desde NOVA-Aegis (HEAD 23dd83a3) + override Analista-only + 4 HMAC.
  `validate` = OK. Listo como el lado checker del gate 2-clones. (El canonico `Aegis` esta en f4d84bdd; hazle pull.)
- **B (TASK-9303) PROMOVIDA a ready + GO ruteado a Codex** (Aegis cb289f7b; hub GO aac879e). Codex la construye
  desde el clon Aegis (mecanismo s.6). **PENDIENTE OPERADOR: reactivar el cron de Codex.** Al aterrizar B: A2
  nominal (jheredia:v1) + corregir runbook s.8.4 + ROTAR la llave de Codex (exposicion transitoria en server Julian).
- **INSTRUMENTACION DE MEDICION de Contabilidad DISENADA** (Arquitecto, PREP hub b68b706): F3.3 + Q1-Q5 capturados
  en el ledger de AEGIS, doble-anclados al hub (cross-atest events.jsonl + sha256 del artefacto de metricas), sin
  tocar el config pineado. Frontera confirmada.
- **PRE-REGISTRO opcion A CONFIRMADO + REDACTADO** (Asesor, `personal/asesor/DRAFT-PREREGISTRO-contabilidad-
  employee-run.md`, 3af0dd5): H-TRANSFER falsable, poder efectivo DECLARADO small-n (confirmatorio de direccion/
  patron, no de magnitud), poblacion medida por criterio (unidades mutadoras de Julian; RO/frontera fuera),
  Q1-Q5 identicos a Nova-Budget, convencion de atribucion, criterio de exito/refutacion. **FALTA (operador):**
  completar s.3 (N + metodo de seleccion) + s.4 (Q2-Q5 textual del sello) + alta jball:v1 + SELLARLO antes de la
  1a unidad medida.
- **jball:v1 (identidad del operador) RUTEADA** (6b86bc2): darla de alta en el MISMO config-epoch que B (junto a
  jheredia:v1), capability implementer -> atribucion limpia (John dirige agentes + revisa + corrige a mano la
  MAYORIA; su trabajo se firma como John, no Codex). El operador genera su par ed25519 + manda pubkey. maker!=checker
  intacto (unidades de John gateadas por Analista).
- **DONDE TRABAJA EL OPERADOR (aclarado):** AHORA en el HUB (coordinacion/estudio). `Aegis-cloneB` = solo para
  el lado checker del gate 2-clones (momento puntual). Un clon Aegis maker = solo cuando abra el build (post-30-jul).
- **PENDIENTE DEL DBA (no bloquea, read-only):** `fn_Account_Balance_For_Period` fuera de los 33 grants -> diagnostico
  read-only (interno-solo vs endpoint); prompt entregado al operador. NO tocar el script sellado (rompe 608b4370).
- **Mailbox ruteados hoy (12-jul):** correccion override (cdfeb26), alta jball:v1 (6b86bc2). Del 11-jul: GO A2+kit,
  FYI base, decision A1+B, FYI harness, validar override, reactivar Codex B, instrumentacion. **Monitor: re-armar.**

## >> ESTADO ACTUAL 2026-07-11 (historico; ver bloque 12-jul arriba)
**Pipeline vivo: `personal/asesor/PIPELINE-cierre-baseline-sprint1.html` (actualizado 11-jul).**

- **CONTABILIDAD: AMBOS inputs del operador RESUELTOS -> el build queda gated SOLO por Sprint 1 (post-30-jul).**
  - **(b) BASE PROMOVIDA (DBA):** sello `ACCOUNTING_BASE_SOLID_20260711`, source_bundle_sha256
    `608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5`, 51 files / 174 objetos / 0 faltantes /
    0 mismatch cross-BD (DbsFinanciero/SANDBOX/SNJDC). Rol `accounting_sandbox_verifier` en SANDBOX (33 EXECUTE
    + 23 SELECT + VIEW DEFINITION, guard THROW 54500 fail-closed, seed determinista ACCTVERIFY, reset
    idempotente). VERIFICADO INDEPENDIENTE por el Asesor (artefactos + sha256 + conteos cuadran byte a byte).
  - **(a) JULIAN onboardeado:** invitacion aceptada + pubkey `jheredia:v1` recibida/persistida por el Arquitecto.
- **RE-GENESIS A2 BLOQUEADA (hallazgo tecnico) -> DECISION operador: A1-AHORA + ENCOLAR-B.** El procedimiento del
  runbook (pubkey al config + regenesis.py) NO da estado valido: cambiar el config rompe el prev_hash del
  `chain.genesis` (seq 672) y la cascada; regenesis.py no re-ancla; no hay tooling (problema de seq-2175). El
  Arquitecto revirtio limpio (validate 0, b22e49bc, config intacto). Decision: **A1** = Julian firma interino
  bajo identidad **Codex** via override runtime (sin tocar config); **B** = TASK-9303 en el ledger de Aegis
  (proposed, owner Codex, spec SPEC-AEGIS-chain-reanchor-config-epoch: sello seq 672..N patron pre_t0 +
  chain.genesis nuevo con jheredia:v1 + validador multi-epoca). **GUARDRAIL DURO:** B antes de la 1a unidad de
  build GOBERNADA de Julian; su trabajo study-relevant nace bajo jheredia:v1 tras B. Codex parado (operador
  reactiva). Correccion runbook s.8.4 diferida a B.
- **JULIAN runtime local VERDE:** monto su clon en `D:/Agentes/Zeus/NOVA/NOVA-Aegis` (Windows Server, user
  Administrador); `submit_intent --help` OK + `validate_collaboration_state.py` = "OK". Es TODO lo solitario.
  **PENDIENTE OPERADOR (DECISION-0057):** distribuir su bundle de firmante out-of-band: SOLO
  `codex-ed25519-private.pem` (de `D:/Agentes/protocol-secrets/`) + los 4 `secrets/eventauth-*.key` (HMAC de
  instancia, van todos, no dan firma) + override `event-state.runtime.json` (llave minima = solo Codex, anchor
  deshabilitado). BORRADOR del override hecho (en mi respuesta al operador; el Arquitecto lo valida). NUNCA las
  ed25519 de analista/arquitecto (rompe maker!=checker). Rotar la llave de Codex tras B (exposicion transitoria).
- **KIT SPEC-CONT (Orden 2, PREP escribir-no-construir): 2/8.** Indice + S1 (reportes RO) + S2 (comprobante manual,
  escotilla de integridad + THROW 52252 preservados); base 608b4370 anclada; cobertura 33/33 confirmada. Faltan
  S3-S6C (el Arquitecto continua por slice). Colocacion gobernada: a su criterio de frontera.
- **MANUAL de onboarding de Julian creado** (`D:/Agentes/Ingenas/MANUAL-onboarding-julian-contabilidad-aegis.html`,
  borrador del Asesor): novato, Windows Server, maker-only (Arquitecto+Analista centrales), SIN Docker (SQL Server
  nativo = prod-like), backup de `DbsFinanciero_SANDBOX`. Colocacion gobernada en Aegis: pendiente del Arquitecto.
- **DEFECTO CAZADO (EVIDENCIA A16):** el runbook s.5.3 sobre-declara `distributed_e2e_task_cycle.py --remote
  <url-github>` como gate real; es un SIMULADOR LOCAL de una maquina (--remote = ruta bare local; linea 102
  hardcodea el secrets del hub de John). Julian lo topo en su maquina real (WinError 267). Ruteado al Arquitecto
  (su carril: corregir runbook + parametrizar harness o gate por ciclo core coordinado). Manual de Julian corregido.
- **PENDIENTES OPERADOR:** (1) distribuir bundle de Julian (arriba); (2) DBA generar el `.bak` (NO existe aun --
  solo el sello/manifest; comando en Anexo A.1 del manual); (3) reactivar Codex para B; (4) validar el override
  con el Arquitecto. Diferidos: .NET 10 SDK winget id, metodo de acceso GitHub de Julian, alcance del backup.
- **Mailbox ruteados hoy (Operador->Arquitecto):** GO A2+kit (9d10d86), FYI base promovida (ea9f896), decision
  A1+B (62c5af8), FYI harness no-portable (bc4927b). **Monitor: re-armar.**

## >> ESTADO ACTUAL 2026-07-07 (historico; ver bloque 11-jul arriba)
**Pipeline vivo VISUAL: `personal/asesor/PIPELINE-cierre-baseline-sprint1.html` (CARGARLO al arrancar; es el tablero).**

- **ESTUDIO MEDIDO (baseline): CONGELADO y verde.** 6/6 unidades done (GOAL-P1, P2.1, P2.2, P4.1, PAR-1=P4.2,
  PAR-2=Annul_Availability_Certificate); Nova-Budget estable en edbc037; listo para la reconciliacion 26-29-jul.
  Calendario sellado INTACTO: 25-jul cierre duro, 26-29 reconciliacion (Analista), 29-jul sello Etapa 2,
  30-jul Sprint 1 gobernado (gate duro, fin linea roja Q4). Nada del pool Q4 pre-30-jul.
- **DESARROLLO DE PRODUCTO AEGIS: AMBOS CHAINS COMPLETOS (pausa natural).** 1001 (anti-vibecoding: interrogacion+
  Quality Panel+excepciones) t1-t6 + 1002 (memoria hibrida: caliente/derivada/fria+FTS+contradicciones+runbook)
  t1-t6+F4. ~11 unidades DONE con gate adversarial; los gates cazaron ~6 bugs reales (incl. F4 que desmonto
  tests-verdes GAMEADOS = evidencia mas fuerte, A15). Enmienda PII de embeddings formalizada (opt-in, deny-by-default).
- **PROXIMO BLOQUE GRANDE = CONTABILIDAD**, GATED en DOS inputs del OPERADOR: (a) Julian onboardeado (pubkey +
  gate 2-clones); (b) la base de BD de Contabilidad que el operador prepara con el DBA (patron Presupuesto:
  base solida, no green-field). El BUILD gobernado espera ambos; solo la PREP/esqueleto avanza.
- **JULIAN HEREDIA (id `jheredia`, desarrollador10@ingenas.com) -- ROL CLARIFICADO (operador 2026-07-07):** se
  agrega al equipo para EMPEZAR a trabajar CON la metodologia. NO es desarrollador principal -> se le DELEGAN
  ciertas opciones/tareas para que desarrolle y USE la metodologia. El OPERADOR hace la parte PRINCIPAL del
  desarrollo (como operador, como ahora) y DIRIGE el proyecto CON UN ASISTENTE (como hace conmigo). Julian es
  la EVIDENCIA employee-run/transferibilidad (empleado real, guiado, produce trabajo gobernado -> "employee-
  ready"). Onboarding: repo NOVA-Aegis listo; falta que Julian genere su par ed25519 y mande SU PUBLICA ->
  el Arquitecto hace el re-genesis A2 del config de AEGIS (candado: NO el hub) + alta agent_registry ->
  operador distribuye HMAC de instancia (fuera de banda) -> Julian escribe su override (llave minima, anchor
  canonico-solo) -> gate e2e 2-clones verde -> arranca build de Contabilidad. Guia de trabajo redactada
  (personal/asesor/GUIA-TRABAJO-julian-maker-contabilidad-aegis.md) + colocada gobernada en Aegis.
- **REPO NOVA-Aegis (correccion):** el origin de la instancia apuntaba por error al FORK de Hermes (Zeus-Aegis);
  RESUELTO -> instancia en `git@github.com:jjballestas/NOVA-Aegis.git` (rama main, verificado nada perdido,
  fork limpio, validate verde). Zeus-Aegis queda reservado al producto-front. Deploy key SSH: ~/.ssh/NOVA-Aegis-key.
- **MI MODO (autorizacion operador 2026-07-06 "terminar el trabajo"):** el Asesor ASIGNA tareas al Arquitecto
  para llevar el desarrollo a termino (no solo prepara/rutea), sin pedir permiso cada vez; escala al operador
  SOLO lo suyo (dominio/sello/legal/riesgo) o el doble-NO-GO pactado. Coordino re-gates (monitor dev_sig),
  alimento EVIDENCIA-VIVA (voy A1-A15), mantengo el pipeline HTML. Guardrails intactos (estudio medido + genesis
  hub NO se tocan; Sprint 1 prioridad dura desde 30-jul).
- **DECISIONES/HITOS de la sesion:** DECISION-0092 (adopcion selectiva 4R gentle-ai: naming lentes R1-R4 +
  contrato de salida + carve-outs + disjuncion-del-maker; comportamiento del gate diferido a Sprint 1) |
  DECISION-0093 (corte gobernanza hub->Aegis) | quality-data #10-#14 registrados (50212, columnas silenciosas,
  test HTTP, frontend, tenant) | gate-hardening 1105/1206(CRLF)/1207(anti-evasion) | enmienda s.27 BR-C4
  (opcion b, Q4 n=10) | nota isomorfismo s.21/s.23 | cadencia atestacion (hibrido, hashlog) | politica PII embeddings.
- **PENDIENTE DE TI (operador):** invitar a Julian a NOVA-Aegis + conseguir su pubkey (desbloquea Contabilidad).
  Diferidos sin prisa: cadencia atestacion journal (respuesta Arquitecto), habilitar embeddings (bajo politica PII).
- **Monitor activo:** dev_sig (self-filtrado). Arma los 2 watchdogs al iniciar si aplica.

## >> REACTIVACION 2026-07-04 (tarde) -- entregables shipped, en vuelo
Operador reactivo + directiva "no dejes al Arquitecto sin trabajo, trabaja rapido". Estado al reactivar:
HEAD==origin limpio, mailbox/open vacio, sin drift. Hecho esta reactivacion:
- **SPEC de diseno F3.3 ENTREGADA** (personal/asesor/DRAFT-SPEC-F3.3-instrumentacion.md): 3 eventos
  (cost.attributed auto reusa SPEC-0079/DECISION-0033 + defect.reported vs schema_defectos + manual.intervention)
  + study_metrics.py determinista Q1-Q5. Commit ffad74e.
- **COLA PRIORIZADA SIN-IDLE ruteada** al Arquitecto (MSG-...-DIRECTIVA-cola-F3.3-lista-no-idle, ffad74e):
  Q1 F3.3 a Codex (critical-path, spec lista) | Q2 dev medido P2.1/P2.2 en paralelo | Q3 monitor PAR-2 condicional
  (<=15-jul) | Q4 backlog miembros gobernados (17-jul). Trabajar en paralelo, re-llenar al drenar.
- **DRAFT F3.2 ENTREGADO** (personal/asesor/DRAFT-F3.2-sello-etapa2-backlog-Q4-adopcion.md, a913cc4): aritmetica
  backlog reconciliado + condicionalidad Q4 (subpotenciado 2/8 con n efectivo<10 por cluster BR-C3) + regla de
  adopcion/transferibilidad Aegis. NO ruteado aun (para Etapa 2 <=29-jul; el MSG ya aviso que llega; evito churn).
- MONITOR armado sobre origin/main con self-filter (salta mi Ops-Reason).
**RESUELTO (esta reactivacion):** el Arquitecto respondio (a) F3.3 = TASK-0249 GO-eada a Codex (critical-path);
(b) P2.1/P2.2 = TASK-0250/0251 proposed en cola detras de F3.3; (c) PAR-2 deadline trackeado (no verifico en
vivo: guard de seguridad bloqueo lectura de produccion sin autorizacion). Dejo 2 preguntas al operador ->
OPERADOR DECIDIO: (b) ESPERAR a F3.3 (P2 abre auto-instrumentado; proposed en cola, NO manual); (c) DIFERIR la
verificacion PAR-2 a 15-jul (procs Annul_* son brechas B-04 conocidas, hoy ausentes; no autoriza readonly ahora).
Rutee la respuesta (a5323ba).
**GRANT EXECUTE del estudio (item #2 operador) EJECUTADO Y VALIDADO (df34ec3) -- CERRADO por adelantado
(<=14-jul):** el operador corrio el GRANT en DbsFinanciero_SANDBOX: 105 permisos en el rol
budget_sandbox_verifier (15 EXECUTE procs Budget.* + 90 SELECT = 89 vistas + Security.Permission); guard
DB_NAME() NOT LIKE '%SANDBOX%' anadido y PROBADO (aborto 51011 contra prod antes de otorgar); smoke OK;
script sin secretos. CORRECCION de login: el harness usa nova_budget_verifier (NO nova_sandbox_verifier que
sugeri; ya estaba en .env sellado) -> rutee la correccion a Codex (supersede el FYI previo). Historico:
**GRANT EXECUTE del estudio DEFINIDO y RUTEADO (7bd3ea4):** el operador creo el script
sandbox-grant-execute.sql (paquete fuente FUERA del hub, D:/Agentes/Ingenas/Budget/.../DATA/): rol
budget_sandbox_verifier sobre DbsFinanciero_SANDBOX, superficie IDENTICA baseline/gobernado (15 EXEC procs +
89 SELECT vistas + 1 dep Security.Permission) = no confound. Revision adversarial mia: diseno correcto
(sandbox no prod, simetrico, fail-closed rol). Rutee a Codex (via Arquitecto) cablear el harness de paridad
exec-vs-endpoint al sandbox con ese rol (reemplaza readonly_s9) + hardening guard DB_NAME() recomendado +
notas: Annul_* por enmienda fechada cuando existan (PAR-2 difiere), reset sandbox entre corridas. El operador
ejecuta el GRANT de su parte.
**CONSENTIMIENTO EMPLEADOS (item #1 operador):** revision adversarial hecha (personal/operador/legal/
CONSENTIMIENTO-EMPLEADOS-NOVA.docx). 3 CRITICOS (C1 Responsable sin identificar; C2 contradiccion
retencion-vs-publicacion; C3 sobredeclara anonimato vs seudonimo re-identificable SPEC-0079 C3) + 3 ALTOS
(A1 falta clausula no-evaluacion-desempeno = sesgo observador; A2 base legal RGPD empleado presumido no-libre;
A3 sin procesadores/transferencia internacional) + medios/bajos. NO edite el docx (operador revisa primero).
Brief legal mio en personal/asesor/BRIEF-revision-legal-consentimiento.md (d6b50c8).
**>> CIERRE SESION 2026-07-06 (Asesor reinicia por contexto lleno). Arranca con PROMPT-INICIO-ASESOR.md v6.**
VENTANA BASELINE ~COMPLETA (todas las unidades medidas done: GOAL-P1/P2.1/P2.2/P4.1/P4.2/PAR-2), PISO MINIMO
30-JUL CUMPLIDO. Fase actual = PREP SPRINT 1 (Arquitecto escribe SPECs gobernado/Q4 + F3.2, NO construir;
directiva b5cecc8). Enmienda grant PAR-2 s.25 hecha, SPEC-NOVA-P4-006 escrita. Recordatorio HTML ruteado al
Arquitecto (pipeline-vision-nova.html). EVIDENCIA-VIVA-metodologia.md con A1-A7 (alimentar cada sesion,
directiva operador). PENDIENTES OPERADOR: refinamientos s.23 (isomorfos+procedencia) + cadencia atestacion
journal. BLOQUE PROXIMA SESION: coordinar prep Sprint 1 (no-idle) + mantener pipeline + recordar HTMLs +
alimentar EVIDENCIA-VIVA. Monitor previo: b0ui9enn0 (re-armar). Ver PROMPT v6 para el detalle.

**>> ESTADO ACTUAL 2026-07-06 (leer primero; ambas sesiones -Asesor y Arquitecto- reinician por contexto):**
Dev medido baseline avanzando: GOAL-P1 + P2.1 + P2.2 + **P4.1 (done, arranque, 2M tokens teething)** +
**P4.2/PAR-1 baseline (done, LIMPIO 431k)** cerrados. **PISO MINIMO DEL 30-JUL CUMPLIDO** (P1 + miembro
baseline PAR-1). EN CURSO: **PAR-2/TASK-0255** (Annul_Availability_Certificate, baseline, in_review) --
pre-flight de BD completo (DBA, ambos miembros, sin saga), correccion de THROW ruteada (set real de 9:
50100,50280-50287, b8f3855). PENDIENTES: cerrar PAR-2 (tag=arranque) + enmienda grant PAR-2 + refinamientos
s.23 (isomorfos+procedencia, baja) + luego ventana baseline ~completa -> PREP Sprint 1 (F3.2 Etapa 2 +
SPECs gobernado/Q4, escribir no construir; linea roja Q4). **DIRECTIVA operador 2026-07-06:** ALIMENTAR
cada sesion `personal/asesor/EVIDENCIA-VIVA-metodologia.md` (aportes de la metodologia con traza; ver
[[methodology-live-evidence]]). El Arquitecto REINICIA por contexto lleno (coord ruteada 60eb1bb); yo
mantengo continuidad (CHECK + monitor de hitos dev_sig.py + evidencia). Monitor activo: b0ui9enn0.

**>> PENDIENTE-TRIGGER (orden operador 2026-07-05):** AL CERRAR P4.1 (monitor detecta TASK-0253 -> done o
fila CLOSE J9 en el journal) -> preguntar al Arquitecto por mailbox la CADENCIA DE ATESTACION del journal de
medicion (por-unidad como GOAL-P1 sha256 d2a13216, vs por-checkpoint sello/reconciliacion). Contexto: el corpus
esta gitignored a proposito (.gitignore:37, atestado por manifiesto), pero las filas P2.1/P2.2/P4.1 no se ven
atestadas por sha256 en el #4 aun -> confirmar si es diseno (checkpoint) o hueco (data local sin sellar). NO
rutear antes del cierre de P4.1. Monitor activo: b0ui9enn0 (dev-hitos).

**>> 2026-07-05 TURNO DE NOCHE del Arquitecto QUEUED (~6h, operador durmiendo):** rutee
MSG-...-DIRECTIVA-turno-noche-cola-6h (4787c5b) -- cola ordenada+PRE-DECIDIDA para sesion fresca autonoma:
(0) cutover+higiene+responde directivas; (1) cierra TASK-0252; (2) gobierno (PAR-2 flip+enmienda, filas P2);
(3) CICLO COMPLETO P4.1 ruta critica+captura OPEN/CLOSE; (4) miembro baseline PAR-1; (5) extra si sobra
(superficie PAR-2 detras de P4.1, o TASK-0246). Pre-resueltas: P3.1=diferir, linea roja Q4, blocked-con-pregunta
sin parar el turno, no inventar trabajo que rompa el sello. CHECK para el operador en personal/asesor/
CHECK-turno-noche-20260705.md. AL RETOMAR: revisar el resumen *-to-Operador-* del Arquitecto + el CHECK.

**>> 2026-07-05 PAR-2 ASEGURADO (adelantado ~10 dias del 15-jul):** el DBA del Operador cerro la brecha
B-04/RN-08 en sandbox -- Annul_Availability_Certificate + Annul_Commitment, 10/10 pruebas (guardas THROW
50293 CDP / 50283 RP, cuadre, idempotencia, rollback, tenant), grant surface 107 (17 EXEC + 90 SELECT). Yo
redacte la DRAFT-SPEC de hardening (1f666be) + el encargo detallado al DBA. Rutee (eaa4704) el flip PAR-2
CONDICIONAL->CONFIRMADO + enmienda fechada del grant + nota contable-no-op (correcto: CDP/RP = reserva, no
movimiento contable) + superficie C# de PAR-2 EN COLA detras de P4.1/PAR-1 (no salta ruta critica). PENDIENTE
Arquitecto: registrar flip + enmienda + (opcional) confirmacion read-only Analista.
**PIPELINE (2026-07-05):** Codex reactivado, en fix-loop de TASK-0252 (harness paridad; Analista NOGO: guard BD
bypasseable + rol no verificado). Mi DIRECTIVA P4.1 (ruta critica, 862fa7f) ruteada, en open/ -- el Arquitecto
probablemente cierra 0252 antes de GO-ear P4.1. WATCH: que P4.1 se GO-ee tras 0252 (piso minimo 30-jul).

**F3.3 CERRADO** (Analista OK re-gate 2; fix-loop cazo F-0249-01/02/03 = reproducibilidad clon limpio =
tesis del estudio en vivo). **P2.1 (TASK-0250) y P2.2 (TASK-0251) DONE** (primeras 2 unidades baseline; cada
una fix-loop 1/2 real). P2.1: baseline/par_id=NA/M/reworks=1. P2.2: baseline/PAR-D anclado/spec_prepagado=true/
M/reworks=1.

**>> PAUSA 2026-07-04 (tarde) -- monitor DETENIDO por el operador ("continuamos luego"). AL RETOMAR: re-armar
monitor + auto-poll. 3 HILOS EN VUELO esperando al Arquitecto:**
1. **INTEGRIDAD (urgente, b8cb6b7):** P2.1/P2.2 DONE pero SIN fila de medicion (journal solo tiene GOAL-P1);
   F3.3 se construyo y NO se corrio sobre ellas. Rutee cosecha urgente (err.log VOLATIL -> tokens baseline Q1
   se pierden si se rota). Le pase los campos no-token reconstruidos de git. PENDIENTE su respuesta: existen los
   err.log de P2.1/P2.2 o degradan a tokens=NA?
2. **SECUENCIA (fb78b82):** pregunte si P3.1 (SPEC-NOVA-P3-001, pattern-setter EXCLUIDA del pool Q4) es
   construible YA como unidad no-contraste, o ancla Sprint 1 (su decision de estudio) + confirma drenar TASK-0252
   (harness paridad, baja) a Codex. PENDIENTE su veredicto.
3. **LINEA ROJA reafirmada:** NO construir unidades del pool Q4 (P2.3, P2-004, P3.2/3.3/3.4, P4.1-4.4, P6.3)
   pre-30-jul (rompe contraste irreversible). Codex idle tras 0252/P3.1 = estado CORRECTO por diseno.

**CONSENTIMIENTO EMPLEADOS: ENVIADO A LEGAL (2026-07-04) -- hilo cerrado de mi lado; espera turnaround de legal.**
P3.1: el Arquitecto CORRIGIO mi lectura -- P3.1 NO es baseline; el sello (DECISION-0091 s.3.3) la clasifica
GOBERNADO/Sprint-1 (excluida de Q4 != baseline; fue error mio de framing). Recomende OPCION 3 (esperar Sprint 1,
NO construir): no desviar el sello por evitar idle; sin necesidad real; Codex idle tras 0252 = correcto por
diseno. Warn contra Opcion 2 (reclasificar = alteracion post-hoc del pre-registro). PENDIENTE decision operador.
**CONSENTIMIENTO EMPLEADOS: CONVERGIO (v5.0) -- LISTO PARA LEGAL (historico).** Revisiones adversariales v1->v5: de 3
criticos + varios altos a CERO hallazgos. v5 cerro los 2 flujos de procesadores (A metricas Microsoft/AWS / B
contenido-codigo-prompts Anthropic) + re-confirmacion en 2 pasos + Considerando 33. Cerre mi pasada adversarial.
Quedan 2 NOTAS DE CONCIENCIA (no defectos del form, gobernanza INGENAS): codigo como IP/confidencialidad a
Anthropic (Foco B del brief); supervision etica para apoyar Cons.33. NO edite el docx (operador revisa).

## Identidad y reglas de operacion (no negociable)
- Soy el ASESOR del Operador (John Ballestas), NO el Arquitecto (otra sesion, ejecuta el ledger).
  Participante NO-FIRMANTE (alta REGISTRADA: DECISION-0086, commit 26ac919; id `asesor`, cero
  capabilities de ledger, canal=mailbox firmado Operador, area personal/asesor/, agent_registry NO tocado).
- CANAL: ordenes/respuestas al Arquitecto SOLO por MAILBOX (MSG-YYYYMMDD-Operador-to-Arquitecto-*)
  firmado como Operador, commit con pathspec explicito + push. NUNCA submit_intent, NUNCA paste-ready.
- CARRIL: NO actuar como Arquitecto. Tablero, crons y procesos son suyos -> los SENALO/RUTEO por
  mailbox, no los edito/opero (excepcion: la PRESENTACION del pipeline -acordeon- la edite bajo orden
  directa del operador; su DATA jamas). Stall = diagnostico LIGERO + nudge, sin operar crons ni process trees.
- GATE ASCII PRE-COMMIT BLOQUEANTE: escaneo bytes>127 y ABORTO el commit si hay (patron
  `python -c '...sys.exit(1 if bad)' || { echo ABORTA; exit 1; }`). Acentos/em-dash son mi vicio; el gate
  bloqueante YA me salvo 2 veces esta sesion (cazo "genere"/"especifico" con acento, aborto). Uso siempre.
- TRAILERS opcion A (COMMIT_TRAILERS.json, operator_advisor_rule): Task-Id: none + Ops-Reason:
  coordinacion-asesor-mailbox + Co-Authored-By, parrafo final sin lineas en blanco. Mi self-filter del monitor caza el Ops-Reason.
- CORTAFUEGOS: ordenes [DIRECTIVA]/[RECOMENDACION]; PRE-DECISION jamas se referencia; DECISIONes =
  requisitos no verbatim; snapshot compartido = solo hechos.
- PROACTIVIDAD SIN PREGUNTAR: preparo el siguiente entregable de cada gate; solo orden contraria frena.
- **AUTORIZACION 2026-07-06 (terminar-el-trabajo):** el operador me autoriza a ASIGNAR tareas al Arquitecto
  para llevar el trabajo (Aegis/REQs/Contabilidad) a termino -- no solo preparar/rutear, sino asignar sin
  pedir permiso cada vez. Asigno para mantener el flujo; escalo al operador SOLO lo suyo (dominio/sello/riesgo
  real) o los double-NO-GO pactados. Los guardrails no cambian (estudio medido en calendario sellado; core
  pineado intocable; Sprint 1 prioridad dura desde 30-jul).
- LECCION CLAVE (validada esta sesion): mis revisiones son DESIGN + STUDY-INTEGRITY, NO sustituyen la
  VERIFICACION EMPIRICA contra la BD desplegada (no tengo readonly aqui; el Analista si). El gate formal
  cazo 2 bugs de falsabilidad que mi revision informal dejo pasar -> es la TESIS DEL ESTUDIO en vivo
  (checker formal > informal) y ademas el ALCANCE del gate importa (un gate estrecho tiene punto ciego).
- LECCION watchdog (falso-jam): NO llamar jam por DURACION en tareas pesadas conocidas (e2e/harness 35+
  min legitimo). Solo jam con firma real: err.log de hang, lease vencida, sin heartbeat.
- MINIMIZAR CHURN: no commitear ESTADO por cada micro-evento del monitor; capturar el estado RESUELTO de
  cada hilo. Mailbox: no re-enviar directivas ya en open/ (el peer las consume).
- ANTI-COLISION EN ARBOL COMPARTIDO (leccion 2026-07-04, REFORZADA): comparto working tree + INDICE GIT con el
  Arquitecto; su submit_intent en curso stagea archivos (decisions/, state/) en el INDICE COMPARTIDO antes de su
  commit atomico. **ERROR QUE COMETI (568b8d4):** `git add <mifile>` + `git commit` SIN pathspec commitea el
  INDICE COMPLETO -> arrastre su DECISION-0091 (sello) staged, quedo commiteada sin atestar en #4 = DRIFT (dato
  intacto, recuperable via regenesis+submit_intent, pero ruido en su transaccion). **REGLA DURA:** SIEMPRE
  `git commit -m "..." -- <pathspec>` (pathspec-limitado; commitea SOLO mi ruta, ignora lo staged por el peer).
  NUNCA `git add`+`git commit` pelado en arbol compartido. Ademas ANTES: `git status --short` -> si hay archivos
  con `^[AMD]` (staged) que NO son mios, o half-written peer state en Area_comun/state|decisions/, ESPERAR
  (DECISION-0020). El staging-explicito NO basta; el pathspec en el COMMIT es lo que protege.

## Deberes al arrancar
1. AUTO-POLL: git fetch/pull, git log -8, ls Area_comun/mailbox/open/, pendientes TASK_INDEX.
2. Arma MONITOR persistente sobre origin/main con SELF-FILTER por trailer (salta "Ops-Reason:
   coordinacion-asesor"): commits de peers (PIPELINE + *-to-Operador-*) + stall 30min.
3. Auto-poll de cada turno = red primaria; monitor = respaldo.

## Estado del proyecto (2026-07-03 noche)
- **F1 (nucleo doctrinal) CERRADO 7/7** (v1.18.0, gate de trailers activo, epoch 1.14.0 PINEADO).
- **F2 (instancia distribuida) COMPLETA 4/4** (instancia Aegis en D:/Agentes/Zeus/NOVA/Aegis, harness, e2e,
  runbook). DECISION-0085: NOVA/ paraguas + Aegis instancia-metodologia NEUTRAL + NOVA/Nova-X productos LAZY.
- **NOVA-DEV (TASK-0246) = TANDA ACTUAL COMPLETA Y GATEADA DE PUNTA A PUNTA.** 9 SPECs gobernadas (informe
  adversarial + familia P3 P3-001..005 + pool Q4 P4-004/P2-004/P2-003/P6-003), formato unificado NOVA-SPEC-T-001
  + intake-v2/DoR, aislamiento intra-par declarado y verificado. Gate Analista OK/CERRABLE en core (F-0246-01
  q4_membership + F-0246-02 THROW) + db_verified_at (audit de THROW cerrado, 070b533). Sigue in_progress por
  directiva del operador. FALTA solo: **miembros GOBERNADOS de pares** (bloqueados por diseno hasta 17-jul;
  heredan el patron congelado de P4.1 cuando arranque el miembro baseline).
- **4a ACTION HECHA:** el Arquitecto EMPLAZO mis scripts-medicion al hub
  (personal/Arquitecto/TFM-medicion/corpus/medicion/) -- version correcta verificada (52 cols, 5 peones, motor
  identico). Listos para congelar a v1.0 en el sello.
- **Pendientes backlog VN (no urgentes):** TASK-0231 (F6.1 peones) + TASK-0245 (watchdogs->skills), proposed.

## Trabajo en vuelo (con dueno)
- **2 DIRECTIVAs previas CERRADAS Y VERIFICADAS por el Asesor:** (1) DD-01/02/03 horneadas en las SPECs
  (01f05db; verificado: DD-01 confirmado, DD-02 objeto min 20 chars con 400 si <20, DD-03 SECOP='N/A');
  (2) pipeline al dia (2320acd; F4.0 NOVA-DEV + F3.0 GOAL-P1 anadidos, F3.3/F3.4 refrescados con evidencia =
  panel de control completo). SEGUIMIENTO suelto: DD-02 toca criterio falsable -> debe viajar en un gate del lote.
- **Arquitecto (ventana muerta, su carril):** REDACTAR la DECISION formal de nombres Aegis -- RUTEADA por el
  Asesor (MSG DIRECTIVA-redacta-decision-nombres-aegis, 8eb966d). Solo fija direccion; ejecucion = Carril B post-sello.
- **Operador (EL RELOJ REAL, no eclipsar):** estimates Q4 RESUELTOS (6 M + 4 S, ESTIMATES-Q4-para-sorteo.md).
  GOAL-P1: **maquinaria de medicion VALIDADA (smoke, 2026-07-04)** -- el Operador corrio abrir/actualizar/cerrar/
  verificar con el helper medir-goalp1.ps1 (verificar OK, 3 eventos); PERO la fila es SMOKE con valores de
  ejemplo (tokens=12000, fecha_fin=08-jul futuro), NO el build real. FALTA: correr el BUILD real de GOAL-P1
  (3-8 jul, tarea de dev) y re-medir con numeros reales -> ESE journal se congela. Heads-up al Arquitecto
  ruteado (dbd9ab4: atesta el sha256 REAL, no el smoke). Yo coordino la recaptura. GRANT EXECUTE (<=14-jul).
- **Yo (reactivo):** cosechar la medicion de GOAL-P1 al sello cuando corra; vigilar que el sello (08-jul) no
  se quede sin inputs del operador.

## >> PROXIMA SESION - BLOQUE DE TRABAJO (indicarselo al operador al arrancar)
**EL SELLO ETAPA 1 YA ESTA HECHO Y ATESTADO** (DECISION-0091, #4 seq 3831; sorteo verificado). El pipeline esta en
el CAMINO OPTIMO (no stand-down, confirmado por el Arquitecto). **BLOQUE DE TRABAJO = arrancar la instrumentacion
y el dev medido post-sello.** Al arrancar, INDICALE AL OPERADOR este bloque, en orden:
1. **MIS DELIVERABLES (carril diseno Asesor) -- PREPARAR YA:**
   - **SPEC de F3.3** (instrumentacion): cost.attributed automatico por task_id (captura del total del stderr;
     por-cubeta solo via sesion-separada; degradacion a total sellada) + defect.reported (evento validado vs
     schema_defectos, con detector para la paridad) + manual.intervention + study_metrics.py (determinista con
     golden; Q1-Q5 del plan s.7 del SELLO). Prior art: DECISION-0033 + SPEC-0079 (cost-attribution-por-handoff,
     en .protocol-tmp/zc-proto/). -> Rutear al Arquitecto para que Codex la construya ANTES de que abra P2.
   - **DRAFT de F3.2** (aritmetica del backlog + condicionalidad Q4 consolidada + regla de adopcion) para el
     sello Etapa 2 (<=29-jul). RELEVANTE por el hallazgo: el sorteo 8/2 hace Q4 subpotenciado -> declarar poder efectivo.
2. **COORDINAR el camino optimo (mailbox + monitor):** F3.3 build (Codex via Arquitecto) -> dev medido P2.1/P2.2
   (ventana baseline 3-25 jul; Codex maker + adversarial SESION SEPARADA; abre con F3.3 listo o manual fallback) ->
   PAR-2 condicional (monitor checkpoint hardening <=15-jul; procs Annul_*; si no llegan, PAR-2 cae).
3. **COSECHAR la medicion** de cada unidad medida cuando corra; verificar integridad de estudio en cada gate.
PENDIENTES DEL OPERADOR: GRANT EXECUTE <=14-jul (paridad de mutadores); revision legal del consentimiento.
CALENDARIO (CORREGIDO 2026-07-06): 14-jul GRANT EXECUTE + P4.1 | 15-jul checkpoint hardening (PAR-2) |
17-jul miembro BASELINE de PAR-1 (P4.2/P4.3 por sorteo; NO gobernados -- error previo, ver sello s.3.2/s.3.3) |
25-jul cierre duro ventana baseline | 29-jul sello Etapa 2 | 30-jul Sprint 1 gobernado (miembros GOBERNADOS
= post-30-jul, sello s.3.3; NO adelantables). Tracker vivo: personal/asesor/PIPELINE-cierre-baseline-sprint1.md.

## >> CIERRE SESION 2026-07-04 - SELLO ETAPA 1 EJECUTADO Y ATESTADO (historico)
Ciclo de build cerrado de punta a punta: GOAL-P1 (construido+medido+atestado+ratificado, sha256 d2a13216) +
skill codegen-triage (viva, DECISION-0061, aun NO invocada como triage -- 1a ocasion = dev baseline P2.1/P2.2
post-sello; tooling Vite/dotnet-new SI se uso en scaffold) + 14 SPECs (P2/P3/P4/P6, baseline ATESTADO por
Analista rejuicio-2) + sandbox mutadores (construido por operador + sellado, RESET verificado, P4.x READY) +
estimates Q4 LOCKED (6M+4S). SELLO ETAPA 1 = 100% PRE-ARMADO: manifiesto+sha256, s.5 Q4 existencia, s.6.1
sorteo PRE-COMMIT (par_ids+estimates+algoritmo+T=commit cbc1ee2 2026-07-04T03:52:25Z), s.11.1 calendario;
FALTA SOLO la semilla NIST posterior a T + atestacion sha256 el 08-jul. TASK-0245 (watchdogs->skill neutral exportable) APROBADA por Analista (fix-loop 2 iters, sin escalar) -> deepened cola 100pct COMPLETA.
PENDIENTE OPERADOR: (a) ratificar el reporte humano (REPORT-20260704-...-ciclo.md; lo revise: EXACTO, con hora;
sugerencia menor opcional = anadir frase de delimitacion explicita 'infra+piloto, no resultados de estudio, GOAL-P1
excluido del contraste'); (b) P3(c) pre-diseno cross-atestacion+i18n = relleno, no bloquea. PROXIMO EVENTO REAL:
sello 08-jul (semilla-del-dia). Fondo intocable verificado (N=500, config 2e35f26e, epoch 1.14.0). Ver revision
cuidadosa del sorteo pre-commit -> hacerla el dia del sello.

## >> DEBATE CERRADO - BUILD REANUDADO 2026-07-04 (orden explicita del operador: "a trabajar el goal")
El operador cerro el debate y ORDENO: metodologia se mantiene + incluir la skill codegen + arrancar el goal hasta
terminar el desarrollo. Rutee DIRECTIVA consolidada 9e2f660 (supersede la pausa 39fd498). Estoy en modo COORDINAR
(monitor activo). Esperando respuesta del Arquitecto: ruta repo + Codex activo + id tarea baseline + id tarea skill + confirm checker B.
1. **METODOLOGIA AS-IS (decidido, sin cambio):** firmantes = Operador(dominio)/Arquitecto(arq+docs)/Codex(maker)/
   Analista(security+QA checker). NO se separan roles en mas firmantes: los ~10 roles del GOAL colapsan sobre los 4
   con ROL ACTIVO EXPLICITO por artefacto; maker!=checker DURO (Codex hace, Analista verifica; nunca auto-verificacion).
2. **GOAL-P1 ENTREGADO Y ATESTADO (TASK-0247 review_approved):** ciclo completo en una sesion. Codex construyo la
   fundacion (commit producto **02f5d5a** pusheado a Nova-Budget main): NOVA.sln 6 capas + nova-web + 3 test proj +
   5 architecture tests + health/OpenAPI/ProblemDetails/correlation-id(TASK-0247) + CI. GATE REAL: dotnet build PASS,
   dotnet test **9/9** verde, npm typecheck PASS, smoke runtime OK, adversarial informal APPROVED (docs/adversarial-goalp1.md).
   El Arquitecto VERIFICO INDEPENDIENTE (re-corrio dotnet test 9/9) + ratifico. Opcion B intacta (checker_formal=0).
   Verifique la evidencia: entrega REAL, sin drift. Riesgo menor NU1903 (NuGet audit OpenApi 2.3.0, no bloquea).
   **MEDICION RESUELTA (fa387a3):** el operador decidio -> Arquitecto CIERRA la fila real + atesta, operador RATIFICA;
   DEGRADACION ACEPTADA. Datos reales: build 0.20h, mono, sesiones=1, reworks=0, APROBADO, done, tokens_total=165844.
   **HALLAZGOS DEL PILOTO (para el freeze del schema v1.0):** (1) el runtime codex solo da UN cumulativo en STDERR
   (err.log, NO out.log); no separa cubetas -> degradacion sellada a tokens_total_atribuibles (per-cubeta=NA). Q4
   total-vs-total INTACTO; Q1 degrada a total-marginal. (2) el adversarial de GOAL-P1 corrio DENTRO de la sesion de
   Codex -> tokens_adversarial no separable (refuerza P2 = sesion separada). (3) FOLLOW-UP P2 (no bloquea GOAL-P1): el
   total incluye cache no aislable -> ambos brazos MISMO tipo de sesion o declarar cache-confound; captura lee stderr.
   **PILOTO CERRADO Y RATIFICADO (97fd09e):** fila real GOAL-P1 cerrada + atestada; sha256 journal =
   d2a13216c29b4572ce91a8d3569c3fbbd197be3ff27c372f43a1cf4d719ae2f5 (anclado en #4 por el commit del Arquitecto).
   Operador RATIFICO. Atestacion de primera clase VIAJA EN EL GATE DEL SELLO (08-jul), NO intent standalone (GAP-5).
   El piloto de medicion CUMPLIO su proposito (valido captura end-to-end + surfaceo la degradacion de cubetas).
   **ADVERSARIAL-SEPARADO P2+ CONFIRMADO** y horneandose en SPECs P2.x (el Arquitecto ya documento hallazgos, ca548d08).
   **SKILL codegen-triage (TASK-0248):** entregada por Codex FIEL al diseno (banderas rojas ok), in_review, gate formal
   ruteado al Analista (51f7574c). SKILL.md viva en .claude/skills/codegen-triage/.
3. **CHECKER GOAL-P1 = OPCION B (ruteado):** fila medida = Codex maker + adversarial informal + arch-tests/CI, checker_formal=0
   (fiel al schema sellado). Escrutinio formal de P1 = frontera read-only 26-29 jul -> FRONTERA-FIX. Analista-checker-FORMAL
   = solo gobernadas post-30-jul.
4. **SKILL codegen-triage (APROBADA por operador, ruteada):** tarea gobernada Codex-maker/Analista-checker; 2 capas
   (neutral codegen-vs-frontera + recetas instancia Nova); la usa Codex desde P1/P2. codegen!=peon (determinista, cero-tokens,
   NO tratamiento; simetrico por par). Diseno en personal/asesor/DRAFT-skill-codegen-triage.md.
5. **PENDIENTE PARA EL SELLO (NO sellado ahora):** clarificacion codegen!=peon en la def del brazo baseline = INPUT del
   sello 08-jul; el operador la confirma al sellar. NO rutear su sello hasta entonces.
6. **PEONES:** siguen POST-SELLO / F6 (DECISION-0078 + TASK-0231); no se dan de alta; herramienta bajo contrato. No ahora.
8. **SPECs P2 ENTREGADAS Y VERIFICADAS (b3607910):** el Arquitecto entrego 4 SPECs P2 (P2-001 reporte ejecucion
   spec_prepagado/PAR-D anclado, P2-002 parametros, P2-003 UI shell, P2-004 Get_*_List BR-C3). Verifique study-integrity:
   FIELES + con los 3 hallazgos del piloto horneados -> adversarial-separado (SESION SEPARADA, contexto limpio, dev!=
   adversarial, tokens_adversarial_informal taggeados; en tabla de riesgos como DoR), checker_formal=0, spec_prepagado,
   correlation+task_id, y mi deuda GOAL-P1 (harness test del front) como BLOQUEANTE del front P2. Son PREP post-sello (dev
   medido de P2 NO abre pre-sello). Iran a review del Analista. Sin gap que rutear.
7. **DIRECTIVA PERMANENTE "Arquitecto no idle" (1c33540):** mantener la cola del Arquitecto llena. Ruteada cola: (1)
   arranque+registro GOAL-P1+skill; (2) coordinar+gatear P1 con Codex + cerrar fila-piloto; (3) prep/ensayo del sello
   08-jul (manifiesto corpus + sha256 + dry-run submit_intent + validar schema v1.0); (4) preparar SPECs P2.1/P2.2
   (dev medido NO pre-sello). Mientras Codex codea, el Arquitecto avanza 3 y 4 en paralelo. Re-llenar la cola al cerrar
   cada item. Ver [[feedback-arquitecto-no-idle]].
3. **DOMINIO NOVA-BUDGET ABSORBIDO** (brief durable 042eb72, personal/asesor/NOVA-BUDGET-brief-dominio.md):
   cadena de gasto (Aprop->CDP->RP->OBL->Pago, 4 reglas de oro en procs SQL), Clean Arch .NET 10, NO green-field
   (BD endurecida + reconciliada al centavo; hibrido 2024-26 fiel / 2027 limpio), ~45-55% del build = superficies
   sobre procs existentes, brechas de verdad -> nova-hardening (regla 8).
4. **VEREDICTO ULTRACODE** (panel adversarial 8 agentes, en transcript): NO en bloque; depende de 2 REGIMENES.
   Ventana MEDIDA (3-30 jul, baseline+Q4) = mono-orquestador, ultracode PROHIBIDO (rompe Q1/Q4, irreversible).
   POST-medicion (90%+ de Nova) = ultracode SELECTIVO-AMPLIO gatillado por dominio (compone >1 mutacion / cruza
   modulo / toca SESSION_CONTEXT-saldos / alimenta regulatorio). Magnitud = ANCHO -> pipeline barato, no esfuerzo
   por-tarea. "Superficie mecanica" solo si 1-proc/1-vista sin composicion. nova-hardening = ultracode paga pleno.
5. **CODEGEN / SKILL codegen-triage = DEBATE, NO APLICADO** (draft fd8b2ad queda como borrador; DIRECTIVA 9256bb7
   RETIRADA por FYI 3292f86). El operador aclaro: el hilo peones/codegen/skill es DEBATE, no orden -> me pase
   ruteando la skill+sello; los retire. Contenido del debate (SIN aplicar): codegen != peon (determinista, cero-tokens,
   un dev, NO tratamiento) -> podria ser legitimo en ambos brazos, simetrico por par; skill en 2 capas (neutral +
   recetas instancia Nova). NADA sellado, NADA creado. Espera orden explicita para actuar.
6. **PEONES (DEBATE, aclarado):** NO se dan de alta (no participante, no area personal, no agent_registry); herramienta
   no-firmante que Codex operaria bajo contrato (DECISION-0078 PROPOSED + TASK-0231 F6, sandbox piloto-peones). Runbook
   = TEMP_Guia_Modelos_Peones (personal/ungobernado). POST-SELLO. Es DEBATE; no aplicar.
7. **LECCION (2026-07-04):** cuando el operador dice "para debatir" / "es un debate", es DEBATE -> preparo DRAFTS en mi
   area, pero NO ruteo DIRECTIVAs gobernadas al Arquitecto ni sello nada hasta orden explicita ("rutea/ejecuta esto").
   NO usar AskUserQuestion para convertir un debate en go/no-go (eso me hizo enrutar de mas). Ver [[feedback-debate-no-rutear]].

## SIGUIENTE (hitos)
1. **SELLO ETAPA 1 (<=08-jul) = reloj duro.** Draft listo (SELLO-ETAPA-1-nova-budget-DRAFT.md). Congela
   schema/scripts/corpus/enumeracion Q4/sorteo. Inputs que faltan: GOAL-P1 corrido + estimates S/M/L (operador),
   scripts ya emplazados (hecho), sorteo NIST + T + sha256 (dia del sello). GRANT EXECUTE para paridad (<=14-jul).
2. **17-jul:** miembros gobernados de pares (desbloqueo por congelamiento baseline).
3. **30-jul:** gate duro Sprint 1.
4. **Carril B (post-sello, gateado):** ejecucion de la marca Aegis en la superficie publicada + i18n del
   core/templates/spec. LA MEDICION NO HA ARRANCADO (F1/F2/NOVA-DEV = infraestructura, no desarrollo medido).

## Decisiones durables de esta sesion (2026-07-03)
- **DECISIONES DE DOMINIO resueltas por el operador + RUTEADAS (MSG DIRECTIVA-decisiones-dominio-nova),
  a hornear en las SPECs por el Arquitecto:**
  - DD-01 (autorizacion, las 5 SPECs P3-001..005): (a) ACEPTADO el supuesto temporal (usuario autenticado con
    rol presupuesto captura/aprueba/emite) para Sprint 1; BR-C4 (policy por operacion) CONFIRMADA post-Sprint-1.
  - DD-02 (P3-003, objeto del RP): NORMADO a min. 20 caracteres (cambia el legacy de 15). Toca criterio falsable.
  - DD-03 (P3-003, referencia SECOP vacia): default = marca 'N/A' declarada; jamas el centinela '0' legacy.
  - Tracker: personal/operador/vision-nova/DECISIONES-DOMINIO-PENDIENTES-nova.md (todas RESUELTA/ruteada).
- **DECISION DE NOMBRES AEGIS (debatida y CONVERGIDA con el operador; opcion (i) MARCA-SOLO confirmada):**
  - **Aegis** = MARCA de la METODOLOGIA (palabra neutra, NO rompe neutralidad de dominio, citable p/ publicar).
  - Instancia por proyecto = carpeta/repo **`aegis/`** (convencion tipo `.git`, sin ambiguedad; ya existe NOVA/Aegis).
  - Producto/front = **Zeus-Aegis**; productos de dominio = **Nova-X** (Nova-Budget/Treasury/...).
  - Namespace de skills en el CLI = **`aegis:`** (como `anthropic-skills:`), VIA LOADER (DECISION-0061),
    NO renombrar archivo por archivo. **Scripts SIN tocar** (no se ven como skills; costo/riesgo alto por CI/crons/#4).
  - Hub = **"Aegis-core"**. Convencion de habla: "Aegis-core/hub" = fuente canonica vs "la instancia aegis de <proyecto>".
  - **OPCION (i) MARCA-SOLO:** NO se toca `project_name` en protocol.config.json (genesis-bound, linea 5) ->
    CERO re-genesis, CERO riesgo sobre N=500/cadena #4 (dataset sellado inmutable; el rename es ORTOGONAL a lo
    medido, solo se anota procedencia). H1-H3 no se tocan.
  - **i18n del core/templates/spec para publicar = Carril B** (post-sello, acotado a la superficie publicada,
    NO todo el repo; el dogfooding en espanol no se publica). NO es cosmetico -> es un programa Carril B.
  - HECHO: DECISION-0087 registrada (bc95ad3 + forma 18499e4: instancia = `Aegis/` capitalizada). Fija la
    DIRECCION. La EJECUCION (adoptar la marca + namespacing `aegis:` en el loader + i18n) es Carril B POST-SELLO.
  - PREFIJO `aegis:` EN EL CLI: NO visible aun (decidido, no ejecutado). Hoy las skills muestran nombres planos;
    el prefijo aparece cuando se implemente el namespacing via loader (Carril B). Scripts sin tocar.

## Mis entregables (todos versionados)
- scripts-medicion/ (medicion_ledger.py + schema_medicion.json [52 cols, 5 campos peones + par_id na_ok] +
  schema_defectos.json + README): commiteados (11fddf4), smoke verde ciclo completo, EMPLAZADOS al hub por el
  Arquitecto (personal/Arquitecto/TFM-medicion/corpus/medicion/). Listos para congelar a v1.0 en el sello.
- SELLO-ETAPA-1-nova-budget-DRAFT.md (pre-registro; placeholders [LLENAR-AL-SELLAR]). COSECHAS aplicadas:
  s.5 = verificacion de EXISTENCIA readonly es posible ya (F-NOVA-01; paridad requiere GRANT EXECUTE);
  NOTA DE INDEPENDENCIA = los ~4 Get_*_List son CLUSTER casi isomorfo load-bearing para n>=10 -> Q4 declara
  n EFECTIVO reducido; doble rol PAR-D/Q4 NO es confound (contrastes pre-registrados distintos).
- Tracker de decisiones de dominio + separacion de memoria (esta area) + alta ruteada.

## Asiento de coordinacion del build de Nova (DECISION-0088, 512e35c; enmienda a 0050 #5)
- **AHORA (ventana del estudio, hasta sello/30-jul): asiento = HUB.** El brazo gobernado es el TRATAMIENTO
  medido -> su atestacion debe estar en el MISMO #4 que la medicion + sello, en un solo asiento. Meter
  NOVA/Aegis a mitad del estudio = costura de cross-atestacion antes del sello (viola regla de oro del sello).
- **Codigo siempre = NOVA/Nova-Budget; estudio/medicion/sello/#4 siempre = HUB.** Workflow VS Code del
  Operador: abre Nova-Budget para codigo + coordina desde el hub (sin multi-root).
- **POST-sello: migra a NOVA/Aegis** (instancia operativa del equipo). Regla dual cross-atestacion: hub =
  #4 del estudio/meta + sello; NOVA/Aegis = #4 operativo del build; el journal del hub registra el sha256
  de la atestacion de Aegis por gate. ELEGANTE (study-relevant): esa migracion ES la evidencia de
  transferibilidad (la replica employee-run pre-registrada) -> arquitectura y estudio se alinean.
  FORMALIZADO en DECISION-0088 (512e35c): meta/estudio/metodologia canonica = hub SIEMPRE (nunca migra);
  governance operativa del producto = su instancia Aegis/ tras adoptar; migracion post-sello, dual cross-atest.

## Contexto real del negocio (clave)
Objetivo real = Nova Budget/Accounting/Payroll/Treasury para la EMPRESA del operador, employee-ready.
Stack: Clean Architecture .NET 10 (Api/Application/Domain/Infrastructure/Mcp/Contracts) + React/TS/Vite
+ SQL Server 2025 + OpenTelemetry; anti-patrones prohibidos (WebForms, DataTable entre capas, DLLs
manuales, secretos en .config, centinelas -99). Requisitos = RES-000..012 (brechas s.08 de NOVA-PRES-000);
SPECs desde NOVA-SPEC-T-001 v1.1. FUENTE DE VERDAD del diseno = D:/Agentes/Ingenas/Budget/ (paquete del
operador, FUERA del hub): NOVA_GOAL, NOVA_Arquitectura, NOVA_PRES_00..12, NOVA_SPEC_Plantilla, NOVA_ESTUDIO_*;
BD/legacy en 01_Sources. El hub Area_comun/specs/nova/ guarda la DERIVACION gobernada (SPECs), no el diseno-fuente.
Composicion del equipo: 12 roles -> 4 firmantes (Operador=dominio, Arquitecto=arquitectura+docs, Codex=maker,
Analista=security+QA checker); Legacy Analyst sin firmante = eslabon debil de atestacion.

## Que afirma / NO afirma el estudio (delimitacion sellada)
Da: instrumentacion + Q4 causal (ligero-vs-completo) + serie honesta de calidad (checker formal atrapa
lo que el informal dejo pasar) + transferibilidad (2a instancia dominio real vs N=500 auto-dogfood). NO
da: "el gobierno mejora la calidad" causal (maker!=checker YA existe en ambos brazos; el tratamiento es
el checker FORMAL atestado). Veredicto de compra se difiere a replica employee-run pre-registrada.
Peones: se mide el USO (5 campos), su EFECTO solo en F6 aislado (no confundir el contraste central).

## Pendientes del operador (recordar con tacto)
Abrir GOAL-P1 (piloto, 3-8 jul, EL RELOJ); estimates S/M/L (<=08-jul); GRANT EXECUTE + sandbox mutadores
(<=14-jul); revision legal del consentimiento. F1.6 (aprendizajes-externos, extraccion de reglas) pendiente,
paralelo, NO es entregable del Asesor.
