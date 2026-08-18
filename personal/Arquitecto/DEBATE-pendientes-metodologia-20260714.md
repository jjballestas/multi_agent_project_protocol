# DEBATE: pendientes de METODOLOGIA al 2026-07-14 (~03:25 local)
# Modo debate: solo draft, NO rutear, NO sellar. Verificado contra ledger/artefactos, no de memoria.

## A. SELLO ETAPA 2 -- el paraguas (draft estructural YA escrito, 3 bloqueos, 1 se LEVANTO anoche)
Artefacto: Area_comun/artifacts/DRAFT-SELLO-ETAPA2-estructura-arquitecto.md (estructura completa,
placeholders [LLENAR-AL-SELLAR-E2]). Sella: aritmetica backlog reconciliada + condicionalidad Q4 +
regla de adopcion/migracion Aegis + DISENO peones (Q-PEON) + roster. Bloqueos vigentes:
1. Reconciliacion 26-29-jul (calendario; Analista read-only, s.10 Etapa 1) -- aun no llega la ventana.
2. DEC de dominio P3.x (hoy viven del lado NOVA; su trio las cierra).
3. Aprobacion + firma del Operador.
LEVANTADO ANOCHE: el roster s.5 estaba "BLOQUEADO por onboarding de Julian" -> jheredia OPERATIVO +
gate nominal 2-clones CERRADO (cross-atest Entrada 2, hub ffd2faa). El roster ya es sellable.
INSUMO NUEVO: corpus de Contabilidad con design-source REGISTRADO (hito 11-jul, artefacto atestado).
Ventana real: hoy 14-jul -> sellar <=29-jul. Lo redactable esta hecho; el camino critico es (1)+(2).

## B. PEONES (Q-PEON) -- diseno LISTO, pendiente de ADJUDICACION en el sello E2
Artefacto: Area_comun/artifacts/NOTA-DISENO-peones-vs-tokens-sello-etapa2.md (propuesta pre-registrable).
- Contraste: mono-orquestado (brazo A, identico a Etapa 1) vs peones bajo gobierno completo (brazo B:
  peon = maker-borrador KEYLESS fuera del ledger, no-frontera; firmante frontera revisa y FIRMA;
  maker!=checker intacto). Metrica primaria tokens_total_atribuibles; guardia de NO-inferioridad en
  calidad (D1-D4, reworks). Ahorro con degradacion = NO exito.
- Instrumentacion YA existe (schema v1.0, 52 cols, 5 campos peones desde F3.3). Apertura del brazo:
  por COMPLETITUD CERTIFICADA (redisenado por DIRECTIVA 30a4252 s.4; ya NO es F6 post-Sprint-1).
- TASK-0231 queda proposed como traza historica (no se activa antes del sello E2).
- PENDIENTE REAL: (1) adjudicar Q-PEON dentro del sello E2 (firma operador); (2) corpus enumerable
  (sale del analisis de Contabilidad; las 6 unidades medidas + resto); (3) INFRA del peon: backend
  router/keyless + prueba negativa PII cero-egress (alcance viejo de TASK-0231 / DECISION-0074/0078).
- SINERGIA NUEVA (anoche, DECISION-0096): el runner generico peer_mailbox_cron.ps1 acepta CUALQUIER
  CLI via -AgentExe/-AgentArgs con prompt por STDIN -> es el enchufe natural para un peon-drafter
  keyless (un "peer" sin llaves que draftea y NO firma; el firmante frontera toma el draft y firma).
  La infra del brazo B puede ser el MISMO harness con un prompt de rol "drafter" -- barato de pilotar.
  (Solo diseno; adjudica el sello E2.)

## C. MEMORIA HIBRIDA -- la RUTA ya esta sellada; lo pendiente es DISENO detallado + BUILD
- DECISION-0081 (2026-07-02, supersede 0071): ruta UNICA = REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO v0.3.0
  (repo caliente + archivo frio verificable + DB derivada; s.26 absorbe las lecciones adversariales de
  Engram). Engram = CERRADO PERMANENTE (capability OFF, ENG-* sin efecto).
