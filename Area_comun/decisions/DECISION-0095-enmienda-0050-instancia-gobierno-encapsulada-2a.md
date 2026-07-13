---
decision_id: DECISION-0095
title: Enmienda a DECISION-0050 - modelo de instancia de gobierno ENCAPSULADA (2.A, un-repo) bajo carpeta constante Aegis/ + frontera de dos trios + marca Aegis
status: accepted
ratified_at: 2026-07-13
date: 2026-07-13
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
amends: [DECISION-0050]
relates_to: [DECISION-0050, DECISION-0049, DECISION-0035, DECISION-0047, DECISION-0088, DECISION-0093]
phase: P2
---

# DECISION-0095 - Enmienda a DECISION-0050: instancia de gobierno encapsulada (modelo 2.A)

> ACCEPTED por el operador (2026-07-13, directiva en sesion). Convencion de METODOLOGIA, neutral (cero
> dominio). REFINA (no reemplaza) DECISION-0050. NO toca el config pinned del hub (#4 epoca 1.14.0,
> 2E35F26E), ni el dataset N=500, ni el sello N=6. Ya IMPLEMENTADA y atestada (ver Evidencia).

## Contexto / por que la enmienda

DECISION-0050 punto 1 dice "Gobernanza/coordinacion/atestacion -> SIEMPRE en el protocolo (hub);
nunca dentro de un repo de producto (alli no se atestaria)". En la practica, lo que NO puede vivir en
el repo de producto es el **ANCLA de atestacion** (el hub/beacon externo que atesta la cadena). Los
**eventos de gobierno de una instancia de producto** (su ledger #4, tasks, mailbox) SI pueden vivir
DENTRO del repo de producto -- como una subcarpeta -- siempre que se **cross-atesten al hub**. Esto
permite "un solo git por producto" sin perder el rigor, y es la demostracion viva de adoptabilidad.

## Decision (refina DECISION-0050 punto 1; el resto de 0050 sigue vigente)

1. **Aegis = nombre de la capa de gobernanza (la metodologia).** Al instanciarse dentro de un producto,
   el gobierno vive en una **carpeta CONSTANTE `Aegis/`** en la raiz del repo de producto. La carpeta es
   constante en TODOS los productos (asi `new_instance.py`, el CI y el harness apuntan a `Aegis/` sin
   saber el nombre del producto); la **identidad de la instancia** lleva el nombre simbolico
   `<Producto>-Aegis` (en config/agent_registry). "Aegis" = el escudo del producto.

2. **Modelo 2.A (un-repo, instancia ENCAPSULADA):** para el tier **attested** (productos), TODO el
   gobierno (Area_comun/, runtime/, scripts/, skills/, personal/, protocol.config.json,
   event-state.runtime.json, AGENTS.md) vive bajo `Aegis/`. La **raiz del repo queda SOLO producto**
   (codigo, build, README propio). El tier attested nace encapsulado por defecto; los tiers
   coordination/runtime conservan el layout raiz (retrocompatibles).

3. **La cross-atestacion (ANCLA) vive en el HUB.** Cada instancia de producto se ancla en el hub con un
   registro append-only `Area_comun/artifacts/CROSS-ATESTACION-hub-<producto>-registro.md` (patron
   DECISION-0088 p.5 / 0093). Eso es lo que "no puede vivir en el producto"; los eventos de gobierno del
   producto SI (en `Aegis/`).

4. **Frontera de DOS TRIOS:** cada producto tiene su PROPIA instancia de gobierno con su trio
   (Arquitecto/Codex/Analista + firmantes humanos). El **hub-Arquitecto NO escribe el ledger de otras
   instancias** (ni submit_intent, ni task/claim); solo lo LEE (git fetch) para anclar la cross-atestacion
   en el hub. Dos Arquitectos en repos distintos = sin colision.

5. **El sello es agnostico a la ruta.** El `protocol.genesis` liga `canonical_hash(protocol.config.json)`
   = JSON parseado (independiente de line-endings y de la RUTA del archivo). Por tanto **mover el gobierno
   a `Aegis/` es un `git mv` puro: NO requiere re-genesis ni re-sello** (los hashes de contenido de
   events.jsonl y config no cambian). Los hashes crudos de una atestacion se computan sobre el **blob de
   git** (`git show <commit>:<path>`), nunca sobre el working copy (que puede tener CRLF por autocrlf).

6. **Contrato de layout encapsulado (invariantes que emite `new_instance.py`):**
   - `.github/workflows/validate.yml` queda en la **raiz del repo** (GitHub solo corre `.github/` de la
     raiz) con `defaults.run.working-directory: Aegis`. El tooling se auto-localiza (root = parents[1] de
     la ruta del script), sin flags nuevos.
   - El validador runtime-tier acepta el workflow requerido en la raiz del repo (un nivel arriba del root
     de la instancia encapsulada). Retrocompatible: las instancias root-layout pasan por la rama in-root.
   - `.gitattributes` con `eol=lf` scoped a `Aegis/**` (byte-estabilidad); `.gitignore` con las rutas de
     gobierno bajo `Aegis/`.
   - `Aegis/.claude/` + `Aegis/CLAUDE.md` = config de Claude Code de GOBERNANZA, aislada del `.claude` del
     producto. **Claude Code enraiza en el CWD:** una sesion de gobernanza lanzada con cwd=`Aegis/` carga
     SOLO `Aegis/.claude`; una sesion de producto en la raiz nunca la carga (aislamiento bidireccional
     verificado empiricamente). Caveat operacional: el "trust gate" de Claude Code aplica por carpeta una vez.
   - Las instancias generadas nacen con COMMIT_TRAILERS deshabilitado (no heredan el gate vivo del hub) y
     validan al nacer.

## Alcance / No-alcance

- **En alcance:** fijar el modelo 2.A + la marca Aegis + la frontera dos-trios como contrato de layout de
  instancia; neutral, metodologico. Ya reflejado en `scripts/new_instance.py`, los validadores py+ps1 y el
  registro de cross-atestacion.
- **Fuera de alcance:** tocar #4/config pinned del hub, el dataset N=500 o el sello N=6; cambiar el modelo
  single-operator (multi-tenant = DECISION futura). No obliga a migrar instancias root-layout existentes.

## Consecuencias

- Un producto mantiene UN solo git con raiz limpia (solo producto) y su gobierno encapsulado en `Aegis/`,
  cross-atestado al hub. Es la adoptabilidad "publicar para ser citado" hecha carne.
- El hub sigue siendo el ancla permanente de atestacion de todas las instancias (DECISION-0050 intacto en
  ese punto); lo que se refina es DONDE viven los EVENTOS de gobierno de un producto (subcarpeta, no hub).
- Cada producto futuro nace encapsulado con `new_instance.py --tier attested` (carpeta `Aegis/` por defecto).

## Evidencia (ya implementada y atestada)

- **NOVA** (primera instancia 2.A) retrofiteada: commit NOVA `5518b5a`, gobierno bajo `Aegis/`, sello
  byte-preservado (events `4f69a3dc...`, config canonical `C157FE00`, blob `C2DE91F9`), validate/scan/
  neutralidad 0. Cross-atest hub: `Area_comun/artifacts/CROSS-ATESTACION-hub-nova-registro.md` (Entrada 1).
- **Hub** commit `8b03d4d`: `new_instance.py` (tier attested encapsulado + `Aegis/.claude`), validadores
  py+ps1 encapsulation-aware, `test_attested_instancing.py` verde.
- Hallazgo empirico del aislamiento por-CWD del `.claude` (medido con `claude -p --debug`).
