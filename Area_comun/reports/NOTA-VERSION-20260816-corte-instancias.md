# Nota de version -- paquete de actualizacion para instancias, corte 2026-08-16

- Emitida: 2026-08-16, corte 09:00 hora local (UTC+2)
- Destinatario primario: instancia NOVA (modelo 2.A, gobierno anidado, tier runtime)
- Emisor: Arquitecto del hub `multi_agent_project_protocol`
- Adoptable por: `scripts/upgrade_instance.py`

---

## 1. Que entra

**(A) El aparato de verificacion vuelve a operar.** El pin sha256 de `.githooks/pre-commit` en
`.github/workflows/validate.yml` estaba desincronizado del gancho desde `6f0feb3b` (2026-08-14). El
paso 4 del job `validate` moria y **saltaba 78 de sus ~86 pasos**. Medido con control historico:

    corrida 31802752243  (14-ago, ANTES)    26 success,  1 failure, 60 skipped
    corrida 31913703515  (15-ago, DESPUES)   6 success,  2 failure, 78 skipped

Corregido, y con un **negativo permanente cableado dentro del propio paso de CI**: perturba el
gancho y exige que el pin viejo lo rechace (`PIN_MISMATCH_NEGATIVE`).

**(B) Guardia de residuo consciente del alcance (TASK-0337, AC7 + AC10).** Es lo que NOVA pidio
como prioridad unica (su D-1), tras medir **137 aplazamientos `worktree_residue_live` en un solo
dia** entre su maker y su checker.

- **AC7:** el diferimiento ya no es mudo. El log emite `intersections_json` diciendo QUE ruta sucia
  intersecta QUE ruta del mensaje, en vez de un `worktree_residue_live` sin sujeto.
- **AC10:** la exencion de area personal **deriva el prefijo de instancia** (`git -C $Root rev-parse
  --show-prefix`) en vez de anclar en `^personal/`. **Esto es lo que hacia la exencion inoperante en
  gobierno ANIDADO**: alli `git status` emite `Aegis/personal/...` y el ancla en raiz no casaba
  jamas. En layout plano el prefijo es cadena vacia y el comportamiento no cambia. Acreditado por el
  checker **en las dos topologias**, con el cron lanzado desde la raiz del repo.

---

## 2. Residuos ABIERTOS -- leer antes de operar

Se declaran porque **no estan cerrados**, no como formalidad. Cada uno con su causa medida.

### R-1. El interbloqueo sigue vivo para todo mensaje sin `task_id` resoluble

**Y la causa NO es el guardia de residuo: es `message_scope_ambiguous`.** Esta correccion la aporto
el checker y rectifica un diagnostico previo del Arquitecto que atribuia el bloqueo al guardia.

Poblacion medida en el hub: **292 de 458 tareas y 10 de 38 mensajes abiertos** no tienen scope
resoluble. **Incluye los mensajes del canal Operador, que llevan `task_id: none`** -- tambien en
vuestra instancia.

Efecto operativo: un mensaje sin tarea resoluble puede diferirse en bucle hasta agotar su ventana
de 7200 s y **morir sin que nadie lo lea y sin error visible**. Desde fuera el cuadro es identico al
de un peon ocupado.

**Mitigacion interina recomendada:** vigilancia manual del `retry.json` de cada peon, mirando
`defers` crecientes y `RETRY_EXHAUSTED`. Trabajo abierto: TASK-0408 (que el encargo agotado deje
rastro donde alguien mire) y H-3 de TASK-0337.

Un intento de arreglo (`f2de3ad7`) **se reviritio antes de este corte**: pasaba la letra del
requisito pero su efecto en el arbol vivo era **nulo** -- ningun vector pasaba de "no arranca" a
"arranca" -- y dejaba en rojo `check_falsification_contracts`. Se prefirio declarar el residuo antes
que embarcar un cambio de efecto nulo.

### R-2. La reincidencia del pin no esta cerrada

El pin **casa hoy**, y su negativo demuestra que el control **puede decir que no**. Lo que NO esta
cerrado es la recaida:

- El negativo original no discriminaba: el checker lo desdento y siguio imprimiendo `PASS`.
  Remediacion R1 pendiente (aceptacion **por mutacion**, no por texto).
- Y hay una via mas ancha: **`.github/` no esta en el perimetro de producto gobernado**, asi que el
  checker **borro el paso del pin ENTERO** en un commit sin `Task-Id`, sin claim y sin evento de
  ledger, **y aterrizo**. El gate no protege el fichero donde vive el gate.

Decision de politica tomada: `.github/` **entra** en el perimetro gobernado -- un workflow que
ejecuta los gates es infraestructura de control, no documentacion. Sale como tarea propia
registrada, no ampliando TASK-0378.

### R-3. Separacion maker/checker: medio abierta

Heredado de TASK-0378 y ya declarado en su alcance: el claim obligatorio cierra el incidente
reportado (commits de producto sin claim), pero **un actor puede auto-clamarse y commitear**. El
cierre completo depende de la liveness de checker como paso 0, que es tarea aparte.

Relacionado: **la identidad de gobierno es forjable** (TASK-0386, no incluida en este corte). El
gate deriva el actor de `git config user.name`, que los tres agentes comparten. Verificado en el hub
esta madrugada: un commit de coordinacion del Arquitecto entro firmado como `Codex`.

