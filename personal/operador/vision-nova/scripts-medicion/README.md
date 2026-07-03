# Scripts de medicion NOVA Budget (nueva-fila / cerrar-fila) -- DRAFT del asesor

**Estado:** DRAFT del asesor (2026-07-03). Entregable pendiente #1 del plan (prompt v3).
Preparado en el area del operador; se rutea al Arquitecto por mailbox para emplazarlo en el
HUB (`personal/Arquitecto/TFM-medicion/corpus/`) DESPUES de las ordenes F2 y NOVA-DEV.
Referencia: NOVA-ESTUDIO-002 (Protocolo de medicion) s.1-s.6.

## Que resuelve

El estudio exige un CSV **APPEND-ONLY** que **jamas se edita a mano** y donde a la vez **la
fila se actualiza en cada veredicto adversarial y se cierra en integracion** (s.1, s.3). Esas
tres reglas solo son compatibles con un modelo **journal + vista materializada**:

- `medicion_journal.csv` -- log APPEND-ONLY de eventos `OPEN`/`UPDATE`/`CLOSE`. Nunca se
  reescribe: es la fuente inmutable y lo que se atesta por sha256.
- `medicion.csv` -- VISTA materializada (ultimo estado por `tarea_id`). La (re)genera el
  script tras cada evento; nadie la edita a mano.

`defectos.csv` usa el mismo motor (`--tabla defectos`, clave explicita `--clave DEF-0001`).

## Archivos

| archivo | rol |
|---|---|
| `medicion_ledger.py` | motor unico (subcomandos abajo); stdlib pura, sin dependencias |
| `schema_medicion.json` | fuente unica de columnas/enums de `medicion.csv` (52 cols; incluye los 5 campos peones s.9 del sello) |
| `schema_defectos.json` | idem `defectos.csv` (9 cols) |

**Congelar el schema en el sello Etapa 1 (<=08-jul) = editar SOLO el JSON** (subir `version`,
registrar su sha256 en el sello). El codigo no cambia.

## Subcomandos

```
nueva-fila    abre una fila. Exige los 6 campos de apertura (tarea_id, brazo, par_id,
              estimate_previo_SML, criticidad, fecha_commit_estimate); NA prohibido ahi.
actualizar    superpone campos sobre una fila abierta (un evento por veredicto).
cerrar-fila   actualiza + exige estado_final (done|abandonada|truncada|bloqueada).
materializar  regenera la vista desde el journal (idempotente).
sha256        imprime sha256 del journal y la vista + la linea para el intent de atestacion.
verificar     valida secuencia 1..N del journal + enums/tipos + consistencia con la vista.
```

Flags: `--tabla medicion|defectos` (def. medicion), `--corpus <dir>` (def. `.`),
`--schema-dir <dir>` (def. junto al script), `--clave`, `--set campo=valor` (repetible),
`--no-commit`, `--atestar` (imprime sha256 tras escribir), `--event-ts`.

## Ejemplo (ciclo de una tarea gobernada)

```bash
cd personal/Arquitecto/TFM-medicion/corpus/     # el HUB
S=../../../operador/vision-nova/scripts-medicion  # o donde lo emplace el Arquitecto

# abrir (2 min): 6 campos
python "$S/medicion_ledger.py" nueva-fila --set tarea_id=NB-P4-2 --set brazo=gobernado \
  --set par_id=PAR-1 --set estimate_previo_SML=M --set criticidad=alta \
  --set fecha_commit_estimate=2026-07-08

# cada veredicto adversarial:
python "$S/medicion_ledger.py" actualizar --clave NB-P4-2 --set reworks_n=1 \
  --set "secuencia_veredictos=RECHAZADO;OK"

# cerrar en integracion (10 min): consumos + calidad + estado_final
python "$S/medicion_ledger.py" cerrar-fila --clave NB-P4-2 --set estado_final=done \
  --set fecha_fin=2026-07-12 --set tokens_total_atribuibles=41000 --atestar
```

## Fronteras (importante)

- **El script hace pseudo-atestacion** (commit git plano del repo hub, stage de rutas
  explicitas) e **imprime el sha256 del journal**. La **atestacion REAL** (sha256 -> intent
  barato del ledger #4 del hub) la ejecuta **el Arquitecto** en cada gate del estudio (sello
  Etapa 1, cada sorteo, cierres semanales, 25-jul, sello Etapa 2). El script NO escribe el
  ledger #4 (no es su rol).
- `--no-commit` para correr sin tocar git (util en pruebas / sandbox).
- Pensado para el **brazo gobernado**; el baseline registra sus filas con el mismo script
  (misma moneda), pero sus cubetas 3/4 (checker_formal, coordinacion_gobierno) son 0 por
  definicion.

## Pendiente al emplazar en el hub (decision del Arquitecto)

1. Ruta final del corpus y de los schema (sugerido: schema junto al journal en el corpus).
2. Si la pseudo-atestacion commitea en cada evento o por lote (el default commitea por evento;
   `--no-commit` + commit por lote es valido para reducir ruido git).
3. Congelar `schema_*.json` a `version: v1.0` en el sello Etapa 1 y anclar su sha256.
