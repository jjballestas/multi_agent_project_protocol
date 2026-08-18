# SEGUNDA REVISION ADVERSARIAL (Arquitecto), multi-vector, de la PROPUESTA v2 del Analista

- Fecha: 2026-08-16, 02:09 hora local (UTC+2), reloj real
- Objeto: `personal/Analista/drafts/PROPUESTA-20260816-eficiencia-coordinacion-v2.md`
- Revision previa: `personal/Arquitecto/REVISION-ADVERSARIAL-20260816-propuesta-eficiencia-coordinacion.md`
- Formato pedido y respetado: veredicto POR VECTOR (sostiene / rompe / rompe con enmienda),
  sin sintesis prematura.
- Estado: DRAFT en area personal. Modo debate por orden del operador: NO ruteado, NO es
  DECISION, NO toca ledger.

---

## C0. CORRECCION DE MI PROPIO F1 -- y es la que mas mueve la v2

**Mi hallazgo F1 estaba mal en su titular, y el Analista lo concedio ENTERO y reconstruyo E4
sobre el. Hay que deshacer las dos cosas.**

Dije: "la review de TASK-0378 nunca llego a ejecutarse; al checker jamas se le pregunto".
Verificado ahora abriendo `Area_comun/mailbox/archived/`, que no habia abierto:

    14-ago 15:18   Codex entrega 6f0feb3b  (rompe el pin del gancho; nadie lo nota)
    14-ago 16:10Z  review ruteada -> 22 defers por `active_external_claim`, attempts=0,
                   agota los 7200 s a las 16:15Z
    14-ago 16:40Z  el Analista ENTREGA VEREDICTO IGUALMENTE: CHANGE-REQUIRED, anclado en
                   HEAD b454ce80 / implementacion 6f0feb3b, vector a vector, clon limpio,
                   con un hallazgo propio (I2) que no venia en mis dos adendas
    15-ago 01:19Z  remediacion r2 ruteada a Codex
    15-ago 02:05Z  Codex ENTREGA r2 en a5c5ad57 y pregunta explicitamente:
                   "Can Arquitecto route the independent review from commit a5c5ad57?"
    ...            NADIE la ruteo. ~47 h en `in_review` esperando al COORDINADOR.

Fuente: `MSG-20260814-Analista-to-Arquitecto-REVIEW-TASK-0378-veredicto.md` (archivado,
creado 2026-08-14T16:40:00Z) y `MSG-20260815-Codex-to-Arquitecto-HANDOFF-TASK-0378-remediation-2.md`.

**Lo que se cae:**

1. **La perdida de 48 h NO es de clase B (sustrato).** Es de clase C, y es MIA: una peticion
   explicita del maker que no atendi. Del episodio, al sustrato solo le imputan las **2h05m**
   de diferimiento por colision de claim -- reales, pero son 2h, no 48h.
2. **La convergencia de la v2 pierde una de sus dos patas.** La seccion 0 afirma que "dos
   diagnosticos independientes convergen" en clase B. No eran independientes: el Analista
   adopto mi error. Un diagnostico y su eco no son dos mediciones.
3. **M5 pierde su baseline.** "Edad maxima de in_review sin actividad de checker = 48h (0378)"
   mide una variable que en este caso vale ~0: el checker actuo dos veces. Lo que estuvo
   parado 47 h fue el RUTEO. M5 debe medir **edad de un handoff entregado sin review ruteada**,
   que es la variable que de verdad fallo.
4. **Y el dato que mas vale para la metodologia**, que ninguno de los dos habia visto: el
   defecto del pin **sobrevivio a una review adversarial completa**. El veredicto del 14-ago
   audito el gancho vector a vector, con clon limpio y exit codes -- y no lo vio. Ninguna
   lente miraba el CABLEADO de CI. *Un defecto que apaga el instrumento de verificacion es
   invisible para todo verificador que mire a traves de ese instrumento.* Esto refuerza M7
   mucho mas que mi F3 original, y por una via distinta: no es que nadie mirase, es que
   mirando bien no se ve.

**Leccion de metodo, para mi:** cite un `retry.json` sin abrir el `archived/` del mismo
task_id. Es la reincidencia exacta de "citar un run sin abrirlo" con otro instrumento. Un
`attempts: 0` prueba que ESE mensaje no se ejecuto -- no que el trabajo no se hiciera por
otra via.

