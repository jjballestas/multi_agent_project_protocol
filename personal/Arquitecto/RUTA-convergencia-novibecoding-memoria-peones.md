# RUTA DE CONVERGENCIA: no-vibecoding + memoria hibrida + peones
# 2026-07-14 ~15:20 local. Pedida por el operador ("estan relacionados, detalla los pasos").
# Plan de desarrollo (papel, sin rutear); cada gate nombrado con su dueno. Fuentes: DECISION-0084/1001
# (no-vibecoding sellado + 8/8 MVP), SPEC-MEMORIA-HIBRIDA v0.2.0 (9376bb4), NOTA-DISENO peones +
# DRAFT-SELLO-ETAPA2 (s.4 sellable), DIRECTIVA probe 14-jul (answered), corpus 35 CONT-U (NOVA 35a1b4e).

## 1. Por que son UNA maquina (la relacion exacta)

- **No-vibecoding = la capa de SEGURIDAD.** Sus gates (intake DoR, AC obligatorio, maker!=checker,
  taxonomia D1-D4, excepciones auditadas) son lo que hace VIABLE delegar drafting a modelos baratos:
  sin esos gates, "peon que draftea" = vibecoding con modelo barato. El peon jamas firma; el firmante
  frontera revisa y firma. ESTADO: metodologia viva en el hub (0238/0239/0240/0241) + MVP producto
  8/8 done (DECISION-1001, TASK-11xx).
- **Memoria hibrida = la capa ECONOMICA.** Un peon es barato porque es efimero -- y efimero significa
  que MUERE con su contexto. El revive_pack (SPEC s.5.5: memoria vigente + tareas vivas + decisiones
  aplicables + context cache, con identidad derivada y procedencia firmada) es lo que hace que morir
  sea barato: revivir cuesta un pack, no releer el repo. Sin memoria, el ahorro del peon se lo come
  el re-onboarding. ESTADO: SPEC v0.2.0 commiteada + revision adversarial incorporada; probe aislado
  ordenado (DIRECTIVA 14-jul); Gate-1 pendiente de 3 inputs del operador.
- **Peones = el PAYOFF medible.** Q-PEON: bajo gobierno completo, el peon reduce
  tokens_total_atribuibles del firmante SIN degradar calidad (guardia de no-inferioridad D1-D4 +
  reworks: ahorro con degradacion = NO exito). ESTADO: diseno pre-registrable listo (NOTA-DISENO,
  capitulo s.4 del sello E2); poblacion enumerada (35 CONT-U); instrumentacion lista (5 campos en
  schema v1.0 desde F3.3); infra del peon pendiente (router keyless + PII cero-egress); apertura por
  COMPLETITUD CERTIFICADA post-sello.
- **El endgame que las une:** el "empleado digital que revive" -- peon gobernado (capa 1) que muere y
  revive con su contexto (capa 2) y cuyo ahorro esta medido con guardia de calidad (capa 3). Julian
  (empleado humano) ya demostro el ciclo firmado equivalente; el peon es su espejo barato.

## 2. REGLA DE NO-CONTAMINACION (lo que NO se mezcla, pre-sellado)

- El contraste Q-PEON del sello E2 corre **SIN memoria en AMBOS brazos** (regla de simetria del draft
  E2 s.4: la DECISION de memoria no llega antes del sello -> ninguno la usa). El probe de memoria corre
  AISLADO en Nova-Payroll (firewall anti-HARKing, NO citable).
- **Peones CON memoria = la GENERACION SIGUIENTE** (post-estudio): replica o sub-estudio pre-registrado
  (lo redacta el Asesor) SOLO si (a) Q-PEON dio senal y (b) el probe de memoria dio indicios y el
  operador adopto. Nada de esto entra al corpus citable de Etapa 1/2.
- Contabilidad (ancla citable, pre-registro N=6) SIEMPRE gana el cuello de botella.

## 3. LOS PASOS (por carril, con gates y duenos)

### Carril A -- Sello E2 (papel; cierra la fase de diseno de peones) [YA EN CURSO]
- A1 [hecho 14-jul]: insumos cerrados -- corpus 35 CONT-U + BR-C4 verificada gobernada (n=10,
  enmiendas s.27/s.28) + hardening 15-jul SI + roster desbloqueado (Julian).
- A2 [26-29 jul, Analista read-only]: reconciliacion de la ventana baseline -> llena s.1.
- A3 [<=29-jul, OPERADOR]: firma del sello E2 -> submit_intent decision (sha256 del doc, patron 0091).
  EFECTO: Q-PEON queda PRE-REGISTRADO (diseno congelado, apertura por completitud, poblacion = las 35).
- A4 [post-sello, tercero read-only]: certificacion de completitud ((a) reconciliacion, (b) corpus
  [YA], (c) sello) -> ABRE el contraste peones. Nunca por fecha.

### Carril B -- Probe de memoria (Nova-Payroll aislado) [ESPERA 3 INPUTS DEL OPERADOR]
- B1 [OPERADOR]: los 3 inputs pedidos en mi RESP de hoy: GO al draft de Gate-1 + repo (propuesto
  NOVA-Suite/Nova-Payroll) + roster del trio.
