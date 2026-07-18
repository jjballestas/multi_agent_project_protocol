---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-rubric-enrutado-peon-vs-codex
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-tramo-t2-cerrado-topologia-adoptada.md
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-topologia-autor-arquitecto-qc-codex-bounce.md
one_line_summary: "GO: materializa el RUBRIC DE ENRUTADO (peon-vs-Codex) como artefacto con 5 filtros; ruta a peon SOLO si se cumplen los cinco. Calibralo con el grid (T1 paso / T2 borrador son los 2 primeros datos) y mide tu tasa de acierto de enrutado vs el mejor tier empirico. La discernimiento no carga sola: rubric + calibracion + bounce-backstop la reparten. Demo NO citable."
---

# DIRECTIVA - Rubric de enrutado (peon vs Codex) como artefacto calibrable

## Por que
La topologia aplanada solo funciona si enrutas razonablemente (no perfecto): mal-enrutar una
tarea sobre el techo del peon cuesta mas que hacerla directo (leccion B1). Materializa el
criterio como artefacto explicito y auditable, no como juicio implicito.

## Los 5 filtros (ruta a PEON solo si se cumplen los CINCO; si falla uno -> Codex)
1. ESPECIFICABLE A COMPLETITUD MECANICA: se puede escribir una spec que fije la respuesta como
   aplicacion de patron. Si exige inventar estructura, decidir tradeoffs o inferir intencion no
   dicha -> Codex.
2. GATE OBJETIVO Y DURO (no negociable): pass/fail mecanico (tests/asserts/type-check). Si la
   correccion es juicio subjetivo -> Codex. Este filtro es la defensa contra el unico fallo que
   el bounce NO caza (peon produce algo mal-pero-plausible): con gate duro el QC no se engana.
3. CONTEXTO LOCAL: cabe en la ventana del peon sin sostener medio repo. Radio amplio / cross-file
   -> Codex.
4. FAMILIA REPETIDA: N-esima instancia de un patron con spec reutilizable (hallazgo B0-reuse).
   One-off novel -> Codex (spec no amortiza + riesgo de calibracion alto).
5. FALLO NO CATASTROFICO: aunque el peon pudiera, si un error sutil es grave y dificil de cazar
   en QC (PII, ledger, genesis, seguridad, codigo soberano) -> Codex por principio. Este filtro
   se aplica DURO: ante cualquier duda de soberania/seguridad, Codex.

## Calibracion (la discernimiento NO es a priori)
El grid ES la base de conocimiento del enrutador. Primeros dos datos ya tuyos:
- T1 (patron puro, baja variacion): peon PASA (3b 10/10). Zona peon-apta.
- T2 (parser con variacion, gate 18 asserts): NINGUN peon paso a la primera; verde a la 2a con
  1 correccion. El peon aporta BORRADOR, no producto -> zona FRONTERA (bounce-apta, no
  peon-solo). Refina el filtro 1: a mayor VARIACION/edge-cases, el peon degrada a borrador.
Actualiza el rubric con cada tramo (T3, T4, escala) anclando cada filtro a evidencia real.

## Metrica de la propia discernimiento
Mide tu TASA DE ACIERTO DE ENRUTADO: por celda, registra el tier que elegiste vs el mejor tier
empirico observado (peon-solo / bounce / Codex-directo). Ese numero dice si el rubric enruta bien.

## Marco
Artefacto en tu area (personal/Arquitecto/), versionado, referenciado desde el diseno del
piloto. Demo PRIVADA, NO citable. Fondo intocable N=500 / 2E35F26E / epoch 1.14.0. No bloquea la
celda de escala en curso; el rubric se materializa en paralelo y se calibra al cerrar cada tramo.

## Nota sobre el sello (respondo tu matiz)
El check via claude-per-0101 subagent respeta maker!=checker por proveedor; para una demo
PRIVADA NO hace falta levantar el cron del Analista. Mantenlo en subagent; si el piloto
escalara a un confirmatorio sellado, ahi si reactivamos el Analista formal. No spin-up de infra
para el piloto.

-- Operador (via Asesor). 18-jul.
