# Runbook - Medicion del piloto GOAL-P1 (abrir / loguear / cerrar la fila)

> Redactado por el Asesor (diseno de medicion). GOAL-P1 = fundacion tecnica + PILOTO DE MEDICION del
> brazo BASELINE. Su medicion_journal.csv (build 3-8 jul) alimenta el corpus que se congela en el SELLO
> Etapa 1 (<=08-jul). GOAL-P1 esta EXCLUIDO del contraste causal (es el opener/fundacion); se mide para
> ESTRENAR la maquinaria del ledger y dar una fila de referencia baseline.
> Scripts ya emplazados en el hub: personal/Arquitecto/TFM-medicion/corpus/medicion/ (motor + schemas).

## 0. Que responde "definir el owner de la medicion"
La medicion NO es automatica: el journal es APPEND-ONLY y se corre A MANO (abrir fila -> actualizar por
evento -> cerrar). Alguien tiene que EJECUTAR esos comandos y CAPTURAR el consumo del build (tokens por
cubeta, reworks, tiempo, defectos). Eso es "el owner de la operacion de medicion". Hay que asignarlo
porque hoy "la medicion no ha arrancado" y el piloto existe justo para estrenarlo. Roles:

- **Owner de la operacion (propuesto): el OPERADOR** corre los comandos de este runbook (es quien observa
  el piloto de punta a punta). Alternativa: delegarlo al Arquitecto (dueno del corpus + atestacion).
- **Fuente del dato:** el dev/maker que construye GOAL-P1 (consumo real) + la evidencia git del build.
- **Atestacion (SIEMPRE el Arquitecto):** sha256 del journal -> intent barato del ledger #4 del hub. El
  script imprime el sha256; el ledger lo escribe SOLO el Arquitecto (capability). El asesor NO opera el
  ledger ni escribe el corpus del hub (no-firmante).

Confirma el owner (Operador vs Arquitecto) antes de arrancar; el resto del runbook es igual.

## 1. Ubicacion
```
CORPUS=personal/Arquitecto/TFM-medicion/corpus/medicion   # donde el Arquitecto emplazo el motor+schemas
cd "$CORPUS"     # o usa --corpus "$CORPUS" desde la raiz del repo
```
El journal (medicion_journal.csv) y la vista (medicion.csv) viven en el corpus. JAMAS editarlos a mano.

## 2. Paso A - ABRIR la fila (6 campos de apertura; NA prohibido aqui)
```
python medicion_ledger.py nueva-fila --corpus "$CORPUS" \
  --set tarea_id=GOAL-P1 \
  --set brazo=baseline \
  --set par_id=NA \
  --set estimate_previo_SML=L \
  --set criticidad=fundacion \
  --set fecha_commit_estimate=2026-07-04
```
- `estimate_previo_SML`: GOAL-P1 es un vertical-slice grande -> **L** (confirma tu numero; es su fila propia,
  NO entra al sorteo Q4).
- `brazo=baseline` -> por definicion las cubetas checker_formal y coordinacion_gobierno seran 0.

## 3. Paso B - LOGUEAR durante el build (un `actualizar` por evento; campo sin fuente = NA sin culpa)
```
python medicion_ledger.py actualizar --corpus "$CORPUS" --clave GOAL-P1 \
  --set orchestration_mode=mono \
  --set reworks_n=<n> \
  --set "secuencia_veredictos=<p.ej. OK  o  RECHAZADO;OK>" \
  --set tag_incidente_maquinaria=<regimen|arranque|incidente|NA>
```
Que capturar en el piloto (lo que se pueda; el resto NA):
- **Costo (4 cubetas de tokens):** `tokens_dev` (real), `tokens_adversarial_informal` (si hubo revision
  informal), `tokens_checker_formal`=0, `tokens_coordinacion_gobierno`=0 (baseline). Subsets informativos
  (NO se suman): `tokens_cache_reads`, `tokens_peones` (si se usaron peones; GOAL-P1 probablemente mono).
- **Peones (si aplica):** `peones_n`, `peon_revivals_n`, `peon_modelos`, `tokens_peones`.
- **Tiempo/sesiones:** fechas; sesion=tarea; sesiones fallidas son costo real.
- **Aislamiento de teething:** si hay remediacion de incidentes de maquinaria (no del producto), va a filas
  OVERHEAD-FIJO con `tag_incidente_maquinaria=incidente`, JAMAS a la cubeta de GOAL-P1.
- **Defectos (si aparecen post-entrega):** se registran en la tabla defectos (motor `--tabla defectos
  --clave DEF-0001`) con su `detector` (gate_determinista/adversarial_informal/checker_formal/...).

## 4. Paso C - CERRAR la fila (exige estado_final)
```
python medicion_ledger.py cerrar-fila --corpus "$CORPUS" --clave GOAL-P1 \
  --set estado_final=done \
  --set fecha_fin=<YYYY-MM-DD> \
  --set tokens_dev=<n> --set tokens_adversarial_informal=<n> \
  --set tokens_checker_formal=0 --set tokens_coordinacion_gobierno=0 \
  --set tokens_total_atribuibles=<n> \
  --atestar
```
- `estado_final`: done | abandonada | truncada | bloqueada.
- `--atestar` imprime el sha256 del journal tras escribir (la linea para el intent del Arquitecto).
- DEGRADACION EX-ANTE: si el desglose por cubeta es incapturable en baseline, cae a
  `tokens_total_atribuibles` (decidido AHORA por runbook, no improvisado en agosto).

## 5. Paso D - Verificar + atestar
```
python medicion_ledger.py verificar --corpus "$CORPUS"    # secuencia 1..N + enums/tipos + consistencia vista
python medicion_ledger.py sha256    --corpus "$CORPUS"    # imprime sha256_journal + la linea del intent
```
El **Arquitecto** toma ese sha256 y lo registra via `submit_intent` (atestacion #4 del hub). Ese sha256 del
journal del piloto entra al corpus del SELLO Etapa 1.

## 6. Lo que el piloto debe DEJAR CLARO (es su proposito)
- Que campos del schema son REALMENTE capturables en un build baseline y cuales caen a NA/degradacion.
- El tiempo real de abrir/loguear/cerrar una fila (overhead de instrumentacion).
- Si el desglose por cubeta de tokens es viable o hay que degradar a total.
- Que el journal append-only + atestacion funcionan de punta a punta antes de sellar.
Esos hallazgos se reflejan en el SELLO (schema congelado a v1.0) y en el checklist del dia del sello.

## 7. Fronteras (recordatorio)
- El asesor DISENA (este runbook); NO opera el ledger ni escribe el corpus del hub (no-firmante).
- La atestacion #4 la ejecuta SOLO el Arquitecto.
- GOAL-P1 esta FUERA del contraste causal; su fila es de referencia baseline + prueba de maquinaria.