- B2 [Arquitecto, tras B1]: redacto Gate-1 (DECISION de activacion scopeada: implementar REQ/SPEC SOLO
  en Nova-Payroll; memoria OFF en hub/medidas; firewall anti-HARKing; freno Contabilidad-gana) ->
  firma del operador -> submit_intent.
- B3 [Arquitecto]: nace Nova-Payroll born-operational (new_instance --tier attested: harness + skills
  del arsenal 0096) + guardrail PII de nomina en su AGENTS desde el nacimiento + cross-atest de
  nacimiento anclada en el hub.
- B4 [Arquitecto (esqueleto) + trio Nova-Payroll]: PREP del slice de liquidacion (empleados/contratos/
  conceptos + 002t/007t/028t + FindBaseTra + %concepto + consecutivo + control periodo + 1 reporte RO),
  analogo al kit SPEC-CONT.
- B5 [trio Nova-Payroll; post-sello E2 salvo ventana ociosa]: FASE A = implementar de la SPEC:
  F1 (build_memory_db + query + dump + check_drift; PORT/SUPERSEDE del memdb.py de Zeus-protocol-Aegis
  -- hallazgo M6 -- hacia UN master neutral del hub que se exporta) + revive_pack (s.5.5) + F2 minimo.
  Tests: round-trip AC5, I2 read-only, I6 identidad, PII negativos.
- B6 [la DEMOSTRACION]: un peon/agente del slice MUERE -> REVIVE solo con su pack -> continua la tarea
  CORRECTAMENTE; pack atestado (procedencia firmada). + drift 0 + recall util (cualitativo).
- B7 [OPERADOR]: decision de adopcion de la memoria (con los indicios del probe). Si NO: se documenta
  y la linea se congela sin tocar nada medido. Si SI: habilita Carril D.

### Carril C -- Peones brazo B (post-apertura A4) [DEPENDE DE A4; NO de B]
- C1 [Arquitecto propone / OPERADOR aprueba]: infra del peon SIN memoria (regla s.2): backend keyless
  (router empresa OpenAI-compat u Ollama local; punto unico de claves/costo; alcance viejo TASK-0231/
  DECISION-0074) + PRUEBA NEGATIVA PII cero-egress + prompt de rol DRAFTER para el runner generico
  (scripts/harness/peer_mailbox_cron.ps1 con -AgentExe al CLI del peon: el enchufe ya existe, se
  entrego anoche). El peon NO firma, NO toca ledger; el firmante toma el draft, revisa y firma.
- C2 [trio NOVA]: correr el contraste Q-PEON sobre las unidades asignadas del corpus (brazo A mono vs
  brazo B peon+firmante), instrumentacion ya lista (5 campos), en la ventana que el sello defina.
- C3 [Asesor/estudio]: lectura de Q-PEON (tokens frontera por unidad equivalente + guardia D1-D4).

### Carril D -- Convergencia (la generacion siguiente) [DEPENDE DE B7=SI + C3 con senal]
- D1 [Asesor redacta pre-registro; OPERADOR firma]: replica/sub-estudio "peones CON memoria":
  el peon del brazo B revive con revive_pack entre unidades; se mide si la memoria AMPLIFICA el ahorro
  (menos re-onboarding) manteniendo la guardia de calidad. Primera medicion CITABLE de la memoria
  (REVIVE atestado + round-trip + procedencia firmada -- el angulo que Engram no tiene).
- D2 [Codex/Zeus-protocol; requiere decision de panel]: no-vibecoding item 8 = integracion memoria->
  Quality Panel (vista read-only de memoria/archivo + busqueda FTS; SPEC s.8 Q6: UI = producto).
- D3 [Codex]: no-vibecoding item 7 (plantillas por tipo de trabajo) -- barato, cualquier ventana
  post-30.
- D4 [OPERADOR]: si D1 confirma, la memoria entra a la metodologia exportable (new_instance la shippea
  como capa opcional de instancia; DECISION propia) -> toda instancia futura nace con "peones que
  reviven" disponibles.

## 4. Dependencias en una linea

A3 (sello) -> A4 (abre peones) -> C1-C3 (Q-PEON sin memoria)
B1-B2 (Gate-1) -> B3-B6 (probe aislado) -> B7 (adopcion)
[C3 senal] + [B7 SI] -> D1 (peones CON memoria, pre-registrado por el Asesor) -> D4 (metodologia)
D2/D3 (panel) -> gateados aparte por la decision Zeus-protocol vs fork.
Contabilidad N=6 (ancla) corre por encima de todo y gana cualquier conflicto de recursos.

## 5. Que necesita el operador decidir (los 5 botones, en orden)

1. AHORA: los 3 inputs del probe (GO Gate-1 + repo + roster) -- ya pedidos en la RESP de hoy.
2. 26-29 jul: firma del sello E2.
3. Post-B6: adopcion de la memoria (go/no-go con la demo).
4. Post-A4: GO a la infra del peon (C1: backend keyless + PII negativa).
5. Cuando quiera: decision de panel (Zeus-protocol vs fork) -- gatea D2/D3, no bloquea nada mas.
