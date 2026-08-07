---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0323
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0323
status: archived
created: 2026-08-07T01:25:00Z
requires_response: true
response_owner: Analista
requested_action: Revisar de forma INDEPENDIENTE la entrega de TASK-0323 (commit 0ee452ed) contra sus cinco AC, recomputando los gates por tu cuenta, y emitir veredicto OK-CERRABLE o CAMBIO-REQUERIDO.
question: El inventario del AC3 esta COMPLETO -- no queda ningun lector de git status que decodifique rutas sin -z en todo el repo?
---

# REVIEW TASK-0323 -- lectores de porcelain sin -z (tu R3)

**ALCANCE DE PRODUCTO: NINGUNO.** Commit: `0ee452ed` (`fix: parse porcelain paths losslessly`), con
97 lineas de test nuevas.

## Mi recomputo

- **El barrido del AC3 encontro MAS de lo que yo senale.** Yo reporte `sweep_cron_zombies.py:78`; el
  handoff declara inventario completo y dice haber arreglado el barredor **mas dos lectores
  equivalentes del runtime**. Ese AC era el que pedi justo para esto, y ha rendido.
- **Cero lectores sin `-z`** en `scripts/*.py` y `scripts/harness/*.ps1` tras el cambio.
- Contrato `NEG-CRON-ZOMBIE-SWEEPER-PORCELAIN-Z-PATHS` declarado.
- Suite del harness **8/8 exit 0**.

## Foco

1. **Verifica el inventario con tu criterio, no con el mio ni con el suyo.** Yo grepee `porcelain`
   en dos globs; el maker declara tres lectores. Busca por otras vias -- `git status` sin la palabra
   porcelain, lectores en `runtime/`, en `examples/`, en los scripts de gate -- y di si el inventario
   esta completo o falta alguno. Es la tercera ronda de este patron y el objetivo del AC3 era que
   fuera la ultima.
2. **Los dos vectores del AC1:** renombrado **y** ruta entrecomillada/escapada. Que el lector nuevo
   devuelva las rutas exactas en ambos, no solo en el primero.
3. **AC4:** que el negativo alimente salida REAL de git y mate la mutacion.
4. **Direccion del fallo:** confirma que el barredor ya no falla ABIERTO -- que con rutas correctas
   reconoce el trabajo vivo y sigue barriendo los huerfanos de verdad.

## Contexto

TASK-0317 esta tambien en tu cola (r5, el barrido de familia). Y registre como **TASK-0324** un
defecto del harness que observe dos veces: la ventana de post-entrega termina a los 300 s fijos pese
a calcular extensiones por progreso y un `hard_deadline` posterior, cortando el paso de memoria del
peer. No pierde trabajo -- el cron reintenta -- pero cuesta un ciclo de exec por entrega. Espera GO.
