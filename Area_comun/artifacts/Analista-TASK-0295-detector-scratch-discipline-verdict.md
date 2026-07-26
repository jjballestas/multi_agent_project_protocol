---
artifact_id: Analista-TASK-0295-detector-scratch-discipline-verdict
task_id: TASK-0295
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-07-26
local_time: "2026-07-26 21:17 (UTC+2)"
anchor_commit: b1b3bbca5c6c25f2354f98b8258e014615aefa31
implementation_commit: 3aa332d3e8aedf4d8128d035ad0420412290558f
verdict: OK-CLOSABLE
scope: protocol only (no product in scope; Nova-Budget / npm test NOT gated)
---

# VEREDICTO Analista - TASK-0295 (detector read-only de scratch discipline)

**OK-CLOSABLE.** 31/31 vectores adversariales PASS, 0 SLIPS. Los cuatro terminos del contrato de
acceptance (read-only, neutralidad, deteccion, exit codes) se sostienen por comportamiento en clon
limpio, no por nombre de test. No encontre ningun path de escritura, ningun falso positivo dentro
del contrato, ni un falso negativo que viole la letra del acceptance. Declaro 5 residuales
accionables (R1-R5) fuera del texto del acceptance; **R1 y R2 son materiales para que los teeth de
DECISION-0104 muerdan de verdad** y recomiendo unidad de seguimiento, pero ninguno bloquea el cierre
de 0295 tal como fue especificada.

## 1. Ancla canonica y reproduccion

Ancla: `origin/main` HEAD `b1b3bbc` (== `origin/main` local en el arranque: `8f1e495`; el delta
`b1b3bbc..8f1e495` es **solo** el MSG de REVIEW del Arquitecto, 1 archivo, 46 lineas: no toca el
detector). `git diff 3aa332d b1b3bbc -- scripts/scan_scratch_discipline.py examples/scratch_discipline_cases/`
= vacio: el artefacto revisado es byte-identico al commit de implementacion.

Clon limpio bajo el scratch root designado (DECISION-0104: **jamas** en la raiz real del disco):
`D:/Aegis_Scratch/multi_agent_project_protocol/an0295` (clon fresco, `git status --short` vacio).
Fixtures propios bajo `D:/Aegis_Scratch/multi_agent_project_protocol/an0295fx` y `.../an0295fix`;
banco adversarial en `.../an0295adv`. Cero artefactos fuera del scratch root.

Gates por exit code, todos en el clon limpio:

