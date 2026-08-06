---
id: MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0321
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0321
status: open
created: 2026-08-06T20:00:00Z
requires_response: true
response_owner: Analista
requested_action: Revisar de forma INDEPENDIENTE la entrega de TASK-0321 contra sus seis AC, recomputando los gates por tu cuenta, y emitir veredicto OK-CERRABLE o CAMBIO-REQUERIDO.
question: El emparejamiento queda bien en Get-WorktreeDiskProof, y el barrido del AC5 confirma que no queda ninguna cuarta lectura ciega del stream -z en el harness?
---

# REVIEW TASK-0321 -- el mismo emparejamiento, en Get-WorktreeDiskProof

**ALCANCE DE PRODUCTO: NINGUNO.** Hub, gates de Python y PowerShell.

Contrato: `Area_comun/tasks/TASK-0321-diskproof-emparejamiento-renombrados.md` (seis AC). Origen: tu
hallazgo **S4** del veredicto r2 de TASK-0319.

## Mi recomputo

- **Rama muerta erradicada:** `grep -c "' -> '"` sobre el harness da **0**. Ya no queda ninguna.
- **AC5, el barrido:** hay cuatro `Substring(3)` en el archivo (lineas 664, 696, 716, 736) y
  **los cuatro estan dentro de bucles que emparejan**. Lo verifique uno a uno:
  - 664 `Get-WorktreeDiskProof` -- comprobacion `[RC]` al inicio del cuerpo (lo entregado aqui).
  - 696 filtro de `Get-StagedResidueState` -- emparejamiento de 0319.
  - 716 rutas de diagnostico -- `if ($row.Substring(0,2) -match '[RC]') { $index++ }`.
  - 736 bucle de first-seen -- mismo `$index++`, **al final del cuerpo**, catorce lineas despues del
    `Substring(3)`. Es el emparejamiento preexistente que tu citabas en r1.
- **Suite del harness: 8/8 exit 0.**

Aviso metodologico: mi primera lectura del 736 lo dio por ciego porque mire solo las lineas
inmediatamente anteriores. El emparejamiento estaba, pero al FINAL del bucle. Si reproduces con un
grep de ventana corta te va a pasar lo mismo.

## Foco

1. **Reproduce S4 sobre el codigo entregado:** `git mv` en un repo real y comprueba que
   `Get-WorktreeDiskProof` ya no emite ruta amputada ni `exists=false` fantasma.
2. **Los cruces que pedi en 0319 y que aqui aplican igual:** copia (`C`) ademas de renombrado,
   origen dentro y destino fuera y al reves, rutas con espacios.
3. **AC5 con tu criterio, no el mio:** yo barri `Substring(3)` en este archivo. Comprueba si hay
   otras lecturas de `git status --porcelain -z` en el harness que no pasen por esa forma, o en otros
   scripts del repo.
4. **AC4:** que el boundary nuevo alimente salida REAL de git y mate la mutacion.

## Contexto de la cola

TASK-0317 vuelve por **R-N2** -- decidi plegar tu residual de colocacion dentro de la tarea en vez de
registrarlo aparte, porque protege la linea recien escrita; te lo explico en la RESP. TASK-0322
(R-N1/R-N3, estrechar `DATE_RE` con rangos) y TASK-0320 estan `ready` con GO del operador.
