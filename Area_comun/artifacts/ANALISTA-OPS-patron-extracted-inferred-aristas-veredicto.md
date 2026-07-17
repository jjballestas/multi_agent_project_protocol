# ANALISTA - Veredicto adversarial sobre EXTRACTED-vs-INFERRED por arista

Firma: Analista  
Fecha: 2026-07-17  
Veredicto: REFUTA la reserva en DDL v1 y el descarte definitivo de confianza continua.  
Posicion final: DIFERIR-LIMPIO a F4, sin cambio al DDL v1 de F1.  
Recomendacion de cierre: CERRABLE como soporte a decision solo si la respuesta al Operador conserva esta disidencia y no presenta la posicion del Arquitecto como consenso.

## Ancla canonica y alcance

- Protocolo e instruccion REVIEW: `cae10ad95d194d263ad5eff88f5d16fc714ae28c` (`origin/main` y `HEAD`).
- Instruccion: `Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Analista-REVIEW-refutar-patron-extracted-inferred-aristas.md`.
- Insumos leidos desde ese commit: DIRECTIVA del Operador, EVAL del Arquitecto, `SPEC-MEMORIA-HIBRIDA.md` v0.2.0 y `DECISION-0096`.
- Alcance canonico: documentos solamente; ningun repo de producto ni `npm test` aplica por prohibicion expresa de la instruccion.

## Mejor argumento contra la recomendacion

La "reserva" no es papel inocuo. El default `provenance='extracted'` convierte toda omision de un productor futuro en una afirmacion epistemica fuerte y silenciosa. En F1 no existe productor `inferred`, consumidor de procedencia ni contrato de extraccion de cada `edge_type`; por tanto, las dos columnas no prueban ninguna garantia y agregan superficie al port/supersede M6 justamente cuando la SPEC exige reconciliar dos DDL divergentes. Como la DB es cache gitignored y el round-trip se define por rebuild total, F4 puede introducir el modelo que realmente necesite con `PRAGMA user_version` nuevo y rebuild, sin migrar datos canonicos. Diferir-limpio domina a diferir-con-reserva: menor complejidad ahora y ninguna perdida de historia.

Ademas, reservar solo `provenance` e `inference_source` congela prematuramente una forma incompleta. La PK actual es `(from_artifact_id,to_artifact_id,edge_type)`: una arista inferida y otra extraida con el mismo triple colisionan. El EVAL recomienda precedencia extracted, pero no la codifica en PK, DDL ni regla de upsert. Tampoco define evidencia de la inferencia, version/configuracion de la heuristica o semantica de un score. Es mejor disenar estas piezas juntas cuando exista el productor F4.

## Veredicto por vector

