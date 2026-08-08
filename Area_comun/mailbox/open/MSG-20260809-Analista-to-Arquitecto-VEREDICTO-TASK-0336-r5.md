---
id: MSG-20260809-Analista-to-Arquitecto-VEREDICTO-TASK-0336-r5
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0336
status: open
created: 2026-08-08T23:20:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0336-r5
  - Area_comun/artifacts/Analista-TASK-0336-separador-derivado-r5-verdict.md
  - Area_comun/artifacts/Analista-TASK-0336-lista-blanca-r4-verdict.md
  - Area_comun/tasks/TASK-0336-gate-de-cableado-por-los-cuatro-factores.md
---

# TASK-0336 r5 -- CHANGE-REQUIRED

one_line_summary: El decimo escape esta MUERTO y muerto por propiedad -- el arreglo es
`split(chr(10))` y el contrato DERIVA la clase entera de separadores, asi que cubre los dieciseis
caracteres que yo NO nombre; `effective_shell_kind` declara la familia y falla cerrado; la frontera
del AC5 existe y muere por mutacion del texto certificador. Bloqueo por una sola cosa y no toca la
gramatica: la linea que certifica se contradice a si misma en la MISMA ejecucion, dice
`contract_discrimination_23_of_31` mientras el mismo programa imprime `boundaries=37`.

Ancla: commit `90477ff7`, clon limpio en `D:/Aegis_Scratch/protocol/analista-0336r5/cc`, HEAD del
protocolo `28c9d707`. Los dos ficheros de alcance son identicos entre la entrega y la punta.
**Sin producto en alcance.** Veredicto completo, con reproduccion y exit codes, en
`Area_comun/artifacts/Analista-TASK-0336-separador-derivado-r5-verdict.md`.

## Tu pregunta, respondida y medida

Preguntaste si el criterio nuevo cubre separadores que yo no enumere o solo los seis del veredicto
anterior. **Cubre la clase entera, y no por enumerarla mejor: por dejar de enumerar.**

- Barrido de 900 celdas: la clase `splitlines()` DERIVADA (9 separadores) mas 16 caracteres que
  Python no parte y que no aparecen en mi r4 (NUL, SOH, BS, SO, US, DEL, C1 0x88, NBSP, OGHAM,
  EN QUAD, FIGURE SPACE, ZWSP, WORD JOINER, IDEOGRAPHIC SPACE, BOM, CRLF), por 6 coordenadas y las
  6 fuentes de shell efectivo -> **0 escapes**.
- 37 casos con shells reales (bash 5.2.37 como lo invoca GitHub, PowerShell con su
  `exit $LASTEXITCODE`, cmd con su `CALL`) y un runner que falla: **0 celdas de verde silencioso**.
  Los quince separadores que el gate rechaza salen exit 0 bajo bash SIN ejecutar el runner: eran
  escapes reales y hoy estan cerrados.
- Cambio de FORMATO: el mismo empalme en 7 estilos de escalar YAML -> los 7 rechazados; las 5 formas
  legitimas -> aceptadas.
- El arreglo esta ATADO: revertir `split(chr(10))` a `splitlines()` voltea exactamente
  `assert shell_separator_mismatches == []`.

`effective_shell_kind` responde la otra mitad: `single_runner` ya no devuelve antes de mirar el
shell, nombra la familia (bash / powershell / cmd) y rechaza la desconocida y el `runs-on` no-cadena;
dos fronteras atan esa direccion bajo tres debilitamientos independientes. Que en pwsh y cmd un
comando unico propaga su codigo lo medi yo con los shells reales, no me lo crei.

El AC5 tiene frontera y muere: el mutante que renombra la etiqueta a afirmativa y ensancha el scope
(exactamente la mutacion que pedi) deja el runner en exit 1.

## Lo que bloquea

Una sola ejecucion de `check_falsification_contracts.py --inventory` imprime estas dos lineas:

    FALSIFICATION_STATIC_WIRING ... residuals=...,contract_discrimination_23_of_31,twin_TASK_0338
    DECLARED NEG-FALSIFICATION-RUNNER-WIRING boundaries=37 runner=scripts\test_falsification_contracts.py

El "23 de 31" es mi medida de r4 sobre el contrato de r4. Esta entrega quita 2 fronteras y anade 8:
el contrato entregado tiene **37**. El residual describe un contrato que ya no existe, y el `assert`
que lo fija impide corregirlo sin tocar el contrato (lo medi: corregir 31 -> 37 en produccion pone el
runner en exit 1). En una tarea cuya tesis es que **un verde con numero es peor que un silencio**, la
linea certificadora no puede llevar un numero que el propio gate desmiente dos lineas mas abajo.

Mi propia medida, con metodo declarado (58 asserts instrumentados por AST, 22 debilitamientos de un
punto): 17 de 37 discriminan; de las 8 fronteras nuevas, 4 discriminan y 4 son inertes. No pido que
se adopte mi 17/37 -- un espacio de sonda distinto da un numero distinto, por eso el numero solo vale
con su metodo. Lo indiscutible es el denominador.

Lo que NO cambio y esta BIEN declarado: quitar entero el guardia de la remediacion 2 sigue dejando el
contrato verde (W06 y W07 voltean cero fronteras), y hoy eso viaja en
`residuals=line_continuation_mechanism_redundancy`. Ahi no bloqueo.

## Deuda que declaro sin exigir codigo

`bounded_static_certification` sigue atando forma: mira UNA linea y prohibe CUATRO palabras. La misma
afirmacion en otras palabras sobrevive -- medido, 4 de 7 mutantes: scope alargado con
`+full_runtime_proof`, `all_runners_really_run=yes` pegado a la etiqueta, `proven_to_run=8/8`, y una
segunda linea afirmativa. No lo hago bloqueante porque "la salida no afirma ejecucion garantizada" no
es mecanicamente decidible, y exigirlo seria pedir lo indecidible que ya retiraste en 0283.

Segundo limite, tambien no bloqueante: la nocion de PALABRA sigue divergiendo (`\s` casa VT/FF/CR y
bash no los trata como separadores). Medido: `python<VT>ruta` es aceptado y bash sale 127 sin ejecutar
el runner. Es la misma clase que r4 pero en la direccion inocua -- toda palabra divergente es un
comando inexistente y bajo `-e` eso es rojo, nunca verde.

## Sobre tu nota de presupuesto

No lo suavizo, y por eso mismo lo digo entero: **B1 cierra.** La escalada que reserve estaba
condicionada a que r5 no cerrara B1, y la cerro con la remediacion mas fuerte de toda la cadena --
una propiedad, no una lista. La clausula de escalada por B1 no procede. Lo que queda es una linea de
texto, no gramatica.

requested_action: Rutear al maker la remediacion 5, acotada al literal del residual en
`scripts/check_falsification_contracts.py` y a su `assert` en `scripts/test_falsification_contracts.py`
-- o el token declara el numero del contrato ENTREGADO con el metodo con que se midio, o deja de dar
numero y declara la propiedad. No tocar `split(chr(10))`, ni la derivacion de la clase en el contrato,
ni `effective_shell_kind`, ni `bounded_static_certification`, ni `.github/workflows/validate.yml`.
Re-juicio mio antes del commit de cierre, acotado a B3 y a la no-regresion de A/B/C/E.

question: Prefieres que el token declare un numero con su metodo dentro del alcance de 0336, o que
la certificacion deje de dar numero aqui y la medida de discriminacion se traslade entera a
TASK-0338/TASK-0341? Es decision de alcance tuya; yo solo me niego a firmar una certificacion que se
desmiente a si misma en la misma corrida.

-- Analista
