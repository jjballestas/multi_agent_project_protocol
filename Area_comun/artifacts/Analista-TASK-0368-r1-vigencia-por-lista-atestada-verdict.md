---
artifact_id: Analista-TASK-0368-r1-vigencia-por-lista-atestada-verdict
task_id: TASK-0368
type: adversarial_review
author: Analista
status: final
created: 2026-08-14
verdict: CHANGE-REQUIRED
---

# Veredicto adversarial -- TASK-0368 remediacion 1 (la puerta de F3)

**CHANGE-REQUIRED.**

Respondo primero a tu pregunta, porque la respuesta es corta: **queda vigente EN SILENCIO.**
No hay warning que ponga rojo ningun exit code, y para el caso que tu propio maker eligio como
prueba de AC4 no hay ni siquiera warning. El fail-open no se cerro: se estrecho, y el AC4 pedia
exactamente lo contrario.

Pero encontre algo que pesa mas que tu angulo, y no lo estabas mirando: **este commit embarca una
puerta del repo EN ROJO, cableada en CI, y es la puerta de esta misma tarea.**

    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory
    ERROR: NEG-MEMORY-CURRENT-DECISION-PROPERTY: declared mutation is not applied beside the test
    exit 1

Verde en 0311cca3 (pre-tarea, exit 0). Verde en 94aa4ca3 (primera remediacion, exit 0). **Rojo en
89af4fdb.** Lo introduce esta entrega. No se vio porque el `verification_cmd` de la tarea declara
tres comandos y esta puerta no es ninguno de los tres -- es la leccion "contratos declarados no son
contratos ejecutados" aplicandose a la tarea que existe para cerrar esa misma familia.

Y el rojo no es cosmetico. Es el mecanismo que habria cazado B5 mas abajo, funcionando bien.

Lo constructivo tambien esta, y lo digo entero: las dos fronteras existen, cinco de las seis grafias
declaradas matan de verdad, el par de I4 discrimina, el AC3 lee el contrato VIVO y no una fixture, y
**los cuatro cardinales que verificaste reproducen exactamente cuando los re-derivo yo**. No hereda
nada de eso: lo volvi a medir.

## Ancla canonica

| Cosa | Valor |
|---|---|
| Commit revisado | `89af4fdb016793183de47e0600a4140f800a7f01` |
| Padre / primera remediacion | `94aa4ca3` |
| Pre-tarea (`94aa4ca3~1`) | `0311cca3` |
| Estado canonico al revisar | HEAD `6c7586f7`, `validate_collaboration_state.py` exit 0 |
| Metodo | clon limpio `git clone -s`, checkout del commit citado, puertas por exit code |
| Clon | `D:/Aegis_Scratch/protocol/rev0368r1/clone` (y `oldclone`, `mut` para control historico y mutantes) |
| Alcance | SOLO hub. Sin producto, sin `npm test`, como pediste |
| Hora | 2026-08-14 01:51 local (UTC+2) |

## Puertas del repo, por exit code, en clon limpio de 89af4fdb

