# PLAN RECONCILIADO REQ-ZEUS-001 (borrador para aprobacion del operador)

> Directiva OPS `MSG-...115242Z-...DIRECTIVA-REQ-ZEUS-001-producto`. Entregable: mapa tareas->workstreams +
> D1-D5 redactadas + alta Analista + guia de peones en WS4/D3 + ETA. Gobernanza en el HUB (DECISION-0050).
> Fuentes: `REQUERIMIENTO_Zeus-Aegis_Productizacion_y_Metodologia.md`, `TEMP_Guia_Modelos_Peones_y_Medicion.md`,
> `D:/Agentes/Zeus/NOVA/Area_comun/decisions/DECISION-0001..0006` (ya accepted). HEAD hub 349a8ca.

## 0. Hallazgo que cambia la secuencia: D1-D5 YA ESTAN CERRADAS

Las decisiones D1-D5 (y una D6 de facto) EXISTEN como archivos **accepted** (aprobados por el operador,
2026-06-30) en la instancia producto **NOVA**, no en el hub ni en Zeus-Aegis:

| Archivo (NOVA/Area_comun/decisions/) | Decide | vs tu endoso en la directiva |
|---|---|---|
| DECISION-0001-D1-gobernanza-tiered.md | **D1** coordination (defecto NOVA) + attested conmutable; demo TFM apunta al CORE, no a NOVA | == coordination-only (Ed25519 add-on opcional) OK |
| DECISION-0002-D2-una-instancia-por-proyecto.md | **D2** una instancia/proyecto via new_instance.py; human_owner=lider | == OK |
| DECISION-0003-D3-backend-modelos-hibrido.md | **D3** frontera (router multi-proveedor) + peones Ollama keyless fuera del ledger; PII cero-egress | == OK (la guia de peones detalla el nivel; ver s.4) |
| DECISION-0004-D4-hermes-agent-desde-fuente.md | **D4** hermes-agent MIT verificado; **vendorizar PERMITIDO** conservando LICENSE; purga logo NousResearch aparte | compatible: tu endoso "desde fuente si no permite; vendorizar si permite" -> resuelto a "permite" |
| DECISION-0005-D5-rebranding-superficial.md | **D5** UI/i18n + alias ZEUS_*<-HERMES_* con shim; sin renombrar binarios/appId; NOTICE MIT; purga 154 assets = gate | == OK |
| DECISION-0006-gate-cierre-doc-only.md | **D6** gate doc-only (docs se gatean por checks de doc, no npm test) | (extra, ya usado en TASK-0226) |

**Implicacion:** TASK-ZEUS-0001 ("cerrar D1-D5") esta esencialmente HECHO en NOVA. Lo que falta es
**decidir donde se gobierna** (ver duda 1, s.8). Recomiendo: dejar D1-D5 como decisiones de la INSTANCIA NOVA
(gobernanza de producto vive en su Area_comun, no en el core neutral del protocolo -> el core NO se contamina,
coherente con DECISION-0050 y con que el hub hoy NO tiene decisiones de producto), y que el HUB registre solo
la **DECISION de ADOPCION** de REQ-ZEUS-001 + el backlog de build.

## 1. Mapa de reconciliacion: tareas actuales -> workstreams / TASK-ZEUS (NO se tira trabajo)

Estados verificados en TASK_INDEX (HEAD 349a8ca). Cruce con la enumeracion autoritativa del REQUERIMIENTO:

| Tarea hub actual | Estado | TASK-ZEUS / WS | Rol |
|---|---|---|---|
| **TASK-0226** WS1 inventario+plan branding | **done** | **TASK-ZEUS-0002 (WS1)** | Cerrada. |
| **TASK-0227** npm test verde + boundary F1 | in_review (gate Analista) | INFRA (habilita gates de 0002/0008) | NO es fuga F1 (diagnostico Arquitecto). |
| **TASK-0222** vista Estadisticas F1 | in_review (gate Analista) | **TASK-ZEUS-0008 (WS6)** parcial (F1 read-only) | Vista panel. |
| **TASK-0223** vista Instanciar F1 (preparar-cmd) | ready | **TASK-ZEUS-0008 (WS6)** parcial (F1 read-only) | Vista panel; NO ejecuta. |
| **TASK-0224** fix redactor reportes | review_approved | INFRA (tooling) | Utilitario. |
| **TASK-0225** Arquitecto-cron headless | in_review (gate Analista) | HABILITADOR 24/7 | Orquestador; habilita headless del goal. |
| (D1-D5) | accepted en NOVA | **TASK-ZEUS-0001** | Hecho (ver s.0). |