| Gate | Comando | Exit |
|---|---|---|
| Suite del maker | `python examples/scratch_discipline_cases/run_scratch_discipline_cases.py --scratch-root D:/Aegis_Scratch/multi_agent_project_protocol/an0295fx` | **0** |
| Estado canonico | `python scripts/validate_collaboration_state.py` | **0** |
| Encoding | `python scripts/scan_encoding.py` | **0** |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py` | **0** |
| Banco adversarial propio (31 vectores) | `python adversarial_0295.py <clon> <fixtures>` | **0** (0 SLIPS) |

Nota de higiene verificada: la suite del maker limpia sus fixtures (`shutil.rmtree` en `finally`);
el directorio de scratch queda vacio tras correrla.

## 2. Vector por vector (banco propio, no el del maker)

Construi un fixture independiente del entregado, con familias que el ejemplo del acceptance NO
cubre (ssh scp-like, worktree, remote de ruta local con backslashes, dir oculto, markers parciales,
profundidad 2, case/trailing-sep del scratch root, config malformada).

### A. READ-ONLY (contrato 1)

| Vector | Resultado | Evidencia |
|---|---|---|
| A1 bytes del arbol de fixtures antes/despues (contenido completo, incl. `.git/**`) | **PASS** | sha256 `f8d721c6de734f60...` == `f8d721c6de734f60...` tras 3 corridas (json, text, sin `--check`) |
| A2 metadatos: `st_mtime_ns` + `st_size` de **todo** nodo, incl. internals de git | **PASS** | `6ea95b082fc10807...` == `6ea95b082fc10807...` (ni siquiera se toca la mtime de `.git/config`) |
| A3 el propio clon revisado no se muta (`git status --porcelain` antes/despues) | **PASS** | 0 entradas antes y despues |
| B4 auditoria de API mutante en el fuente (`.write_text`, `.mkdir`, `open(`, `os.remove`, `os.rename`, `shutil.*`, `.unlink`, `.rmdir`, `.touch`) | **PASS** | 0 ocurrencias. Solo `iterdir`, `is_dir`, `exists`, `read_text`, `resolve`, `print`, y `git config --get-regexp` (lectura) |

A2 es mas fuerte que el fingerprint del maker (que solo hashea contenido): descarta tambien
escrituras silenciosas de git que no cambian bytes. No hay ninguna.

### B. NEUTRALIDAD (contrato 2)

| Vector | Resultado | Evidencia |
|---|---|---|
| B1 cero marca/dominio/raiz hardcodeada en el detector | **PASS** | busqueda case-insensitive de `Aegis, Zeus, Nova, trading, D:/, D:\, C:/, C:\, Agentes, bot_spot, budget, payroll` -> 0 hits |
| B2 idem en la suite de examples | **PASS** | 0 hits (la suite exige `--scratch-root` obligatorio; no inventa raiz) |
| B3 fuente ASCII puro | **PASS** | todos los bytes < 128 |
| Gate oficial | **PASS** | `scan_domain_neutrality.py` exit 0 |

Scan-root, scratch-root y known-repo son parametro CLI o campo de config (`scratch_discipline.*` con
fallback a las claves top-level). Confirmado por comportamiento en D8 (config-driven) y D3 (sin raiz
declarada, error explicito).

### C. DETECCION (contrato 3) - familia completa, no solo el ejemplo

| Vector | Esperado | Resultado |
|---|---|---|
| C1 clon con remote https en el set conocido | FLAG | **PASS** |
| C2 mismo repo con remote scp-like `git@host:owner/repo.git` vs known dado en https | FLAG (identidad equivalente) | **PASS** |
| C3 clon ajeno (remote fuera del set) | IGNORAR | **PASS** |
| C4 dir con los 3 marcadores atestados | FLAG | **PASS** |
| C5 marcadores parciales (sin `protocol.config.json`; y solo `Area_comun`) | IGNORAR (contrato = los 3) | **PASS** (ver R5) |
| C6 compliant bajo el scratch root, anidado 3 niveles + clon conocido bajo scratch | IGNORAR | **PASS** |
| C7 dir ajeno sin huella | IGNORAR | **PASS** |
| C8 dir **oculto** con marcadores (`.hidden-markers`) | FLAG | **PASS** |
| C9 remote de **ruta local** con backslashes vs known en forward-slash | FLAG | **PASS** (normcase+resolve) |
| C10 archivo top-level llamado `protocol.config.json` | IGNORAR (no es dir) | **PASS** |
| C11 scratch root en MAYUSCULAS + separador final | mismo veredicto | **PASS** (exit 1, mismo set) |
| C13 **git worktree** (`.git` como archivo, config compartida) | FLAG | **PASS** |
| C-EXACT set exacto de hallazgos (cero falsos positivos) | 6 esperados | **PASS** `{stray-https, stray-ssh, stray-markers, .hidden-markers, stray-localpath, stray-worktree}` |

### D. EXIT CODES (contrato 4)

| Vector | Esperado | Resultado |
|---|---|---|
| D1 `--check` con hallazgos (json) | 1 | **PASS** |
| D1b `--check` con hallazgos (texto) | 1 | **PASS** |
| D2 `--check` sobre arbol limpio | 0 | **PASS** |
| D3 sin scratch root (ni CLI ni config) | 2 | **PASS** (`ERROR: scratch root is required...` a stderr) |
| D4 scan root inexistente | 2, **no** 0 silencioso | **PASS** |
| D5 sin `--check` con hallazgos | 0 (modo reporte) | **PASS** (ver caveat U1) |
| D6 scan root apuntando a un archivo | 2 | **PASS** |
| D7 config sin las claves + CLI completa | usable | **PASS** (exit 1) |
| D8 config con `scratch_root` + `known_repositories` | 1 con hallazgos | **PASS** |
| D9 `known_repositories` malformado (string en vez de lista) | 2, falla ruidoso | **PASS** |

D4/D6/D9 son los que importan de verdad: el detector **no** convierte un error de entrada en un
"limpio" silencioso. Ese era el modo de fallo mas peligroso para unos teeth y no ocurre.

## 3. Intentos de refutacion que NO prosperaron

- **Escritura oculta:** ninguna. Ni por API, ni empiricamente (A1+A2 incluyen `.git/**` con
  mtime_ns; git `config --get-regexp` no toca el repo).
- **Falso positivo dentro del contrato:** no logre que flagee un dir sin huella, un clon ajeno, un
  archivo, ni nada bajo el scratch root (incluido un clon conocido colocado **dentro** del scratch).
- **Hardcode:** no hay. El detector es inejecutable sin declarar scratch root (exit 2), que es
  exactamente lo que DECISION-0104 pide ("ante duda, preguntar; nunca improvisar").
- **Colision de identidad de remote:** https / scp-like ssh / ruta local con backslashes /
  sufijo `.git` / trailing slash convergen a la misma identidad. No consegui que un mismo repo se
  escapara por escribir el remote en otra forma.

## 4. Residuales declarados (no bloquean el cierre de 0295)

**R1 (material) - el escaneo es solo de profundidad 1.** `find_anomalies` itera unicamente los hijos
top-level de cada scan root. Es lo que el acceptance pide literalmente ("directorios de nivel
superior"), asi que **no es un SLIP**; pero medi su efecto real en esta maquina, en seco y read-only:

```
python scripts/scan_scratch_discipline.py --scan-root D:/ --scratch-root D:/Aegis_Scratch \
  --known-repo D:/Agentes/multi_agent_project_protocol --known-repo D:/Agentes/Zeus/Zeus-protocol-Aegis --check --json
-> exit 0, FINDINGS 0   (12 dirs top-level en D:/)
```

y sin embargo, sondeando profundidad 2 con un script propio, `D:\Agentes\runtime-test-instance`
tiene los **3 marcadores atestados** y vive fuera del scratch root: es justo la clase que
DECISION-0104 persigue, y el detector apuntado a la raiz del disco devuelve 0 hallazgos. Los teeth
solo muerden si el operador apunta `--scan-root` a cada dir contenedor. Seguimiento sugerido:
`--max-depth` (default 1) o multiples scan roots documentados en el runbook.

**R2 (material) - no hay allowlist de "hogar canonico".** Al apuntar al scan root util:

```
python scripts/scan_scratch_discipline.py --scan-root D:/Agentes --scratch-root D:/Aegis_Scratch \
  --known-repo D:/Agentes/multi_agent_project_protocol --check --json
-> exit 1, FINDINGS 2:
   D:\Agentes\multi_agent_project_protocol  (marcadores atestados)   <- hogar canonico del hub
   D:\Agentes\runtime-test-instance         (marcadores atestados)   <- stray real
```

Por la letra del acceptance flagear el hub es **correcto** (no esta bajo el scratch root), pero
DECISION-0104 regula el **scratch**, no el hogar canonico del repo. Sin un allowlist
(`--allow-home` / `scratch_discipline.canonical_homes`) todo informe exige triage manual y el
hallazgo de ruido convive con el real. Seguimiento sugerido.

**R3 - fail-open ante metadatos git irresolubles.** Si `git` falla para un candidato (gitfile
corrupto, `safe.directory`/dubious ownership, git ausente del PATH), `_remote_urls` devuelve `[]` en
silencio; sin marcadores atestados el stray no se flagea y `--check` sale 0, sin warning.
Reproducido: dir con `.git` = archivo `gitdir: /nonexistent/garbage` + payload ->
`OK: no scratch-discipline anomalies found.`, exit 0. Sugerido: canal de warning (stderr) por
candidato cuyo git falle, para que el fail-open sea visible.

**R4 - deteccion entregada, enforcement no cableado.** `protocol.config.json` (pineado, epoch
1.14.0) **no tiene** campo `scratch_root` -- el chequeo de DECISION-0098 en el validador es
condicional a que el campo exista, y hoy no existe -- y nada invoca al detector desde un gate, CI o
cron. Es decir: DECISION-0104 cl.5b tiene detector funcional y **cero disparo automatico**. El
`out_of_scope` de 0295 excluye explicitamente el campo de config, asi que es unidad de seguimiento,
no defecto de esta.

**R5 (menor) - marcadores atestados en AND estricto.** `_attested_tree` exige los 3
(`Area_comun` + `runtime` + `protocol.config.json`). Una copia parcial de la metodologia sin
`runtime/` escapa la deteccion por marcadores (verificado en C5). Es el contrato del acceptance;
lo dejo declarado por si el seguimiento quiere una regla 2-de-3.

**U1 (caveat de uso, no residual) - `--check` es obligatorio para que el exit sea no-cero.** Sin
`--check`, el detector imprime los hallazgos y sale 0 (D5, que es lo especificado). Un llamador de
CI que olvide `--check` pasa en verde con anomalias en pantalla. Documentar en el runbook.

## 5. Recomendacion de cierre

**OK-CLOSABLE (GO).** El entregable cumple los 4 terminos del acceptance por comportamiento en clon
limpio, con gates verdes por exit code y sin defecto concreto. Los residuales R1-R5 y el caveat U1
son ampliaciones de alcance (profundidad, allowlist, warning de fail-open, cableado a gate), no
incumplimientos: recomiendo registrarlos como unidad(es) de seguimiento antes de declarar que
DECISION-0104 cl.5b esta **enforced** -- hoy esta **detectable**, que no es lo mismo.

-- Analista (checker independiente, TASK-0295)
