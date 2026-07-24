# LENS_COVERAGE_GATE.md - Mecanismo de cobertura obligatoria de lentes (Sprint-1-ready, NO CONSTRUIR AUN)

> Version: 1.0-DISENO (DECISION-0092 seccion B.7). Dominio-neutral. ASCII puro.
> **ESTADO: DISENO/SPEC, no operado.** Este documento describe el mecanismo que activa el gate de
> cobertura de lentes (`REVIEW_CONTRACT.md`); su CONSTRUCCION (codigo que computa `lenses_required` y
> falla el gate por cobertura incompleta) es un cambio de comportamiento del proceso de revision y se
> DIFIERE a la ventana gobernada de cada instancia (para la instancia Nova: post-30-jul, respetando el
> sello DECISION-0091). Escribir esta SPEC ahora es preparacion legitima; construirla no.

## 1. Problema que resuelve

Sin este mecanismo, que lentes corren en una revision depende de que el AGENTE (maker, checker, juez)
decida aplicarlas -- bajo carga esa disciplina se cae, y las lentes sin disparador natural (ver
REVIEW_CONTRACT.md, R2/R4 tipicamente) quedan decorativas: se nombran pero no se ejercitan de forma
sistematica. El sintoma observado (instancia Nova): un hallazgo de acople estructural (senal R2) se
detecto por una pasada transversal AFORTUNADA, no porque el proceso lo exigiera.

## 2. Mecanismo: el requisito de cobertura vive en el ARTEFACTO, no en el agente

`lenses_required` es un campo de la TAREA/HANDOFF, computado deterministicamente a partir de senales
observables del cambio (diff, evento, tipo de superficie tocada). Cualquier agente que toque la tarea
(maker, checker adversarial, checker formal, juez) hereda el mismo requisito -- el artefacto viaja, la
obligacion viaja con el. Ningun agente decide individualmente "si mira una lente en particular"; la
tarea declara que lentes aplican y el gate lo exige.

Contrato (ver `REVIEW_CONTRACT.md` s.3.1): la tarea declara `lenses_required: [Rx, Ry]`; el revisor
emite `lenses_run: [...]` en su veredicto. **Gate de cobertura: `lenses_run` DEBE ser superconjunto de
`lenses_required`; si no lo es, el gate falla POR COBERTURA INCOMPLETA, no por hallazgo.** Es una
categoria de fallo distinta de un NO-GO por defecto: significa "no se demostro haber mirado lo que se
tenia que mirar", no "se miro y esta mal".

## 3. Computo de `lenses_required` (neutral: la SENAL; el GLOB que la detecta es de instancia)

| Senal observable en el diff/evento (NEUTRAL) | Lente que dispara |
|---|---|
| El cambio toca una superficie de riesgo declarada por la instancia (secretos, auth, guardas de procedencia de evidencia) | R1 |
| El cambio toca un componente/archivo/simbolo REFERENCIADO por >=2 unidades/verticales distintas (senal de acople estructural, detectable por grep/analisis estatico, no de dominio) | R2 |
| El cambio ANADE o MODIFICA comportamiento observable (nuevo endpoint, contrato, regla de negocio) | R3 |
| El cambio toca runtime en produccion (mutador nuevo, error-mapping, retry, rollback, observabilidad) | R4 |
| El evento es un handoff pre-revision (GO/REVIEW entre maker y checker) | R1+R3 como piso minimo |
| El evento es una fase de diseno post-SDD (arquitectura/plan antes de construir) | disparo de judgment-day (ver s.5), tier alto (H3/coste) |

Cada instancia declara SUS PROPIOS globs/reglas concretas que detectan estas senales (que directorio
es "superficie de riesgo", que patron de referencia cuenta como "componente compartido") en su propio
PROFILE (ver s.4); el vocabulario de la tabla de arriba es neutral y va al core.

## 4. Formato del campo en la tarea/handoff

```
lenses_required: [R1, R2]   # computado al abrir/actualizar la tarea, antes de rutear a revision
lenses_required_computed_at: <timestamp>
lenses_required_computed_by: <coordinador de dominio que lo estampo>
```

Se estampa en la tarea (o en el handoff que rutea a revision) por el COORDINADOR DE DOMINIO -- no un
orquestador unificado (DECISION-0092 seccion C.12): cada instancia/dominio resuelve sus propias senales
con su propio profile, per-dominio.

## 5. Integracion con judgment-day (dual-juez ciego)

El patron judgment-day (dos jueces ciegos en paralelo, taxonomia de acuerdo, re-juicio tras fix,
escalada terminal humana tras 2 iteraciones) se activa como el TIER MAS ALTO de revision (evento
post-diseno/SDD, o gate de mayor riesgo declarado por `lenses_required`), heredando:
- el mismo bloque de `lenses_required` que cualquier otro revisor (ambos jueces evaluan las mismas
  lentes, resolucion de skills per-dominio inyectada identica a ambos, DECISION-0092 seccion A.5-por-
  extension);
- el principio de disjuncion-del-maker (`REVIEW_CONTRACT.md` s.5): ningun juez puede compartir familia
  de modelo con el maker de lo revisado.

**Esto sigue siendo DISENO.** La OPERACION de judgment-day (lanzar 2 jueces reales en paralelo,
sintetizar por cubos de acuerdo, re-lanzar tras cada fix) es la parte que DECISION-0092 seccion B.8
difiere explicitamente a la ventana gobernada de cada instancia.

## 6. Que SI se puede hacer ahora (sin cruzar a "construir")

- Declarar `lenses_required` MANUALMENTE en una tarea nueva como ejercicio de diseno/documentacion (sin
  que ningun gate lo EXIJA todavia).
- Escribir el PROFILE de instancia (globs concretos) como documento, sin cablear el computo automatico.
- Revisar SPECs existentes y anotar, a mano, que `lenses_required` tendrian bajo este esquema (util
  como insumo para calibrar el computo automatico cuando se construya).

## 7. Que NO es prep (cruza a "construir", se difiere)

- Codigo/script que compute `lenses_required` automaticamente del diff.
- Modificar el validador de estado colaborativo (`validate_collaboration_state.py` o equivalente) para
  fallar por cobertura incompleta.
- Lanzar judgment-day como mecanismo real sobre cualquier unidad (baseline o gobernada).

## 8. Relacion con otros documentos

- `REVIEW_CONTRACT.md`: define el formato de `lenses_run` que este gate compara contra
  `lenses_required`.
- `CARVE_OUTS.md`: los carve-outs por lente aplican ANTES del gate de cobertura (un carve-out valido no
  cuenta como "no cubierto").
- Perfil de instancia Nova: ver `Area_comun/specs/nova/PROFILE-NOVA-lens-triggers.md`.