Lo hecho/en-vuelo cubre: WS1 (0002), parte de WS6 (0008 F1), infra y el habilitador. El GRUESO del producto
(WS2/WS3/WS4/WS5/WS3.5/WS7/runbooks) esta SIN registrar -> ahi pivota el backlog.

## 2. Backlog de producto TASK-ZEUS-00xx (enum autoritativa del REQUERIMIENTO)

| ID | Titulo | WS | Owner (maker/checker) | Estado reconciliado | Deps |
|---|---|---|---|---|---|
| TASK-ZEUS-0001 | Cerrar D1-D5 | (decisiones) | Arquitecto / aprueba Operador | **HECHO** (NOVA DECISION-0001..0006) | - |
| TASK-ZEUS-0002 | Inventario hermes + plan branding | WS1 | Codex / Analista | **HECHO** (=TASK-0226) | - |
| TASK-ZEUS-0007 | Alta Analista + mapeo rol->agente + wrapper new_instance(4) | WS5 | Arquitecto / Codex | **SIGUIENTE** (condiciona owner:Analista) | D1,D2 |
| TASK-ZEUS-0003 | Capa branding + alias env + pantalla "Preparando Zeus" | WS3 | Codex / Analista | por registrar | D5, WS1 |
| TASK-ZEUS-0004 | Bootstrapper (gateway+backend+config+lifecycle Electron) | WS2 | Codex / Analista | por registrar | D3,D4 |
| TASK-ZEUS-0005 | Backend modelos por defecto (D3) + bloqueo PII | WS4 | Codex / Analista(seg) + decision Operador | por registrar | D3 |
| TASK-ZEUS-0006 | Instalador electron-builder firmado + desinstalacion limpia | WS3.5 | Codex(DevOps) / Analista | por registrar | D4, WS2, WS3 |
| TASK-ZEUS-0008 | Puente gobernanza desde UI (F1 hecho; resto en limites D1) | WS6 | Codex / Analista | PARCIAL (=0222/0223 F1) | D1, F2 |
| TASK-ZEUS-0009 | Verificacion e2e VM limpia + checklist licencias/seguridad | WS7 | Analista | por registrar | WS1-WS6 |
| TASK-ZEUS-0010 | Runbooks instalacion/operacion | (docs) | Arquitecto(Docs) | por registrar | WS3.5 |

**Secuencia que pide el REQ:** primero 0001 (hecho) y **0007 (4 firmantes)**, porque condicionan el resto.
Regla dura: **NO crear tareas owner:Analista antes del alta del Analista (0007)** -> el validador las rechaza.

## 3. WS4 / D3 -- guia de modelos-peon (requisito del operador)

De `TEMP_Guia_Modelos_Peones_y_Medicion.md` (doc personal, no gobernado):
- **Niveles:** firmante frontera (logica de negocio/seguridad/migraciones/diseno, nunca se delega) + peon LLM
  no-firmante (drafter para repetitivo con poca variacion). Peones concretos: **Qwen2.5-Coder-7B-Instruct**
  (Q4 ~4.7GB, cabe en 8GB VRAM) opcion A; **DeepSeek-Coder-6.7B** contraste; `qwen2.5-coder:3b` para CRUD trivial.
  Free tiers sin instalar (Gemini Flash-Lite / OpenRouter :free / Groq) -- NUNCA PII.
- **Codegen antes que LLM:** si la salida es funcion mecanica de la entrada (CRUD, DTOs, mappers, cliente OpenAPI)
  -> scaffolding/plantillas/Roslyn, cero tokens. El peon solo para la variacion con criterio. Decide el firmante.
- **Patron:** peon = maker barato, borradores FUERA del ledger (no toca events.jsonl, no pasa por submit_intent,
  nunca firma); un firmante distinto (Codex) integra, prueba y FIRMA. maker!=checker. Peon nunca toca reglas de
  negocio ni el repo del protocolo.
