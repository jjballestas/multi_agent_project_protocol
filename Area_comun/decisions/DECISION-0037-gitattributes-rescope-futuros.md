---
decision_id: DECISION-0037
title: .gitattributes eol=lf acotado a releases FUTUROS; v1.1.0 = release pre-normalizacion (rescope TASK-0100, opcion A)
status: accepted
date: 2026-06-14
ratified_at: 2026-06-14
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0001, DECISION-0023, SPEC-0075, TASK-0100]
phase: P2
---

# DECISION-0037 - .gitattributes eol=lf acotado a releases futuros (opcion A)

> Estado: ACCEPTED (2026-06-14). GO del operador a opcion A, condicionado a la concurrencia del analista
> (flujo 0036); el analista CONCURRIO con A con ajustes de DOCUMENTACION (no de alcance), incorporados.
> Cambio ADITIVO, neutral, OFF-PILOT. NO toca la firma de v1.1.0. NO toca #3/#4/SA.4.

## Contexto

TASK-0100 (.gitattributes eol=lf) se bloqueo al evidenciar Codex que el manifest firmado
`dist/v1.1.0/manifest.json` (commit 04436c3, 757 ficheros SBOM, sbom_hash 0083c1c9) no es reproducible bajo
LF. La pasada del analista clasifico los 757 al byte (artefacto
`Area_comun/artifacts/ANALISTA-TASK-0100-decision-A-eol-rescope.md`, scripts reproducibles):

- **616 LF** -- casan bajo LF puro (reproducibles).
- **127 CRLF** -- el blob en 04436c3 almacena CRLF; su hash LF-normalizado NO casa el manifest -> rompen la
  reproducibilidad LF. (Codex nombro ~3; reales = 127.)
- **14 mismatch no-EOL** -- el blob en 04436c3 NO casa el manifest ni crudo ni LF ni CRLF. De esos, **13
  casan con un working tree (sucio) del emisor** y **1 (`runtime/protocol_replay.py`) no casa con NADA**
  (ni worktree, ni 04436c3, ni el tag): su contenido original se perdio.

**Hallazgo central (mas serio que el EOL):** el manifest firmado se genero sobre un **ARBOL DE TRABAJO
SUCIO**, no sobre un checkout limpio de su commit registrado 04436c3 (`provenance.json` declara `--commit
04436c3`, pero 14 ficheros corresponden a contenido no commiteado). Por tanto **v1.1.0 NO se reproduce
desde un `git checkout` limpio de ningun commit, ni en la plataforma original**, y al menos un fichero es
**irrecuperable**.

**Correccion de premisas (honestidad):** "los blobs en git ya son LF" es cierto para **HEAD** (verificado:
`git ls-files --eol` -> 0 CRLF en HEAD; se normalizaron DESPUES), pero NO para el commit del release
04436c3 (127 blobs CRLF). La premisa de SPEC-0075 ("ningun blob SBOM cambia con renormalize") era **falsa**
para v1.1.0: 127 blobs eran CRLF, por eso `renormalize` los cambiaria e invalidaria la firma -- exactamente
el bloqueo de Codex. `dist/v1.1.0/verify.integrity.json` (`ok:true`) refleja la verificacion **LOCAL del
emisor sobre su arbol**, no la reproducibilidad por terceros.

Consecuencia: `.gitattributes` solo puede garantizar releases **FUTUROS** (v1.2.0+); v1.1.0 queda como
release historico con deuda de integridad documentada.

## Decision (opcion A)

Se acota TASK-0100 a **proteger releases futuros**, sin tocar el artefacto firmado de v1.1.0. Alcance fijo
(sin cambios respecto al GO del operador):

1. **`.gitattributes eol=lf` para v1.2.0+**: anadir `.gitattributes` raiz que fije LF en checkout para
   archivos de texto (binarios marcados), de modo que los releases **a partir de v1.2.0** sean
   LF-reproducibles cross-platform. Pre-condicion ya verificada: en HEAD, `git add --renormalize .` solo
   stagea `.gitattributes` (CERO cambios de bytes en SBOM-included del HEAD).