| Vector | Veredicto | Evidencia canonica y prueba falsable |
|---|---|---|
| Reserva de dos campos en DDL v1 | REFUTA - WARNING-real | SPEC s.3 declara DDL objetivo v1, `PRAGMA user_version=1` y columnas procedentes del REQ s.6; s.8/M6 obliga a port/supersede del memdb divergente. Las columnas no tienen productor/consumidor en F1. Falsable: implementar F1 sin ellas y verificar que todos los DoD s.13 y el round-trip s.6 siguen cubiertos; la SPEC no contiene AC que exija esos campos. |
| Diferir-limpio vs reserva | CONFIRMA diferir-limpio - WARNING-real | SPEC s.2.3 define la DB como cache gitignored y s.6 exige rebuild completo desde canon. No hay datos canonicos que migrar. Falsable: en F4, bump de `user_version`, rebuild A/B y `dump(A)==dump(B)`; si eso falla por ausencia de columnas en v1, la tesis queda refutada. |
| Caso para adoptar completo en F1 | REFUTA por falta de base - WARNING-theoretical | SPEC s.5.1 solo dice que el indexador extrae frontmatter allowlisted y upserta `artifact_edges`; s.7 allowlistea `relates_to`, `linked_decisions`, `supersedes` y `superseded_by`. Aunque s.3 enumera `mentions`, la SPEC no define de que campo se deriva ni autoriza inferencia textual en F1. Por tanto, `mentions` no demuestra que ya existan aristas inferidas; revela un contrato de mapeo edge_type-fuente incompleto que F1 debe precisar, sin adoptar aun el patron F4. |
| Claim "todas las aristas F1-F3 son extracted" | CONFIRMA solo como intencion, no como garantia - WARNING-real | Es compatible con s.7 (metadata allowlisted, summaries sin cuerpo/LLM en F1-F3) y con s.12 (heuristica textual en F4), pero no queda probado porque s.5.1 no especifica el mapeo de todos los edge_type. Falsable: un contrato F1 que derive `mentions` o cualquier edge por heuristica invalidaria el claim y obligaria a etiquetar desde F1 o eliminar esa inferencia. |
| Descartar confianza continua | REFUTA el descarte definitivo - SUGGESTION | La falta de calibracion impide llamarla probabilidad, pero no vuelve inutil un score determinista de ranking. SQLite REAL y un dumper canonico pueden serializarlo de forma byte-estable; el riesgo de floats no es imposibilidad. Tiers discretos pierden orden y atan umbrales prematuros. F4 debe decidir entre score bruto determinista, confianza calibrada o tiers, con semantica, algoritmo/version y golden de serializacion. No reservar columna ahora. |
| Riesgo al round-trip s.6 | REFUTA cobertura del EVAL - WARNING-real | `artifact_edges` entra en la particion DERIVADA y en el dump byte-identico. `source_commit` fija el blob, no necesariamente la version/config de la heuristica. F4 debe bindear algoritmo+version+config y ordenar/serializar score de modo canonico. Falsable: dos rebuilds del mismo commit con distinta version/config local no deben producir dumps distintos ni pasar sin detectar el cambio. |
| Riesgo por default `extracted` | REFUTA - WARNING-real | Un default silencioso etiqueta como hecho cualquier fila cuyo productor omita el campo. Falsable: insertar una arista desde un productor inferente sin columna; el DDL propuesto la acepta y la clasifica `extracted`. En F4 la procedencia debe ser explicita/fail-closed para productores inferentes. |
| DDL master unico | CONFIRMA encaje futuro, corrige atribucion - SUGGESTION | El patron puede vivir en una sola tabla y no exige segundo esquema. Pero `DECISION-0096` decide exportar la capa operacional; la obligacion concreta de un master neutral aparece en SPEC s.8 Q6/M6 y en el REQ citado, no en una clausula DDL de 0096. |

## Posicion final y residuales

Posicion: **DIFERIR-LIMPIO A F4**. F1 debe cerrar primero el contrato de mapeo `frontmatter key -> edge_type` y declarar que no produce inferencias. F4 debe disenar de una vez: procedencia explicita, identidad/precedencia ante colision del mismo triple, evidencia y algoritmo+version+config, semantica del score y serializacion canonica. No adoptar columnas v1, no descartar para siempre un score continuo y no alterar DECISION-0081.

Residual declarado: este veredicto no prueba implementacion porque la instruccion la excluye y la SPEC esta en estado `draft-reviewed-informal`. La recomendacion es soporte a decision, no evidencia citable ni autorizacion de build.

## Reproduccion y gates

- `git rev-parse HEAD` -> `cae10ad95d194d263ad5eff88f5d16fc714ae28c`, exit 0.
- `git rev-parse origin/main` -> mismo commit, exit 0.
- Insumos con `git show HEAD:<ruta>` -> exit 0.
- Producto / `npm test` -> NO APLICA por alcance canonico docs-only y prohibicion expresa.
- Gates finales del protocolo: se registran en el commit de entrega; todos deben salir exit 0, drift 0 y config #4 byte-identica antes del push.

task_id: none
status: CERRABLE-COMO-SOPORTE-A-DECISION
executive_summary: REFUTA diferir-con-reserva y descartar definitivamente confianza continua; recomienda diferir-limpio a F4.
artifacts: Area_comun/artifacts/ANALISTA-OPS-patron-extracted-inferred-aristas-veredicto.md; Area_comun/mailbox/open/MSG-20260717-Analista-to-Arquitecto-REVIEW-patron-extracted-inferred-aristas.md
gates: docs-only; protocolo validate con/sin secretos, drift, domain, encoding y config #4 deben quedar verdes antes del push.
next_recommended: Arquitecto debe responder al Operador preservando la disidencia y elegir diferir-limpio salvo nueva evidencia de un productor inferred en F1.
risks: mapeo edge_type-fuente incompleto; default extracted falsea procedencia; PK colisiona extracted/inferred del mismo triple; score F4 aun sin semantica.
