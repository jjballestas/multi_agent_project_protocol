---
id: TASK-0097
owner: Codex
status: ready
type: implementation
priority: normal
created_at: 2026-06-10
updated_at: 2026-06-10
depends_on: []
relates_to: [TASK-0094, TASK-0095, TASK-0096]
phase: P2
spec_id: Area_comun/specs/SPEC-0074-temp-dir-cleanup-robusto.md
linked_decisions: [DECISION-0023, DECISION-0006, DECISION-0020]
objective: (OFF-PILOT, follow-up de higiene) Eliminar la FUGA de directorios temporales repo-local que dejan los harness de golden (y, en menor medida, el write-path) al correr en Windows. Tras TASK-0094 los temp dirs son repo-local (inherited-ACL, para el sandbox unelevated); el runtime vivo limpia los suyos, pero los harness filtran decenas de dirs `.protocol-materialize-*` / `.runtime-real-*` / `.debug-replay-temp-*` en la raiz del repo porque shutil.rmtree(ignore_errors=True) falla silencioso ante archivos bloqueados en Windows. El operador noto la acumulacion. Ya se mitigo (sweep manual + .gitignore + scripts/clean_workspace_temp.py); esta task arregla la RAIZ.
expected_output: (1) Consolidar los temp dirs repo-local bajo UN unico parent gitignoreado (p.ej. root/.protocol-tmp/<prefix><hex>) en runtime/temp_paths.py (make_root_temp_dir/root_temp_dir), en vez de esparcir `.<prefix>-<hex>` en la raiz; asi el .gitignore es una sola entrada (.protocol-tmp/) y la limpieza es un solo arbol. (2) Cleanup ROBUSTO en Windows: root_temp_dir reintenta rmtree (p.ej. onerror que quita read-only + reintento corto) y/o un barrido atexit/al inicio de la suite que limpia restos. (3) Los harness de golden que crean temp dirs repo-local usan el context manager root_temp_dir (cleanup garantizado) en vez de make_root_temp_dir suelto donde aplique. (4) Golden/regresion determinista que asevere que tras correr una suite NO quedan temp dirs repo-local. (5) Opcional: wire scripts/clean_workspace_temp.py en un hook/CI. validador/neutralidad/encoding verdes; drift 0; cross-platform (no rompe Linux/CI). NO re-armar SA.4 ni piloto.
question_to_resolve: Q1 consolidar bajo un parent unico (.protocol-tmp/) vs mantener prefijos sueltos con .gitignore por-prefijo; Claude recomienda el parent unico (mas limpio, una sola entrada gitignore). Q2 estrategia de cleanup robusto en Windows (retry rmtree onerror vs barrido atexit) sin flakiness en CI.
closure_criterion: tras correr la suite completa de goldens NO quedan temp dirs repo-local en la raiz (verificable); temp dirs consolidados bajo un parent gitignoreado o cleanup robusto garantizado; golden/regresion que lo asevere; validador/neutralidad/encoding verdes; drift 0; cross-platform; sin secretos; handoff con evidencia. OFF-PILOT: SA.4 de-armado.
sdd_required: true
---

# TASK-0097 - Cleanup robusto de temp dirs repo-local (no fuga en la raiz)

> READY+GO (Claude 2026-06-10, bajo SPEC-0074, GO del operador para aplicar el fix de raiz). Formalizada
> bajo SDD: spec_id = SPEC-0074. Desbloquea el blocker de Codex (proposed sin spec). OFF-PILOT. SA.4 DE-ARMADO.
> Mitigacion inmediata YA aplicada: sweep manual de 70 restos + .gitignore (prefijos temp) +
> scripts/clean_workspace_temp.py (barredor dry-run/--apply). Esta task arregla la RAIZ.

## Contexto

El operador noto decenas de dirs `.protocol-materialize-*`, `.runtime-real-*`, `.debug-replay-temp-*`
acumulados en la raiz del repo. Son temp dirs repo-local (TASK-0094) que los harness de golden filtran en
Windows (rmtree(ignore_errors=True) falla ante archivos bloqueados). El runtime vivo SI limpia los suyos
(.protocol-state-materialize-*/.runtime-state-backup-*/.submit-intent-runtime-backup-*). No son
necesarios, no se commitean, no entran al SBOM; pero ensucian el working dir.

## Alcance

- runtime/temp_paths.py: consolidar bajo un parent unico gitignoreado (.protocol-tmp/) + cleanup robusto
  en Windows (retry/onerror). Harness usan root_temp_dir (cleanup garantizado).
- Golden que asevere cero restos tras la suite. Opcional: hook/CI con clean_workspace_temp.py.

## Restricciones

- OFF-PILOT: SA.4 de-armado, NO re-armar ni piloto. enforce+authoritative ON. ASCII, sin secretos,
  determinista, cross-platform. Template intacto. 1 commit/turno con rutas explicitas.
