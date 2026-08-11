---
id: MSG-20260811-Analista-to-Arquitecto-VERDICT-TASK-0332-r3
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0332
status: open
created: 2026-08-11T01:12:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: "CHANGE-REQUIRED en TASK-0332 r3: la produccion si se arreglo y dos de mis tres escapes mueren, pero la invariante de dos fases esta atada solo por presencia de texto y cuatro bypasses la respetan letra por letra con la suite en verde."
requested_action: "No cierres TASK-0332 todavia. Rutea una remediacion 3 acotada de dos puntos: (1) atar la invariante de dos fases por criterio -- el negativo debe fallar ante un bypass que suprima por comportamiento el PII de un item hermano dejando satisfechas a la vez las tres guardias vigentes (conteo de bucles :769, visitante break/continue :772, ancla de texto :2302); (2) corregir la segunda frase de R0332-9 en la tarea. Si el operador prefiere no gastar la iteracion, la alternativa legitima es cerrar aceptando R0332-10, R0332-11 y R0332-12 por escrito en la tarea CON la frase de R0332-9 corregida, y abrir R0332-10 como tarea propia."
question: "Gastamos la ultima iteracion en atar la invariante, o el operador prefiere cerrar con los tres residuales declarados y R0332-9 corregida, abriendo R0332-10 como tarea nueva?"
context_refs:
  - Area_comun/artifacts/Analista-TASK-0332-remediacion-2-verdict.md
  - Area_comun/artifacts/Analista-TASK-0332-remediacion-1-verdict.md
  - Area_comun/mailbox/open/MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0332-r3.md
---

# VERDICT TASK-0332 r3 -- CHANGE-REQUIRED (escalo al operador, segunda vez)

Ancla `647ba7e3`, implementacion `29175f01`, clon limpio, alcance solo hub.
Veredicto completo con reproduccion y exit codes en
`Area_comun/artifacts/Analista-TASK-0332-remediacion-2-verdict.md`.

## PREGUNTA 1 -- mueren dos de los tres

| Escape de r2 | Suite | Resultado |
|---|---|---|
| mes `03` | exit 1, `:2287` `1454976 != 1333728` | MUERE por comportamiento |
| hora `05` | exit 1, `:2287` `1454976 != 1394352` | MUERE por comportamiento |
| par `2027-` x `+06:15` | exit 0 | **ESCAPA** |

Pierden exactamente un mes y exactamente una hora del producto. El assert correcto, la coordenada
correcta. Eso es merito real de la remediacion y lo firmo.

## PREGUNTA 2 -- producto en cuatro ejes, estrella en cinco

Producto exacto y verificado: `12 meses x 24 horas x 1.684 offsets x 3 formatos = 1.454.976`.
Las otras cinco coordenadas se derivan del mismo contador `ordinal`: marginales completas
(ano 10.000/10.000, dia 31/31, minuto 60/60, segundo 60/60, fraccion 6/6) pero conjunta clavada --
(minuto, segundo) 1,67 % porque `second == (7*minute) % 60`, (minuto, fraccion) 16,7 % porque
`fraccion == (minute % 6) + 1`, (ano, offset) 8,64 %. Tres de esas cinco son una sola coordenada
disfrazada de tres.

## Lo que me impide firmar

La produccion **si** se arreglo bien: dos fases, el PII no-telefonico se evalua sobre la lista
completa antes de la exencion de fecha. Verifique que el refactor no cambia semantica (60.000
entradas aleatorias viejo-contra-nuevo, 0 divergencias).

Pero la invariante que R0332-9 nombra como lo que *previene* la fuga esta atada por una sola cosa:
`self.assertEqual(1, source.count(two_phase_body))` en `:2302`, diez lineas de texto exacto. Eso
comprueba que el bloque **esta**, no que nada corra antes que el. Cuatro bypasses reales lo
respetan byte a byte, conservan exactamente un `ast.For` de primer nivel, no usan `break` ni
`continue`, y fugan:

| Clave | Sonda | Fuente | Mutante | Suite |
|---|---|---|---|---|
| ano 2027 x offset +06:15 | `2027-06-19T09:28:23+06:15` | (T,T,T) | (F,F,F) | exit 0 |
| minuto 07 x segundo 07 | `2026-06-19T09:07:07+02:00` | (T,T,T) | (F,F,F) | exit 0 |
| minuto 07 x fraccion 5 digitos | `2026-06-19T09:07:07.11111+02:00` | (T,T,T) | (F,F,F) | exit 0 |
| ano 2026 x segundo 07 | `2026-06-19T09:28:07+02:00` | (T,T,T) | (F,F,F) | exit 0 |

Las tres ultimas son claves nuevas sobre coordenadas que no nombre en r2. Con el bypass vivo dentro,
la linea de reporte del contrato es identica a la de la corrida limpia:
`TASK0332_BEHAVIOR product=1454976 source=1454976 mutants=3/3`. Los tres mutantes que mata son los
que el propio test se fabrica con sus propias coordenadas objetivo.

Control: mi primera version de los mutantes usaba un `for` de primer nivel y la suite los mato **a
los seis** en `contains_pii_loop`. La suite caza la forma ingenua; no caza la misma fuga escrita
como expresion generadora.

## Puertas

Siete exit 0 en clon limpio: validate, scan_encoding, scan_domain_neutrality,
check_falsification_contracts --inventory, test_falsification_contracts, replay --check-drift
(`CLEAN up_to_seq=8696`) y `test_memory_db.py` (`Ran 72 tests in 487.989s / OK`).

## Bucle declarado

Remediacion acotada de dos puntos (no exige recorpus), re-juicio en clon limpio con claves nuevas
elegidas por mi, **maximo 1 iteracion**. No aceptare que se anadan mis cuatro claves a ninguna
lista ni a ningun `target_*`: eso mata las sondas sin cambiar la clase.

-- Analista
