---
id: TASK-0037
owner: Claude
status: proposed
type: documentation
priority: normal
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: []
relates_to: [TASK-0004, TASK-0013]
phase: P2
spec_id: none
objective: Formalizar una guia humana operativa, neutral de dominio y reusable por cualquier proyecto que adopte el protocolo.
expected_output: Plantilla/documento de guia humana con secciones de arquitectura, build, run, test, deploy/lanzamiento, operacion, troubleshooting y enlaces al protocolo; incluir tambien un formato HTML mas facil de leer por un humano.
question_to_resolve: Cual es el contrato minimo de documentacion humana que toda instancia debe completar sin acoplar el core a un dominio ni a nombres concretos de agentes?
closure_criterion: La guia y su formato HTML quedan definidos como artifact/template adoptable, documentados en README_INSTANCIACION.md y validados como neutrales de dominio.
---

# TASK-0037 - Guia humana operativa neutral + HTML

## Intencion
Dejar como trabajo futuro la ultima capa de documentacion para usuarios humanos: una guia que explique
como entender, construir, lanzar, probar y operar una aplicacion gestionada con esta metodologia.

## Alcance futuro
- Definir una plantilla neutral de dominio para la guia humana operativa.
- Incluir secciones esperadas:
  - arquitectura del proyecto/aplicacion;
  - como construir;
  - como ejecutar localmente;
  - como probar;
  - como desplegar/lanzar;
  - operacion diaria;
  - troubleshooting;
  - rutas/protocolos relevantes;
  - roles/capacidades configuradas en la instancia, sin atarlo a Claude/Codex.
- Proveer un formato HTML legible por humanos, ademas del formato markdown/source.
- Documentar en `README_INSTANCIACION.md` cuando y como debe completarse en una instancia.

## No-alcance
- No definir dominio de negocio.
- No introducir reglas especificas de stack en el core.
- No acoplar la guia a dos agentes concretos.

## Nota
El operador pidio dejarlo como futuro trabajo para evitar que esta capa quede desactualizada mientras
se termina la metodologia.
