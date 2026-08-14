---
artifact_id: Analista-TASK-0368-r2-current-with-warning-verdict
task_id: TASK-0368
type: adversarial_review
author: Analista
status: final
created: 2026-08-14
verdict: CHANGE-REQUIRED
---

# Veredicto adversarial -- TASK-0368 remediacion 2 (la puerta de F3)

**CHANGE-REQUIRED.**

Respondo primero a tu pregunta, con la respuesta corta y la larga.

Corta: **solo se escribe.** `current_with_warning` no puede enrojecer nada. Los dos modos de
`check_memory_db_drift.py` meten `warnings` en un campo del JSON al lado de `"result":"pass"` y
devuelven 0; ninguna puerta del repo lee ese campo. Sobre el corpus real de `31867185` ya hay **229**
lineas de warning: una mas no es una senal, es una gota.

Larga, y es peor que tu sospecha: **`current_with_warning` no es el silencio de B3 mudado un nivel
mas abajo -- es el desague donde cae exactamente la familia que AC4 existe para cerrar.** La mitad
ruidosa que verificaste funciona, pero solo dispara para grafias que ALGUNA otra superficie ya tenia
registradas. Una grafia genuinamente nueva -- la tercera grafia del AC4, la que nadie declaro en
ningun sitio -- la tira `validate_metadata` aguas arriba, llega a la funcion de vigencia como `None`,
y entra por la rama de "ausente": **vigente, caliente, exit 0**.

Lo mostre de punta a punta sobre el corpus real, no en fixture: una decision con `status: retired`
pasa a ser la **decision vigente numero 109** con las dos puertas protocolares en verde.

Y hay un segundo hallazgo que no estabas mirando: **B5 no esta cerrado.** La frontera del puntero
sigue indefensa; el mutante que ignora `superseded_by` sobrevive las **73** pruebas de la suite
completa. El limite que el maker declara para esa frontera compara dos conjuntos sacados de
poblaciones distintas, asi que se cumple para cualquier implementacion.

---

## 1. Ancla canonica y reproduccion

| Elemento | Valor |
|---|---|
| Commit bajo revision | `31867185750f703ffef117947f889a949527f617` |
| HEAD del protocolo al revisar | `2c3e56f9e0d8fcaeed3256f76319ae22478a2724` |
| Alcance | SOLO hub (protocolo). Sin producto: no gateo `npm test`. |
| Clon limpio | `git clone -s -n <repo> clone && git checkout 31867185` |
| Raiz de scratch | `D:/Aegis_Scratch/protocol/0368r2/` (DECISION-0104) |
| Hora | 2026-08-14 03:10 local (UTC+2) |

### Las SEIS puertas del `verification_cmd`, por exit code, en el clon limpio

