---
artifact_id: Analista-TASK-0326-untracked-files-convergence-verdict
task_id: TASK-0326
author: Analista
role: checker (adversarial, independent)
created: 2026-08-07T08:24:00Z
created_local: 2026-08-07 10:24 (UTC+2)
verdict: OK-CLOSABLE
anchor_commit: 69f7c423aa63477507b0893ab3cedb66511d9d59
hub_head_at_review: 4acf1e5e
---

# Veredicto TASK-0326 -- convergencia de los dos lectores de estado de git

**OK-CLOSABLE.** Los cinco AC pasan sobre `69f7c423` en clon limpio detached, gate por exit code.
Los cuatro focos que pediste estan cubiertos por EJECUCION, no por lectura. Respuesta directa a tu
pregunta: **si, quitar `--untracked-files=all` del lector de PowerShell tira la suite**; la
convergencia esta clavada por los DOS lados, y ademas resiste el mutante de codigo muerto en ambos.

Cinco residuales declarados, ninguno bloqueante. Dos son hallazgos NUEVOS de direccion ABIERTA
fuera del alcance de esta tarea y pido tarea propia para ellos.

## 1. Anclaje

- Arreglo bajo revision: `69f7c423aa63477507b0893ab3cedb66511d9d59` (verificado ancestro de
  `4acf1e5e`, el HEAD del hub al arrancar la revision).
- Contrato: `Area_comun/tasks/TASK-0326-convergencia-untracked-files-lectores.md`.
- Handoff: `Area_comun/handoffs/HANDOFF-TASK-0326-codex-to-arquitecto.md`.
- Clon limpio detached en `D:/Aegis_Scratch/map/an0326/cc` (DECISION-0104: ruta corta bajo el
  scratch root designado, nunca en raiz de disco). `git rev-parse HEAD` = el commit exacto,
  `git status --short` VACIO antes y despues de cada mutacion.
- Alcance respetado: SOLO el hub. Sin producto en alcance, ningun `npm test` de Nova ni de Zeus.
- Nada medido sobre el arbol caliente salvo una medicion explicitamente etiquetada como
  "arbol vivo" en la seccion 5, que es read-only y esta ahi a proposito.

## 2. Gates recomputados por mi, en el clon limpio, por exit code

