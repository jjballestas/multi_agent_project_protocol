---
spec_id: SPEC-0074-temp-dir-cleanup-robusto
task_id: TASK-0097
type: design
status: ready
created_at: 2026-06-10
author: Claude (arquitecto)
linked_decisions: [DECISION-0006, DECISION-0023, DECISION-0020]
relates_to: [TASK-0097, SPEC-0071, TASK-0094]
---

> Formaliza bajo SDD el follow-up de higiene TASK-0097: eliminar la FUGA de directorios temporales
> repo-local que los harness de golden dejan en la raiz al correr en Windows. Aditivo, OFF-PILOT, neutral,
> sin cambio de semantica del write-path. NO requiere decision nueva (DECISION-0006 robustez operacional ya
> cubre la portabilidad/robustez del runtime).

# Diseno - Cleanup robusto de temp dirs repo-local (no fuga en la raiz)

## 1. Objetivo

Tras TASK-0094 los temp dirs son repo-local (ACL heredada, para el sandbox unelevated en Windows). El
runtime vivo limpia los suyos, pero los HARNESS de golden filtran decenas de dirs `.protocol-materialize-*`
/ `.runtime-real-*` / `.debug-replay-temp-*` en la raiz porque `shutil.rmtree(ignore_errors=True)` falla
silencioso ante archivos bloqueados en Windows. Objetivo: cero restos repo-local tras correr la suite, sin
flakiness en CI y sin romper Linux.

## 2. Alcance

- `runtime/temp_paths.py`: consolidar los temp dirs repo-local bajo UN parent unico gitignoreado
  (`root/.protocol-tmp/<prefix><hex>`) y un cleanup robusto en Windows.
- Los harness de golden que crean temp dirs repo-local usan el context manager `root_temp_dir`
  (cleanup garantizado) en vez de `make_root_temp_dir` suelto donde aplique.
- `.gitignore`: una sola entrada `.protocol-tmp/` (reemplaza los prefijos sueltos previos donde aplique).
- Golden/regresion determinista que asevere cero restos repo-local tras una suite.
- Opcional: wire `scripts/clean_workspace_temp.py` en hook/CI para barrer restos legacy + el parent nuevo.

## 3. No-alcance

- NO cambiar la SEMANTICA del write-path autoritativo (la materializacion sigue byte-equivalente; mismo
  `canonical_hash`; `replace()` same-fs intacto). El cambio es solo de UBICACION y LIMPIEZA de los temp dirs.
- NO re-armar SA.4 ni piloto. NO tocar defaults del template ni el runtime vivo mas alla de la ubicacion
  del temp parent. NO secretos.

## 4. Diseno

### 4.1 Parent unico gitignoreado

- `temp_paths.py` crea los temp dirs bajo `root/.protocol-tmp/` (p.ej.
  `root/.protocol-tmp/<prefix>-<hex>`), en vez de esparcir `.<prefix>-<hex>` en la raiz. Mismo fs que el
  repo (preserva la garantia ACL-heredada de TASK-0094 y el `replace()` same-fs). `.gitignore` += una sola
  entrada `.protocol-tmp/`.

### 4.2 Cleanup robusto en Windows

- `root_temp_dir` (context manager) garantiza el cleanup: `rmtree` con un `onerror` que quita el atributo
  read-only (`os.chmod` + reintento) y reintentos cortos acotados; en exito deja cero restos. Alternativa
  complementaria: un barrido idempotente del parent `.protocol-tmp/` al inicio de la suite y/o `atexit`.
  Sin sleeps largos ni dependencia de red -> sin flakiness en CI.

### 4.3 Harness

- Los harness que hoy usan `make_root_temp_dir` suelto y no limpian pasan a `with root_temp_dir(...) as d:`
  donde aplique, de modo que el cleanup este garantizado por el context manager.

## 5. Invariantes (no negociables)

1. Write-path byte-equivalente: materializacion con el mismo `canonical_hash`; `replace()` same-fs intacto;
   drift 0 antes/despues.
2. Cross-platform: no rompe Linux/CI; el cleanup robusto Windows-especifico no introduce flakiness.
3. Cero restos repo-local en la raiz tras la suite (verificable por golden).
4. Neutral de dominio, ASCII, sin secretos, determinista.

## 6. Tests (golden determinista)

- Regresion que corre una operacion que crea temp dirs repo-local y asevera que tras el cleanup NO quedan
  dirs `.protocol-*` / `.runtime-*` / `.debug-*` ni en la raiz ni huerfanos en `.protocol-tmp/`.
- Goldens existentes de materializacion siguen verdes con el mismo `canonical_hash` (write-path intacto).
- Paridad de comportamiento donde haya `.ps1` involucrado; validador/neutralidad/encoding verdes; drift 0.

## 7. SemVer y neutralidad

PATCH/MINOR aditivo (higiene operacional, sin cambio de contrato ni de semantica del write-path). Neutral.
DECISION-0006 (robustez operacional).

## 8. Decisiones / preguntas

- Q1 (resuelta, arquitecto): parent unico `.protocol-tmp/` (mas limpio, una sola entrada gitignore) en vez
  de prefijos sueltos.
- Q2 (a eleccion del implementador con ratificacion): estrategia exacta de cleanup robusto en Windows
  (`rmtree` con `onerror`+retry vs barrido `atexit`/inicio-de-suite, o ambos) priorizando determinismo y
  cero flakiness en CI.

## 9. Cierre

Implementacion = TASK-0097 (owner Codex). Golden cero-restos verde; write-path byte-equivalente (mismo
`canonical_hash`, drift 0); validador/neutralidad/encoding verdes; cross-platform; handoff con evidencia.
Ratificacion adversarial del arquitecto (write-path intacto + cero restos + sin flakiness). OFF-PILOT.
