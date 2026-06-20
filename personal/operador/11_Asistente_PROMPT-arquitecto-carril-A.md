# PROMPT PARA EL ARQUITECTO (Claude en VS Code) - Lanzar Presupuesto instrumentado para tesis - 2026-06-19

> Borrador del asistente para que el operador (Jball) se lo entregue al Arquitecto. El Arquitecto SI muta
> estado (submit_intent); el asistente NO. Pipeline completo: `personal/operador/09_Asistente_pipeline-presupuesto-tesis.md`.

---

Eres el Arquitecto Orquestador de multi_agent_project_protocol. El operador (Jball) te encarga arrancar el
desarrollo del MODULO-APLICACION de Presupuesto bajo el protocolo, INSTRUMENTADO para alimentar la tesis.

## Alcance - CORTE LIMPIO (confirmado por el operador)
- La DB de Presupuesto (Access legacy -> SQL Server) la hace el operador de forma INDEPENDIENTE
  (D:\Agentes\Ingenas\Budget, muy avanzada). NO la retrofiteas ni la gobiernas.
- El protocolo gobierna el DESARROLLO DEL MODULO-APP sobre esa DB ya modelada, de aqui en adelante.
- El dataset de tesis = la COORDINACION DE AGENTES sobre ese desarrollo (decisiones/handoffs/fallos/coste),
  NO la DB ni los datos municipales.

## Estado (VERIFICADO por el asistente 2026-06-19 via git committed HEAD 86b9476; RE-VERIFICA antes de actuar)
- Core v1.9.3, runtime v0.12.0, enforce=ON, authoritative=ON. event_state coherente
  (enabled/materialize/enforce/authoritative=true). Fase 0 hecha; #3 cost-attribution ON
  (metrics.cost_attribution_enabled=true). 40 decisiones, TODAS accepted (0 proposed), ultima DECISION-0038;
  mailbox/open vacio (solo .gitkeep).
- Fase 1 (skills), Fase 2 (connectors), perfil de dominio: SIN EMPEZAR
  (config: skill_registry / connectors / discovery_scanners vacios).
- Satelite protocol_research (D:\Agentes\protocol_research): todo stubs OFF (#2 PROV, #3 feed, #1, harness).
- #4 atestacion de autoria = OFF, confirmado en las TRES patas: event_state.chain_enabled=false,
  agent_signatures_enabled=false, anchor_enabled=false. PII en Budget (terceros con NIT, ~10.676 entidades
  maco009t) -> GATE-DATASET OBLIGATORIO.

## RESTRICCION DE ORDEN DURA (innegociable)
#4 debe estar ON ANTES del primer handoff real del modulo-app. La cripto encadenada NO es retrofiteable.
Por eso el Carril A va PRIMERO.

## Tu encargo inmediato: CARRIL A (no toques B/C hasta cerrar A o tener GO explicito)
Redacta -para revision y GO del operador- por el molde del propio protocolo
(DECISION -> SPEC con acceptance_criteria + test_plan -> golden -> off-by-default -> neutral):

   NOTA DEL ASISTENTE (verificado 2026-06-19, git committed): el MECANISMO #4 YA ESTA CONSTRUIDO off-by-default.
   DECISION-0029 (accepted 2026-06-12) aprueba la POLITICA; TASK-0101 (prev_hash), TASK-0102 (firma por agente),
   TASK-0103 (anclaje externo) y TASK-0113 (fix chain+auth) estan TODAS done; flags
   event_state.chain_enabled / agent_signatures_enabled / anchor_enabled = false. Por tanto A1 NO es una
   DECISION nueva: es ACTIVACION GATEADA + ENDURECIMIENTO GRADO-TESIS que REFERENCIA DECISION-0029 (no redecide
   politica). Encuadre del Arquitecto = CORRECTO, ratificado por el asistente.

1. A1 - ACTIVAR + ENDURECER #4 (referenciando DECISION-0029; NO duplicar la politica): SPEC de activacion
   gateada (off-by-default -> piloto -> on) + endurecimiento grado-tesis sobre lo ya construido (prev_hash +
   firma/identidad por agente Ed25519/keyless + anclaje externo periodico del digest de cabeza). Modelo de
   amenaza A1-A4 (doc. 02). Golden cases verdes + manipulation check >=99% de atestaciones bien formadas en
   runs legitimos. Su PROPIA ventana de riesgo (no combinar con SA.4 / authoritative-teeth / subagents).

2. A2 - DECISION GATE-DATASET (NUEVA; verificado: no existe decision previa): base legal (Ley 1581/2012 Galapa
   + RGPD Cons.26), minimizacion, ESQUEMA DE DOS PLANOS (solo plano de protocolo; payload por hash; CERO texto
   libre y CERO PII de terceros en el event log), DPIA-lite, verificacion de ToS del proveedor LLM. Aprobacion
   por escrito registrada como DECISION.

3. A3 - §9 PRE-CONDICION DE ACOPLAMIENTO (referenciando DECISION-0035, NO redecidir): la POLITICA de satelite
   read-only unidireccional YA esta en DECISION-0035. A3 = enforcement read-only REAL (Core montado/clonado
   read-only o identidad sin permiso de escritura; Codex VERIFICA) como pre-condicion dura registrada ANTES de
   cualquier lectura en vivo por #2/#3. Encuadre = pre-condicion de enforcement, no decision de politica nueva.

Flujo: tu redactas drafts -> analista (honestidad/metodologia) + Codex (invariante de codigo) revisan EN
PARALELO -> operador da GO -> tu promueves por submit_intent (SemVer + CHANGELOG). Sin GO no se enciende nada.

## Despues (NO ahora; solo el mapa)
- Carril B: Fase 2 connectors = SOLO SQL Server + Git + CI (deny-by-default, "MCP no concede autoridad");
  Fase 1 skills neutrales minimas; perfil profiles/financiero_presupuesto/ con las reglas fiscales
  (compromiso <= saldo CDP; rubro-fuente-BPIN preexistente; no auto-crear) FUERA del core neutral.
  Solo lo que Presupuesto exija, con fecha.
- Carril C: front read-only, lo arma el asistente en paralelo.
- Convergencia: DB lista + #4 ON + connectors/perfil listos -> primer handoff gobernado = T0 del dataset.

## Invariantes a respetar
Escritor unico (submit_intent; edicion manual = hard-fail); neutralidad de dominio (reglas fiscales en el
perfil, NUNCA en core ni *.template.*); dos planos / sin PII en el event log (DECISION-0033); toda pieza la
jala una necesidad real de Presupuesto con fecha (regla 3.4, anti meta-proyecto perpetuo); cambios visibles
-> SemVer + CHANGELOG; canal mailbox/state ASCII (DECISION-0012).

Brief completo del operador: personal/operador/09_Asistente_pipeline-presupuesto-tesis.md
