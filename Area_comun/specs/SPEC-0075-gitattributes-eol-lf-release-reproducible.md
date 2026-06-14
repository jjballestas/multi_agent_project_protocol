---
spec_id: SPEC-0075-gitattributes-eol-lf-release-reproducible
task_id: TASK-0100
type: design
status: proposed
created_at: 2026-06-10
author: Claude (arquitecto)
linked_decisions: [DECISION-0023, DECISION-0006, DECISION-0019]
relates_to: [TASK-0100, TASK-0099, DECISION-0023]
---

> Formaliza el follow-up de robustez del release v1.1.0: el SBOM hashea bytes LF, pero un checkout en
> Windows con `core.autocrlf=true` (sin `.gitattributes`) produce CRLF y `verify_release` falla para un
> tercero. Aditivo, neutral, sin cambio de contrato. NO requiere decision nueva (DECISION-0006 robustez
> operacional + DECISION-0023 verificabilidad del release).

# Diseno - .gitattributes eol=lf para releases reproducibles cross-platform

## 1. Objetivo

Hacer que la verificacion del release sea REPRODUCIBLE en cualquier plataforma. Hoy no hay `.gitattributes`;
el repo guarda blobs LF, pero un clon/checkout en Windows con `autocrlf=true` materializa CRLF -> el SBOM
(que hasheo bytes LF) no coincide -> `verify_release` da `ok:false` por diff de line-endings, aunque el
contenido sea identico. El emisor (LF) verifica bien; un tercero en Windows-autocrlf no. Hallazgo concreto:
durante el corte v1.1.0, un `git checkout` re-aplico CRLF a `README_INSTANCIACION.md` (18966 vs 18555 LF) y
rompio la verificacion hasta restaurar los bytes LF.

### Enmienda 2026-06-14 (DECISION-0037)

La premisa original de esta spec ("los blobs ya son LF" y ningun blob SBOM-included cambia) era cierta para
`HEAD`, pero **falsa para v1.1.0**: el manifest firmado contiene 616 ficheros reproducibles bajo LF, 127
ficheros CRLF en el commit registrado y 14 mismatches no-EOL generados desde un arbol de trabajo sucio. Por
tanto esta spec queda acotada a releases **v1.2.0+**. `v1.1.0` queda documentado como release historico
pre-normalizacion en `dist/v1.1.0/KNOWN_LIMITATIONS.md`; su manifest y firma no se regeneran ni se
re-firman.

## 2. Alcance

- Anadir `.gitattributes` en la raiz que NORMALICE line-endings a LF en checkout para los archivos de texto
  que entran al SBOM (y en general al repo), de modo que un checkout fresco sea byte-identico al que el SBOM
  hasheo, independiente de `core.autocrlf`.
- Regression/verificacion determinista: un checkout limpio (simulando autocrlf=true) produce LF y
  `verify_release` da `ok:true` (diff vacio).

## 3. No-alcance

- NO cambiar el contenido de ningun archivo SBOM-included (solo line-endings; los blobs ya son LF, asi que
  no debe cambiar ningun hash de contenido logico). NO renormalizar a CRLF. NO tocar binarios.
- NO re-firmar v1.1.0: `.gitattributes` NO esta en los include-globs del SBOM, asi que anadirlo no cambia el
  `sbom_hash` ya firmado; el fix protege FUTUROS checkouts/verificaciones del tag existente y releases
  futuros. (Confirmar que los blobs LF actuales no cambian al anadir `.gitattributes`; si `git add
  --renormalize` mostrara cambios reales de bytes en archivos SBOM-included, eso INVALIDARIA la firma de
  v1.1.0 -> en ese caso, blocked + nota al arquitecto antes de commitear.)

## 4. Diseno

- `.gitattributes` raiz, p.ej.:
  - `* text=auto eol=lf` (normaliza texto a LF en checkout; git detecta binarios) o un set curado por tipo
    (`*.md`, `*.py`, `*.json`, `*.ps1`, `*.txt`, `*.yml`/`*.yaml`, `LICENSE`, etc. con `text eol=lf`) +
    binarios marcados `-text`/`binary` explicitos. El implementador elige el enfoque mas seguro que NO
    altere bytes de archivos SBOM-included existentes.
- Verificar con `git add --renormalize .` en un arbol limpio que NO hay cambios de bytes en archivos
  SBOM-included (los blobs ya son LF). `.ps1` se mantienen LF salvo que algun consumidor exija CRLF (no es el
  caso aqui; los wrappers .ps1 corren con LF).

## 5. Invariantes (no negociables)

1. NINGUN archivo SBOM-included cambia de bytes (solo se fija la politica de checkout). El `sbom_hash`
   firmado de v1.1.0 (0083c1c9...) sigue valido; `verify_release` del tag sigue `ok:true` en LF.
2. Cross-platform: en Linux y Windows un checkout fresco produce LF identico -> `verify_release` `ok:true`.
3. No rompe `.ps1` (siguen ejecutando) ni CI. Neutral, ASCII, sin secretos.

## 6. Tests

- Regresion determinista: en un clon/worktree limpio con `core.autocrlf=true` simulado, los archivos texto
  salen LF y `verify_release --root . --manifest dist/v1.1.0/manifest.json` da `ok:true` (diff vacio).
- `git add --renormalize .` no introduce cambios de bytes en archivos SBOM-included (prueba de no-regresion
  sobre la firma existente).
- validador/neutralidad/encoding verdes; suites de release tooling siguen verdes.

## 7. SemVer y neutralidad

PATCH aditivo (robustez/reproducibilidad de release engineering; sin cambio de contrato). Neutral.
DECISION-0006 / DECISION-0023.

## 8. Cierre

Implementacion = TASK-0100 (owner Codex). `.gitattributes` + regresion de reproducibilidad verde; firma de
v1.1.0 intacta (verificado que ningun blob SBOM-included cambia); cross-platform; handoff con evidencia.
Ratificacion adversarial del arquitecto (firma intacta + reproducibilidad LF cross-platform).
