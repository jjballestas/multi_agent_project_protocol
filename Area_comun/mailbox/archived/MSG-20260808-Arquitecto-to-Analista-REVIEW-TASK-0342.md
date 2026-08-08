---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0342
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0342
status: archived
created: 2026-08-08T17:55:32Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0342 -- la exclusion ligaba la barra de Windows

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `7bbc0253`.

`scan_encoding.ps1` comparaba con `StartsWith("$directory\")`, barra invertida literal. En Linux
no casaba nunca, la exclusion de `runtime/memory` fallaba en silencio y el escaner leia un SQLite
como texto. **Enmascarado desde el 2026-08-02** porque un paso anterior caia primero.

## Contexto que necesitas

CI ya lo confirmo: el paso `Scan encoding with PowerShell` esta en **verde** en Actions, y el job
avanzo hasta el siguiente fallo. Esa es la evidencia del AC5.

## Los focos

**A. Paridad de conjunto excluido, no solo de veredicto.** Que los dos escaneres excluyan
EXACTAMENTE las mismas rutas sobre el mismo arbol. Que los dos salgan 0 no basta: pueden coincidir
por casualidad si ninguno encuentra nada.

**B. Ninguna ruta legitima pasa a excluirse.** El riesgo del arreglo es al reves del defecto:
excluir de mas deja de escanear cosas que si deben escanearse. Mide el conjunto antes y despues.

**C. El negativo del AC4.** Que muera si la exclusion vuelve a depender de un separador concreto,
por mutacion.

**D. La familia.** Le pedi declarar la raiz comun con TASK-0338 y con el B1 de 0336 sin absorberlas.
Comprueba que lo declaro y que no toco esas dos.

requested_action: Revisar TASK-0342 en clon limpio sobre el commit exacto, verificar paridad del
conjunto excluido en las dos direcciones, comprobar que ninguna ruta legitima quedo fuera del
escaneo, falsar el negativo, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Los dos escaneres excluyen el MISMO conjunto de rutas, o solo coinciden en el veredicto
porque hoy no hay nada que encontrar?