### R-4 (CORREGIDO). El gate de poda: el mailbox era el 73 %, no era irreducible

**Rectificacion de una afirmacion previa de esta misma nota.** Se declaro que `cold_start_tokens`
era IRREDUCIBLE porque media el backlog ABIERTO de tareas mientras la poda solo archiva lo
TERMINAL. **Era falso, y el error de metodo fue medir el gate justo despues de una poda que no
tocaba el mailbox.**

    open/ 61 mensajes  ->  cold_start_tokens 74130
    open/  5 mensajes  ->  cold_start_tokens 20277   (umbral 20000)

**53.853 tokens -- el 73 % -- eran MAILBOX.** `prune_state.py` **si** poda mailbox, pero recoge de
`answered/`, no de `open/`: la clasificacion de "consumido" es del ORQUESTADOR. Correr la poda NO
es hacer higiene de mailbox.

**Secuencia correcta, y va como regla adoptable:** higienizar -> dejar de rutear (la ventana de
poda se abre sola: un peon solo arranca exec si hay mensaje) -> podar -> volver a rutear. Medido
que rutear tres mensajes subio el gate de 20277 a 22201: **rutear engorda lo que la higiene
adelgaza**, por eso el orden no es preferencia.

Lo que queda abierto de verdad: la poda reclama `CLAIMS.json` ENTERO, asi que no coexiste con
ningun claim de peon. Con dos peones activos su ventana dura segundos.

### R-5. Paridad de inventario de identidad: diverge y ademas apunta a vacio

Aislado por el checker al cerrar TASK-0337 y declarado **heredado, no atribuible** a esa entrega.
Registrado como **TASK-0410**.

    NEG-NEUTRALITY-IDENTITY-INVENTORY-PARITY   ROJO
      runner    scripts/test_scan_domain_neutrality.py
      cableado  .github/workflows/validate.yml:522
      censo     92 frente a 91
      causas    1 divergencia de inventario entre gemelos
                3 coordenadas MUERTAS en runtime/context.py

Es la unica variante en la que el ancla **no diverge sino que apunta a VACIO**: exenciones cuyo
objeto ya no esta en la linea declarada. **Una exencion muerta exime algo que ya no existe y puede
estar tapando una violacion nueva en esa misma linea.**

### R-6. Un job INTERMITENTE no puede formar parte del perfil de certificacion

`falsification-runners` fallo el paso 6 (`Execute mailbox retry falsification runner`) con

    AssertionError: mid-log ambiguity was rolled back

Es **TASK-0401**, ya enumerada y declarada fuera de este corte desde el primer plan. Lo NUEVO es la
prueba de que es **intermitente**, medida el mismo dia sobre commits equivalentes:

    run 31950779306  (9ad9b6a5)   falsification-runners  9 success, 0 failure
    run 31955109753  (57d137ff)   falsification-runners  8 success, 1 failure  <- paso 6

**Correccion de una lectura propia:** se dijo que `9ad9b6a5` tenia "perfil limpio". No lo tenia:
dio 9/9 porque 0401 **no disparo en esa tirada**, no porque estuviera sano. Un verde de un job
intermitente no acredita ausencia del defecto.

**Criterio que se adopta, y es la parte reutilizable:** un job con fallo intermitente **se declara y
se excluye explicitamente del perfil de certificacion**, igual que el paso 23. Exigirlo verde haria
que el corte dependiera del azar de la corrida -- que es la forma exacta de un gate que no
discrimina. El perfil de este corte es por tanto el del job `validate`, cuyo fallo unico y su causa
son estables y coinciden con el control.

## 3. Como se certifico este corte

**Por CONTEO DE PASOS EJECUTADOS contra control historico, no por color.** Razon: un job rojo
absorbe reds nuevos gratis -- fue exactamente lo que oculto el defecto del pin durante dos dias.

- Control historico: corrida `31802752243`, ultimo estado sano conocido, **26 success**.
- **RESULTADO: corrida `31950779306` sobre `9ad9b6a5` da 26 success / 1 failure / 60 skipped --
  identico al control en numero Y en causa** (el unico fallo es el paso 23, la poda, que tambien
  fallaba en el control). Punto de partida de la jornada: 6 success, muriendo en el paso 4.
- Criterio: restaurar ese orden de magnitud en el job `validate`.
- **Dos corridas** sobre el mismo commit (DECISION-0115): un verde de una sola corrida es una
  primera corrida, no un verde.
- Se cita la terna completa: `run_id` + `job` + `head_sha`, con el desglose success/failure/skipped.

---

## 4. Nota de metodo

Este paquete se produjo en una noche con **cuatro ciclos completos maker-checker**. El checker
devolvio **CHANGE-REQUIRED en tres de los cuatro**, todos con defecto real, medido y reproducido --
ninguno rubber-stamp. Dos de esos rechazos mataron cambios que **pasaban su propio criterio escrito**
y que sin embargo no producian efecto.

Lo que hace utilizable este paquete no es que salga verde: es que **lo que no esta cerrado esta
nombrado, con su causa medida y su poblacion contada**.