- Es la pieza "employee-ready / peones REVIVEN" de la vision Nova (memoria por agente reconstruible).
- PENDIENTE REAL: no hay SPEC de implementacion ni tarea registrada ni ventana. La DIRECTIVA 30a4252
  s.2 la puso en la cola como "DECISION primero (HECHA = 0081), implementacion despues".
- TENSION a debatir: el compromiso audit-first (PROJECT_STATE: "el CORE no cambia hasta el fin de la
  medicion") vs construir memoria. Mi lectura: (a) SPEC/diseno detallado = papel, no toca core, puede
  avanzar YA (cola proactiva del Arquitecto); (b) BUILD = post-30-jul o en instancia (NOVA/Aegis),
  nunca en el core del hub durante la ventana medida. El build en NOVA ademas seria evidencia de
  transferibilidad (la memoria se instala como capa de instancia, no como fork del core).

## D. Cola de los 4 REQs (DIRECTIVA 30a4252 s.2) -- estado real
1. REQ no-vibecoding (critical): DECISION-0084 sellada + TASK-0243 (doctrina identidad). La
   IMPLEMENTACION de producto depende del pendiente del operador "Zeus-protocol vs Zeus-Aegis (panel)".
2. REQ intake profesional: el intake gate determinista YA shipped en el hub (TASK-0238, v1.18.0).
   El panel/UX de intake = producto Zeus (mismo pendiente del operador).
3. REQ memoria hibrida: ver C.
4. Transcripcion c5Gwx0RcxNE: NO-entregable; absorbida como lecciones. CERRADA como item.

## E. Otros pendientes de metodologia (menores / de fondo)
- TASK-0178 (consola Arquitecto en el front) proposed -- depende del front Zeus (mismo gate que D.1/D.2).
- Port POSIX/py del runner generico (DECISION-0096 p.7, futuro; mantener contrato runtime-state).
- Migracion opcional del hub a scripts/harness/ (hoy legacy personal/<peer>/, documentado en 0096 p.6).
- AGENTS.md header dice "latest v1.17.0" (stale; CHANGELOG top = v1.19.0). Fix de 1 linea cuando
  toquemos AGENTS.md por otra razon (no vale un commit gobernado solo).
- Export de watchdogs a capa neutral: de facto CERRADO anoche (session-watchdogs ya se exportaba;
  las skills de agente-ops ahora tambien, DECISION-0096).

## Mi lectura (orden propuesto para el debate)
1. **El camino critico es el SELLO E2** (fecha dura <=29-jul). Peones (B) es un CAPITULO del sello,
   no un pendiente aparte: su diseno esta listo; lo que falta es lo que el sello ya preve (corpus
   enumerable + adjudicacion + firma). El roster ya quedo desbloqueado anoche.
2. **Memoria hibrida (C) es el unico pendiente GRANDE sin dueno ni ventana.** Propuesta de salida:
   yo escribo la SPEC de implementacion (papel, cola proactiva, sin GO extra) mapeando el REQ v0.3.0
   a la arquitectura de instancia (donde vive la DB derivada, que es archivo frio, como reconstruye
   un peon/agente su memoria al revivir, y el importador markdown->DB que Engram nunca tuvo);
   el BUILD se decide post-30-jul (o como capa de instancia NOVA si el operador quiere evidencia
   de transferibilidad antes).
3. D.1/D.2/E.1 comparten UN desbloqueo: la decision Zeus-protocol vs Zeus-Aegis del operador.
   No hay trabajo de metodologia util que hacer ahi hasta esa decision.

## Salida del debate (cuando el operador ordene)
- "GO SPEC memoria" -> escribo SPEC-MEMORIA-HIBRIDA (papel, hub, capa estudio/diseno).
- "GO prep E2" -> avanzo los redactables restantes del sello E2 + checklist de la reconciliacion 26-29.
- "GO piloto peon-drafter" (post-sello E2 o sandbox) -> diseno el prompt de rol drafter para el runner
  generico + prueba PII cero-egress en sandbox (sin tocar el brazo medido).
- Sin GO -> queda este draft.
