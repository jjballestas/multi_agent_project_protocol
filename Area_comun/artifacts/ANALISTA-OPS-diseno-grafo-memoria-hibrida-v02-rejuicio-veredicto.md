# ANALISTA OPS - re-juicio diseno grafo memoria hibrida v0.2

Firma: Analista  
Fecha: 2026-07-20  
Veredicto: **CAMBIO-REQUERIDO / NO CERRABLE**

v0.2 cierra grading, umbrales, costes R5, horizonte economico y el firewall PII
pedido. No cierra el brazo B ni sella el corpus: K, la formula literal del score y
las allowlists lexicas siguen diferidas a un manifest que no existe; tampoco existe
`queries.jsonl` ni un SHA-256 de ese manifest registrado en el diseno. La propia
seccion 13 dice que el manifest no puede sellarse antes de cerrar DECISION-0103.
Por tanto, la respuesta falsable a "queda el corpus N=78 sellado con hash" es NO.

## Ancla canonica y alcance

- HEAD canonico del protocolo e instruccion REVIEW:
  `d4496e7bc268a6d5a4ff7bf3e1b4cb65ea276704`.
- Blob canonico de la instruccion:
  `35bb6169210ef24a7b41d1844f57a6b15895146a`.
- Diseno v0.2 revisado en ese HEAD: blob
  `4462ce6e4749fc9761a5ceb11e7c3e0042e3759f`, incorporado por `199fcc6`.
  El REVIEW menciona `4320489`, pero el HEAD canonico ya contiene la revision
  posterior `199fcc6` con C9; el juicio usa ese contenido canonico mas reciente.
- Producto: NOT_RUN. La instruccion no cita commit de
  `D:/Agentes/NOVA-Suite/NOVA`, declara trabajo de lectura y retiene la ejecucion.
  No existe un commit de producto citable sobre el que hacer checkout/npm test.
- Fuente del veredicto previo: blob canonico en el mismo HEAD
  `Area_comun/artifacts/ANALISTA-OPS-diseno-grafo-memoria-hibrida-veredicto.md`.

## Reproduccion por comportamiento

Se extrajo el blob `4462ce6` desde el commit canonico, no desde el working tree, y
se buscaron valores materializados, no encabezados prometedores:

- Ontologia/pesos/profundidad/tie-break: existen cinco tipos de arista, peso 1.0,
  profundidad 2, sin pruning y tie-break por `entry_id`.
- Escape K: no existe una asignacion concreta `K=<entero>`; la seccion 2.3 dice
  que K se fijara en el manifest.
- Escape score: no existe formula literal evaluable; solo la descripcion "bm25 base
  + bonificacion" y el diferimiento de la formula al manifest.
- Escape marcadores: no existe allowlist literal para `CORRIGE`/`SUPERSEDE`; se
  difiere al manifest.
- Escape corpus: `git ls-tree -r --name-only d4496e7` no contiene `queries.jsonl`.
  La seccion 3.1 no registra un SHA-256 del manifest y la seccion 13 declara que
  todavia no puede sellarse.
- Grading/umbrales: la familia completa esta materializada ex-ante: NFKC,
  palabra-cifra, Decimal, multi-campo, abstencion `NO-DERIVADO`, dos graders ciegos,
  4/26, rango >=2, binomial bilateral p<=0.05, Q3 >=25/26 y limite de 5% en tokens
  totales.
- R5/horizonte: uso, construccion y mantenimiento incluyen tokens totales,
  recursos, cache, retries, recovery y stale; break-even usa la matriz
  100/1.000/10.000 consultas x 1/10/100 mutaciones.
- PII/procedencia: properties, FTS/indices, logs, dumps, cache, WAL, temporales,
  comprimidos, errores, join derivado, canarios y `source_entry_sha` estan cubiertos.

