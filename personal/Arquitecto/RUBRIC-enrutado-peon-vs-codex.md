# RUBRIC de enrutado peon-vs-Codex (topologia aplanada) -- v0.2

Origen: DIRECTIVA operador 18-jul (rubric-enrutado) sobre la topologia aplanada (d8b81ca).
Artefacto CALIBRABLE: se actualiza al cerrar cada tramo del grid con evidencia real. Version
al cambiar criterios, no al anadir datos. Referenciado desde DISENO-piloto-benchmark-peones-grid.
Demo del piloto NO citable; el rubric en si es operativa del carril.

## Regla: ruta a PEON solo si se cumplen LOS CINCO filtros; si falla uno -> Codex directo
1. **Especificable a completitud mecanica.** La spec fija la respuesta como aplicacion de
   patron. Inventar estructura / tradeoffs / intencion no dicha -> Codex.
2. **Gate objetivo y DURO.** Pass/fail mecanico (tests/asserts/type-check). Correccion
   subjetiva -> Codex. (Defensa contra el mal-pero-plausible que el bounce no caza.)
3. **Contexto local.** Cabe en la ventana del peon sin sostener medio repo. Cross-file /
   radio amplio -> Codex.
4. **Familia repetida.** N-esima instancia de un patron con spec reutilizable (B0-reuse).
   One-off novel -> Codex (spec no amortiza; riesgo de calibracion).
5. **Fallo no catastrofico.** PII / ledger / genesis / seguridad / codigo soberano -> Codex
   POR PRINCIPIO, aunque el peon pudiera. Ante duda de soberania: Codex. (Nota: los tests
   NEG PII del grid usan payloads sinteticos de fixture en area de probe: no son codigo
   soberano; el filtro aplica al codigo que TOCA produccion/ledger.)

## Sub-estado del enrutado a peon (calibracion T2)
- **peon-solo**: se espera salida integrable sin correccion (T1-like: patron puro).
- **bounce-apta**: se espera borrador util + QC-bounce (tope 2) o correccion menor del maker
  (T2-like: variacion/edge-cases). Sigue siendo "peon" en el rubric, pero se presupuesta la
  correccion en el coste esperado.

## Base de calibracion (evidencia del grid; actualizar por tramo)
| Tramo | Naturaleza | Resultado peon | Zona | Refina |
|---|---|---|---|---|
| T1 (lote 10 NEG PII, patron puro) | variacion minima | 3b 10/10 sin correccion; 6.7b semantico 10/10 (cosmetica); 7b 10/10 | PEON-SOLO | filtros 1+4 confirmados; con spec buena el peon mas barato rinde |
| T1-B1 (sin spec calibrada) | extraccion cruda | 0/10, 3 llamadas, maker reescribio | (anti-dato) | la spec calibrada ES la condicion; sin ella no hay enrutado a peon valido |
| T2 (parser refs, 18 asserts, variacion) | variacion media | NINGUNO 1a-verde; 1 correccion real c/u; 3b-reuse 104432 vs baseline 105539 | FRONTERA (bounce-apta) | filtro 1 refinado: a mas variacion/edges, peon degrada a borrador |
| Escala lote 50 | patron puro x volumen | 5 bounces DESLIZ (peon preferia el ejemplo de la spec a las filas de parametros; 1 feedback de 22tk corrigio los 5), 0 techo, 0 correcciones, 50/50 | PEON via BOUNCE | breakeven ~99 u/exec (marginal 956 vs 1180); leccion de spec: parametros ANTES del ejemplo |
| T3 (contrato existente) | juicio moderado | PENDIENTE | prediccion: Codex (falla filtro 1) -- se prueba igual para calibrar | - |
| T4 (logica dura) | ceiling | PENDIENTE | prediccion: Codex (falla filtro 1) | - |

## Tasa de acierto de enrutado (mi discernicion, medida)
Por celda: tier ELEGIDO ex-ante vs mejor tier EMPIRICO ex-post (peon-solo / bounce / directo).
| Celda | Elegido (ex-ante) | Mejor empirico | Acierto |
|---|---|---|---|
| T1 mitad-B (B0 7b) | peon | peon-solo | SI |
| T1-B1 | peon-extraccion (por directiva de medicion) | directo | NO (celda de refutacion: el dato ero el objetivo) |
| T1 reuse 3b/6.7b | peon | peon-solo | SI |
| T2 delegadas x3 | peon | bounce (borrador+correccion) | PARCIAL (acierto de tier, sub-estado no previsto ex-ante; el rubric v0.2 ya lo presupuesta) |
| Escala lote 50 delegado | peon bounce-apta | bounce (5 desliz, 0 correcciones) | PARCIAL: bounce-apta SI y mejor de lo previsto; "per-unit cae bajo directo" NO se cumplio a lote 50 (solo el MARGINAL cayo: 956 vs 1180; cruce a ~99u) |
| T3 / T4 / B2 | (registrar ex-ante ANTES del exec; T3/T4 ya predichos arriba) | - | - |

Predicciones ex-ante registradas (para medir sin HARKing retroactivo):
- Escala lote 50 delegado: bounce-apta con <=1 correccion por bloque; per-unit delegado CAE
  bajo el directo (la dilucion de ceremonia supera el coste de correccion).
- T3: el peon NO pasa el gate ni con bounce x2 (falla filtro 1); Codex directo gana.
- T4: idem T3, mas claro.

## Uso operativo
Antes de rutear cada celda/tarea delegable: evaluar 5 filtros -> registrar decision ex-ante en
este artefacto -> ejecutar -> anotar mejor tier empirico y acierto. El bounce (tope 2) es el
backstop de los errores de enrutado hacia arriba; el filtro 5 no tiene backstop y se aplica duro.