- **Gate determinista:** build + test (unit+golden) + arch-tests + lint/format + scan encoding + guard
  "sin logica de negocio / sin deps nuevas". Verde -> el firmante ojea el diff y firma.
- **Medicion 3 brazos** sobre 10-20 tareas homogeneas reales-sin-PII: A control (firmante solo), B peon->gate->
  firmante, C peon->gate->Gemini Flash-Lite critico-asesor(no firma)->firmante. **Metrica que decide =
  tokens del firmante (tokens_codex).** Reglas pre-comprometidas: adoptar peon si tokens_codex(B)<<A + kickback<20%
  + gate atrapa defectos; vale el critico si tokens_codex(C)<B apreciable y precision fp/(validos+fp)<30%.
- **Sandbox:** el piloto de peones va en repo APARTE `D:/Agentes/Zeus/piloto-peones/`, cero escritura al repo
  medido. (La "regla de oro" condicionaba a post-N=500; el dataset YA esta sellado, la condicion se cumple.)
- **Ubicacion en el backlog:** el piloto/medicion de peones es sub-tarea de WS4 (TASK-ZEUS-0005) o tarea aparte
  TASK-ZEUS-0005b; NO bloquea WS2/WS3. Recomiendo registrarlo como spike separado owner:Codex tras 0007.

## 4. Restricciones (no negociables, de la directiva + REQ)
- **F2 write-through al ledger MEDIDO: gateado / fuera de alcance.** El producto opera coordination-only sobre la
  instancia del proyecto (NOVA), no sobre el ledger del TFM. WS6 escribe en el Area_comun de la instancia, no en el medido.
- **TFM intocable:** no modificar el core de multi_agent_project_protocol salvo orden explicita. 5 pineados byte-identicos.
- Piloto de peones en repo sandbox aparte. Licencias: NOTICE Hermes MIT + LICENSE hermes-agent (MIT verificado);
  purga de assets NousResearch = gate de release. Sin secretos; PII nunca a modelos externos.

## 5. ETA (fases; semi-auto Codex maker + Analista checker, promocion de a una)
- **Fase 0 (ahora):** cerrar los 3 gates en vuelo (0227, 0225, 0222) + 0223. ETA: en curso, ~1-2 ciclos por tarea.
- **Fase 1 -- Adopcion + firmantes:** registrar en hub la DECISION de adopcion + backlog TASK-ZEUS + **TASK-ZEUS-0007
  (alta Analista en NOVA + wrapper new_instance 4 agentes)**. ETA: 0007 ~2-3 ciclos (Codex maker + Analista gate).
- **Fase 2 -- Branding + bootstrapper:** TASK-ZEUS-0003 (WS3) y 0004 (WS2, el mas grande). ETA: WS3 ~2-3, WS2 ~4-6 ciclos.
- **Fase 3 -- Backend + peones:** TASK-ZEUS-0005 (WS4 + spike peones sandbox). ETA: ~3-4 ciclos + medicion A/B/C aparte.
- **Fase 4 -- Instalador + e2e:** TASK-ZEUS-0006 (WS3.5) y 0009 (WS7 VM limpia) + 0010 runbooks. ETA: ~4-6 ciclos.
- Total orientativo: producto e2e verificable en ~4 fases; el camino critico es WS2 bootstrapper -> WS3.5 instalador -> WS7.

## 6. Dudas concretas para el operador (bloquean el registro en el ledger)
1. **Gobernanza de D1-D5:** ya estan accepted en NOVA. Recomiendo dejarlas ahi (gobernanza de producto en la
   instancia; el core neutral no se contamina) y que el HUB registre solo la DECISION de ADOPCION + backlog.
   Alternativa: duplicar/ratificar D1-D5 como decisiones del hub. Que prefieres?
2. **Namespace de tareas:** registrar el backlog como **TASK-ZEUS-00xx** (namespace limpio, propuesto) vs seguir en
   TASK-02xx. Y cruce: 0002=TASK-0226, 0008=TASK-0222/0223 (marcar heredadas/reconciliadas).
3. **Registro:** confirmas que registre en el hub la DECISION de adopcion + TASK-ZEUS-0003/0004/0005/0006/0007/0009/0010
   (owner Codex/Arquitecto; NINGUNA owner:Analista hasta cerrar 0007)? 0007 primero.
