# SPIKE PEONES - Contratos de la tanda 1 (LISTOS; se disparan cuando TASK-0238 = done)

- fecha: 2026-07-02 (preparados por el Asesor por adelantado, directiva de proactividad)
- gate: PLAN-SPIKE-PEONES-SANDBOX.md s.0 (TASK-0238 done con GO Analista -- ya
  review_approved, falta done-flip). Al caer el flip, esto se ejecuta tal cual.
- cada tarea lleva: bloque INTAKE completo (disciplina de F1-A) + contrato 0078 +
  decision de ruteo segun rubrica v1 (ensayo manual del router, PRE-DECISION).
- comun a TODAS: rutas permitidas SOLO dentro de D:/Agentes/Zeus/piloto-peones/;
  PROHIBIDO: hub, Zeus-protocol, ledger, submit_intent, commits fuera del sandbox,
  secretos, PII, decisiones, reglas de negocio. Si falta contexto: BLOCKED + una
  pregunta concreta. Provenance por tarea: peon=<modelo>, prompt_id, ts, rutas,
  resultado de gates. Registrar CADA fila en registro/medicion.csv (plan s.5).

---

## P-01 (brazo B) - Tests unitarios de modulo utilitario

INTAKE: type=infra | goal="Suite pytest para tareas/p01/calc.py (4 funciones dadas)"
| acceptance=["pytest -q verde", ">=2 tests por funcion (>=8 total)", "cubre caso
feliz + 1 borde por funcion"] | verification_cmd=["pytest entregas/p01/ -q",
"python -c \"import ast,sys; t=open('entregas/p01/test_calc.py').read();
print(t.count('def test_'))\""] | scope_routes=[tareas/p01/, entregas/p01/] |
out_of_scope=["modificar calc.py", "otras carpetas"] | risk=low | estimate=S
CONTRATO: entrada=tareas/p01/calc.py (el operador la siembra: 4 funciones puras de
aritmetica de presupuesto SIN datos reales). salida=entregas/p01/test_calc.py.
RUTEO (rubrica): gate objetivo fuerte + mecanica + low + S -> PEON. Anotar en CSV.

## P-02 (brazo B) - Transformacion mecanica CSV -> JSON lines

INTAKE: type=infra | goal="Convertir tareas/p02/movimientos.csv (sintetico) a
entregas/p02/movimientos.jsonl con schema {fecha,concepto,monto_centavos:int}"
| acceptance=["mismo numero de lineas que filas del CSV", "montos como enteros en
centavos", "validador verde"] | verification_cmd=["python tareas/p02/validar.py
entregas/p02/movimientos.jsonl"] | scope_routes=[tareas/p02/, entregas/p02/] |
out_of_scope=["inventar campos", "redondeos creativos"] | risk=low | estimate=S
CONTRATO: entrada=CSV sintetico (20 filas inventadas por el operador, cero datos
reales) + validar.py dado. salida=jsonl + script conversor.
RUTEO (rubrica): golden/validador dado -> PEON.

## P-03 (brazo B) - Fixtures de casos limite (redondeo monetario)

INTAKE: type=infra | goal="Generar entregas/p03/fixtures.json con >=12 casos limite
de redondeo a centavos (negativos, .005, cero, grandes)" | acceptance=[">=12 casos",
"cada caso con input/expected", "JSON parseable"] | verification_cmd=["python -c
\"import json; d=json.load(open('entregas/p03/fixtures.json'));
assert len(d)>=12 and all('input' in c and 'expected' in c for c in d); print('OK')\""]
| scope_routes=[entregas/p03/] | out_of_scope=["implementar el redondeo"] |
risk=low | estimate=S
CONTRATO: entrada=especificacion de la regla de redondeo (half-up a centavos) en
tareas/p03/regla.md. salida=fixtures.json.
RUTEO (rubrica): verificable por comando -> PEON.

## P-04 (brazo B) - Borrador runbook instalacion Ollama Windows

INTAKE: type=doc | goal="Runbook markdown de instalacion Ollama + modelo en Windows
para un empleado nuevo" | acceptance=["secciones: requisitos/instalacion/descarga
modelo/verificacion/problemas comunes", "pasos numerados", "comandos copiables"] |
verification_cmd=["grep -c '^## ' entregas/p04/runbook-ollama.md (>=5)"] |
scope_routes=[entregas/p04/] | out_of_scope=["politica de la empresa", "URLs
inventadas mas alla de ollama.com"] | risk=low | estimate=S
CONTRATO: entrada=ninguna (conocimiento general). salida=runbook-ollama.md.
RUTEO (rubrica): doc con checklist verificable -> PEON (gate mas debil que P-01/03:
buen caso para observar calidad).

## P-05 (brazo B) - Tabla i18n de strings

INTAKE: type=infra | goal="Extraer los strings user-facing de tareas/p05/pantalla.txt
(sintetico) a entregas/p05/i18n-es.json clave-valor" | acceptance=["1 clave por
string", "sin duplicados", "claves snake_case"] | verification_cmd=["python -c
\"import json; d=json.load(open('entregas/p05/i18n-es.json'));
assert len(d)==len(set(d.values()))>=10; print('OK')\""] |
scope_routes=[tareas/p05/, entregas/p05/] | out_of_scope=["traducir a otros
idiomas"] | risk=low | estimate=S
CONTRATO: entrada=pantalla.txt sintetica (>=10 strings, sembrada por operador).
salida=i18n-es.json.
RUTEO (rubrica): mecanica + conteo verificable -> PEON.

---

## Brazo A (control): P-01, P-02 y P-04 ejecutadas por el firmante SOLO

Mismas entradas (copias en tareas/a01..a04), sin peon, cronometradas, misma fila
CSV (brazo=A). Hacerlas ANTES o DESPUES de la tanda B alternando (A,B,A,B...) si
se puede, todo el mismo dia si es posible (menos deriva).

## Cierre de la tanda

1. CSV completo (8 filas) + nota de 10 lineas (donde ahorro, donde reviento,
   overrides de rubrica si los hubo).
2. Se anota el resultado en PLAN-SPIKE-PEONES-SANDBOX.md s.7 y se declara como
   piloto de calibracion en el pre-registro (F3.4).
