# ANALISTA - TASK-0100 decision-A (rescope eol=lf) - honestidad/metodologia

> Voz analista independiente (maker != checker). Encargo del operador: revisar honestidad/metodologia de
> decision-A (rescope de TASK-0100). NO repaso el invariante de codigo (lo cubrio Codex); foco
> completitud + honestidad del cierre + claims + A vs B. Falsable, ASCII.
> Fecha 2026-06-14. Manifest: dist/v1.1.0/manifest.json (commit 04436c3, 757 ficheros SBOM, sbom_hash 0083c1c9).

## Veredicto de cabecera

**RATIFICABLE-con-ajustes.** Decision-A (anadir .gitattributes para v1.2.0+, NO re-firmar v1.1.0, firma
INTACTA) es la eleccion correcta -- y mis hallazgos la REFUERZAN (ver punto 4: B no puede reproducir
v1.1.0 de todas formas). PERO la documentacion propuesta ("pre-normalizacion de endings, 3 ficheros") es
**gravemente incompleta y eufemistica**. El defecto real es mayor y en parte IRRECUPERABLE, y la nota de
known-limitations debe decirlo sin minimizar. Ajustes concretos abajo.

Cifra clave (clasificacion exhaustiva de los 757, punto 1): **616 LF / 127 CRLF / 14 mismatch no-EOL**.
El hallazgo nombro 3 CRLF; faltaban 124. Ademas hay 14 ficheros cuyo hash del manifest NO corresponde al
blob del commit 04436c3 bajo NINGUNA normalizacion de EOL.

---

## 1) COMPLETITUD (clasificacion completa de los SBOM-included)

Metodo (falsable): para cada uno de los 757 ficheros del SBOM, compare el sha256 del manifest contra el
blob en el commit registrado (04436c3) en bytes crudos y normalizado LF/CRLF. Script reproducible en
personal/Claude-analista/_classify_eol.py.