---

## V1 -- Ataque al instrumento (M0-M8): **ROMPE**

**M0 (derivacion de actor) no es implementable como esta escrita, y no es "sin cambio de
protocolo".** Medido:

    trailers presentes en los ultimos 40 commits:
        Task-Id (40), Ops-Reason (26), Co-Authored-By (26), Fixes-Task (3)
    -> NINGUN trailer nombra al actor de gobierno. Co-Authored-By nombra el MODELO.

    subjects con actor derivable directo (ultimos 60):  13 / 60  (22 %)
    el 78 % restante nombra la TAREA, no el actor:
        review(TASK-0396)...  tasks(TASK-0397)...  coord(TASK-0396)...  fix(TASK-0397)...

Se puede construir una heuristica por VERBO (`coord`->Arquitecto, `review`->Analista,
`deliver|fix|feat|test`->Codex), pero **esa heuristica misatribuye exactamente los casos que
E1 quiere contar**: las operaciones de un actor SOBRE otro. Caso real en la ventana medida:

    41b54d2d  state(memoria): commiteo el fichero de memoria de Codex que difiere su cola

Lo hice YO; una derivacion por subject lo lee como Codex. Es el mismo defecto que M0 existe
para corregir, reproducido dentro de M0.

**Enmienda:** M0 exige **anadir un trailer de actor al contrato de commits**
(`COMMIT_TRAILERS.json`). Eso es un cambio de protocolo y cae en la familia de TASK-0386. Por
tanto **D-A esta mal etiquetado**: no es "sin cambio de protocolo". O M0 sale de semana 0, o
D-A deja de ser una decision menor.

**M7 rompe con enmienda: el RATIO es ciego al borrado de pasos.** M7 caza el caso del pin
(8/86 = 9 %). No caza este otro: si alguien BORRA pasos del workflow, "declarados" baja con
"ejecutados" y el ratio se queda en 100 %. Verificacion eliminada = M7 verde. **M7 debe
publicar el CONTADOR ABSOLUTO de pasos ejecutados con suelo historico, no solo el ratio.**
Segundo caso limite real: pasos legitimamente `skipped` por `if:` dejan el ratio
permanentemente por debajo de 100 %, la alerta se vuelve ruido y se ignora -- hay que fijar el
suelo por job contra su propia historia, no contra 100 %.

**M8 rompe con enmienda: no distingue defer sano de defer patologico.** Un defer durante una
ventana de escritura legitima es el sistema funcionando. El discriminante no es el tiempo
diferido sino **el que termina en `defer_terminal` / `RETRY_EXHAUSTED`**. Medido esta misma
noche: el GO de TASK-0337 acumulo defers sanos (que resolvieron) y luego murio con
`RETRY_EXHAUSTED attempts=3`. Solo lo segundo es perdida. **M8 = tiempo-mensaje diferido QUE
ACABA EN MUERTE, por causa.**

---

## V2 -- Ataque de gaming: **ROMPE**

**El golpe fuerte es M4/AC-P1: el numerador lo autoclasifica la parte juzgada.** "Round-trips
por defecto de intake = 0" depende de que alguien declare que un round-trip fue culpa del
intake -- y ese alguien soy yo, el autor del intake. En 0396 clasifique dos commits mios como
defectos propios, pero nada me obligaba. Bajo carga, a las 2 de la manana, la clasificacion
generosa es gratis e indetectable.

**Enmienda (mecanizable, y por eso vale):** M4 se deriva de git, no de una declaracion --
**commits que modifican el bloque `intake` de una tarea DESPUES del commit que ruteo su GO**.
Es `git log -L` sobre el bloque, con el GO como ancla temporal. No opina nadie.

**AC-P2 rompe con enmienda:** "ninguna tarea de sustrato espera >72 h" se satisface **no
etiquetando** algo como sustrato. La v2 dice que el checker puede impugnar la etiqueta -- pero
el checker solo ve tareas RUTEADAS, y una tarea de sustrato nunca ruteada nunca se impugna. El
punto ciego es exactamente la poblacion que el AC pretende proteger. Enmienda: la etiqueta se
audita sobre el BACKLOG (`proposed`+`ready`), no sobre lo ruteado.

**AC-P1 item 1 mecanizado:** el ataque que la propia v2 nombra (goal sin sintoma grepeable) es
real y no tiene mitigacion completa. Aceptable si se declara: el gate solo puede ver lo que el
goal nombra. Que lo diga en el propio script, no en la propuesta.