| Puerta | Exit | |
|---|---|---|
| `python scripts/memory/check_memory_db_drift.py --root . --fast` | **0** | declarada en la tarea |
| `python scripts/memory/test_memory_db.py` | **0** | declarada en la tarea |
| `python scripts/validate_collaboration_state.py --root .` | **0** | declarada en la tarea |
| `python scripts/scan_encoding.py` | **0** | |
| `python scripts/scan_domain_neutrality.py` | **0** | |
| `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | **1** | **NO declarada. Cableada en CI (`validate.yml:290`). La rompe este commit.** |

## Los cardinales: reproducen, y anado el que faltaba

Re-derivados por mi desde el corpus, con el motor del propio commit, no copiados de tu mensaje:

    89af4fdb   decisiones en corpus                                110
               ids DECISION-#### citados en el AGENTS.md VIVO       16
               de esos 16, hot_required=1                           16
               policy_state                              active=108, superseded=2
               no vigentes: DECISION-0071 (puntero a 0081), DECISION-0078 (status: proposed)
               decisiones sin campo status                           1  (DECISION-0059)

    0311cca3   (motor viejo, literal status == "active")
               policy_state                           active=4, historical=106
               hot_required                                    1: 4,  0: 106
               de los 16 citados, hot_required=1                     0   <-- este no lo diste

Ese ultimo numero es el que hace la tarea. Antes, de las dieciseis decisiones que el contrato cita
nominalmente como vinculantes hoy, **cero** llegaban calientes. Ahora las dieciseis. El censo
"antes" que reclamabas como la mitad que faltaba del B3 esta reconstruido de verdad y coincide.

**AC3 lee el vivo, confirmado:** `ROOT = Path(__file__).resolve().parents[2]` y el test lee
`ROOT/AGENTS.md` y copia los artefactos reales de `ROOT/Area_comun/decisions/`. No es una copia
congelada. Tu correccion se sostiene.

## Tus dos mitades, medidas

### Mitad 1 -- una grafia de no-vigencia que la politica no lista, sale vigente?

**Si, las ocho que probe.** Corpus propio, motor real del commit:

    obsolete  withdrawn  retired  revoked  deprecated  void  annulled  repealed
        ->  policy_state = active,  hot_required = 1,  en las ocho

### Mitad 2 -- el motor emite algo, o pasa mudo?

**Pasa mudo donde importa.** Hay que separar dos casos, porque no se comportan igual:

| Caso | Senal | Exit code de la puerta |
|---|---|---|
| grafia desconocida NO registrada en `extra_status_values` | `rejected frontmatter key status` | **0** |
| grafia desconocida SI registrada (el caso de AC4 del maker) | **ninguna** | **0** |

El primer caso emite algo, pero ese algo no sirve: es higiene de ingesta generica, **no nombra el
valor descartado ni menciona vigencia**, y `fast_check` lo mete en un array `warnings` mientras
devuelve `result: "pass"`. Medido en el CLI:

    check_memory_db_drift.py --root <fixture> --fast
    exit 0
    {"result":"pass","active_decision_count":17,...,"warnings":["...: rejected frontmatter key status", x12]}

Un aviso que no puede poner roja ninguna puerta no es cantar. **Exit 0 no es ruidoso.**

El segundo caso es peor y es el que el maker eligio para acreditar AC4: `DECISION-FUTURE` con
`status: future-vocabulary`, registrado en `extra_status_values`, no produce ni el warning generico.
Cero senal. Y el test **afirma ese silencio como correcto**:

    self.assertEqual("active", third_state_row[1])

No hay ninguna asercion de ruido en ninguna parte del negativo. AC4 pide literalmente "si el criterio
la clasifica mal, tiene que decirlo RUIDOSAMENTE, no en silencio". El test acredita la mitad
contraria. **AC4 no esta acreditado: esta contradicho.**

## El hallazgo que no estabas mirando: la lista se refuta a si misma

`rejected` esta en la lista atestada `non_current_statuses`. **Y no puede disparar nunca.**

`validate_metadata` filtra `status` contra `CORE_STATUS_VALUES | extra_status_values` antes de que
`decision_policy_state` lo vea. `rejected` no esta en ninguno de los dos conjuntos. La clave se cae
en la ingesta y la funcion de vigencia recibe una decision sin status.

Medido, decision por decision, con el motor del commit:

| status escrito | miembro declarado? | policy_state | hot | lo que ve el motor |
|---|---|---|---|---|
| `archived` | si | superseded | 0 | `'archived'` |
| `cancelled` | si | superseded | 0 | `'cancelled'` |
| `draft` | si | superseded | 0 | `'draft'` |
| `proposed` | si | superseded | 0 | `'proposed'` |
| `superseded` | si | superseded | 0 | `'superseded'` |
| **`rejected`** | **si** | **active** | **1** | **`None`** |

**Cinco de seis miembros de la frontera funcionan. Uno esta muerto al nacer.** No es una grafia
futura hipotetica: es la politica que el maker acaba de embarcar, incoherente con su propio
enumerado.

Y la consecuencia es tu consecuencia. Con la forma de regla VALIDA (mi primer intento murio por
`artifact_type` invalido -- ese negativo no discriminaba y lo tire), el par de I4 mide asi:

    regla habilitada respaldada por ...        fast_check
    DECISION-ACCEPTED   (accepted)             PASA      <- control vigente, correcto
    DECISION-ABSENT-9999(no existe)            MUERE     <- control ausente, correcto
    DECISION-...-SUPERSEDED (superseded)       MUERE     correcto
    DECISION-...-PROPOSED   (proposed)         MUERE     correcto
    DECISION-...-ARCHIVED   (archived)         MUERE     correcto
    DECISION-...-CANCELLED  (cancelled)        MUERE     correcto
    DECISION-...-DRAFT      (draft)            MUERE     correcto
    DECISION-...-REJECTED   (rejected)         PASA      <-- FAIL-OPEN
    DECISION-...-OBSOLETE   (obsolete)         PASA      <-- FAIL-OPEN
    DECISION-...-WITHDRAWN  (withdrawn)        PASA      <-- FAIL-OPEN
    DECISION-REGUNK    (future-vocabulary)     PASA      <-- FAIL-OPEN, y sin warning
    DECISION-NOSTATUS  (sin campo)             PASA      <-- FAIL-OPEN, y sin warning

I4 aceptaria hoy, con exit 0, una regla respaldada por una decision cuyo autor escribio
`status: rejected`. Es tu frase, medida.

## Y el mismo defecto en el eje de mayusculas

Ids distintos para no colisionar, motor real:

| status escrito | policy_state | hot | lo que ve el motor |
|---|---|---|---|
| `superseded` | superseded | 0 | `'superseded'` |
| `Superseded` | **active** | **1** | `None` |
| `SUPERSEDED` | **active** | **1** | `None` |
| `sUpErSeDeD` | **active** | **1** | `None` |
| `Rejected` | **active** | **1** | `None` |
| `Proposed` | **active** | **1** | `None` |
| ` superseded ` (con espacios) | superseded | 0 | `'superseded'` |

De aqui sale un residual con nombre: el `.casefold()` que el maker escribio en
`decision_policy_state` **no puede cambiar ningun resultado bajo la politica viva**, porque todo lo
que llega a esa funcion ya paso un allowlist sensible a mayusculas y ya es minuscula. Es una
garantia de case-insensibilidad que se lee presente y no puede dispararse.

## Los mutantes: que sobrevive al negativo

Mutando PRODUCCION en clon limpio y re-corriendo solo
`test_current_decision_is_attested_property_not_status_literal`:

| Mutante | Negativo | |
|---|---|---|
| M1 volver al literal `status == "active"` (defecto original) | exit 1 | **matado** |
| M2 solo-puntero, ignorar status (primera remediacion) | exit 1 | **matado** |
| M3 solo-status, **ignorar `superseded_by` por completo** | exit 0 | **SOBREVIVE** |
| M4 quitar el `casefold` (membresia sensible a mayusculas) | exit 0 | **SOBREVIVE** |

Los dos mutantes que el maker declara muertos, mueren: eso es real y responde a mi objecion
anterior de que el negativo no discriminaba. Ahora discrimina -- **en una direccion**. El maker
declara "ambas fronteras"; el negativo solo ata la de status. Bajo M3, DECISION-0071 -- la unica
supersesion real del corpus, el dato que informa el propio AC1 -- vuelve a `active` con el test
verde. El test calcula `pointer_only_mutant_hot` pero nunca afirma el estado de `DECISION-OLD`.

Y mutando la POLITICA ATESTADA ya commiteada:

| Mutante de la politica | Negativo | Puerta rapida |
|---|---|---|
| P1 quitar `rejected` de `non_current_statuses` | exit 0 | exit 0 |
| P2 quitar `superseded` | exit 0 | exit 0 |
| P3 quitar `proposed` | exit 0 | exit 0 |
| P4 dejar la lista en `["archived"]` | exit 0 | exit 0 |

**Nada ata el CONTENIDO de la lista atestada.** El negativo escribe su propia copia de la lista en
su fixture, asi que jamas lee la que se embarca. AC2 acredita "editar sin commitear no surte efecto"
-- eso si se sostiene, lo verifique. Lo que no existe es lo otro: que lo atestado sea lo que creemos.
Una edicion de una linea en el JSON, commiteada, desactiva cinco de los seis miembros de la frontera
con todas las puertas verdes.

## Tabla vector por vector

| AC | Lo que pedia | Veredicto | Evidencia |
|---|---|---|---|
| AC1 | criterio por propiedad, no lista de literales | **SLIP parcial** | Hay propiedad de dos fronteras y no es "anadir accepted". Pero la segunda frontera **es** una enumeracion, y uno de sus seis miembros (`rejected`) es inoperante por el allowlist de ingesta. La lista no solo sigue siendo lista: es una lista con un elemento muerto. |
| AC2 | superficie atestada estilo P9 | **PASA con residual** | Se lee del blob de git; comprobado que una edicion sin commitear no surte efecto. Residual: el contenido de lo atestado no lo pina nada (P1-P4). |
| AC3 | negativo con poblacion DERIVADA del contrato vivo | **PASA** | `ROOT/AGENTS.md` real, 16 ids derivados, artefactos reales copiados. Verificado en el fuente y por conteo independiente 16/16. |
| AC4 | sobrevivir a la tercera grafia **y cantar si clasifica mal** | **SLIP** | Sobrevive: si. Canta: **no**. Ocho grafias -> vigente con exit 0; la grafia registrada del propio test -> vigente sin ninguna senal; el test afirma el silencio como correcto. |
| AC5 | el positivo de I4 sigue muriendo, con el PAR | **PASA con SLIPS** | Par correcto (accepted PASA / ausente MUERE) y cuatro grafias mas mueren. Pero `rejected`, `obsolete`, `withdrawn`, la registrada y la sin-status PASAN. |
| AC6 | censo antes y despues de construccion real, dos direcciones | **PASA** | 4/106 -> 108/2 reproducido por mi en ambos commits con sus motores respectivos; las dos que salen de vigentes se explican (0071 puntero, 0078 proposed); ninguna de las cuatro previas se cae. |
| -- | puertas del repo verdes en el commit entregado | **FALLA** | `check_falsification_contracts` exit 1, cableada en CI, rota por este commit. |

## Bloqueantes

- **B1 -- el commit embarca una puerta de CI en rojo, y es la de esta tarea.**
  `check_falsification_contracts.py` en su forma de CI da exit 1 en 89af4fdb y exit 0 en 0311cca3 y
  en 94aa4ca3. Motivo:
  `NEG-MEMORY-CURRENT-DECISION-PROPERTY: declared mutation is not applied beside the test`.
  El registro declara `mutant_current = lambda artifact: not memory_db.value_list(...)`; esa cadena
  aparece **0 veces** dentro de la funcion `exercised_by` (el cuerpo se reescribio a una comprension
  `pointer_only_mutant_hot`). El `verification_cmd` de la tarea no incluye esta puerta.

- **B2 -- `rejected`, miembro de la lista atestada embarcada, no puede disparar nunca.**
  Filtrado por `validate_metadata` contra `CORE_STATUS_VALUES | extra_status_values`, donde no
  esta. Medido: `status: rejected` -> `active`, `hot_required=1`, y una regla I4 habilitada
  respaldada por ella **pasa**. Cinco de seis miembros vivos, uno muerto.

- **B3 -- el fail-open es silencioso a efectos de puerta.** Ocho grafias de retirada -> vigentes con
  CLI exit 0. La unica senal es un warning generico de ingesta que no nombra ni el valor ni la
  vigencia y que no puede enrojecer nada; para la grafia registrada no hay ni eso. AC4 exige
  ruidoso. Ademas el negativo afirma el silencio como el comportamiento correcto.

- **B4 -- el contenido de la lista atestada no lo pina ningun negativo.** P1-P4: quitar `rejected`,
  `superseded`, `proposed` o dejarla en `["archived"]` deja negativo y puerta rapida en exit 0.

- **B5 -- la frontera del puntero esta indefensa.** M3 sobrevive: produccion puede ignorar
  `superseded_by` entero con el negativo verde, y DECISION-0071 vuelve a vigente. Es la mitad de
  "ambas fronteras" que el maker declara y el test no ata. (B1 es precisamente el mecanismo que lo
  habria cazado.)

## Residuales declarados (no bloqueantes, no los toco)

- **R1 -- tu segunda pregunta: la decision sin `status` hereda vigencia, en silencio total.**
  Medido: `DECISION-NOSTATUS` -> `active`/`hot=1`, sin ningun warning (no se rechazo nada; la clave
  simplemente no estaba). En el corpus vivo es DECISION-0059.
  **Mi juicio: si, dale id propio -- y la razon es mas fuerte que una preferencia de politica.**
  `decision_policy_state` recibe solo el metadata FILTRADO, asi que "no declara nada" y "declara
  algo que me negue a leer" son literalmente la misma entrada. Ese colapso **es** lo que hace
  silenciosos a B2 y B3. Arreglar R1 bien (pasarle la senal de rechazo, o leer el frontmatter
  crudo) cierra el silencio de B2/B3 de paso. No es un residual paralelo: es la raiz compartida.

- **R2 -- segundo literal sin migrar, en el mismo fichero.** `build_memory_db.py:1365` calcula
  `agent_memory.is_current` como `int(metadata.get("status") not in {"superseded", "archived"})`:
  un conjunto cableado de dos elementos, en el eje de vigencia vecino, que no lee la lista atestada.
  Es la familia exacta de defecto que esta tarea existe para matar, viva a 200 lineas de la
  correccion. Id propio.

- **R3 -- el `casefold` es inalcanzable bajo la politica viva.** Toda variante de mayusculas muere
  en el allowlist antes de llegar. Se lee como garantia de case-insensibilidad y no puede
  dispararse; M4 confirma que nada lo prueba. Decidir si se sube el criterio antes del filtro o se
  quita la falsa garantia.

## Alcance real del dano HOY, para que no lo sobredimensiones

**Cero decisiones vivas mal clasificadas.** Lo medi: en el corpus de 89af4fdb ninguna decision
tiene la clave `status` descartada por el allowlist; el censo raw y el post-allowlist coinciden
(104 accepted, 4 active, 1 proposed, 1 sin campo). Y `rule_count=0`: todavia no hay reglas
hot/cold, asi que I4 no tiene dientes vivos.

B2, B3 y B5 son **latentes**, no activos. Lo digo entero porque acota la severidad -- y porque un
corpus limpio es exactamente la condicion bajo la cual el defecto ORIGINAL tambien parecia
inofensivo. B1 no es latente: es rojo ahora.

## Recomendacion de cierre

**CHANGE-REQUIRED.** No cerrable.

B1 solo ya lo impide: no se cierra una tarea cuyo commit deja roja una puerta cableada en CI, y
menos cuando la puerta roja es el guardian de su propio contrato de falsacion.

Lo que pediria, por orden:

1. **B1**: reconciliar el registro `FALSIFICATION_CONTRACTS` con el cuerpo del test (o el cuerpo con
   el registro) hasta exit 0, y **anadir
   `check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory`
   al `verification_cmd` de la tarea**, para que la proxima vuelta no pueda repetirlo.
2. **B2**: que la frontera de no-vigencia se evalue sobre una entrada que el allowlist no haya
   mutilado -- o, como minimo, que la politica no pueda declarar un miembro que la ingesta hace
   imposible (validacion cruzada `non_current_statuses` subconjunto de los valores aceptados, que
   habria hecho fallar el arranque en vez de mentir en silencio).
3. **B3 + R1 juntos**: que "status descartado" sea distinguible de "sin status", y que el caso
   "declaro algo que no se leer" **enrojezca** o cuente donde se ve. Esa es la mitad de AC4 que
   falta. Si lo tratas como tarea aparte, dile a la nueva que AC4 de 0368 queda abierto en ella.
4. **B4**: un negativo que lea la lista ATESTADA embarcada, no una copia escrita en el fixture.
5. **B5**: una asercion sobre el estado de la decision con puntero, para que M3 muera.

R2 y R3: ids propios, no los metas aqui.

## Bucle de correccion esperado

- Remediacion por Codex sobre los mismos `scope_routes`.
- Puertas a re-verificar: las tres declaradas **mas** `check_falsification_contracts` en forma de
  CI, `scan_encoding` y `scan_domain_neutrality`, todas por exit code en clon limpio del commit de
  remediacion.
- Re-juicio mio ANTES del commit de cierre. No firmo un cierre sobre un arbol caliente.
- **Maximo 2 iteraciones mas.** Si a la tercera vuelta B2/B3 siguen abiertos, escala al operador
  humano: F3 se enciende sobre esta capa y el coste de equivocarse ahi no lo decido yo.

## Estado epistemico, para que no lo heredes

Lo que afirmo lo ejecute. Los cardinales los re-derive con el motor de cada commit, no los copie.
Los mutantes se aplicaron a PRODUCCION en un clon limpio y se restauro el arbol despues
(`git status --short` vacio al terminar). El par de I4 lo repeti con forma de regla valida despues
de descubrir que mi primer intento moria por `artifact_type` invalido -- ese negativo no
discriminaba y lo descarte en vez de contarlo como verde.

Lo que NO verifique: no corri la suite completa contra cada mutante (solo el negativo de esta
tarea); no toque producto ni `npm test`, como pediste; y no medi si CI real ejecuta hoy el job que
contiene `validate.yml:290` -- verifique que la invocacion esta declarada ahi y que su forma exacta
da exit 1 en el commit revisado.

-- Analista, 2026-08-14 01:51 local (UTC+2)
