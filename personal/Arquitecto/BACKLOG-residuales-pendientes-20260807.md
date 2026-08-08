# Residuales medidos y NO contratados -- corte 2026-08-07 12:05

Cola de espera deliberada. Los ocho contratos 0327-0334 ya tienen GO; estos quedan aqui **sin
minar contrato** para no diluir esa tanda. Se convierten en tareas cuando la cola drene.

Criterio de entrada: medido por alguien (checker o yo), con repro, y con direccion de fallo
declarada. Nada especulativo.

---

## Prioridad ALTA -- falla ABIERTO o es destructivo

**RES-1. El recorte al tope duro de la rama de post-entrega no tiene negativo permanente.**
Fuente: R-N1 del veredicto r2 de TASK-0324, medido (mutante M7). Borrar
`if ($postDeliveryDeadlineUtc -gt $postDeliveryHardDeadlineUtc) {...}` deja la suite ENTERA en
exit 0. Su gemelo dentro del helper si esta cubierto (M8 muere). Consecuencia acotada: la ventana
podria rebasar su tope duro en como mucho un `ProgressExtensionSeconds`.
**Origen `e266d070`, ANTERIOR a TASK-0324** -- verificado con `git log -S` por el checker, asi que
no es regresion de aquella tarea. El propio checker pide tarea propia.

**RES-2. El estado de reintento no se reconcilia con el mailbox.**
Fuente: yo, en vivo hoy. Un mensaje archivado con entrada de retry (`defers>=1`) **se ejecuta igual
desde `archived/`**: el harness reintenta por NOMBRE. Repro exacta:
`MSG-20260807-Codex-to-Analista-REVIEW-TASK-0320.md`, archivado a las 11:36, ejecutado a las 11:56.
Direccion: gasta un turno de checker -- caro con la exclusion mutua de 0331 activa -- y hace que
superseder un mensaje sea imposible por el camino documentado. Ver
[[archivar-no-desencola-el-reintento]].

---

**RES-10. El claim de `prune_state.py --apply` cubre `CLAIMS.json` ENTERO.**
Fuente: yo, en vivo hoy. Solapa con cualquier claim ajeno (que se declara con FRAGMENTO
`CLAIMS.json#<id>`), asi que **basta un claim vivo de un peer para que la poda no pueda ejecutarse**:
`IntentValidationError: claim acquire overlaps active claim`. Cadena observada: tarea `blocked` ->
claim retenido -> prune imposible -> `prune --check` rojo -> **CI rojo**. Direccion: no corrompe,
pero convierte un bloqueo de coordinacion en un fallo de integracion. El arreglo natural es que el
claim de poda use fragmentos como todo lo demas, o que la poda se ejecute sin claim al ser
read-modify-write sobre estado derivado. Emparejada con RES-2 y con TASK-0331.

**RES-11. El umbral de poda por peso de mailbox penaliza la cola llena.**
Fuente: yo, medido hoy tres veces. El driver `cold_start_tokens >= 20000` mide el PESO de
`Area_comun/mailbox/open/`. Con la directiva operativa de mantener la cola de Codex llena, cinco GO
en espera mas dos reviews en curso mas dos remediaciones ponen el mailbox en ~20.600 **sin un solo
mensaje consumido que archivar**. Es decir: el umbral se cruza por trabajo PENDIENTE legitimo, no por
basura, y no hay accion correctiva disponible mientras el peer no consuma.
Direccion: no corrompe; deja `prune --check` rojo y con el CI, sin remedio a mano. Se agrava cuando
el peer esta bloqueado por el veto de exclusion mutua, porque los mensajes se acumulan sin
consumirse. Candidatos de arreglo: que el driver mida solo mensajes CONSUMIDOS pendientes de
archivar, o que el umbral escale con el numero de tareas activas. Emparejada con TASK-0331.

## Prioridad MEDIA -- fragilidad o falsa alarma futura, falla CERRADO

**RES-3. `Select-Object -First 1` sin exigir unicidad** en el selector del bucle vivo de 0324
(R-N3). Si otro `while` del fichero llegara a contener `POST_DELIVERY_WINDOW_START`, el contrato se
pone rojo sobre fuente sana. Un `if ($matches.Count -ne 1) { throw }` lo cierra.

**RES-4. Acoplamiento al reloj del probe de 0324** (R-N4). Margen medido 0,570-0,584 s en seis
corridas, `ticks=15` en catorce. Hace falta ~35 pct de ralentizacion para volverlo rojo. Estable en
este equipo; candidato natural a intermitencia en un runner de CI cargado. Falla cerrado.

**RES-5. `fullmatch` con dientes en 1 de 3 consumidores** (R2 de 0322). Solo
`NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY` fija la linea de `contains_pii`; las llamadas de
`validate_metadata` y del lector de cold-packs no estan fijadas -- relajarlas a `match` no rompe
ningun test. Heredado.

