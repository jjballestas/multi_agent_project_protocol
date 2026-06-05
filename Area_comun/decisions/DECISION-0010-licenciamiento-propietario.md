---
decision_id: DECISION-0010
title: Licenciamiento propietario (All Rights Reserved) + repo privado
status: accepted
date: 2026-06-05
ratified_at: 2026-06-05
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0001, DECISION-0007]
phase: P2
---

# DECISION-0010 — Licenciamiento propietario (ARR) + repo privado

## Contexto
El operador humano (titular **John Jairo Ballestas Payares**, contacto john.ballestas@gmail.com) añadió
`/LICENSE` (propietaria, *All Rights Reserved*) a la raíz, fuera del flujo de tareas. Faltaba
gobernarla y reconciliar la documentación, que describía el repo como *"reusable template"* — en
contradicción con ARR.

## Decisión
1. **Todo el contenido de ESTE repositorio es propietario, *All Rights Reserved*** según
   [`/LICENSE`](../../LICENSE): no se concede ningún derecho de uso, copia, modificación ni
   redistribución sin acuerdo escrito con el titular. Verlo en una plataforma no concede derechos.
2. **Visibilidad del repo: PRIVADO** (aplicado vía `gh repo edit --visibility private`).
3. **Reconciliación de docs:** `README.md` y `README_INSTANCIACION.md` dejan de venderse como
   "reusable/template" abierto; la instanciación descrita es para **uso autorizado del titular**, no
   una invitación a copiar.
4. **Privacidad:** ningún dato personal sensible (p.ej. NIE) figura en ficheros versionados; `/LICENSE`
   solo lleva **nombre + email de contacto** (verificado).
5. **Protocolo-metodología vs repo-artefacto:** los masters `*.template.*` siguen siendo *tooling*
   **neutral de dominio** (no cambian); pero el repositorio como artefacto es ARR. Cualquier modelo de
   licenciamiento externo futuro (p.ej. liberar el protocolo) sería **otra decisión**.

## Consecuencias
- **Positivas:** la licencia, la visibilidad y la documentación quedan **coherentes** (ARR + privado +
  sin "copia libre"); titularidad clara; sin fuga de datos personales.
- **Costo:** el repo deja de ser escaparate público; colaboradores requieren invitación.
- **Gobernanza de proceso:** `/LICENSE` se añadió sin claim (fuera de flujo); esta decisión lo
  formaliza retroactivamente. Refuerza DECISION-0007 (claim antes de tocar rutas compartidas).

## Alternativas consideradas
- **Público escaparate (visible-pero-no-usable):** descartado por el operador a favor de privado.
- **Mantener "reusable template":** descartado — contradice ARR e induce a error legal.
- **No formalizar (solo el archivo LICENSE):** insuficiente — dejaba la doc contradictoria y sin
  gobernanza trazable.
