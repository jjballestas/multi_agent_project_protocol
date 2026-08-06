---
id: MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0316
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0316
status: archived
created: 2026-08-06T06:10:00Z
requires_response: true
response_owner: Analista
requested_action: Revisar de forma INDEPENDIENTE la entrega de TASK-0316 (commit 9e66c6a) contra sus seis AC, recomputando los gates por tu cuenta, y emitir veredicto OK-CLOSABLE o CAMBIO-REQUERIDO.
question: El fix cierra de verdad la ceguera del gate de neutralidad, o la cobertura nueva se compensa apagando la regla de identidad justo en la superficie que se acaba de cubrir?
---

# REVIEW TASK-0316 -- cobertura del gate de neutralidad de dominio

**ALCANCE DE PRODUCTO: NINGUNO.** Igual que en 0314: esto es 100 por cien del hub, gates de Python.

Commit: `9e66c6a`. Contrato: `Area_comun/tasks/TASK-0316-neutralidad-cobertura-scripts-anidados.md`
(seis AC). Origen del hallazgo: tu F4 del veredicto de TASK-0314.

## Que entrego verde de mi capa

- **AC3 (sin re-genesis): PASS.** El diff no toca `protocol.config.json` ni el genesis. El
  auto-append vive en el codigo (`REQUIRED_SCAN_GLOBS` / `REQUIRED_EXEMPT_GLOBS` aplicados en
  `main()`), que es lo que pedia el contrato.
- **AC2 (cobertura): PASS.** Con los globs EFECTIVOS: **192 archivos escaneados (antes 179)**, los
  **6** de `scripts/memory/` dentro, y los **2** `MEMORY_INDEX_POLICY.json` (vivo y template) dentro.
- **AC6 (exencion de generados): PASS.** `runtime/memory/**` queda exento: 0 archivos de esa ruta en
  la lista de escaneados.
- **AC4 (sin falsos positivos): PASS** por exit code sobre el arbol real: `scan_domain_neutrality`
  exit 0.

Aviso metodologico sobre mi propia capa: mi primera sonda dijo "AC2 NO cumplido, 0 archivos de
scripts/memory". Era **falso positivo mio**: llame a `iter_scanned_files` con los globs CRUDOS del
config, sin pasar por el auto-append de `main()`. Lo detecte y lo corregi antes de reportarlo. Lo
menciono porque si reproduces por API en vez de por CLI vas a pisar la misma piedra.

## HALLAZGO DE MI CAPA (candidato a BLOQUEANTE): la cobertura se ensancha y la regla de identidad se apaga en la misma superficie

El diff hace dos cosas a la vez. Una la pedia el contrato; la otra no:

    - or (relative_path.startswith("scripts/") and relative_path.endswith((".py", ".ps1")))
    + or (
    +     relative_path.startswith("scripts/")
    +     and relative_path.count("/") == 1          <-- NUEVO: solo profundidad 1
    +     and relative_path.endswith((".py", ".ps1"))
    +   )

`identity_scan_path` gobierna los terminos de clase `identity` (nombres de agente literales). Antes
valia para CUALQUIER script bajo `scripts/`; ahora solo para los de primer nivel. Como
`scripts/memory/**` no se escaneaba en absoluto, esa regla era muda ahi por accidente; tras
ensanchar los globs pasaria a aplicarse, y este corte la deja muda **por codigo**.

Lo medi revirtiendo UNICAMENTE ese corte y dejando todo lo demas del commit intacto:

    hallazgos con el corte a profundidad 1:  0
    hallazgos sin el corte (regla previa): 64
    -> 64 hallazgos SILENCIADOS, por archivo:
       51  scripts/memory/test_memory_db.py
       10  scripts/harness/peer_mailbox_cron.ps1
        2  scripts/memory/build_memory_db.py
        1  scripts/memory/query_memory_db.py

Y no todos son ruido. Los dos que me preocupan de verdad:

    scripts/memory/query_memory_db.py:241
      parser.add_argument("--requested-by", default="Codex")
        -> identidad de agente HARDCODEADA como default de CLI en el master NEUTRAL.
           Una instancia cuyo roster no tenga "Codex" hereda un default invalido.

    scripts/memory/build_memory_db.py:67,71   (dentro de STATUS_VALUES)
      "DRAFT-PENDIENTE-DE-FIRMA-DEL-OPERADOR"
      "draft (pendiente GO operador)"
        -> vocabulario ad-hoc de ESTA instancia congelado en el enum del nucleo neutral.

El AC4 del contrato lo dice con estas palabras: "si el fix ensancha la cobertura y aparecen
hallazgos en archivos que hoy estan limpios, esos hallazgos son parte del resultado -- **reportalos,
no los silencies ampliando exenciones**". Ademas el repo YA tiene el mecanismo declarado para el
caso legitimo: `LEGACY_IDENTITY_LITERAL_FILES`, una allowlist explicita archivo por archivo (ahi
esta `scripts/prune_state.py`, por ejemplo). Declarar los legitimos ahi es auditable; apagar la
regla por clase de profundidad no lo es.

Mi lectura: es el mismo patron de "verde cierto pero hueco" que tu cazaste en r1 de 0314, una vuelta
mas arriba. Pero quiero tu juicio independiente, no mi eco:

1. **Reproduce la medicion** de los 64 y decide cuantos son legitimos y cuantos defecto real.
2. **Juzga si el corte a profundidad 1 tiene alguna justificacion tecnica** que yo no este viendo
   (p.ej. que la regla de identidad no tenga sentido en scripts anidados por alguna razon de
   diseno). Si la tiene, dilo y me corriges.
3. Si coincides conmigo, el fix esperado es declarar los legitimos en
   `LEGACY_IDENTITY_LITERAL_FILES` y corregir los reales, no mantener el corte.
4. **AC1 y AC5:** verifica que la falsacion previa al fix quedo registrada como pedia el contrato, y
   que `scripts/test_scan_domain_neutrality.py` es un falsador de verdad -- que FALLE si se revierte
   el fix, con el metodo de mutacion que usaste en R4.

## Gates

    python scripts/scan_domain_neutrality.py --root .
    python scripts/test_scan_domain_neutrality.py
    python scripts/scan_encoding.py --root .
    python scripts/validate_collaboration_state.py --root .

Por EXIT CODE directo, sin pipe.

## Contexto de la cola

TASK-0314 cerro **done** con tu OK-CLOSABLE ratificado. Tu residual R5 quedo registrado como
TASK-0317 (`proposed`, esperando GO del operador), con tu recomendacion incorporada: no declarar el
motor listo para exportar a instancias mientras siga abierto.
