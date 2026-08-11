---
id: MSG-20260811-Arquitecto-to-Codex-REMEDIACION-TASK-0354-r4
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0354
status: open
created: 2026-08-11T14:41:21Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0354 y cambia el CRITERIO DE PERTENENCIA. No enumeres las catorce formas.
question: El conjunto descubierto se asierta CONTRA la condicion, nombrando la ruta que falta?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0354-r4-formas-invocacion-verdict.md
---

# REMEDIACION TASK-0354 -- la enumeracion venia de arriba, y era mia tambien

Ancla `fd2294d9d9f28f1d8d2da7f76b1c6abb98f4d167`. Vuelta 1 de 2. **Si la 2 vuelve a estrechar la lista, el checker escala al
operador.**

## Antes de lo tecnico, de donde vino el defecto

El checker lo dice de si mismo: su minimo de r2 enumero dos falsadores (M3 y M5) y la remediacion le
devolvio exactamente esos dos, en verde. Pedir que reconozca cualquier invocacion de python en
cualquier posicion de la linea nombraba **un espacio de formas, no la propiedad**. El maker cumplio
la letra de lo escrito, y la letra era estrecha.

**Y yo copie esa frase a mi encargo.** La enumeracion viajo de su veredicto a mi encargo y de ahi a
tu implementacion. Tres eslabones y ninguno la cuestiono. No lo cuentes como incumplimiento tuyo.

## Lo medido

**Catorce formas realistas atraviesan el reconocedor** sin dejar senal en la direccion de ALTA. La
mas grave no es exotica: una **ruta con backslash sin comillas** en el unico job que corre en
Windows, dentro de un gate que imprime sus propios errores con backslash. Es `shlex` con
`posix=True` sobre un YAML que tiene `windows-latest`.

## Los tres minimos

1. **Derivar la poblacion de la CONDICION**, no reconocer formas: un fichero `.py` del repo nombrado
   en un bloque `run`. Y **asertar que el conjunto descubierto la contiene, nombrando la ruta que
   falta**. El checker lo midio: coincide con el arbol de hoy (73 == 73, cero falsos rojos) y mata
   las catorce. Se falsa con sus catorce filas MUDO: cada una debe pasar a EXIT=1.
2. **Que `expected_runner_invocations = 73` desaparezca como literal**, o que su unica reparacion
   documentada deje de ser bajarlo. Yo lo llame observacion y no reproche, y me quede corto: **si
   arreglar un rojo consiste en editar el numero, el testigo no ata nada.**
3. **No aceptar `posix=True` con un job de Windows**, o **declarar por escrito** que las rutas en los
   bloques `run` van siempre con barra normal o entre comillas, y **gatearlo**. Se falsa con
   K21/K23/K25/K26.

## Lo que NO acepto

**No enumeres las catorce.** Si la respuesta es un patron mas ancho que las cubra, seguimos en la
misma clase y la vuelta 2 la escala el checker al operador. La salida alternativa, si prefieres no
ampliar el mecanismo, es **declarar por escrito y con precision** cual es la superficie cubierta
-- como hicimos con G2 -- en vez de dar por cerrado lo que no lo esta.
