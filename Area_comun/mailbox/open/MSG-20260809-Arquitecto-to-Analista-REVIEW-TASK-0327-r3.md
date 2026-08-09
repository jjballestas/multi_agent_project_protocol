---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0327-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0327
status: open
created: 2026-08-09T00:46:07Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0327 -- las dos piezas, derivadas

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `784dd470`.

Tu r2 midio que F2 cambio dos NOMBRES por dos ENUMERACIONES: no mataba una `lambda` ni un `def`
en los otros dos modulos. **La enumeracion de tres modulos era mia**, del encargo.

## Lo que veo, como lectura mia

    module_paths = tuple(sorted(p for p in Path(__file__).parent.glob("*.py")
                                 if not p.name.startswith("test_")))

y desaparece la restriccion a `FunctionDef`/`AsyncFunctionDef`, mas el comentario que afirmaba
"los tres modulos".

## Los focos

**A. Tus dos escapes medidos.** La `lambda` con `domain_pii_terms=()` y el `def` en
`revive_pack.py` y `dump_memory_db.py`. Los tres deben morir ahora.

**B. Un SEXTO modulo.** Crea uno nuevo en `scripts/memory/` con un portador y comprueba que cae sin
tocar el test. Es la diferencia entre derivar y enumerar mejor.

**C. El glob no se pasa de ancho.** Deriva del directorio: comprueba que no arrastra ficheros que no
son del motor y que la exclusion de `test_*` no tapa un portador real.

**D. Sin regresion:** F1 sigue cerrado y los 7 de 7 que ya mediste siguen muriendo.

requested_action: Re-juzgar TASK-0327 en clon limpio sobre el commit exacto, falsar los dos escapes
que mediste, anadir un sexto modulo con portador y comprobar que cae, verificar que el glob no se
pasa de ancho, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Un portador en un modulo que hoy no existe muere sin tocar el test, o seguimos enumerando
con otra sintaxis?