2. **v1.1.0 = release historico con deuda de integridad (nota known-limitations EXPLICITA, no
   eufemistica)**: documentar la verdad completa, con la clasificacion real **616 LF / 127 CRLF / 14
   no-EOL** (lista en el artefacto del analista) y, ademas del EOL: (a) el manifest se genero sobre un
   **arbol sucio** (14 deltas vs el commit registrado 04436c3), no sobre un checkout limpio; (b)
   `runtime/protocol_replay.py` es **irreproducible desde refs** (contenido original perdido); (c)
   `verify.integrity.json ok:true` = verificacion **local del emisor**, no garantia de reproducibilidad de
   terceros; (d) la premisa de SPEC-0075 ("ningun blob SBOM cambia") era falsa (127 CRLF) y queda
   corregida. Su **firma NO se toca** y sigue valida (autentica el artefacto que se publico); un
   `verify_release` de v1.1.0 que falle bajo checkout limpio/LF es **esperado y documentado**, no una
   regresion. (Equidad: el tag 703ed93 != 04436c3 NO es defecto -- el tag commitea el `dist/` firmado
   sobre HEAD 04436c3, segun su mensaje de release.)
3. **`verify_release` fija/excluye v1.1.0 de la promesa LF**: la garantia de reproducibilidad LF aplica
   **desde v1.2.0**; v1.1.0 queda marcado/excluido como pre-normalizacion (mecanismo concreto = la
   implementacion de la TASK-0100 reabierta: nota en `dist/v1.1.0/` y/o trato explicito en
   `verify_release`, sin alterar el manifest firmado).

**Descartado: opcion B** (regenerar/rectificar + re-firmar el manifest de v1.1.0). Ademas de invalidar la
firma vigente, el hallazgo del analista la refuerza: **B no puede reproducir v1.1.0** -- el arbol original
esta parcialmente perdido (`protocol_replay.py` irrecuperable; 13 ficheros dependen de un worktree sucio),
asi que B produciria un manifest DISTINTO sobre un commit limpio y lo firmaria como "v1.1.0", **fabricando
un v1.1.0 limpio que nunca existio** -- peor para la integridad/auditabilidad que documentar la deuda real.
Por eso A es preferible **por integridad**, no solo por evitar trabajo. B seria una decision/tarea de
release aparte con aprobacion humana + ceremonia de firma; no se hace aqui.

## Alcance / No-alcance

- **En alcance:** rescope de TASK-0100 (acotada a futuros + documentar v1.1.0 + pin en verify_release);
  `.gitattributes`; nota de v1.1.0; SemVer **PATCH** + CHANGELOG (fix de robustez/reproducibilidad, sin
  nueva capacidad ni ruptura). El bump se aplica al CERRAR TASK-0100 (cuando Codex entregue), no aqui.
- **Fuera de alcance:** regenerar/re-firmar v1.1.0 (opcion B); cualquier cambio al manifest firmado; tocar
  #3/#4/SA.4/subagents/team_bridge; re-armar SA.4. Neutralidad de dominio intacta.

## Versionado y neutralidad (DECISION-0001)

Aditivo (anade `.gitattributes` + docs + un pin de alcance en verify_release; no remueve comportamiento ni
rompe compatibilidad). **PATCH** (v1.9.0 -> v1.9.1) al cierre de TASK-0100. Neutral; sin secretos; firma
v1.1.0 intacta.

## Consecuencias

- Releases v1.2.0+ verifican reproduciblemente cross-platform bajo LF; se elimina el falso-drift por
  endings en verificaciones read-only futuras.
- v1.1.0 queda como release historico pre-normalizacion, honestamente documentado: su firma es valida pero
  su verificacion requiere las condiciones originales (endings mixtos), no LF puro. Sin numero/promesa no
  medida.
- TASK-0100 sale de blocked con alcance acotado; Codex la implementa; trio reanuda 0095 -> 0096.

## Acceptance (estructural, al cierre de TASK-0100)
- `.gitattributes` raiz presente; `git add --renormalize .` no altera bytes SBOM-included del HEAD (firma
  intacta, verificado).
- v1.1.0 documentado como pre-normalizacion; `verify_release` trata/excluye v1.1.0 de la promesa LF sin
  tocar el manifest firmado; releases futuros (smoke) LF-reproducibles.
- validador/neutralidad/encoding verdes; drift 0; .ps1 paridad; PATCH 1.9.1 + CHANGELOG.
