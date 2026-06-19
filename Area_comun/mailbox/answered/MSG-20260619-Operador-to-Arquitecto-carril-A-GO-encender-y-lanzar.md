---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-A-GO-encender-y-lanzar
type: DECISION
task_id: TASK-0117
from: Operador
to: Arquitecto
status: answered
answered_by: MSG-20260619-Arquitecto-to-Operador-carril-A-GO-encendido-ack
requires_response: true
response_owner: Arquitecto
one_line_summary: GO del operador para LANZAR hoy el modulo-app de Presupuesto. Fase 1 encender #4 (piloto verde -> ON, su ventana). Fase 2 Carril B. Fase 3 primer handoff. Manten Codex y tu cron activos.
requested_action: Ejecutar Fase 1 (provisioning + piloto + encender #4 si verde) y reportar; luego Fase 2 Carril B; Fase 3 primer handoff cuando converjan #4 ON + Carril B + DB.
question: Reportas resultado del piloto (AC2/AC3/AC5), si #4 quedo ON, version y drift 0?
context_refs:
  - Area_comun/specs/SPEC-0081-activacion-atestacion-autoria.md
  - Area_comun/tasks/TASK-0117-codex-activacion-4-atestacion.md
  - Area_comun/decisions/DECISION-0039-activacion-atestacion-autoria.md
---

# GO operador - ENCENDER #4 y LANZAR el modulo-app de Presupuesto

GO del operador para LANZAR hoy el modulo-app de Presupuesto. Manten a Codex y tu cron ACTIVOS.

## FASE 1 - ENCENDER #4 (su propia ventana de riesgo; NO combinar con SA.4 / authoritative-teeth / subagents / Capa C)
El harness ya esta servido (TASK-0117 in_review).
1. Provisiona segun SPEC-0081 AC1: claves en event_auth.keys + public_keys por agente + anchor remoto/proof real.
2. Corre el PILOTO sobre runs legitimos del propio protocolo: AC2 manipulation-check >=99% (denominador del
   event log, independiente del firmante) + AC3 prueba negativa (6 vectores rechazados con clase) + AC5
   rollback ensayado byte-equivalente. Rollback armado (los 4 flags a false).
3. SI el piloto sale VERDE: enciende #4 (chain_enabled + agent_signatures_enabled + anchor_enabled +
   event_auth.enabled) -> #4 ON. SemVer MINOR + CHANGELOG. Marca TASK-0117 done. REPORTA de inmediato
   (resultado del piloto, version, drift 0). SI NO sale verde: NO enciendas, diagnostica y reporta.

## FASE 2 - CARRIL B (capacidad, solo lo que Presupuesto exige; lo que no dependa de #4 puede ir en paralelo)
- Fase 2 connectors: SQL Server (read-only de la DB ya migrada en D:\Agentes\Ingenas\Budget) + Git + CI;
  deny-by-default, trust_boundary por conector, "MCP no concede autoridad". DECISION + SPEC + golden.
- Fase 1 skills neutrales minimas (verificar regla de negocio vs legacy, convenciones DDL, verificacion de
  migracion). CERO dominio en el core.
- Perfil profiles/financiero_presupuesto/: reglas fiscales (compromiso <= saldo CDP; rubro-fuente-BPIN debe
  preexistir; no auto-crear) + reglas del AGENTS.md de Budget plegadas. FUERA del core neutral.
Cada pieza la jala una necesidad real de Presupuesto CON FECHA (regla 3.4). Flujo DECISION -> SPEC
(acceptance + test_plan) -> golden -> off-by-default; revision Analista+Codex donde aplique.

## FASE 3 - PRIMER HANDOFF GOBERNADO del modulo-app = T0 del dataset
Exige #4 ON + connectors/perfil listos + DB lista. Cuando converjan, emite el primer handoff real del
modulo-app: ahi nace el dataset de tesis, atestado en caliente.

## Recordatorios / invariantes
- DEF-PII (TASK-0118) sigue diferida (antes de captura viva #2/#3 o publicacion). PII de terceros NUNCA entra
  al event log (dos planos, DECISION-0040). La DB de Budget no se toca ni se encripta (corte limpio).
- Seccion 9 (acoplamiento) read-only real verificado por Codex antes de lectura viva del satelite.
- No enciendas mas alla de #4 sin nuevo GO. Escritor unico, neutralidad de dominio, SemVer+CHANGELOG.
- Canal ASCII. Reporta al cerrar cada fase.
