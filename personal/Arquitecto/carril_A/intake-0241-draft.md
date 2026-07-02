# DRAFT intake block TASK-0241 (F1-D taxonomia) - pegar en frontmatter antes de proposed->ready

intake:
  type: doc
  goal: Taxonomia de defectos D1-D4 ampliada con severidad del checker y subconteo declarado, gateada por el Analista.
  acceptance:
    - Doc versionado en Area_comun/protocol/ cubre los 6 huecos del veredicto (requisito mal entendido, deuda de arquitectura, performance no testeada, UX/soporte, integracion externa, conciliacion tardia) mas seccion de subconteo esperado.
    - Escala de severidad CRITICAL / WARNING-real / WARNING-theoretical / SUGGESTION adoptada con la regla "si el uso normal lo dispara, es real" y reflejada en el prompt del checker (Analista).
    - Prueba de mesa con 10 defectos historicos del repo re-clasificados sin residuo, anexada al doc.
    - GO adversarial del Analista sobre la taxonomia.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - Area_comun/protocol/
    - personal/analista/
  out_of_scope:
    - No toca validadores ni gates automaticos (la taxonomia es doc + prompt del checker, no codigo).
    - protocol.config.json y los 5 pineados permanecen intocables.
    - No re-clasifica el dataset TFM sellado N=500.
  risk: low
  estimate: M