| Gate | Comando | Exit | Salida |
|------|---------|------|--------|
| Suite del harness | `python scripts/test_exec_lease_harness.py` | **0** | 17 PASS |
| Inventario de falsacion | `python scripts/check_falsification_contracts.py --root . --inventory` | **0** | 37 DECLARED |
| Estado colaborativo | `python scripts/validate_collaboration_state.py` | **0** | OK |
| Encoding | `python scripts/scan_encoding.py` | **0** | clean |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py` | **0** | clean |
| Drift del runtime | `protocol_state_drift(Path('.'))` | **0** | `has_drift=false`, `up_to_seq=7394`, `hot_hash == replay_hash` |
| Whitespace | `git diff --check` | **0** | vacio |
| Arbol | `git status --short` | **0** | vacio |

El contrato nuevo aparece en el inventario como
`DECLARED NEG-CRON-STATUS-UNTRACKED-FILE-CONVERGENCE boundaries=6 runner=scripts\test_exec_lease_harness.py`.

## 3. Los cuatro focos

### Foco A -- la convergencia, clavada por los DOS lados

Tu duda era legitima: la cadena de mutacion declarada, `source.replace(untracked_option, "", 1)`,
tiene forma de literal de lista de Python y por si sola solo alcanzaria al lector de Python. Pero
lo que decide es la EJECUCION, y la ejecucion cubre los dos. Cuatro mutantes, todos muertos:

| # | Mutante | Lado | Resultado | Asercion que lo mata |
|---|---------|------|-----------|----------------------|
| M1 | quitar ` --untracked-files=all` de `peer_mailbox_cron.ps1:637` | PowerShell | suite **exit 1** | `assert powershell_paths == [f"?? {untracked_path}"]` (linea 652) |
| M2 | dejar el literal pero neutralizarlo: `("status ... --untracked-files=all" -replace ' --untracked-files=all','')` | PowerShell | **KILLED** | la misma |
| M3 | quitar `, "--untracked-files=all"` de `sweep_cron_zombies.py:100` | Python | suite **exit 1**; el test nuevo AISLADO tambien lo mata | `assert mutant_source != source` |
| M4 | **codigo muerto**: `["git","status","--porcelain=v1","-z","--untracked-files=all"][:4]` -- literal PRESENTE pero opcion INALCANZABLE | Python | **KILLED** | `assert healthy_paths == {untracked_path}` |

M2 y M4 son los que importan. M4 es exactamente la forma de escape que nos mordio en TASK-0324
(el contrato ata el helper y no el efecto): el literal sigue en el fuente, `assert linea in source`
pasaria, y aun asi el contrato lo mata **por comportamiento**. El lado de PowerShell no se guarda
con un mutante sino con una asercion incondicional sobre la salida de la funcion REAL cargada de
`scripts/harness/peer_mailbox_cron.ps1`, que es una guardia igual de dura o mas.

Ademas la declaracion no puede derivar en silencio del test: borre del test la linea
`assert powershell_paths == [f"?? {untracked_path}"]` y el inventario da **exit 1** con
`ERROR: NEG-CRON-STATUS-UNTRACKED-FILE-CONVERGENCE: assertion boundary not found beside the test`.
El comprobador exige que la `mutation` declarada y las 6 `boundaries` aparezcan literalmente dentro
de la funcion ejercitadora (`check_falsification_contracts.py:118-125`).

**Respuesta a tu pregunta:** si alguien quita `--untracked-files=all` del lector de PowerShell, cae
`NEG-CRON-STATUS-UNTRACKED-FILE-CONVERGENCE` y con el la suite entera. La convergencia NO esta
clavada solo por el lado de Python.

### Foco B -- direccion del ensanche: falla CERRADO, sin inversion

Primero por estructura: en el barredor, `dirty_paths` tiene **un solo** consumidor,
`dirty_claimed_route`, y ese solo se usa en `decision_for_lease:205` para convertir `kill` en
`skip`. No existe la rama inversa. Y la rama `cleanup_only` (proceso muerto) se decide ANTES del
chequeo de sucio, asi que ensanchar tampoco puede convertir `skip` en `cleanup_only`.

Despues por comportamiento: reconstrui el lector viejo (mismo fichero con la opcion quitada) y
compare la DECISION completa, no el parser, sobre 13 vectores con repos git reales. **Cero
inversiones** (ningun caso con `old_veto=True` y `new_veto=False`):

| Vector | old ve | new ve | old_veto | new_veto |
|--------|--------|--------|----------|----------|
| B1 claim a fichero dentro de dir sin rastrear | `work/` | `work/nested/item.txt` | False | **True** |
| B2 claim a directorio, mismo dir | `work/` | `work/nested/item.txt` | True | True |
| B3 claim a dir mas profundo que el registro colapsado | `work/` | `work/nested/item.txt` | False | **True** |
| B4 owner AJENO no debe ser vetado por el conjunto ancho | `work/` | `work/nested/item.txt` | False | False |
| B5 claim `released` no debe vetar | `work/` | `work/nested/item.txt` | False | False |
| B6 varios ficheros en un dir sin rastrear | `top.txt`, `work/` | `top.txt`, `work/a/one.txt`, `work/a/two.txt`, `work/b/three.txt` | False | **True** |
| B7 prefijo hermano (`work/ab` vs `work/abc/one.txt`) | `work/` | `work/abc/one.txt` | False | False |
| B8 espacio en el nombre (exige entrecomillado en modo linea) | `work/` | `work/nested/we ird name.txt` | False | **True** |
| B9 no-ASCII en el nombre | `work/` | `work/nested/acente.txt` | False | **True** |
| B10 personal ajena + propia, claim sobre la propia | `personal/` | `personal/Arquitecto/draft.md`, `personal/Codex/note.md` | False | **True** |
| B11 solo personal AJENA, claim en otra ruta | `personal/` | `personal/Arquitecto/draft.md` | False | False |
| B12 fichero directo bajo el dir sin rastrear | `work/` | `work/item.txt` | False | **True** |
| B13 fichero gitignored dentro del dir sin rastrear | `.gitignore`, `work/` | `.gitignore`, `work/seen.txt` | False | False |

B4 y B5 son los que responden a la otra mitad de tu pregunta: **no hay veto de mas**. Ver mas
ficheros no veta a un owner que no los tiene reclamados, ni resucita un claim liberado. B7
descarta el falso positivo por prefijo de nombre hermano. B13 confirma que `--untracked-files=all`
NO arrastra ignorados (para eso haria falta `--ignored`).

Sobre el otro consumidor posible, el guard de residuo de PowerShell: **no hay delta en absoluto**,
porque ese lado YA traia la opcion antes de este commit. `69f7c423` no cambia su sensibilidad, asi
que este arreglo no puede aumentar los `defer_terminal` del peer.

**No encontre ningun punto donde ver MAS ficheros haga matar MAS.** Direccion buena, confirmada por
estructura y por 13 vectores de comportamiento.

### Foco C -- el runner, ejecutado de verdad

Comprobado, no leido del handoff. `.github/workflows/validate.yml:237-238`:

```yaml
      - name: Run peer exec-lease and defer-budget harness cases
        run: python scripts/test_exec_lease_harness.py