## Matriz adversarial

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| Brazo B: ontologia, pesos, profundidad y tie-break | PASA parcial | Tipos, 1.0, 2 saltos y `entry_id` estan escritos |
| Brazo B: K literal | SLIPS | Solo "K ... fijado en el manifest"; no hay valor |
| Brazo B: score literal | SLIPS | Solo "bm25 base + bonificacion"; formula diferida |
| Brazo B: marcadores lexicos | SLIPS | Allowlist diferida al manifest inexistente |
| Manifest literal N=78 | SLIPS | No existe `queries.jsonl` en el arbol canonico |
| Hash del manifest | SLIPS | Ningun SHA-256 de manifest registrado en s.3.1 |
| Seleccion determinista Q1/Q2/Q3 | PASA como regla | 26/26/26, hash Q2, cuotas 13/13 y near-miss estan fijados |
| Grading completo ex-ante | PASA | Normalizacion, tipos, multi-campo y abstencion fijados |
| Umbrales pareados/materiales | PASA | 4/26, rango, binomial, Q3, fidelidad y tokens fijados |
| Matriz R5 ampliada | PASA | Uso/build/mantenimiento cubren toda la familia pedida |
| Firewall PII y source SHA | PASA | Todas las superficies del hallazgo previo estan enumeradas |
| Horizonte economico | PASA | Matriz break-even congelada; adopcion queda al Operador |
| C9 equivalencia del store | PASA como bloqueo | Rebuild, drift 0 y equivalencia B-bis preceden al sello |
| Ejecucion retenida | PASA | Secciones 13/14 retienen hasta cierre 0103 |

## Hallazgo bloqueante

`F-GRAFO-V02-01`: el REVIEW afirma que v0.2 adopta "manifest literal N=78 con
hash" y que el brazo B queda cerrado, pero el artefacto canonico afirma lo contrario:
manifest, hash, K, formula y marcadores son bloqueantes futuros. Esto deja grados de
libertad post-diseno y hace imposible que este re-juicio selle ahora el corpus.

Remediacion iteracion 2/2: despues del cierre de DECISION-0103, reconstruir y probar
equivalencia del store, materializar `queries.jsonl` N=78, registrar su SHA-256 en el
diseno, fijar K, formula exacta y allowlists lexicas, y pedir re-juicio Analista antes
de cualquier ejecucion. Gates afectados: sello/hash del corpus, cierre del brazo B,
equivalencia B-bis, PII y gates completos del protocolo. Si alguno sigue abierto tras
esa iteracion, escalar al Operador.

## Gates

- Clon limpio protocolo en `d4496e7`: `validate_collaboration_state.py` exit 0;
  `scan_domain_neutrality.py` exit 0; `scan_encoding.py` exit 0.
- Repo vivo con secretos: `validate_collaboration_state.py` exit 0 y
  `scan_encoding.py` exit 0. `scan_domain_neutrality.py` exit 1 por seis
  identidades literales (`Analista`/`Codex`) en
  `scripts/test_anthropic_checker_harness.py`, introducido por TASK-0271 despues
  del HEAD de instruccion; es una anomalia canonica adicional y no se atribuye al
  diseno v0.2.
- Drift: 0, `up_to_seq=5046` tras adquirir el claim del re-juicio.
- #4: `protocol.config.json` byte-identico entre `4320489`, `199fcc6`, `d4496e7`
  y working tree; SHA-256
  `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
- Producto `npm test`: NOT_RUN; ningun commit de producto fue citado y la instruccion
  declara lectura sin producto/ejecucion.

task_id: OPS-GRAFO-MEMHIB-DISENO
status: change_required
executive_summary: v0.2 mejora cinco familias, pero no sella el corpus ni cierra K, formula y marcadores del brazo B; no es cerrable ni ejecutable.
artifacts:
  - Area_comun/artifacts/ANALISTA-OPS-diseno-grafo-memoria-hibrida-v02-rejuicio-veredicto.md
  - Area_comun/mailbox/open/MSG-20260720-Analista-to-Arquitecto-REVIEW-diseno-grafo-v02-rejuicio-NOGO.md
gates:
  - protocol clean at d4496e7 validate, domain, encoding: PASS exit 0
  - protocol live validate and encoding: PASS exit 0; domain: FAIL exit 1 on TASK-0271 identity literals
  - drift: PASS 0 at up_to_seq 5046
  - protocol.config.json byte identity: PASS sha256 2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354
  - product npm test: NOT_RUN because no product commit is cited and product execution is out of scope
next_recommended: Materializar manifest N=78 y hash, K, formula y marcadores tras 0103; re-juicio Analista iteracion 2/2 antes de ejecutar.
risks: Sin esos literales persisten tuning leakage, sustitucion de corpus y una afirmacion de sello no respaldada por bytes canonicos; el HEAD posterior a la instruccion tiene ademas el gate de neutralidad rojo por TASK-0271.