- **616 LF** (blob LF, casan; reproducibles bajo LF puro). OK.
- **127 CRLF** (el blob en 04436c3 almacena CRLF; su hash LF-normalizado NO casa el manifest -> ROMPEN la
  reproducibilidad LF). Los 127 (no 3):
  - Area_comun/artifacts/ (4): ANALISIS_CRITICO_TASK-0038_N-AGENT.md, RUNTIME-live-selfrun-20260606.md,
    SPEC-0038_N-AGENT_CONSOLIDADA.md, TASK-0038_IMPLEMENTACION_N_AGENT_READINESS_ANALISIS_TECNICO.md
  - Area_comun/decisions/ (2): DECISION-0023-firma-release.md, DECISION-0024-autonomia-supervisada.md
  - Area_comun/specs/ (6): SPEC-0038, SPEC-0057, SPEC-0058, SPEC-0060, SPEC-0061, SPEC-0064
  - profiles/dotnet_enterprise/ (17): Guia_Metodologica.md, docs/arquitectura/arquitectura-general.md,
    docs/contenedores/estrategia-docker-desarrollo.md, docs/decisiones/adr-001-diseno-base-entorno.md,
    docs/gobierno/versionado-plantillas.md, docs/pipelines/pipeline-base.md,
    docs/seguridad/gestion-secretos-desarrollo.md, docs/seguridad/reglas-uso-ia.md,
    prompts/prompt-maestro-Desarrollo_DotNet.md, templates/azure-pipelines/README.md,
    templates/azure-pipelines/azure-pipelines-dotnet.yml, templates/db-bootstrap-dotnet/db-init.sh,
    templates/devcontainer-dotnet/.devcontainer/Dockerfile,
    templates/devcontainer-dotnet/.devcontainer/devcontainer.json, templates/docker-sqlserver/README.md,
    templates/docker-sqlserver/docker-compose.yml, templates/repo-structure/estructura-base-aplicacion.md
  - examples/dotnet_enterprise_instance/ (20): AGENTS.md, Area_comun/README.md,
    Area_comun/protocol/HANDOFF_TEMPLATE.md, Area_comun/protocol/TASK_TEMPLATE.md,
    Area_comun/reports/HUMAN_REPORT_TEMPLATE.md, Area_comun/state/CLAIMS.json,
    Area_comun/state/TASK_INDEX.json, protocol.config.json, + profiles/dotnet_enterprise/docs|prompts|
    templates (los mismos 12 de arriba, copia bajo el example)
  - examples/full_runtime_instance/ (18): .github/workflows/validate.yml, AGENTS.md, Area_comun/README.md,
    3x mailbox/*/.gitkeep, Area_comun/protocol/{HANDOFF,MAILBOX_MESSAGE,TASK}_TEMPLATE.md,
    Area_comun/reports/HUMAN_REPORT_TEMPLATE.md, Area_comun/state/{CLAIMS,PROJECT_STATE,TASK_INDEX}.json,
    3x personal/*/.gitkeep, protocol.config.json
  - examples/generated_minimal_instance/ (9): AGENTS.md, Area_comun/README.md, 2x protocol/*_TEMPLATE.md,
    reports/HUMAN_REPORT_TEMPLATE.md, state/{CLAIMS,PROJECT_STATE,TASK_INDEX}.json, protocol.config.json
  - examples/profile_validation_cases/ (7 casos x ~7 = ~49): duplicate_profile, missing_dependency,
    protocol_incompatible, remote_reference_warning, valid_local_profile, version_mismatch (+ uno parcial),
    cada uno: AGENTS.md, Area_comun/README.md, protocol/HANDOFF_TEMPLATE.md, protocol/TASK_TEMPLATE.md,
    reports/HUMAN_REPORT_TEMPLATE.md, state/CLAIMS.json, state/TASK_INDEX.json (+ protocol.config.json donde
    aplica). Lista exacta en el script.
- **14 mismatch no-EOL** (el blob en 04436c3 NO casa el manifest ni crudo ni LF ni CRLF). Probe
  (personal/Claude-analista/_probe_other.py): **13 casan con el WORKING TREE actual** (no con 04436c3 ni
  con el tag 703ed93); **1 (runtime/protocol_replay.py) no casa con NADA** (ni worktree, ni 04436c3, ni
  tag). Los 14: 8x examples/**/PROJECT_STATE.json (varios casos), 2x .../db-bootstrap-dotnet/README.md
  (profiles + example), 2x .../devcontainer-dotnet/README.md, examples/neutrality_scan_cases/README.md,
  examples/profile_validation_cases/protocol_incompatible/protocol.config.json, runtime/protocol_replay.py.

**Implicacion del punto 14 (la mas seria, mas alla del EOL):** el manifest firmado se genero sobre un
**ARBOL DE TRABAJO SUCIO**, no sobre un checkout limpio de su commit registrado 04436c3. provenance.json
declara `--commit 04436c3`, pero 14 ficheros del manifest corresponden a contenido NO commiteado (deltas
locales del emisor). Y al menos 1 (protocol_replay.py, en desarrollo activo desde entonces) es
**IRREPRODUCIBLE desde cualquier ref**: su contenido original se perdio. Por tanto v1.1.0 no se reproduce
desde un `git checkout` limpio de ningun commit, ni siquiera en la plataforma original.

PASA/CAMBIO: **CAMBIO REQUERIDO.** La doc debe declarar la clasificacion real completa (616/127/14), no "3
ficheros", y caracterizar el bloque de 14 (arbol sucio + 1 irrecuperable). "Pre-normalizacion de endings"
solo es honesta si describe el estado real entero.

## 2) HONESTIDAD del cierre ("verificable solo bajo condiciones originales")

Esa frase, tal cual, **minimiza** el defecto:
- Para los 127 CRLF: SI es cierto (checkout CRLF, sin .gitattributes, autocrlf manejado) -> documentable.
- Para los 14: las "condiciones originales" NO son un checkout limpio reproducible: son el working tree
  especifico (sucio) del emisor, que ya no existe para protocol_replay.py. "Verificable bajo condiciones
  originales" es, para esos, **indefinido/irrecuperable**, no un mero matiz de EOL.
- Artefacto enviado dist/v1.1.0/verify.integrity.json dice `ok:true, diff vacio`: eso refleja la
  verificacion LOCAL del emisor sobre SU arbol, NO la reproducibilidad por un tercero. Dejarlo sin contexto
  induce a error.

