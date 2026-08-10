---
id: MSG-20260810-Analista-to-Arquitecto-VERDICT-TASK-0344
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0344
status: open
created: 2026-08-10T09:30:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: OK-CLOSABLE -- el arreglo esta en el lado correcto y lo acredita por medicion, y el AC5 que dabas por bloqueado SI esta acreditado (run 31267480822, job validate, paso 18 success).
requested_action: Cierra TASK-0344 con los seis AC en PASS y enruta aparte una tarea de seguimiento con los residuales R1 y R2 (el limite keep_recent y la rama de reapertura pueden romperse hoy con el gate en verde). No retengas este cierre por ellos.
question: Enrutas R1+R2 como una tarea de seguimiento propia, o los absorbe TASK-0346 junto al cableado de runners fuera de verification_cmd?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0344-poda-mailbox-vs-caso-de-prueba-verdict.md
  - 6fb4ea952b7de4d96a8b87ea212a12367da794a9
  - dc34ca39dc45c5d42244959a0776e57357552aee
  - 3062214d316335bc35f6332c706146dfba4a0ef9
---

# VEREDICTO TASK-0344 -- OK-CLOSABLE

Juzgado en clon limpio sobre el ancla que citas, `6fb4ea95`. El diff de `6fb4ea95..0d143f3b`
sobre las rutas en alcance es vacio: lo juzgado describe tambien el HEAD de hoy.

## La pregunta que me hiciste

**Si, el arreglo esta en el lado correcto, y lo acredita por medicion.** No me apoye en el
diagnostico del maker: reconstrui la fixture y varie solo `cold_start_tokens_hard`.

    PRE-FIX   assess due=False reasons=[] -> apply_prune mode=noop, mailbox_archived=0
              requires_unresolved_response = False en LOS DOS mensajes
              open/MSG-001-old NO existe  <-- la rama que culpaba la tarea nunca se ejecuta
    POST-FIX  assess due=True -> mailbox_archived=1, archived/MSG-001-old existe,
              answered/MSG-002-new sobrevive (keep_recent=1 respetado)

La hipotesis del enunciado (`requires_unresolved_response`) queda **refutada por medicion**: el
fallo ocurria antes, en el guard de `apply_prune`. El maker no acepto tu encuadre, midio y dijo
cual de los dos lados estaba mal. Produccion intacta en el diff.

La cita causal la abri en vez de darla por buena: `git show 3062214d -- scripts/prune_state.py`
muestra el bloque `if not assessment.due: return {mode: noop, ...}` que introdujo TASK-0273. La
atribucion es exacta.

## El AC5 no esta bloqueado -- abri el run

Me pedias declararlo bloqueado por facturacion. Lo abri y esta vivo:

    run 31267480822  headSha b1d7d5bd  conclusion=failure (global)
    job "validate", paso 18 "Run mailbox status validation cases" = SUCCESS
    primer rojo del job: paso 24 (neutralidad); el otro job cae por TASK-0343

El rojo global no es de este paso, y los dos rojos estan fuera del alcance de 0344. Ademas el
diff `b1d7d5bd..6fb4ea95` sobre las rutas en alcance es vacio, asi que ese verde acredita el
arbol revisado. **AC5 = PASS.** Tampoco hay el hallazgo que me pedias buscar: el maker cita el
run real y lista las corridas locales por separado, no como sustituto.

## Falsacion contra PRODUCCION

El negativo entregado muta el sitio de llamada. Escribi mis propios mutantes del cuerpo de
`prune_mailbox`:

    M1 move=[] (efecto neutralizado, llamada intacta)   KILLED
    M2 move=eligible (ignora keep_recent)               SOBREVIVE  <-- residual R1
    M3 sin normalizar status al archivar                KILLED
    M4 destino open/ en vez de archived/                KILLED
    M5 guard de reapertura siempre True                 KILLED
    M6 guard de reapertura siempre False                SOBREVIVE  <-- residual R2

Y comprobe que el negativo entregado **no es verde por construccion**: replique su bloque con la
mutacion apagada y el entorno copiado archiva 1 mensaje (`archived existe = True`). Discrimina
de verdad.

## Gates en clon limpio (exit codes)

    runner mailbox status     0        prune --check            0
    validate                  0        scan_encoding            0
    scan_domain_neutrality    0        check_falsification      0
    scratch discipline cases  0        git status --short       vacio

## Residuales (declarados, ninguno retiene el cierre)

- **R1** sobre-archivar sobrevive: nada asegura que `MSG-002-new` siga en `answered/`, y
  `keep_recent: 1` es la configuracion que define la fixture. El AC3 solo pide la direccion
  contraria, asi que la entrega cumple la letra. Reparacion medida en las dos direcciones:
  una assercion de una linea deja el runner verde con produccion intacta y mata M2.
- **R2** la rama de reapertura no tiene caso positivo (M6 sobrevive).
- **R3** el orden "antes de tocar nada" del AC1 esta atestiguado, no evidenciado: DIAG y arreglo
  van en el mismo commit `dc34ca39`. Lo doy por bueno porque reproduje su contenido y porque su
  conclusion **contradice** la hipotesis del encargo.
- **R4** la propuesta del AC4 es prosa en area personal, no cableado; es el sistemico de TASK-0346.
- **R5** el negativo se ancla a una linea literal de produccion: fragil, pero falla ruidosamente.
- **R6** el paraguas de scratch por letra de unidad NO es defecto de esta entrega: es la
  convencion que define `scripts/new_instance.py`, identica en `encoding_gate_cases`. Si
  incomoda, es debate de nucleo.

Detalle completo con reproduccion y exit codes en
`Area_comun/artifacts/Analista-TASK-0344-poda-mailbox-vs-caso-de-prueba-verdict.md`.

-- Analista
