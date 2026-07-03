# DRAFT intake block TASK-0244 (F1-G release v1.18.0) - pegar antes de proposed->ready

intake:
  type: doc
  goal: Release v1.18.0 (CHANGELOG + tag SemVer sobre commit verde en clon limpio) SIN bumpear el epoch pineado; templates sincronizados con las reglas F1.
  acceptance:
    - CHANGELOG.md actualizado a v1.18.0 con las entradas F1 (intake gate, exception.recorded, trailers, taxonomia, envelope+fixloop, DECISION-0084).
    - Tag v1.18.0 creado sobre commit con los 3 gates verdes en clon limpio.
    - Templates (.template.*) sincronizados con intake / exception / trailers / envelope.
    - protocol.config.json byte-identico (epoch 1.14.0 PINNED, DECISION-0047).
    - FYI al operador con el tag y el estado de activacion de trailers.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - CHANGELOG.md
    - AGENTS.template.md
    - Area_comun/protocol/
  out_of_scope:
    - NO bumpear protocol_version/epoch ni tocar protocol.config.json (re-genesis coordinada unica via DECISION-0047).
    - La activacion del trailer_start_seq es un paso explicito SEPARADO previo (residual 0242), no parte del tag.
    - No relanza crons (gate de permisos del operador).
  risk: medium
  estimate: M
