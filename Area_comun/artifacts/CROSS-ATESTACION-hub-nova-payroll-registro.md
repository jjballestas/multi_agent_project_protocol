# Registro de cross-atestacion HUB <-> Nova-Payroll (append-only)

> Patron del registro hub<->NOVA (CROSS-ATESTACION-hub-nova-registro.md). Frontera dos-trios
> (DECISION-0095): el hub-Arquitecto LEE la instancia Nova-Payroll y ancla aqui; el ledger de
> Nova-Payroll lo escribe su propio trio. Entradas append-only; una discrepancia entre una entrada
> y el estado re-computado de la instancia es anomalia DECISION-0018 a investigar, nunca a editar.

## Entradas

### Entrada 0 - Nacimiento de la instancia Nova-Payroll (born-operational, DECISION-0096/0097)
- fecha_utc: 2026-07-14T15:50Z (hora local 17:50, UTC+2; ancla escrita ~19:50 UTC)
- disparador: ceremonia de nacimiento AUTORIZADA por la FIRMA de DECISION-0097 (Gate-1, hub
  commit 8e669fc; sellada b13e090, tx seq 4688-4690). Vehiculo del probe de memoria hibrida
  (Fase A PENDIENTE de GO especifico; freno Contabilidad-gana). Primera instancia nacida
  born-operational con el arsenal DECISION-0096 (v1.19.0) COMPLETO desde el genesis (harness
  runner generico + prompts + 5 skills incl. notion-spec-mirror) y con `scratch_root` declarado
  al nacer (DECISION-0098): D:/Aegis_Scratch/Nova-Payroll/.
- payroll_repo: LOCAL-ONLY por orden del Operador (RESP nova-payroll-remoto-local-por-ahora:
  sin repo GitHub ni push hasta GO explicito, probable post-sello E2). Carpeta de trabajo
  D:/Agentes/NOVA-Suite/Nova-Payroll (modelo 2.A: gobierno como subcarpeta Aegis/ del repo de
  producto). El commit hash es content-addressed: el anclaje sigue siendo verificable cuando el
  remoto se publique.
- payroll_commit: 95af2a4098c85e9d4620c3dab6e6c5ffe0cefa4d (rama main; NOTA: un reporte
  intermedio cito 0e01cb3 -- fue el commit pre-amend; el amend de limpieza que des-trackeo
  __pycache__/ y event-state.runtime.json produjo el hash final 95af2a4, unico commit de la rama)
- head_seq: 1
- head_prev_hash: 11989f135519bbb219849a3753fdcbd436a70f4dffc6477f84704bee1275f253
- sha256_events_jsonl (blob git, Aegis/runtime/state/events.jsonl): 349056de533819cb84d1c2bbaa398bb35a43256f18bb8a4a7eebabc7eb4e2514
- sha256_head_line: 349056de533819cb84d1c2bbaa398bb35a43256f18bb8a4a7eebabc7eb4e2514 (== events:
  1 solo evento)
- event_count: 1 (seq 1 = protocol.genesis FRESCO, boundary 1970-01-01T00:00:00Z, firmado por
  arquitecto:v1; re-emitido tras inyectar las pubkeys REALES de los humanos -- el genesis liga el
  config FINAL)
- config-epoch sha8 (blob git, Aegis/protocol.config.json): 4229BDBC
- config canonical_hash (JSON parseado, lo que liga el genesis): 0345B5D9
  (0345b5d9f3388c6776b39bcfbc6853ed97d1aea1799ddb94064f683d92a306eb)
- firmantes ed25519 (5, en event_state.signature_config.public_keys + agent_registry):
  arquitecto:v1 (orchestrator+reviewer), codex:v1 (implementer), analista:v1 (reviewer),
  jball:v1 (human_owner, John), jheredia:v1 (implementer, Julian) -- **jball y jheredia con sus
  PUBKEYS REALES (las mismas de NOVA), firmantes DESDE EL GENESIS**; sus privadas generadas por
  el instanciador fueron BORRADAS antes del genesis (jamas viven en esta maquina); el override
  local firma solo por el trio. Llaves del trio en protocol-secrets/ (gitignored).
- guardrails de nacimiento (AGENTS.md s.4, clausulas de DECISION-0097): PII de nomina FUERA del
  store de memoria y del ledger; probe = demostracion NO citable (anti-HARKing); Fase A solo
  tras GO especifico del operador.
- verificacion (re-computada por el Arquitecto en CLON LIMPIO D:/Aegis_Scratch/Nova-Payroll/ccv
  en 95af2a4): validate_collaboration_state.py exit 0; scan_encoding.py exit 0; genesis unico
  con los 5 firmantes; sin secretos/pycache/override en el arbol commiteado. El hub (2E35F26E /
  1.14.0, dataset N=500, sellos E1/N=6) NO se toco.