```

Es un paso `run:` propio, sin `if:`, sin `continue-on-error`. El inventario que declara el contrato
tambien esta cableado y gatea (`validate.yml:45-47`). **Este contrato SI corre en CI.** (Tu medida
de 23 contratos declarados con runner que CI nunca ejecuta no aplica a este; queda para su tarea.)

### Foco D -- la exclusion de areas personales ajenas: intacta, y ademas la opcion es lo que la sostiene

Ejercite `Get-StagedResidueState` cargando la funcion REAL del harness, con y sin la opcion, sobre
repos git reales:

| Caso | Lector REAL (`-uall`) | Mutante (sin `-uall`) |
|------|----------------------|----------------------|
| D1 solo personal AJENA sucia | `state=none`, `paths=[]` | `state=live`, `paths=['personal/']` |
| D2 personal PROPIA sucia | `state=live`, `['personal/Codex/note.md']` | `state=live`, `['personal/']` |
| D3 ajena + propia | `state=live`, `['personal/Codex/note.md']` | `state=live`, `['personal/']` |
| D4 ajena + ruta compartida | `state=live`, `['Area_comun/shared.md']` | `state=live`, `['Area_comun/shared.md', 'personal/']` |

La exclusion sigue vigente (D1 con el lector real da `none`), y el ensanche no la rompe: la afina.
El motivo es que el registro colapsado `personal/` **no casa** con
`^personal/([^/]+)(?:/|$)`, asi que el mutante lo clasifica como relevante y bloquea al peer con
los borradores de OTRO. Es literalmente el fallo operativo "el guard de residuo bloquea al peer en
paralelo". Con la opcion, el registro es `personal/Arquitecto/draft.md`, casa, y se excluye.

Dicho eso, insisto en el matiz de la seccion anterior: el lado de PowerShell ya traia la opcion, o
sea que esto NO es una mejora que traiga `69f7c423`; es la confirmacion de que sigue en pie.

## 4. Los cinco AC, uno a uno

| AC | Que promete | Veredicto | Como lo medi |
|----|-------------|-----------|--------------|
| AC1 | Falsacion sobre repo git real: sin la opcion, un fichero dentro de un dir sin rastrear no aparece como ruta propia y un claim acotado a el no casa | **PASS** | 13 vectores B1-B13 con repos git reales. B1: viejo ve `work/`, `dirty_claimed_route=False`; nuevo ve `work/nested/item.txt`, `True` |
| AC2 | Los DOS lectores interrogan a git con el MISMO juego de opciones, declarado en el handoff | **PASS** | `sweep_cron_zombies.py:100` y `peer_mailbox_cron.ps1:637` con `status --porcelain=v1 -z --untracked-files=all`. Las cuatro opciones estan justificadas una a una en el handoff. Clavado por M1/M2/M3/M4 |
| AC3 | El ensanche no rompe el guard de residuo ni hace matar lo que no debe; efecto colateral declarado y acotado | **PASS** | Foco B (cero inversiones, B4/B5/B7 sin veto de mas) + foco D (D1-D4). Colateral real: ninguno; el lado PS no cambia |
| AC4 | Negativo permanente con salida REAL de git que cubra el dir colapsado, declarado en el registro y cableado en CI | **PASS** | El fixture corre `git init`/`git commit`/`git status` de verdad. `DECLARED ... boundaries=6`. CI `validate.yml:238`. Mata M4 (codigo muerto), no es un contrato de cadena |
| AC5 | Suite del harness y gates del repo exit 0 en clon limpio | **PASS** | Tabla de la seccion 2, ocho gates, todos exit 0 |

## 5. Medicion en el arbol VIVO (read-only): el arreglo es portante HOY

No me quede en los fixtures. En el hub real, ahora mismo, hay **9 directorios sin rastrear que
colapsan**, todos bajo `personal/`:

```
personal/Analista/drafts/            personal/operador/Hermes/
personal/Codex/task0294_attested/    personal/operador/Revision/
personal/Codex/task0294_generated_sample/  personal/operador/encargos-sueltos/
personal/Codex/task0294_runtime/     personal/operador/legal/
                                     personal/operador/requerimientos-futuros/
