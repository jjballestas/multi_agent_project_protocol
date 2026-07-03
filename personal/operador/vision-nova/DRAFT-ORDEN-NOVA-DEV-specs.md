# DRAFT ORDEN NOVA-DEV - Revision adversarial del paquete + SPECs gobernadas (post-F1)

- estado: DRAFT listo del asesor (2026-07-03). SE CONVIERTE EN MSG cuando F1 cierre
  (el hold del operador "despues de que termine lo que esta haciendo" expira ahi).
  Enviar DESPUES de la orden F2 (la instancia es el camino critico).
- contenido del MSG futuro (ACTION Operador -> Arquitecto):

[DIRECTIVA]
1. El Operador construyo el paquete NOVA-DEV en D:/Agentes/Ingenas/Budget/02_Analysis/
   Arquitectura/ (NOVA_GOAL_Desarrollo_Aplicacion.md, NOVA_PROMPT_Arranque_Agente_
   Desarrollo.md, NOVA_SPEC_Plantilla_Requisitos.md, maestro NOVA_PRES_00 + Docs
   01-12). Tu tarea (registrala con intake, owner Arquitecto): (a) REVISION
   ADVERSARIAL del paquete (tomar lo bueno, complementar huecos, senalar
   contradicciones con la doctrina v1.18.0); (b) GENERAR las SPECs gobernadas del
   Sprint 1 usando NOVA-SPEC-T-001 UNIFICADA con el intake v2/DoR de DECISION-0084
   (un solo formato, no dos compitiendo).
2. ALCANCE ACOTADO POR EL ESTUDIO: SPECs SOLO para unidades del brazo GOBERNADO
   segun NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md (misma carpeta Ingenas):
   miembros gobernados de pares, familia P3, pool Q4, BR-C4. Las unidades BASELINE
   (GOAL-P1, P2.1, P2.2, P4.1, miembros baseline de pares) son del Operador y NO se
   tocan ni se leen sus fuentes (regla de aislamiento intra-par del estudio).
3. RESPETAR el sello del estudio: los alcances de unidades selladas no se
   redefinen; cambios = enmienda fechada via Operador.
4. Entregable: SPECs commiteadas + informe corto de la revision adversarial
   (hallazgos/complementos) + FYI al Operador.

[RECOMENDACION]
- Secuencia sugerida de SPECs: primera_unidad P3.1, luego pool Q4 en el orden del
  sorteo de Etapa 2; los miembros gobernados de pares al final (encajan post-17-jul
  cuando el patron congelado exista).
- El informe adversarial puede proponer mejoras al NOVA_PROMPT para v1.1 del
  paquete; se aplican por el Operador, no directo (los docs viven fuera del hub).