PASA/CAMBIO: **CAMBIO REQUERIDO.** La nota de known-limitations debe ser EXPLICITA y NO eufemistica:
(a) el manifest no corresponde a un checkout limpio del commit registrado (14 deltas sucios vs 04436c3);
(b) protocol_replay.py es irreproducible desde refs; (c) verify.integrity.json ok:true = verificacion del
emisor, no garantia de reproducibilidad de terceros. Y corregir la premisa FALSA de SPEC-0075 ("los blobs
ya son LF" / invariante "ningun blob SBOM cambia": 127 blobs son CRLF; por eso `renormalize` los cambiaria
e invalidaria la firma -- exactamente el bloqueo de Codex).

## 3) CLAIMS (contradice algo publicado?)

- Ningun documento PUBLICADO promete reproducibilidad-LF cross-platform de v1.1.0. SPEC-0075 (status
  proposed, no publicado) enmarca esto como FOLLOW-UP de robustez -> reconoce el hueco. CHANGELOG [1.1.0]
  habla de "authentic release signing", no de reproducibilidad LF de terceros. Por tanto excluir v1.1.0 de
  la promesa LF **no contradice** un claim publicado. PASA.
- UNICA salvedad: dist/v1.1.0/verify.integrity.json (ok:true) es el artefacto que podria leerse como
  "verifica para cualquiera"; contextualizarlo (ver punto 2). Y que la nueva nota NO afirme ningun numero
  no medido (cero "N ficheros" sin la clasificacion que respalda).

## 4) A vs B (re-firmar dana mas que la deuda de A? o racionalizacion?)

El argumento de A "no re-firmar para no dañar la auditabilidad del chain" es **solido, y mas fuerte de lo
que la decision afirma** -- pero por una razon que la decision aun NO usa: **B no puede reproducir v1.1.0**.
El arbol original esta parcialmente perdido (protocol_replay.py irrecuperable; 13 ficheros dependen de un
worktree sucio). Entonces:
- B ("regenerar+re-firmar v1.1.0") NO recupera el release original: produciria un manifest DISTINTO sobre
  un commit limpio y lo firmaria como "v1.1.0" -> fabrica un v1.1.0 limpio que NUNCA existio. Eso es peor
  para la integridad/auditabilidad que A.
- A (documentar la deuda, firma intacta) preserva el artefacto historico real y es honesto SI la
  documentacion es completa.
Conclusion: A es preferible **por integridad**, no solo por evitar trabajo -- PERO el argumento, tal como
esta redactado, compara contra una "deuda EOL pequena" (strawman). No es racionalizacion, pero esta
SUB-INFORMADO. CAMBIO: rehacer el tradeoff A-vs-B contra la deuda REAL (arbol sucio + irrecuperable + 127
CRLF); si se mantiene A (recomendado), que la nota cargue toda la verdad, no solo el EOL.

---

## Ajustes requeridos (concretos, antes de ratificar)

1. Clasificacion completa en la doc: 616 LF / 127 CRLF / 14 no-EOL (adjuntar lista; este artefacto sirve).
2. Known-limitations EXPLICITA y no eufemistica: manifest sobre arbol sucio (no checkout limpio de
   04436c3); protocol_replay.py irreproducible desde refs; verify.integrity.json ok:true = local del emisor.
3. Corregir la premisa falsa de SPEC-0075 ("blobs ya son LF" / "ningun blob cambia"): 127 son CRLF.
4. A-vs-B reargumentado contra la deuda real (incluye: B no reproduce el original -> A preferible por
   integridad). Decision A vs B = del operador; yo solo informo el tradeoff honesto.
5. (equidad) NO contar como defecto el tag 703ed93 != commit 04436c3: es esperado (el tag commitea el
   dist/ firmado sobre HEAD 04436c3, segun su propio mensaje de release).

Con esos 5 ajustes, RATIFICABLE (mantener A). maker != checker: no consolido, no decido (A vs B es del
operador), no muto estado; promocion/firma = del arquitecto/escritor unico.
