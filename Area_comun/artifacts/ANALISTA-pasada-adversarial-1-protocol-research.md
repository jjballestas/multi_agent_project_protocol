# ANALISTA - Pasada adversarial #1 / protocol_research (estructura + scaffolding)

> Voz analista independiente (maker != checker). Lente: honestidad / metodologia (NO ingenieria).
> Insumo: drafts en `personal/Claude/drafts-research/` (DECISION-0035, satellite README, GATES,
> ACCEPTANCE, dataset README+schema, 3 stubs). Orden: `personal/operador/07_...md`.
> Fecha: 2026-06-14. HEAD revisado: b600309 (v1.7.0). Proporcional al peso del insumo (estructura+stubs).
> No consolido, no decido, no muto estado: entrego esta voz antes de ratificar.

## Veredicto de cabecera

**GO con cambios menores ANTES de ratificar.** El scaffolding es honesto en lo sustantivo y los gates
estan bien nombrados; ningun stub puede correr ni capturar datos sin su gate (verificado). Pero hay
**tres correcciones de honestidad/precision** que deben entrar antes de la ratificacion, porque el texto
afirma garantias que el diseno no provee:

- P1 Honestidad de #1: **PASA** (ninguna frase se excede).
- P2 Acoplamiento unidireccional: **CAMBIO REQUERIDO** (el diseno DECLARA + verifica por inspeccion, NO
  GARANTIZA tecnicamente; el lenguaje absoluto debe matizarse y GATE-INST debe exigir enforcement real).
