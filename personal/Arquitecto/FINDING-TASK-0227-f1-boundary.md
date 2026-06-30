# FINDING TASK-0227 -- Diagnostico boundary F1 / `submit_intent` (Arquitecto)

Fecha: 2026-06-30 · Autor: Arquitecto · Repo producto: `D:\Agentes\Zeus\Zeus-Aegis`
(codigo bajo `vendor/hermes-2.3.0/`). linked: DECISION-0064 (F1 read-only), DECISION-0069 (ceremonia
preparar-comando atestada), DECISION-0050.

## Pregunta
El test `governance-readonly.test.ts:160` "does not expose direct ledger write surfaces in F1 routes"
falla porque `src/routes/governance.tsx` contiene el literal `submit_intent` (assert linea 169).
Es (a) una fuga real de F2 dentro de F1, o (b) un test obsoleto/sobre-amplio post-sello?

## Evidencia (falsable)
1. **Sin write-path de red.** Los unicos `fetch` en `governance.tsx` son GET read-only:
   - `:228` `fetch(url, { cache: 'no-store' })`
   - `:300` `fetch('/api/governance/health?refresh=1', ...)`
   - `:303` `fetch('/api/governance/metrics?project=...', ...)`
   CERO `POST/PUT/PATCH/DELETE`, cero axios, cero XHR. El assert `:168` (no fetch con metodo de escritura) PASA.
2. **Las rutas server no exponen el writer.** Los asserts `:166-167` (combinedRoutes sin `submit_intent.py`
   ni `Area_comun/state/`) PASAN. La lista `GOVERNANCE_FORBIDDEN_WRITE_PATTERNS` en
   `server/governance-readonly.ts:824` sigue intacta.
3. **Los `submit_intent` de `governance.tsx` son TEXTO inerte** del helper read-only "Preparar archivado":
   - `:645` tooltip: "...Read-only: el panel NO escribe el ledger; copias el comando y lo ejecuta el Arquitecto."
   - `:911-916` `buildArchiveTransaction()`: construye un STRING JSON `{intents:[...]}` client-side. Comentario:
     "Pure client-side, no fetch, no writer-path."
   - `:997` literal del comando CLI `python runtime/submit_intent.py --intents archive-mailbox.json ...` (a copiar).
   - `:1054-1055` copy de UI: "El panel NO escribe el ledger (F2 gateado)... Copia este submit_intent y ejecutalo
     el Arquitecto."

## Veredicto
**(b) Test obsoleto / sobre-amplio. NO es fuga de boundary.** El panel solo LEE (GET) y GENERA texto de
comando que un humano/Arquitecto ejecuta fuera del panel. Es exactamente el patron *preparar-comando*
sancionado por DECISION-0064 (F1 read-only) y DECISION-0069 (ceremonia atestada preparar-comando), y el mismo
que TASK-0223 describe ("modo preparar-comando... NO ejecuta"). El assert literal `:169` quedo sobre-amplio: el
helper "Preparar archivado" (read-only) introdujo el literal `submit_intent` en texto de ayuda, y el ban
ciego del string lo marca como si fuera escritura.

**No hay relajacion F1->F2.** F1 sigue read-only; F2 sigue gateado. Esto NO requiere una DECISION de
relajacion de boundary; es una correccion de PRECISION del test, cubierta por DECISION-0064/0069 vigentes.

## Direccion de arreglo (para 0227)
1. **Precisar el assert `:169`**: en vez del ban ciego `not.toContain('submit_intent')`, afirmar la invariante
   real -> sin write-path: ningun `fetch(... submit_intent ...)` ni `method: POST/PUT/PATCH/DELETE`, y que cada
   mencion de `submit_intent` en la UI vaya acompanada del guard "NO escribe el ledger" (preparar-comando).
   Conservar los dientes `:166-168` y `GOVERNANCE_FORBIDDEN_WRITE_PATTERNS`.
2. **Arreglar #1** (timeout `governance-readonly` "lists artifacts, decisions, handoffs, and ledger events"):
   pre-warm/poll/timeout adecuado, sin enmascarar fallo legitimo.
3. `npm test` exit 0 en clon limpio, sin enmascarar fallos reales.

## Nota de gobernanza
Hago la llamada de boundary como Arquitecto y la documento aqui (no la decido en silencio). Si el operador
prefiere un addendum DECISION explicito en vez de apoyarse en 0064/0069, lo planteo; mi juicio es que esta
cubierto y solo es precision de test.
