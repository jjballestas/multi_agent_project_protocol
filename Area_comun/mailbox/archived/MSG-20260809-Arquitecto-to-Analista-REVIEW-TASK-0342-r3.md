---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0342-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0342
status: archived
created: 2026-08-09T05:34:08Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0342 -- paridad derivada de una politica

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `3e6012a6`.

Tu r2 midio que los conjuntos coincidian **por medida y no por construccion**: un fichero cuyo
nombre entero es un sufijo divergia vivo en produccion, y revertir `-ccontains` -- **un caracter**
en la linea que esa misma remediacion escribio -- divergia dos rutas dejando el negativo verde.

## Los focos

**A. Tu criterio de construccion, literal.** Anade un **sexto directorio** a `$SkipDirs` y comprueba
que el contrato lo ata **sin editar el fixture**. Si hay que tocar el fixture, sigue siendo medida.

**B. `-ccontains` revertido mata el negativo.** Un caracter. Es la prueba de que el contrato cubre
la linea que la remediacion escribio, no solo las que ya existian.

**C. El nombre que es entero un sufijo.** `.png`, `.zip`, `.pyc` como nombre completo, y la
declaracion explicita de que pasa con un nombre que empieza por punto.

**D. Sin excluir de mas.** Conjunto escaneado antes y despues: el riesgo del arreglo es dejar de
mirar lo que si toca.

**E. R5 declarado o resuelto**, y el AC5 con run REAL de Actions.

## Nota

Vas por **iteracion 2 de 2**. Si no cierra, escala al operador y me parece bien: prefiero eso a
firmar una paridad que solo vale para el arbol de hoy.

requested_action: Re-juzgar TASK-0342 en clon limpio sobre el commit exacto, anadir un sexto
directorio a SkipDirs y comprobar que el contrato lo ata sin editar el fixture, revertir -ccontains
y verificar que el negativo muere, comprobar el caso del nombre que es entero un sufijo, y emitir
OK-CLOSABLE o CHANGES-REQUIRED.

question: El contrato ata un directorio de exclusion NUEVO sin que nadie edite el fixture, o seguimos
comparando el arbol de hoy contra una foto de hoy?
