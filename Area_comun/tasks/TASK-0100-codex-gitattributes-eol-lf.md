---
id: TASK-0100
owner: Codex
status: proposed
type: implementation
priority: normal
created_at: 2026-06-10
updated_at: 2026-06-10
depends_on: []
relates_to: [TASK-0099, SPEC-0075, DECISION-0023]
phase: P2
spec_id: Area_comun/specs/SPEC-0075-gitattributes-eol-lf-release-reproducible.md
linked_decisions: [DECISION-0023, DECISION-0006, DECISION-0019]
deliverables:
  - .gitattributes
relevant_files:
  - .gitattributes
  - scripts/generate_sbom.py
  - scripts/verify_release.py
blocked_by_questions: []
objective: (OFF-PILOT, follow-up de robustez del release) Hacer la verificacion del release REPRODUCIBLE cross-platform anadiendo .gitattributes que normalice line-endings a LF en checkout. Hoy NO hay .gitattributes; el repo guarda blobs LF pero un checkout Windows con core.autocrlf=true materializa CRLF -> el SBOM (que hasheo LF) no coincide -> verify_release da ok:false por diff de line-endings aunque el contenido sea identico. Visto en vivo en el corte v1.1.0 (git checkout re-aplico CRLF a README_INSTANCIACION.md, 18966 vs 18555 LF, y rompio la verificacion hasta restaurar LF).
expected_output: (1) .gitattributes raiz que fija LF en checkout para archivos de texto (p.ej. "* text=auto eol=lf" o un set curado por tipo + binarios marcados -text/binary), eligiendo el enfoque que NO altere bytes de archivos SBOM-included existentes. (2) Verificacion con git add --renormalize . en arbol limpio: CERO cambios de bytes en archivos SBOM-included (los blobs ya son LF) -> la firma de v1.1.0 (sbom_hash 0083c1c9...) sigue valida. Si renormalize mostrara cambios reales en SBOM-included -> blocked + nota al arquitecto (NO commitear; invalidaria la firma). (3) Regresion determinista: en un clon/worktree limpio con autocrlf=true simulado, los archivos texto salen LF y verify_release --manifest dist/v1.1.0/manifest.json da ok:true (diff vacio). (4) Cross-platform: no rompe Linux/CI ni los wrappers .ps1. validador/neutralidad/encoding verdes.
question_to_resolve: Q1 enfoque de .gitattributes ("* text=auto eol=lf" global vs set curado por extension + binarios explicitos) priorizando NO alterar bytes de archivos SBOM-included existentes. Q2 forma de la regresion de reproducibilidad (clon temporal con core.autocrlf=true + verify_release) determinista en CI sin depender del autocrlf de la maquina.
closure_criterion: .gitattributes anadido; git add --renormalize . NO cambia bytes de archivos SBOM-included (firma v1.1.0 intacta, verificado); regresion de reproducibilidad verde (checkout LF + verify_release ok:true); cross-platform; .ps1 intactos; validador/neutralidad/encoding verdes; sin secretos; handoff con evidencia. OFF-PILOT: SA.4 de-armado.
sdd_required: true
---

# TASK-0100 - .gitattributes eol=lf para releases reproducibles cross-platform

> PROPOSED (Claude 2026-06-10, follow-up de robustez tras el corte v1.1.0; el operador pidio encolarlo).
> Formalizada bajo SDD: spec_id = SPEC-0075. OFF-PILOT. SA.4 DE-ARMADO. Promover a ready+GO cuando el
> operador lo indique.

## Contexto

El SBOM del release hashea bytes LF. Sin `.gitattributes`, un checkout en Windows con `core.autocrlf=true`
materializa CRLF y `verify_release` falla por diff de line-endings aunque el contenido sea identico. El
arbol del emisor (LF) verifica bien; un tercero en Windows-autocrlf no. Esta task fija LF en checkout para
que la verificacion sea reproducible en cualquier plataforma.

## Restriccion critica (firma existente)

`.gitattributes` NO esta en los include-globs del SBOM, asi que anadirlo NO cambia el `sbom_hash` firmado de
v1.1.0. PERO si `git add --renormalize .` alterara bytes de algun archivo SBOM-included, eso invalidaria la
firma -> en ese caso, **blocked + nota al arquitecto** antes de commitear. Los blobs ya son LF, asi que no
deberia haber cambios; verificarlo es parte del DoD.

## Restricciones

- OFF-PILOT: SA.4 de-armado, NO re-armar ni piloto. enforce+authoritative ON. ASCII, sin secretos,
  determinista, cross-platform. Template intacto. 1 commit/turno con rutas explicitas.