```

Registros sucios: 742 con el lector viejo, 780 con el nuevo. Con rutas de ficheros REALES de ese
arbol:

| Ruta real reclamada | old_veto | new_veto |
|---------------------|----------|----------|
| `personal/Analista/drafts/DRAFT-MSG-0258-rejuicio-GO.md` | False | **True** |
| `personal/Analista/drafts/DRAFT-veredicto-0258-rejuicio-F01.md` | False | **True** |
| `personal/operador/legal/gen-v2.js` | False | **True** |
| `personal/Codex/task0294_runtime/AGENTS.md` | False | False *(ver R2)* |

O sea: con el barredor de ayer, un claim acotado a cualquiera de esos ficheros no habria vetado
nada y el barredor habria matado trabajo vivo. Coste medido del ensanche: `0.139s` -> `0.054s`
(dentro del ruido; ninguno).

## 6. Residuales declarados

Ninguno bloquea el cierre de TASK-0326. Los dos primeros son hallazgos NUEVOS y pido tarea propia.

### R1 -- HAY UN TERCER LECTOR, y sigue ciego (direccion ABIERTA, fuera de alcance)

`runtime/orchestrator.py:680 dirty_worktree_paths` interroga a git con
`["git", "status", "--porcelain=v1", "-z"]`, **sin** `--untracked-files=all`. Es la misma raiz que
esta tarea cierra en los otros dos, en un consumidor distinto: `unreported_dirty_paths` alimenta
`orchestrator.py:1033`, que RECHAZA un turno cuando aparece un cambio no declarado.

Falsacion medida:

```
turno crea: work/declared_note.md, work/hidden/backdoor.py, work/hidden/deep/more.py
turno declara: changed_paths = ["work/"]
orchestrator ve:      ['work/']
convergido veria:     ['work/declared_note.md','work/hidden/backdoor.py','work/hidden/deep/more.py']
unreported marcados:  []        <-- CERO. El turno pasa.
ocultos al gate:      ['work/hidden/backdoor.py','work/hidden/deep/more.py']
```

`normalize_report_path("work/")` da `"work"` y el registro colapsado tambien, asi que declarar UN
directorio esconde un subarbol entero del gate de cambios no declarados. Es direccion ABIERTA.
(`dirty_tracked_worktree_paths:689` usa `--untracked-files=no` a proposito y para su fin es
correcto; no lo toco.)

Pido tarea propia con el mismo criterio con el que registrasteis 0326 desde mi R4 de 0323.

### R2 -- `--untracked-files=all` NO desciende a un repo git EMBEBIDO (direccion ABIERTA, familia no cerrada por ninguna opcion)

Esta es la parte de la familia del AC1 que el arreglo no alcanza, y ninguna opcion de `git status`
la alcanza. Falsacion:

```
fixture: work/inner es un repo git anidado, con work/inner/live_work.md sin commitear
claim scope: work/inner/live_work.md
  status --porcelain=v1 -z                       -> ['?? work/']
  status --porcelain=v1 -z --untracked-files=all -> ['?? work/inner/']     <-- baja UN nivel y para
  ... --untracked-files=all --ignored            -> ['?? work/inner/']     <-- tampoco
dirty_claimed_route(root, owner) con el lector ARREGLADO -> False
```

`False` significa que el barredor mata el trabajo vivo. Y **esta forma existe en el hub HOY**:
`personal/Codex/task0294_runtime/` es un repo embebido (tiene su propio `.git`), que es justo la
fila `False/False` de la tabla de la seccion 5.

No es un defecto de este arreglo ni se arregla con opciones: exige otro mecanismo (interrogar cada
repo anidado, o que `dirty_claimed_route` trate un registro de directorio como prefijo del claim).
Pido tarea propia.

### R3 -- el `#` del scope se trunca en el claim pero no en la ruta observada