---

## Prioridad BAJA -- cosmetico o informativo

**RES-6. `inherited_deadline_observed` promete mas de lo que prueba** (R-N2 de 0324). Solo comprueba
que el campo del log no sea `none`; con el cableado inalcanzable devuelve `True`. NO es agujero -- lo
que sostiene el contrato es la pareja `live=False`/`dead_wiring=True` -- pero el nombre invita a
leerla como prueba de la herencia. Renombrar a `post_delivery_deadline_field_present`: una linea.
Entra en el siguiente ciclo que toque ese fichero.

**RES-7. `\d` sin `re.ASCII` en `DATE_RE`** (R3 de 0322). Acepta digitos decimales Unicode;
`validate_metadata` admite sin aviso un `created_at` con ano en indo-arabigo. El gate
`scan_encoding` impide que llegue a un artefacto gobernado. Ya declarado en el ledger del SPEC.

**RES-8. El consumidor de cold-packs de `DATE_RE` no lo ejercita el corpus real** (R4 de 0322):
`cold_pack_count: 0` en clon limpio. El estrechamiento hace que ese camino lance `ValueError` sobre
mas entradas -- direccion correcta -- pero sin evidencia de corpus.

**RES-9. El baseline de vocabulario solo cuenta los declarados de la INSTANCIA, no los del nucleo.**
Fuente: yo, al revisar 0320. Nueve grafias del mismo concepto conviven en el nucleo "neutral"
(`REVIEW`, `REVIEW-RESPONSE`, `REVIEW_REQUEST`, `REVIEW_RESULT`, `REVIEW_VERDICT`, `review`,
`review-verdict`, `review_result`, `review_verdict`) y ningun mecanismo detecta esa deriva. Pendiente
de la respuesta del Analista a la adenda de 0320: si alguna esta muerta en el corpus, sube a ALTA.

---

## Nota de proceso

Nueve residuales medidos en una sola jornada, ninguno inventado. La tasa a la que aparecen es la
evidencia de que el ciclo de dos capas funciona; el riesgo es tratar la lista como deuda y no como
inventario. Regla: **no se mina contrato mientras la tanda anterior no drene**, y los de direccion
ABIERTA suben antes que los de direccion CERRADA, con independencia de cuantos casos toquen.

---

**RES-12. `RETRY_TRANSIENT reason=staged_residue_aborted` nombra una accion que NO ejecuta.**
Fuente: yo, midiendo en vivo el 2026-08-08. En `peer_mailbox_cron.ps1:1345` el veredicto `aborted`
del guard de residuo **solo escribe la linea de log y continua al exec**: no llama a
`Register-PreExecDefer`, no incrementa nada, no penaliza. Pero la etiqueta `RETRY_TRANSIENT` es la
misma que usa la contabilidad real de reintentos, la que si agota el presupuesto a los 3.
Direccion: no corrompe y no bloquea -- el dano es de OBSERVABILIDAD, y cae sobre el diagnostico
humano. Yo mismo estuve a punto de concluir que el Analista estaba siendo penalizado por su propio
draft sin commitear del 20-jul, cuando en realidad ejecutaba con normalidad. Un log que nombra una
accion que no toma es una trampa para quien diagnostica bajo presion.
Encaja en el inventario que ya pide **TASK-0337** (todos los vetos pre-exec, que liga cada uno y que
garantiza); anadirlo alli al promoverla en vez de abrir tarea propia.

**Medicion #2 para TASK-0337, mas nitida que la primera (08-ago 10:03).** Codex fue diferido dos
veces por residuo que era **un mensaje de mailbox dirigido al ANALISTA**:

    reason=worktree_residue_live
    paths=["Area_comun/mailbox/open/MSG-20260808-Arquitecto-to-Analista-REVIEW-..."]
    defer=2 elapsed_seconds=3146 (52 min de presupuesto consumidos)

Un fichero que Codex no va a leer nunca, dirigido a otro agente, sobre otra tarea, bloqueando su
exec. La primera medicion (review de 0329 diferida por ficheros de 0331) ya era clara; esta lo es
mas, porque ni siquiera hay solape conceptual: es correo ajeno.

**Y la causa fui YO**, escribiendo en el mailbox mientras ambos peers sondeaban. Es reincidencia
sobre una leccion que ya tengo escrita (ventana compartida / silencio de escritura). Atenuante real:
commitee en el acto cada vez y con 7200 s de presupuesto no murio ningun mensaje. Pero el patron es
el mismo, y la conclusion operativa tambien: **agrupar las escrituras de mailbox en un solo commit
por ventana en vez de gotearlas.**
