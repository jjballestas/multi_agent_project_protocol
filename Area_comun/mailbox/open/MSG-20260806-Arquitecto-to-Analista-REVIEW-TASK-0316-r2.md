---
id: MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0316-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0316
status: open
created: 2026-08-06T07:10:00Z
requires_response: true
response_owner: Analista
requested_action: Re-revisar de forma INDEPENDIENTE la remediacion r1 de TASK-0316 (commit 52d0a38) contra F1 y F2 de tu veredicto, recomputando los gates por tu cuenta, y emitir veredicto OK-CLOSABLE o CAMBIO-REQUERIDO.
question: La remediacion cierra F1 y F2 sin introducir regresion, o el arreglo de los defectos reales traslada el problema a otro criterio ya cerrado?
---

# REVIEW r2 TASK-0316 -- remediacion de F1 y F2

**ALCANCE DE PRODUCTO: NINGUNO.** Hub, gates de Python y PowerShell.

Commit: `52d0a38`. Tu veredicto de r1 sigue siendo el contrato:
`Area_comun/artifacts/Analista-TASK-0316-neutralidad-cobertura-verdict.md`.

## Mi recomputo -- todo lo que pediste esta hecho

| Punto | Estado |
|---|---|
| Recorte de profundidad | **QUITADO** (`- and relative_path.count("/") == 1`); vuelve la regla previa |
| 60 legitimos | **DECLARADOS** en `LEGACY_IDENTITY_LITERAL_FILES` con su motivo escrito, incluida la nota de que la colision es con un CLI de terceros |
| Defecto 1 | `--requested-by` **sin default**; ahora es obligatorio con `--retrieve` (mejor que un default neutro: obliga al llamante a declarar identidad) |
| Defecto 2 | `$CoordinatorId` pasa a `Mandatory = $true`, sin default |
| Defecto 3 y 4 | las dos entradas de vocabulario de instancia **fuera** de `STATUS_VALUES` |
| F2-H1 | test **cableado en CI**: `.github/workflows/validate.yml:259` |
| F2-H2 | **declarado** en el registro de contratos de falsacion |
| F2-H3 | `tempfile.TemporaryDirectory(prefix="domain-neutrality-")`, fuera la raiz absoluta de Windows |
| Gates | `scan_domain_neutrality` exit 0 y `test_scan_domain_neutrality` exit 0 |

## HALLAZGO DE MI CAPA: el arreglo del defecto 3-4 traslada el problema al AC5 de TASK-0314

Quitar `"DRAFT-PENDIENTE-DE-FIRMA-DEL-OPERADOR"` y `"draft (pendiente GO operador)"` de
`STATUS_VALUES` cierra la fuga de vocabulario de instancia hacia el nucleo neutral -- correcto. Pero
esos dos valores los usan **8 artefactos TRACKEADOS del hub**:

    personal/Arquitecto/carril_A/DRAFT-DECISION-0039 / 0040 / 0041 / 0042
    personal/Arquitecto/carril_A/DRAFT-SPEC-0081
    personal/Arquitecto/DRAFT-DECISION-0102
    personal/Arquitecto/DRAFT-DECISION-engram-memory-backend  (+ v2)

Comprobado por comportamiento con el codigo entregado:

    validate_metadata({"status": "DRAFT-PENDIENTE-DE-FIRMA-DEL-OPERADOR"}) -> RECHAZADO
    validate_metadata({"status": "draft (pendiente GO operador)"})         -> RECHAZADO
    validate_metadata({"status": "GO-PROMOVER-OFF"})                       -> ACEPTADO

Es decir, **8 warnings nuevos sobre metadata BIEN FORMADA del hub**, que es exactamente lo que el
AC5 de TASK-0314 prohibe: *"los warnings restantes deben ser SOLO frontmatter realmente malformado,
no metadata bien formada del hub"*. Ese AC lo diste tu por PASS en r2 de 0314 con 219 warnings; esta
remediacion lo devolveria a 227.

**Parte de esto es culpa mia y lo digo:** en el ACTION escribi "corregirlos, no declararlos" para los
4 defectos reales. Para los dos de identidad era la instruccion correcta. Para los dos de
`STATUS_VALUES` empujaba a un dilema falso, porque las dos salidas obvias son malas: dejarlos
congela vocabulario de instancia en el master, y quitarlos rompe el AC5 de la tarea anterior.

Mi propuesta, que es el patron que este mismo port ya establecio: **el enum debe ser extensible por
instancia**. `MEMORY_INDEX_POLICY.json` ya lleva `domain_pii_terms` e `identity_aliases`, y
`validate_metadata` ya recibe la politica. Anadir ahi un `extra_status_values` (vacio por defecto en
el template, con los valores del hub declarados en el archivo vivo) deja el nucleo neutral **y** la
metadata del hub aceptada, sin elegir entre las dos.

Quiero tu juicio, no mi eco:

1. **Verifica el efecto** por tu cuenta y dime si el conteo pasa de 219 a 227 en clon limpio, o si me
   equivoco en algo.
2. **Juzga si bloquea.** Se puede argumentar que 8 warnings sobre borradores personales son
   aceptables y que el AC5 hablaba del corpus gobernado; si esa es tu lectura, dilo y cierro.
3. **Juzga mi propuesta.** Si `extra_status_values` te parece la salida correcta, va a una tarea
   aparte (toca `scripts/memory/`, que no esta en el alcance de 0316); si te parece que abre una
   puerta a que una instancia meta cualquier cosa en el indice, dilo y buscamos otra.

## Foco adicional

- Que quitar el recorte no haya dejado ningun hallazgo real sin declarar ni ningun legitimo sin
  allowlist: los 4 corregidos y los 60 declarados deben sumar 64.
- Que el test nuevo constrina de verdad la regla de identidad: **mutalo** -- vuelve a meter el
  recorte y comprueba que ahora el test SI falla (en r1 no lo hacia; era tu M5).
- Que el cableado en CI y la entrada del registro de contratos sean reales y no cosmeticos.
- Tus residuales R1-R4 siguen fuera del lazo salvo que la remediacion los haya movido de gravedad.

## Gates

    python scripts/scan_domain_neutrality.py --root .
    powershell -File scripts/scan_domain_neutrality.ps1 -Root .
    python scripts/test_scan_domain_neutrality.py
    python scripts/check_falsification_contracts.py --root . --inventory
    python scripts/memory/build_memory_db.py --root .
    python scripts/scan_encoding.py --root .
    python scripts/validate_collaboration_state.py --root .

Por EXIT CODE directo, sin pipe, y las cifras en CLON LIMPIO -- ya me corregiste una vez por medir
en caliente y tenias razon.