`dirty_claimed_route` hace `str(scope).split("#", 1)[0]` sobre la ruta reclamada y nunca sobre la
ruta observada. Un claim sobre un fichero real cuyo nombre contenga `#` no puede casar jamas.
Preexistente, no lo introduce 0326, direccion ABIERTA pero de probabilidad muy baja en este repo
(el `#` es el separador de ancla del protocolo). Una linea de runbook basta.

### R4 -- la `mutation` declarada solo expresa el lado de Python

El campo `mutation` del contrato es `source.replace(untracked_option, "", 1)`, que es la mutacion
del lector de Python. La garantia del lado de PowerShell no viaja en una mutacion sino en una
asercion incondicional (`boundaries[3]`). Verificado que es PORTANTE (M1, M2) y que esta PINEADA
por el inventario (borrar la asercion pone el inventario en exit 1). No es un hueco: es una brecha
de LECTURA -- quien lea solo el registro concluye que el lado PS no esta guardado, que es
exactamente la duda con la que abriste el foco A. Una frase en `negative` cerraria esa lectura.

### R5 -- el mapa sigue sin ver los ignorados

`--untracked-files=all` no incluye ficheros gitignored (medido en B13). Un claim acotado a una ruta
gitignored no veta nunca. Es correcto por diseno, pero la premisa del intake es "el barredor decide
sobre un mapa incompleto", asi que conviene que el runbook diga en voz alta que el mapa excluye
ignorados a proposito.

## 7. Reproduccion

```bash
# clon limpio, ruta corta bajo el scratch root designado (DECISION-0104)
mkdir -p /d/Aegis_Scratch/map/an0326 && cd /d/Aegis_Scratch/map/an0326
git clone --no-checkout --shared D:/Agentes/multi_agent_project_protocol cc
cd cc && git checkout --detach 69f7c423aa63477507b0893ab3cedb66511d9d59
git status --short                                                   # vacio

python scripts/test_exec_lease_harness.py                            # exit 0, 17 PASS
python scripts/check_falsification_contracts.py --root . --inventory  # exit 0, 37 DECLARED
python scripts/validate_collaboration_state.py                        # exit 0
python scripts/scan_encoding.py                                       # exit 0
python scripts/scan_domain_neutrality.py                              # exit 0
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; \
import sys; d=protocol_state_drift(Path('.')); sys.exit(1 if d.get('has_drift') else 0)"  # exit 0
git diff --check                                                      # exit 0

# M1 -- el lado de PowerShell, por ejecucion
python - <<'EOF'
from pathlib import Path
p=Path("scripts/harness/peer_mailbox_cron.ps1"); s=p.read_text(encoding="utf-8")
p.write_text(s.replace(" --untracked-files=all","",1),encoding="utf-8",newline="\n")
EOF
python scripts/test_exec_lease_harness.py    # exit 1, muere en la linea 652
git checkout -- scripts/harness/peer_mailbox_cron.ps1

# M4 -- codigo muerto en el lado de Python: literal presente, opcion inalcanzable
python - <<'EOF'
from pathlib import Path
p=Path("scripts/sweep_cron_zombies.py"); s=p.read_text(encoding="utf-8")
old='["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],'
new='["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"][:4],'
assert old in s
p.write_text(s.replace(old,new,1),encoding="utf-8",newline="\n")
EOF
PYTHONPATH=scripts python -c "import importlib.util as u; \
s=u.spec_from_file_location('h','scripts/test_exec_lease_harness.py'); m=u.module_from_spec(s); \
s.loader.exec_module(m); m.test_git_status_readers_enumerate_untracked_files_without_overbroad_veto()"
# AssertionError en: assert healthy_paths == {untracked_path}
git checkout -- scripts/sweep_cron_zombies.py
```

Sondas completas de los focos B, D, R1 y R2 en `D:/Aegis_Scratch/map/an0326/` (`probe_b_d.py`,
`probe_d_ps.py`, `probe_r_orchestrator.py`, `probe_nested.py`, `probe_live.py`). Fuera del arbol
atestado, nunca la unica copia, se limpian al stand-down.

## 8. Recomendacion de cierre

**OK-CLOSABLE** para TASK-0326 sobre `69f7c423`.

Lo pedido esta hecho y esta clavado por comportamiento en los dos lectores, el contrato resiste el
mutante de codigo muerto en ambos lados y su runner corre de verdad en CI. Pido registrar R1 y R2
como tareas propias: son direccion ABIERTA, estan medidos, y R2 existe en el arbol vivo hoy.

Analista -- checker-only. No implemento, no promuevo, no cierro, no ratifico.
