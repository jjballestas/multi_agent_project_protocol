# 06_Asistente - Orden Fase 0 (E5 + E6) para el arquitecto

> Insumo del operador (asistente Cowork) para el ARQUITECTO (Claude en VS Code).
> El asistente no redacta los docs del protocolo ni muta estado: esto es el brief de requisitos.
> El arquitecto redacta la DECISION + docs y construye via submit_intent desde VS Code.
> Fecha: 2026-06-14. Alcance aprobado por el operador: E5 + E6. #1/protocol_research DIFERIDO (decision aparte).

## 0. Estado de partida (verificado read-only)
Sistema en reposo tras v1.6.0: HEAD 60465f1, flag cost_attribution_enabled=true, TASK-0111/0113 done,
gate duro (chain/agent_signatures/anchor/subagents) OFF. Fase 0 sin empezar: E5, E6, protocol_research no existen.

## 1. Objetivo
Arrancar Fase 0 acotada a:
- E5: catalogo nombrado de modos de fallo -> guardrail.
- E6: gobernador "merece un loop?" (prerrequisito de gobierno del loop/scanners; sin E6 no se construye E3
  ni se amplia SA.4).
Documental, neutral de dominio, in-repo. Esfuerzo bajo.

## 2. Entra por el metodo
DECISION-00xx (aditiva, neutral) -> los docs -> acceptance/test estructural -> SemVer MINOR + CHANGELOG.
maker!=checker: el arquitecto redacta; revisa OTRO agente (analista para E5/fidelidad MAST; Codex o arquitecto
para E6). Escritor unico via submit_intent.

## 3. E5 - FAILURE_MODES.md  (crear en Area_comun/protocol/)
- Tabla: modo -> sintoma -> guardrail, con la taxonomia MAST como vocabulario.
- Insumo (fallos YA mitigados en el protocolo, mapear cada uno a su modo MAST + el guardrail que lo contiene):
  drift (DECISION-0017), anomalias (DECISION-0018), colision (DECISION-0020), liveness/visibilidad
  (DECISION-0013), budget/deadline, dirty no declarado, escalada a humano, schema errors, etc.
- DoD: cubre los 14 modos MAST + sus guardrails; queda enlazada desde el onboarding y la guia de review.
- HONESTIDAD: "taxonomia MAST aplicada a incidentes operacionales de protocolo". NO afirmar equivalencia 1:1
  con MAST-Data (eso es #1, diferido). Donde un modo MAST no tenga incidente propio en este repo, decirlo.

## 4. E6 - gobernador "merece un loop?"  (en TASK_PROTOCOL.md, existe)
- 4 condiciones + check de 30s, checklist OBLIGATORIO antes de crear cualquier discovery_scanner o flujo de
  autonomia:
  1. se repite >= semanal?
  2. hay verificacion automatizada / objetiva?
  3. el budget absorbe el reintento?
  4. requiere tools de nivel senior?
- DoD: checklist obligatorio, enlazado; referenciado como pre-check de Fase 4 (E3 scanners) y de ampliar SA.4.
- Regla del roadmap: "no construir E3 antes que E6".

## 5. Acceptance (verificable)
- E5: el doc lista los modos MAST; cada fila tiene sintoma + guardrail con referencia (DECISION/mecanismo);
  enlazado desde onboarding + guia de review.
- E6: las 4 condiciones + check de 30s presentes; marcado como obligatorio antes de scanner/autonomia; enlazado.
- Test: el que el arquitecto decida; estructural basta. No fuerces un golden artificial si no aporta senal.

## 6. Restricciones (innegociables)
- Neutralidad de dominio: nada de Galapa/ScanPay/negocio en core ni *.template.*.
- submit_intent escritor unico; SemVer MINOR + entrada en CHANGELOG.
- NO tocar #3/flag, ni #4/chain/auth, ni SA.4. Fase 0 es independiente.
- #1 / protocol_research DIFERIDO: requiere su propia DECISION (montar repo satelite read-only). No lo crees aqui.

## 7. Orden corta para pegar al arquitecto
"Arquitecto: arranca Fase 0 acotada a E5 + E6, por el metodo (DECISION aditiva neutral + docs + acceptance
estructural + MINOR/CHANGELOG, maker!=checker). E5 = FAILURE_MODES.md en Area_comun/protocol/: tabla
modo->sintoma->guardrail con taxonomia MAST como vocabulario, cubre los 14 modos MAST + enlazada desde
onboarding/review; honesto: MAST aplicado a incidentes de protocolo, sin afirmar equivalencia 1:1 con
MAST-Data. E6 = gobernador 'merece un loop?' en TASK_PROTOCOL.md: 4 condiciones (>=semanal / verificacion
objetiva / budget absorbe reintento / tools senior) + check 30s, checklist OBLIGATORIO antes de cualquier
scanner o flujo de autonomia, enlazado como pre-check de Fase 4 y de ampliar SA.4. Neutralidad estricta;
#1/protocol_research DIFERIDO (decision aparte); no toques #3/#4/SA.4. Reporta para mi ratificacion."