| # | Comando | Exit |
|---|---|---|
| 1 | `python scripts/memory/check_memory_db_drift.py --root . --fast` | **0** |
| 2 | `python scripts/memory/test_memory_db.py` (73 pruebas, 333 s) | **0** |
| 3 | `python scripts/validate_collaboration_state.py --root .` | **0** |
| 4 | `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | **0** |
| 5 | `python scripts/scan_encoding.py --root .` | **0** |
| 6 | `python scripts/scan_domain_neutrality.py --root .` | **0** |

**Seis de seis en verde.** Este veredicto no es "una puerta esta roja". Es "las puertas verdes no
prueban lo que su contrato promete". Confirmo tambien que la puerta 4 -- la que la vuelta anterior
dejo roja -- volvio a verde y declara `NEG-MEMORY-CURRENT-DECISION-PROPERTY boundaries=10`.

---

## 2. Tabla vector por vector

| Vector | Lo que declara la entrega | Veredicto | Evidencia |
|---|---|---|---|
| **B1** puerta de contratos | inventario exit 0, 10 fronteras | **PASS con reserva** | exit 0; 9 de las 10 discriminan, 1 es tautologica (ver 3.2) |
| **B2** `rejected` vivo | se ingiere, da `superseded`, `hot_required=0` | **PASS** | motor ve `'rejected'`; estado `superseded`; regla I4 respaldada por el MUERE exit 1; control `accepted` exit 0 |
| **B3a** grafia desconocida ruidosa | falla nombrando valor y ruta | **PASS parcial** | 4/4 grafias registradas mueren con `ValueError` que nombra valor Y ruta |
| **B3b** grafia AUSENTE | `current_with_warning` | **SLIP -- BLOQUEANTE** | 13/13 grafias no registradas -> `active`/HOT, CLI exit 0; e2e sobre corpus real: decision vigente #109 |
| **B4** contenido atestado pinado | quitar un miembro rompe el contrato | **PASS** | 9/9 miembros (6 no-vigentes + 3 vigentes) matan al negativo |
| **B5** frontera del puntero | el negativo mata al mutante pointer-only | **SLIP -- BLOQUEANTE** | mutante que ignora `superseded_by` en PRODUCCION sobrevive las 73 pruebas |
| **AC2** superficie atestada | el mapeo sale a la politica atestada | **PASS parcial** | las dos listas se consumen de verdad; `missing_status` no se desreferencia nunca (ver 3.3) |

---

## 3. Los tres hallazgos, falsables

### 3.1 -- BLOQUEANTE: la tercera grafia no llega a la rama ruidosa

**Mecanismo.** `validate_metadata` (`build_memory_db.py:860`) filtra `status` contra
`configured_status_values()`. Una grafia que no este en `CORE_STATUS_VALUES` ni en
`extra_status_values` ni en las dos clases de vigencia se **descarta** con el warning generico
`rejected frontmatter key status`, y no entra en `accepted`. Cuando `load_artifacts` llega al bloque
nuevo (`build_memory_db.py:970-982`), `metadata.get("status")` ya vale `None`, asi que cae en
`if status is None:` -- la rama de ausencia -- y **nunca** en el `elif ... not in classified: raise`.

El `raise` solo puede dispararse para una grafia que otra superficie ya registro: los 27 miembros de
`CORE_STATUS_VALUES` mas los 8 de `extra_status_values`, menos los 9 clasificados = **26 grafias**
que ahora mueren ruidosamente. Todas ellas son estados de TAREA que una decision tomo prestados. El
conjunto que sigue pasando en silencio -- las grafias que nadie registro -- es **ilimitado**, y es
justo donde nace una palabra nueva de retirada.

**Medido (fixture, familia completa, no un ejemplo):**

    grafia               motor ve      policy_state   caliente?
    retired              None          active         HOT
    obsolete             None          active         HOT
    withdrawn            None          active         HOT
    deprecated           None          active         HOT
    revoked              None          active         HOT
    expired              None          active         HOT
    void                 None          active         HOT
    inactive             None          active         HOT
    derogada             None          active         HOT
    no-longer-current    None          active         HOT
    supersedida          None          active         HOT
    closed               None          active         HOT
    historical           None          active         HOT

    13 reglas hot/cold respaldadas por esas 13 decisiones retiradas:
    check_memory_db_drift.py --fast  ->  exit 0
    {"active_decision_count":13, "result":"pass", "rule_count":13, ...}

**Medido (corpus real, extremo a extremo).** En un clon de `31867185` anadi un solo fichero,
`Area_comun/decisions/DECISION-9999-probe-retired.md`, con `status: retired`, y lo commitee:

    python scripts/memory/check_memory_db_drift.py --root . --fast   exit 0
      result=pass  active_decision_count=109  (era 108)  rule_count=0
    python scripts/validate_collaboration_state.py --root .          exit 0
      OK: collaboration state is valid.

    unica huella, 2 lineas entre 231 warnings:
      DECISION-9999-probe-retired.md: rejected frontmatter key status
      DECISION-9999-probe-retired.md: decision currentness status is missing;
                                      attested policy treats it as current

Verifique ademas que **ninguna otra puerta del repo restringe el `status` de una decision**:
`validate_collaboration_state.py` no tiene enum de estado de decision y no existe ningun
`decision_status` en `scripts/`. No hay red debajo.

**Por que esto es fail-open y no una minucia.** Para I4 la ausencia de estado se lee como vigencia:
una regla hot/cold respaldada por una decision retirada-en-grafia-nueva se habilita. Para I7 y s.8
Q3, cuando F2/F3 enciendan el enfriado, esa decision se queda caliente por una razon falsa. La forma
del defecto es la del original: **el instrumento decide por una lista, y lo que la lista no nombra
entra por la puerta buena**. La remediacion estrecho el dano -- de 0 grafias ruidosas a 26 -- sin
cambiar la clase.

**Nota justa sobre el AC4.** El negativo del maker si prueba una tercera grafia
(`future-vocabulary`), pero la registra antes en `policy["extra_status_values"]`. Por eso su probe
llega viva a la rama del `raise`. Una grafia real que nazca manana no lleva ese pasaporte.

### 3.2 -- BLOQUEANTE: B5 sigue abierto; su frontera es una tautologia

La entrega declara: *"el negativo ejecuta el mutante pointer-only y prueba que su poblacion caliente
difiere"*. La frontera es `self.assertNotEqual(hot, mutant_hot)`. Los dos conjuntos no salen de la
misma poblacion:

    cited (poblacion de `hot`)      n=16     ids DECISION-#### citados por el AGENTS.md vivo
    hot                            n=16     subconjunto de `cited`
    mutant_hot (poblacion = TODAS) n=21     todas las decisiones del fixture sin puntero
    mutant_hot - hot  = [DECISION-ACCEPTED, DECISION-FUTURE, DECISION-PROPOSED,
                         DECISION-REJECTED, DECISION-RETIRED]
    hot - mutant_hot  = []
    decisiones CITADAS que llevan superseded_by = []

La desigualdad la sostienen las 5 decisiones sinteticas que `hot` no puede contener nunca, porque
`hot` esta restringido a `cited`. El puntero no quita nada de `hot` (`hot - mutant_hot = []`) y
ninguna decision citada lleva puntero. Recalculado con un motor **ciego al puntero**:
`hot` identico (n=16), `assertEqual(cited, hot)` pasaria, `assertNotEqual(hot, mutant_hot)` pasaria.
La frontera se cumple para **cualquier** implementacion de `decision_policy_state`.

**Mutante sobre PRODUCCION** (no sobre el mutante del runner), en `build_memory_db.py:1198`:

    -   if value_list(metadata.get("superseded_by")) or declared_non_current
    +   if declared_non_current

    python scripts/memory/test_memory_db.py   ->  Ran 73 tests ... OK   exit 0

El motor deja de mirar la supersesion por completo y **la suite entera pasa**. Contraste con el
control: el mutante espejo (ignorar la clase de estado, `declared_non_current = False`) SI muere
(exit 1) -- lo matan los tres `assertEqual("superseded", rows[...])`. Es decir: la frontera de
ESTADO esta defendida por asertos explicitos; la del PUNTERO no la defiende nadie.

Bateria completa contra el runner declarado (`test_current_decision_is_attested_property_not_status_literal`):

    M0 control (sin mutar)                                  exit 0
    M1 clase de estado ignorada (motor pointer-only)        exit 1   MUERE
    M2 puntero de supersesion ignorado                      exit 0   SOBREVIVE
    M3 vocabulario no clasificado aceptado en silencio      exit 1   MUERE
    M4 politica: quitar no_vigente {rejected|proposed|archived|
       cancelled|draft|superseded}                          exit 1   MUERE (6/6)
    M5 politica: quitar vigente {accepted|active|approved}  exit 1   MUERE (3/3)
    M6 politica: missing_status -> 'non_current'            exit 1   MUERE
    M7 motor: status ausente -> no vigente                  exit 0   SOBREVIVE

M4 y M5 acreditan B4 sin reserva: el contenido embarcado esta pinado de verdad, miembro a miembro.

### 3.3 -- `missing_status` es un literal pinado, no un mecanismo

`"missing_status": "current_with_warning"` aparece cinco veces en el repo: en la politica, en el
fallback, en el `set()` de forma, en la comparacion de igualdad y en el `expected_` del test. **Nunca
se desreferencia**: `mapping["missing_status"]` no existe en el codigo. `decision_policy_state`
devuelve `mapping["current"]` para el ausente sin consultarlo.

Consecuencia medida (M7): invertir la conducta del motor -- ausente pasa a NO vigente -- deja la
politica atestada diciendo `current_with_warning` y la suite de 73 pruebas en verde. El texto
atestado y la conducta pueden divergir sin que nada lo note. Es un falso-seguro: parece que el
tratamiento del ausente esta bajo la superficie atestada de AC2, y no lo esta. Las dos listas si lo
estan (B4 lo prueba); este tercer campo no.

---

## 4. Alcance del dano HOY (para que nadie lo infle ni lo minimice)

Sobre `31867185`: `rule_count = 0`, asi que I4 no tiene sobre que fallar; `active_decision_count = 108`
y la unica decision sin `status` del corpus es `DECISION-0059`, que es legitimamente vigente. **No hay
ninguna decision viva mal clasificada hoy.** Los tres hallazgos son **latentes**.

Y repito mi acotacion de la vuelta anterior, que sigue siendo el marco: *un corpus limpio es
exactamente la condicion bajo la cual el defecto original tambien parecia inofensivo.* El censo
106/4 tampoco dolia hasta que alguien miro que decisiones eran las 106.

---

## 5. Residuales declarados (no bloqueantes, no los cuento en el veredicto)

- El mutante literal y el pointer-only son **re-implementaciones** en el test (lambdas), no mutaciones
  de produccion. Es el patron establecido en esta instancia; lo anoto porque 3.2 muestra su coste:
  un mutante escrito a mano puede quedar verde por construccion.
- El aserto `assertNotEqual(cited, literal_mutant_hot)` compara tambien poblaciones distintas. Codifica
  el defecto historico y hoy discrimina, pero es de la misma familia debil que 3.2.
- 229 warnings en el corpus real. Cualquier senal nueva que se emita por ese canal nace enterrada.
- No corri `check_memory_db_drift --full`: no esta en el `verification_cmd` de la tarea.

---

## 6. Veredicto y lazo de correccion

**CHANGE-REQUIRED.** Dos bloqueantes abiertos (3.1, 3.2) y un falso-seguro (3.3).

Lo que aceptaria como cerrado, por conducta y no por forma:

1. **3.1** -- Una decision cuyo `status` no este registrado en NINGUNA superficie debe hacer salir
   con exit distinto de 0 a alguna de las seis puertas del `verification_cmd`. El mecanismo es del
   maker (clasificar sobre el frontmatter CRUDO antes del filtro de allowlist es lo evidente, pero no
   me corresponde disenarlo). Prueba de aceptacion: el probe e2e de 3.1 -- un fichero de decision con
   `status: retired` sobre el corpus real -- debe dar rojo.
2. **3.2** -- La frontera del puntero debe tener un limite cuyos dos lados salgan de la **misma**
   poblacion. Prueba de aceptacion: el mutante M2 sobre produccion (quitar el termino
   `value_list(metadata.get("superseded_by")) or`) debe poner rojo al runner declarado.
3. **3.3** -- O el motor desreferencia `missing_status` y la politica atestada decide de verdad, o el
   campo sale de la politica. Prueba de aceptacion: M7 debe poner rojo.

**Puertas afectadas:** las seis del `verification_cmd`; la 2 y la 4 son las que deben cambiar de
signo bajo los mutantes.

**Lazo declarado:** remediacion -> re-juicio mio ANTES del commit de cierre -> maximo 2 iteraciones
antes de escalar al operador humano.

**Aviso de gobierno, que decides tu y no yo:** tu propio mensaje fijo dos vueltas como techo y esta
era la segunda. Por tu regla, esto es el punto de escalada, no una cuarta vuelta. Doy el dato que te
falta para decidirlo: los tres arreglos son pequenos y mecanicos -- una reordenacion del filtro, un
aserto reescrito sobre la poblacion correcta y un `mapping[...]` -- ninguno toca el criterio de AC1,
que **si esta bien planteado y bien implementado**. La propiedad es la correcta; lo que falla es la
frontera por donde entra el vocabulario.

-- Analista, 2026-08-14 03:10 local (UTC+2)
