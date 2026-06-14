---
id: TASK-0100
owner: Codex
status: done
type: implementation
priority: normal
created_at: 2026-06-10
updated_at: 2026-06-10
depends_on: []
relates_to: [TASK-0099, SPEC-0075, DECISION-0023]
phase: P2
spec_id: Area_comun/specs/SPEC-0075-gitattributes-eol-lf-release-reproducible.md
linked_decisions: [DECISION-0023, DECISION-0006, DECISION-0019, DECISION-0037]
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

## RESCOPE 2026-06-14 (DECISION-0037) -- AUTORITATIVO (supersede objetivo/DoD de arriba)

El bloqueo de Codex revelo que el manifest firmado de v1.1.0 NO es reproducible bajo LF: clasificacion al
byte (artefacto `Area_comun/artifacts/ANALISTA-TASK-0100-decision-A-eol-rescope.md`) = **616 LF / 127 CRLF
/ 14 no-EOL**; ademas el manifest se genero sobre un **arbol sucio** (14 deltas vs el commit 04436c3) y
`runtime/protocol_replay.py` es **irreproducible desde refs**. Por tanto v1.1.0 NO puede arreglarse sin
re-firmar (opcion B, descartada). El operador eligio **opcion A** (DECISION-0037): acotar a releases
FUTUROS, firma de v1.1.0 INTACTA.

**Objetivo (rescoped):** que los releases **v1.2.0+** sean LF-reproducibles cross-platform, y documentar
v1.1.0 honestamente como release historico con deuda de integridad. NO re-firmar ni regenerar v1.1.0. NO
tocar el manifest firmado.

**Expected output (rescoped):**
1. `.gitattributes` raiz que fije LF en checkout para texto (binarios marcados). Pre-condicion ya
   verificada: en HEAD `git add --renormalize .` solo stagea `.gitattributes` (0 cambios SBOM en HEAD).
   **GUARDA DURA intacta:** si renormalize alterara bytes SBOM-included del HEAD -> BLOCKED + nota (no
   commitear).
2. **Nota known-limitations de v1.1.0 EXPLICITA y NO eufemistica** (p.ej. en `dist/v1.1.0/` y/o doc de
   release): clasificacion real 616 LF / 127 CRLF / 14 no-EOL; el manifest se genero sobre arbol sucio (no
   checkout limpio de 04436c3); `protocol_replay.py` irreproducible desde refs; `verify.integrity.json
   ok:true` = verificacion local del emisor, no de terceros; corrige la premisa falsa de SPEC-0075 ("ningun
   blob SBOM cambia" -- 127 eran CRLF). Sin numeros no respaldados por la clasificacion.
3. `verify_release` fija/excluye v1.1.0 de la promesa LF (la garantia aplica desde v1.2.0); un verify LF
   que falle en v1.1.0 es esperado y documentado, NO silenciado. SIN tocar el manifest firmado.
4. Regresion de reproducibilidad sobre un release **futuro** (smoke): checkout LF -> verify_release ok:true.
   Cross-platform; `.ps1` paridad; validador/neutralidad/encoding verdes; drift 0.

**Closure (rescoped):** lo de los 4 puntos verde + handoff con evidencia (clasificacion, .gitattributes,
nota v1.1.0, pin verify_release, smoke futuro). Bump **PATCH 1.9.1** + CHANGELOG (lo aplica el arquitecto al
cierre). Firma v1.1.0 INTACTA. OFF-PILOT; NO re-armar SA.4; #4 OFF; #3 ON.