- P3 Gates como hard-stops: **PASA en sustancia** + **CAMBIO REQUERIDO** (la frase "raises
  NotImplementedError if forced to run" es inexacta: ejecutar el fichero sale 0 en silencio).
- P4 Neutralidad: **PASA en sustancia** + **CAMBIO REQUERIDO** (la afirmacion "neutrality scan clean =>
  no research terms in the Core" es un non-sequitur y literalmente falsa como esta redactada).

Ninguno bloquea la EXISTENCIA del scaffolding; son correcciones para no sobre-afirmar antes de ratificar.

---

## 1) Honestidad de #1: comparabilidad como LIMITE, sin 'citable'/empirico

**Veredicto: PASA. Ninguna frase se excede.** Revise cada aseveracion sobre #1 en DECISION-0035,
satellite README, dataset README y schema. Todas las afirmaciones llevan su calificador:

- DECISION-0035 l.56,70: "NO se afirma comparabilidad 1:1 ... solo se reporta como limite"; "'citable'
  depende de GATE-DATASET"; "Sin numeros de severidad/frecuencia hasta tener datos validados". OK.
- dataset README l.13-18: "Comparability ... REPORTED as a limit, never asserted"; "Not 'citable'";
  "No numbers without validated data". OK.
- schema l.20: el campo `notes` "MUST note this is MAST-applied, not MAST-Data"; ejemplo etiquetado
  "illustrative, NOT a real record". OK. Conserva la distincion honesta `incident_kind`
  (incident/partial/preventive) que fija la frontera de FAILURE_MODES (coherente con DECISION-0034 y con
  mi observacion previa del overreach "12 incidentes reales").

No encontre ninguna frase que ASUMA comparabilidad, ni que llame al corpus "citable", "empirico" o
"validado". Confirmo: **ninguna se excede.**

**CAMBIO REQUERIDO:** ninguno.

**RIESGO DECLARADO:** la honestidad vive en PROSA + en el "MUST note" del schema, no en un gate duro.
Cuando se pueble el dataset (post GATE-DATASET) nada IMPIDE mecanicamente afirmar comparabilidad o meter
numeros no medidos. Mitigacion proporcional: que el checklist de GATE-DATASET incluya una asercion
explicita y verificable ("cero claim de comparabilidad 1:1; cero 'citable'; cero numeros sin corpus
validado") como condicion de franqueo. (Recomendacion, no bloqueante a nivel estructura.)

---

## 2) Acoplamiento unidireccional: el satelite NO puede escribir al Core

**Veredicto: CAMBIO REQUERIDO.** El diseno **DECLARA** y **verifica por inspeccion estatica** la
unidireccionalidad, pero **NO la GARANTIZA tecnicamente**. A nivel "estructura" el invariante se cumple
trivialmente (nada se ejecuta) -> PASA para el alcance actual; el problema es que DECISION-0035, README y
GATES lo presentan como garantia permanente ("innegociable", "the one hard invariant", "NEVER").

**Ruta falsable por la que el satelite PODRIA mutar el Core:** escritura directa de filesystem. Por el
layout hermano, el proceso del satelite tiene permiso de escritura del SO sobre
`../multi_agent_project_protocol`; nada tecnico impide `open("../multi_agent_project_protocol/...", "w")`.
Los stubs incluso reciben `core_repo_path` como parametro. Las unicas barreras existentes son: (a) repo
git separado (impide COMMIT al Core, no la escritura del working tree), (b) convencion read-only en los
docstrings, (c) extension `.py.stub` no ejecutable, (d) el grep de ACCEPTANCE
(`open(.*w|write|submit_intent`). El grep es trivialmente evadible (p.ej. `Path.write_text`, `os.replace`,
`shutil.copy`) y no es un sandbox.

El Core no protege esas rutas hoy: el escritor unico `enforce`/B.3 (DECISION-0022/0028) esta **OFF** en
esta instancia, asi que `Area_comun/state/*.json` no esta blindado a nivel runtime contra una escritura
externa.

**CAMBIO REQUERIDO (falsable):**
- (a) Matizar el lenguaje: cambiar "innegociable / hard invariant / NEVER" por "unidireccionalidad
  sostenida por repo-separado + convencion read-only + inspeccion estatica; **no hay sandbox** en la fase
  de estructura". Falsable: hoy una sola linea de escritura al Core desde codigo del satelite tendria
  exito y pasaria todos los gates declarados salvo, quiza, el grep.
- (b) GATE-INST (el gate que habilita lecturas/ejecucion vivas) debe **exigir un enforcement read-only
  real** antes de que CUALQUIER codigo del satelite corra contra el Core vivo: p.ej. Core montado/clonado
  read-only, o el satelite corriendo bajo una identidad sin permiso de escritura al Core. Anadir esto como
  condicion de franqueo en GATES.md (no solo "confirm the read path is read-only").

**RIESGO DECLARADO:** mientras todo sea stub OFF el riesgo real es nulo; el riesgo es de HONESTIDAD
(afirmar una garantia tecnica inexistente) y se materializa el dia que se franquee GATE-INST sin el
enforcement de (b).

---

## 3) Gates como hard-stops: stub OFF, no ejecutable, cita su gate

**Veredicto: PASA en sustancia + CAMBIO REQUERIDO en redaccion.**

Sustancia (verificado fichero por fichero):
- `exporters/prov`: `ENABLED=False`, `GATE="GATE-INST"`, `.py.stub`, README cita GATE-INST. OK.
- `feeds/cost_attribution`: `ENABLED=False`, `GATE="GATE-INST"`, `.py.stub`, README cita GATE-INST;
  ademas declara que NO toca `metrics.cost_attribution_enabled`. OK.
- `harness/ablation_tfm`: `ENABLED=False`, `GATE="PRE-REG"`, `.py.stub`, README cita PRE-REG. OK.
- `datasets/mast_over_history`: sin codigo ejecutable, sin `data/`, gobernado por GATE-DATASET. OK.

**No pude nombrar ningun stub que pudiera correr o capturar datos sin franquear su gate -> confirmo que
ninguno.** Razon: las funciones nunca se auto-invocan, no hay `__main__`, y la extension `.py.stub` no es
importable por nombre de modulo. Verificado empiricamente: `python interface.py.stub` -> **exit 0, sin
salida** (el cuerpo de la funcion no se ejecuta, no captura nada).

**CAMBIO REQUERIDO (falsable):** corregir una frase **inexacta** repetida en los 3 README y en ACCEPTANCE:
"if forced to run it raises NotImplementedError". **Es falso:** ejecutar el fichero (`python
interface.py.stub`) sale 0 en silencio; el `NotImplementedError` solo se dispara si se **invoca la
funcion**, no al ejecutar/importar el modulo. Redaccion correcta: "el fichero es inerte al ejecutarse (las
funciones nunca se llaman, no hay `__main__`); `NotImplementedError` solo se lanza si se invoca la
funcion". Falsable: corre `python <cualquier>.py.stub` -> exit 0.

**RIESGO DECLARADO:** ninguno sustantivo (el diseno es fail-closed para captura de datos, de hecho mas
fuerte de lo que el texto afirma). Endurecimiento OPCIONAL (no requerido): un guard a nivel de modulo que
falle-cerrado al importar; pero la propiedad protectora ya se cumple sin el.

---

## 4) Neutralidad: leer datos del Core NO arrastra dominio al Core

**Veredicto: PASA en sustancia + CAMBIO REQUERIDO en una afirmacion imprecisa.**

Sustancia: la frontera de neutralidad del Core (CLAUDE.md regla 1; `denylist` =
`trading/spot/binance/backtest/estrategia de trading`) prohibe terminos de NEGOCIO/TRADING. El satelite es
un repo SEPARADO; el flujo de datos es satelite <- Core (read-only); los ficheros genericos/template del
Core no ganan nada; leer datos del Core no puede empujar dominio HACIA el Core. **No encontre punto de
fuga -> confirmo ninguno.**

**CAMBIO REQUERIDO (falsable):** la frase de ACCEPTANCE "Neutrality scan stays clean: NO research/domain
terms added to the Core" es a la vez un non-sequitur y **literalmente falsa** como esta redactada:
- `Area_comun/decisions/**` esta en `exempt_globs` (verificado en `protocol.config.json`): DECISION-0035
  NO pasa por el scan; puede contener "MAST/PROV/ablation/TFM/research" y el scan sigue verde pase lo que
  pase. `grep -E 'MAST|PROV|ablation|TFM|research' DECISION-0035` -> multiples hits.
- El `denylist` no contiene NINGUN termino de research; el scan **nunca fue capaz** de detectar fuga de
  agenda de research. "Scan clean" NO es evidencia de "no research terms in the Core".
Redaccion correcta: "Ningun termino de negocio/trading entra en los ficheros genericos/template
escaneados; los terminos de research aparecen solo en el REGISTRO de decision (exento del scan) y en el
CHANGELOG, no en ficheros genericos de protocolo/template. La independencia del Core respecto de la agenda
de research se sostiene en el diseno repo-separado + cero dependencia de codigo, **no** en el scan de
neutralidad (que solo mira terminos de trading)."

**RIESGO DECLARADO:** el scaffolding vive HOY en `personal/Claude/drafts-research/` DENTRO del working
tree del Core (ruta exenta + no rastreada). Nada tecnico impide que un `git add` accidental committee el
satelite dentro del Core, rompiendo la propiedad "repo separado / no committeado en el Core". Mitigacion
proporcional: que el change-set de ratificacion lo copie FUERA y anada la ruta del satelite al
`.gitignore` del Core (o verifique explicitamente que nunca se estaciona).

---

## Cierre (maker != checker)

Produje esta voz por mi cuenta, sin leer otras voces. No consolido, no ratifico, no muto estado
autoritativo. La promocion (DECISION accepted + CHANGELOG + bump 1.8.0 via submit_intent, y la creacion
del repo separado) corresponde al arquitecto/escritor unico tras la ratificacion del operador. Mi
recomendacion: **incorporar los 3 cambios de redaccion (P2 lenguaje + GATE-INST, P3 frase del stub, P4
afirmacion de neutralidad) ANTES de ratificar**; con eso, GO.