---

## V3 -- Ataque de carrera a P6: **ROMPE CON ENMIENDA**

La precondicion 1 de P6 v2 ("`validate` verde post-commit sobre HEAD PUSHEADO") **no cierra la
carrera**, porque el maker valida un SHA y el checker clona una REFERENCIA. Entre el push del
maker y el clone del checker, cualquier commit del peer mueve `origin/main`, y el checker
verifica un arbol que nadie atesto. No es hipotetico: esta noche pushee `09652bc3` con el exec
de Codex vivo; un commit suyo en esa ventana habria hecho exactamente esto.

**Enmienda decisiva:** el HANDOFF debe **nombrar el SHA exacto que el maker valido**, y el
checker debe clonar ESE sha, no `origin/main`. Es la terna minima que este repo ya exige para
citar CI (run_id + job + head_sha) aplicada al handoff. Sin eso, P6 sustituye un gate humano
por un exit code sobre un objeto distinto del que se revisa.

Nota: el HANDOFF de Codex del 15-ago YA lo hacia bien ("route the independent review from
commit a5c5ad57"). El maker no es el eslabon debil aqui.

---

## V4 -- Ataque de coste oculto: **ROMPE CON ENMIENDA**

Asimetria estructural: **los beneficios de la propuesta caen en variables medidas (M1-M4,
mensajes, commits) y sus costes caen en variables NO medidas.** El preflight por GO, la linea
de justificacion por item de juicio, el campo `review_focus`, el computo del panel y la
auditoria del preflight por el checker no producen ni un mensaje ni un commit: son tiempo de
coordinador y tiempo de checker. El panel no puede ver su propio overhead, asi que P1 saldra
"gratis" por construccion.

**Enmienda: M9 = latencia ready->GO (tiempo de coordinador por encargo)**, derivable de los
sellos del ledger sin instrumento nuevo. Si P1 funciona, M9 sube y M4 baja; si M9 sube y M4 no
baja, P1 es ceremonia. Sin M9, P1 no es falsable.

---

## V5 -- Contrafactual del 15-ago completo: **SOSTIENE, y decide D1 sin esperar dos semanas**

Clasificados los ~21 commits de coordinacion de la ventana 15-ago 13:00 -> 16-ago 02:00:

    eliminables por P1 (defectos de intake mios):            4
        4a91f463 (AC5 insatisfacible)  0c577329 (alcance)
        704332b3 (bloqueo por ese alcance)  512c68d0 ("mi out_of_scope estaba mal")
    eliminables por sustrato 0337 cerrada (destrabes de residuo):  3
        09652bc3   41b54d2d   f6f58544
    irreducibles (GO, ruteo de review, done-flips, checkpoint, poda, registros):  ~14

**Semana 0 elimina ~7 de ~21 = 33 %.** P6 quitaria ~3 mas (los tres ruteos de review de la
ventana: 3558c948, f5619397, 44249e8d) = 14 %.

**Y el resultado que decide D1: P5 no elimina NADA en el dia medido.** Los ~14 irreducibles
son todos escrituras de `Area_comun/state/` o `runtime/state/` -- **tier 2 por la propia
definicion de P5**. Y las tres tareas revisadas (0392, 0395, 0396) tocan `scripts/` y
`examples/` = tier 1, que conserva review completa. La ceremonia que cuesta es ceremonia de
LEDGER, y el ledger esta fuera del alcance de P5 por decision de ambos.

**D1 se decide aqui: P5 se retira, sin pilotar.** No por debate, por aritmetica sobre el unico
dia con datos finos. Es el desenlace que la propia v2 preveia y que su metodo exige.

---

## V6 -- Ataque de compatibilidad: **ROMPE CON ENMIENDA**

- **P6 vs DECISION-0020 punto 6** (ninguna asercion de mailbox antes de que el ledger la
  respalde): **compatible**. El maker flipea a `in_review`, libera claim, pushea y ENTONCES
  emite el HANDOFF. El orden se conserva.
- **P1 vs el estado real de CI: incompatible en la secuencia propuesta.** El script
  `preflight_intake` entra al inventario de contratos de falsificacion
  (`check_falsification_contracts.py --inventory`), y este repo ya tiene la leccion
  "contratos declarados no son ejecutados". Con el job `validate` corriendo 6 de 86 pasos,
  **un gate nuevo se declara pero no se ejecuta, y nadie lo nota**. P1 no puede acreditarse
  antes del pin. Enmienda: la secuencia urgente de la seccion 6 es PRECONDICION de semana 0,
  no algo paralelo.
- **Evidencia en vivo de esta noche que lo confirma:** el exec de TASK-0337 aborto TRES veces
  y agoto su GO con dos errores de contrato -- uno propio nuevo
  (`retry-residue-scope-pair: declared mutation is not applied beside the test`) y otro
  **de TASK-0397, ya entregada** (`NEG-POWERSHELL-HOST-ASSUMPTION-CLASS: assertion boundary
  not found beside the test`). Un contrato roto de una entrega anterior mata el gate de la
  siguiente tarea. Eso es coste de sustrato que ni M1-M8 ni el panel v2 registran.
- **P1 vs DECISION-0038:** las lineas de justificacion en el GO caben en el carve-out
  (contenido sustantivo accionable). Sin conflicto.

---

## V7 -- Abogado del diablo sobre la secuencia urgente 0378: **ROMPE** (por C0)

La seccion 6 de la v2 esta construida sobre mi F1 erroneo, asi que su paso 4 ("rutear la
review de 0378 -- que nunca se ha ejecutado") describe algo que ya ocurrio. Secuencia
corregida:

    1. Rechazo formal de 0378 por el pin (AC8 el pin, AC9 el negativo).   [sigue valido]
    2. Codex remedia gancho + pin EN EL MISMO COMMIT, sobre r2 (a5c5ad57), sin revertirla.
    3. Rutear la RE-REVIEW que le debo a r2 desde 15-ago, ampliada al pin, sobre el commit
       que incluya AC8+AC9. Una sola pasada, no dos.
    4. Limpiar el retry.json: **innecesario** si el mensaje nuevo tiene id distinto -- la firma
       es `Name|Length|Ticks` y un nombre nuevo es una entrada nueva. Las dos entradas
       `defer_terminal` del 14-ago no tienen reintento programado (verificado). Se limpian por
       higiene, no por necesidad.

**Y un riesgo que introduce mi propio rechazo, contra mi:** al ampliar `scope_routes` de 0378
con `.github/workflows/validate.yml` agrando la superficie de colision de claims para la
re-review -- que es justamente la causa que la difirio 2h05m el 14-ago. Mitigacion inmediata:
rutear solo con cero claims activos sobre esas rutas. Mitigacion de fondo: **D-6**
(`scope_routes` a nivel de directorio), sin registrar todavia. Refuerza P2.

---

## Sintesis (ahora si, despues de los vectores)

| Pieza | v2 | Tras esta revision |
|---|---|---|
| E4 / clase del episodio 0378 | clase B, 48h | **clase C, mia, 47h de ruteo + 2h05m de sustrato** |
| Convergencia "dos diagnosticos" | reforzaba P2 | **una sola medicion con eco**; P2 sigue en pie por otras razones |
| M0 | semana 0, sin protocolo | **requiere trailer de actor = cambio de protocolo** |
| M5 | edad de in_review | **edad de handoff entregado sin review ruteada** |
| M7 | ratio | **ratio + contador absoluto con suelo por job** |
| M8 | tiempo diferido | **tiempo diferido QUE ACABA EN MUERTE, por causa** |
| M4 | autoclasificado | **derivado de git (`-L` sobre el intake tras el GO)** |
| M9 | no existe | **nueva: latencia ready->GO, o P1 no es falsable** |
| P5 | condicionada, pendiente de datos | **retirada: ahorro medido = 0 en el unico dia con datos** |
| P6 | precondiciones 1+2 | **+ el HANDOFF nombra el SHA y el checker clona ESE sha** |
| Secuencia urgente 0378 | 5 pasos | **corregida por C0: la review ya existio; lo que falta es la RE-review de r2** |
| P1, P2, P4, P7 | endosadas | **se sostienen**, con P1 subordinada al pin (V6) |

Lo que NO ataque por falta de instrumento y declaro como hueco: no medi la retro-linea-base de
2 semanas (requiere M0, que esta roto), asi que todo juicio sobre medianas fuera del 15-ago
sigue sin evidencia -- de ninguno de los dos lados.
