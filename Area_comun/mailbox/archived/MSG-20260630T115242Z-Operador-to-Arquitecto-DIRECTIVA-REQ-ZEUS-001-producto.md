---
message_id: MSG-20260630T115242Z-Operador-to-Arquitecto-DIRECTIVA-REQ-ZEUS-001-producto
task_id: REQ-ZEUS-001
type: DIRECTIVE
from: Operador
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
operator_directive: true
created_at: 2026-06-30T11:52:42Z
context_refs:
  - D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/REQUERIMIENTO_Zeus-Aegis_Productizacion_y_Metodologia.md
  - D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/TEMP_Guia_Modelos_Peones_y_Medicion.md
  - D:/Agentes/Zeus/Zeus-Aegis
question: "Reconciliado el trabajo en curso bajo REQ-ZEUS-001, cerradas D1-D5 (con D3/WS4 segun la guia de peones) y dado de alta el Analista? Confirmar plan + ETA."
requested_action: "Adoptar REQ-ZEUS-001 como meta activa de Zeus-Aegis-como-producto: registrar la decision de adopcion + backlog (TASK-ZEUS-0001..0010) en el protocolo (hub, DECISION-0050); cerrar primero D1-D5 (recomendaciones endosadas por el Operador) con D3/WS4 incorporando la guia de peones; dar de alta al Analista (WS5) antes de tareas owner:Analista; reconciliar 0222/0223/0225/0226/0227 como F1/infra ya hechos y pivotar el backlog a WS2/WS3/WS4/WS5. F2 al ledger medido sigue FUERA de alcance; TFM intocable. Registrar plan + ETA por mailbox."
one_line_summary: "Operador adopta REQ-ZEUS-001 como meta de producto, reconcilia el trabajo actual y ordena incorporar la guia de modelos peones en WS4/D3."
---

Directiva del Operador al Arquitecto.

META
- El Operador quiere **ejecutar Zeus-Aegis como producto** para desarrollo de apps con agentes coordinados.
  Esa ES la idea de la metodologia y tu respuesta previa fue correcta. REQ-ZEUS-001 es la pista; adoptarla.

1) ADOPTAR REQ-ZEUS-001 como meta activa
   - Registrar en el HUB del protocolo (DECISION-0050): una DECISION de adopcion + el backlog
     TASK-ZEUS-0001..0010 en TASK_INDEX (refinado por ti). Gobernanza siempre en el protocolo.
   - Reconciliar lo en curso (NO tirar trabajo): 0226 = WS1 branding (hecho); 0227 = infra test-verde;
     0222/0223 = vistas F1 (stats / instanciar-preparar-comando). Cerrar/encolar lo abierto y PIVOTAR el
     backlog hacia el grueso de producto: WS2 bootstrapper, WS3 instalador, WS4 backend, WS5 4 firmantes.

2) SECUENCIA (como pide el propio REQ): primero las decisiones y los firmantes
   - TASK-ZEUS-0001: cerrar D1-D5 en Area_comun/decisions/ (aprueba el Operador). Endosos del Operador:
     D1 = coordination-only (Ed25519 = add-on opcional, no base del producto).
     D2 = una instancia por proyecto via new_instance.py (lider = human_owner).
     D3 = backend por niveles (ver punto 3, guia de peones).
     D4 = hermes-agent desde fuente si la licencia no permite redistribuir; vendorizar solo si la permite.
     D5 = rebranding ligero (UI/strings/i18n + alias ZEUS_*->HERMES_* con shim), sin renombrar binarios.
   - TASK-ZEUS-0007: ALTA del Analista (checker) en la(s) instancia(s) ANTES de tareas owner:Analista
     (si no, el validador las rechaza); decision de mapeo rol->agente citando NOVA-ARQ-001; mantener
     allow_self_review:false / allow_self_qa:false (maker!=checker).

3) WS4 / D3 -- INCORPORAR LA GUIA DE MODELOS PEONES (requisito del Operador)
   Fuente: TEMP_Guia_Modelos_Peones_y_Medicion.md. El producto debe contemplar:
   - **Niveles de modelo:** frontera (firmantes: Arquitecto/Codex/Analista) + **peon NO-firmante** (drafter
     barato). Peon local recomendado: Qwen2.5-Coder-7B (Ollama, Q4 ~4.7GB); contraste DeepSeek-Coder-6.7B.
     Alternativa sin instalar: free tiers (Gemini Flash-Lite / OpenRouter / Groq) -- nunca PII al free tier.
   - **Codegen antes que LLM:** si la salida es funcion mecanica de la entrada (CRUD, DTOs, mappers,
     cliente OpenAPI) usar scaffolding/plantillas/Roslyn, no modelo. Reservar el peon para la variacion con criterio.
   - **Patron obligatorio:** peon = maker barato; un firmante distinto hace de checker y FIRMA (maker!=checker).
     El peon nunca toca reglas de negocio ni el repo del protocolo.
   - **Gate determinista** que abarata la supervision: build + test + arch-tests + lint + scan encoding +
     guard "sin logica de negocio / sin deps nuevas". Verde -> el firmante ojea el diff y firma.
   - **Procedimiento de medicion** (3 brazos A/B/C; la metrica que decide = tokens del firmante) para
     decidir con datos si el peon ahorra. D3 = punto unico de claves/costo + bloqueo de PII.

4) RESTRICCIONES (no negociables)
   - F2 write-through al ledger MEDIDO sigue gateado/fuera de alcance; el producto opera coordination-only
     sobre la instancia del proyecto (NOVA), no sobre el ledger del TFM.
   - **TFM intocable:** no modificar el core de multi_agent_project_protocol salvo orden explicita.
   - Nota N=500: la "regla de oro" de la guia condicionaba los peones a post-N=500; el dataset YA esta sellado
     en 500, asi que esa condicion se cumple. Aun asi, el piloto de peones va en repo sandbox aparte
     (D:/Agentes/Zeus/piloto-peones), nunca dentro del repo medido.
   - Licencias: conservar NOTICE de Hermes (MIT) y verificar la licencia de hermes-agent antes de redistribuir.
   - Sin secretos en repos; sin PII saliente.

ENTREGABLE INMEDIATO
- Plan reconciliado (mapa tareas-actuales -> workstreams REQ-ZEUS) + D1-D5 redactadas para aprobacion del
  Operador + ETA. NO crear tareas owner:Analista antes del alta del Analista.

Reportar por mailbox: plan + ETA + dudas concretas si las hay.
