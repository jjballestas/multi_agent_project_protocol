# PREP - Reconciliacion ventana baseline (26-29-jul): mapeo commit -> tarea_id

> Preparado por el Arquitecto como turnkey para la reconciliacion sellada (SELLO-ETAPA-1-nova-budget-
> DRAFT.md s.10: "26-29-jul, Analista read-only, mapea commits/ramas del repo producto contra tarea_id;
> huerfanos = abandonada retroactiva, se publican como metrica de integridad"). NO ejecuta la
> reconciliacion antes de fecha; deja el mapeo COMPUTADO y el metodo REPRODUCIBLE para que la pasada
> del Analista sea mecanica, no exploratoria.
> Repo producto: `D:/Agentes/Zeus/NOVA/Nova-Budget`. Computado 2026-07-06 ~03:30 local (UTC+2) contra
> `git log --all` (19 commits totales al momento de este prep; la reconciliacion real del 26-jul debe
> RE-CORRER el comando, no reusar esta tabla si hay commits nuevos entre esta fecha y el 26-jul).

## Metodo (reproducible, un solo comando)

```bash
cd D:/Agentes/Zeus/NOVA/Nova-Budget
for c in $(git log --all --format="%H"); do
  taskid=$(git log -1 "$c" --format="%B" | grep -oE "Task-Id: [A-Za-z0-9_.-]+" | head -1)
  subj=$(git log -1 "$c" --format="%s")
  ts=$(git log -1 "$c" --format="%ai")
  echo "$c|$ts|${taskid:-NONE}|$subj"
done
```

Regla de reconciliacion (sello s.10): todo commit del repo producto debe tener un `Task-Id:` trailer
que mapee a una fila del journal de medicion (`personal/Arquitecto/TFM-medicion/corpus/medicion/
medicion_journal.csv`). Un commit SIN `Task-Id:` o que mapea a un `tarea_id` sin fila de journal es
HUERFANO -> se marca `abandonada` retroactiva y se PUBLICA como metrica de integridad del propio
estudio (no se oculta, no se descarta en silencio).

## Mapeo computado (19 commits, `git log --all`, 2026-07-06 ~03:30 local)

| Commit | Fecha (local) | Task-Id | Subject | Fila en journal? |
|---|---|---|---|---|
| `edbc037` | 2026-07-06 00:00 | TASK-0255 | test: add annulment mutation evidence | SI (seq 14, CLOSE) |
| `9aff84d` | 2026-07-05 23:54 | TASK-0255 | feat: add availability certificate annulment surface | SI (seq 13/14) |
| `02e67d8` | 2026-07-05 21:59 | TASK-0254 | feat: add availability adjustment baseline | SI (seq 11, CLOSE) |
| `a9246a5` | 2026-07-05 20:35 | **NONE** | fix: run appropriation evidence against live sql | **VERIFICAR: candidato TASK-0253 por proximidad temporal (entre 25e18d1 20:18 y 02e67d8 21:59, subject "appropriation" = familia P4.1) y por contenido (evidencia en vivo del harness de paridad de apropiacion) -- NO asignar solo por esta nota, confirmar con `git show a9246a5 --stat` contra el alcance de TASK-0253** |
| `25e18d1` | 2026-07-05 20:18 | TASK-0253 | test: version apply budget evidence harness | SI (seq 9, CLOSE, multiples sesiones) |
| `33adb5b` | 2026-07-05 13:58 | TASK-0253 | fix: align appropriation SQL gateway with deployed proc | SI |
| `75913aa` | 2026-07-05 12:26 | TASK-0253 | fix: rename budget SQL options | SI |
| `6cb9016` | 2026-07-05 12:15 | TASK-0253 | fix: harden live parity reset harness | SI |
| `00a3f47` | 2026-07-05 10:42 | TASK-0253 | fix: remediate appropriation modification baseline | SI |
| `e328196` | 2026-07-05 02:48 | TASK-0253 | feat: add appropriation modification baseline | SI (seq 8, OPEN) |
| `5ccb82c` | 2026-07-05 02:14 | TASK-0252 | fix: harden budget parity harness | N/A -- TASK-0252 es harness QA, fuera de la ventana baseline P2/P4 medida (verificar si tiene fila propia o si es infra sin medicion) |
| `dc04bd8` | 2026-07-05 01:30 | TASK-0252 | test: add budget parity harness | N/A -- idem |
| `9d9e744` | 2026-07-04 17:13 | TASK-0251 | fix: avoid duplicate execution report pagination | SI (seq 6/7, CLOSE) |
| `fa4ad82` | 2026-07-04 16:53 | TASK-0251 | feat: add budget execution report | SI |
| `f2be4e8` | 2026-07-04 15:53 | TASK-0250 | feat: add budget parameters read model | SI (seq 4/5, CLOSE) |
| `e3a03a8` | 2026-07-04 05:07 | **NONE** | test: add Nova web harness | **VERIFICAR: candidato TASK-0247 (fundacion, GOAL-P1) o TASK-0248 (skill codegen-triage) por proximidad temporal (entre 02f5d5a 03:00/TASK-0247 y af790be 03:55/TASK-0248) -- confirmar con `git show e3a03a8 --stat`** |
| `af790be` | 2026-07-04 03:55 | TASK-0248 | fix: add Nova web test gate | N/A -- TASK-0248 es skill/infra (codegen-triage), verificar si tiene fila de medicion propia o si esta fuera del journal por diseno (herramienta, no unidad de dominio) |
| `88af254` | 2026-07-04 03:25 | TASK-0248 | docs: add Nova codegen triage recipes | N/A -- idem |
| `02f5d5a` | 2026-07-04 03:00 | TASK-0247 | feat: add Nova Budget technical foundation | SI (GOAL-P1, piloto, journal sha256 d2a13216, fuera del contraste) |

## Resumen

- **17/19 commits** tienen `Task-Id:` trailer explicito.
- **2/19 commits huerfanos de trailer** (`a9246a5`, `e3a03a8`) -- candidatos de asignacion por
  proximidad ya anotados arriba, PERO la asignacion final la hace la reconciliacion real (26-jul),
  verificando el DIFF de cada commit contra el alcance declarado de la tarea candidata, no solo la
  cercania temporal (la cercania es una pista, no una prueba).
- **TASK-0252/TASK-0248** no son unidades de la ventana baseline P2/P4 medida (harness QA e
  infra/skill respectivamente) -- la reconciliacion debe confirmar si caen dentro o fuera del alcance
  de "medicion completa" del sello, o si su naturaleza de herramienta las excluye por diseno (a
  verificar contra NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md).
- **6 unidades baseline confirmadas con journal completo:** GOAL-P1 (TASK-0247), P2.1 (TASK-0250), P2.2
  (TASK-0251), P4.1 (TASK-0253), P4.2 (TASK-0254), PAR-2 (TASK-0255) -- todas con fila CLOSE y commits
  mapeados sin huerfanos dentro de su propio rango de tarea.

## Que falta para que la reconciliacion del 26-jul sea 100% mecanica

1. Re-correr el comando de la seccion "Metodo" contra el estado del repo producto al 25-jul (cierre
   duro de la ventana) -- puede haber commits nuevos entre este prep (06-jul) y esa fecha.
2. Resolver los 2 huerfanos (`a9246a5`, `e3a03a8`) contra el diff real, no solo la proximidad temporal.
3. Confirmar el tratamiento de TASK-0248/TASK-0252 (infra/QA vs unidad medida) contra la particion
   sellada.
4. Cruzar el resultado final contra `medicion_journal.csv` (las 6 filas baseline ya cerradas) para
   confirmar 1:1 sin huerfanos NO explicados.

task_id: TASK-0246
status: prep-completo
executive_summary: Mapeo commit->tarea_id del repo producto Nova-Budget computado y documentado para que la reconciliacion del 26-29-jul sea mecanica. 17/19 commits con Task-Id explicito; 2 huerfanos candidatos anotados con pista de resolucion (no asignados con certeza); metodo reproducible con un comando.
artifacts: Area_comun/artifacts/PREP-RECONCILIACION-baseline-commit-tarea-id.md
gates: N/A (documento de preparacion, no cambia codigo/estado gobernado).
next_recommended: El Analista re-corre el metodo el 26-jul y resuelve los 2 huerfanos + el tratamiento de TASK-0248/0252 contra la particion sellada.
risks: Ninguno -- prep de solo lectura; no ejecuta la reconciliacion antes de fecha, no asigna huerfanos con falsa certeza.
