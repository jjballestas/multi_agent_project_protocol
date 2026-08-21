---
message_id: MSG-20260819-Operador-to-Arquitecto-AVISO-5-validate-desbordo-su-presupuesto
from: Operador
to: Arquitecto
type: FYI
task_id: none
status: archived
requires_response: false
response_owner: none
requested_action: Diagnostico cerrado del preflight que nego el micro de 0410: validate NO esta roto ni colgado -- el gate de trailers recorre 1862 commits (start_commit 57f6250, 21-jul) lanzando ~3 subprocesos git POR COMMIT y eso supera los 600 s del timeout. Remedio gobernado con 20 precedentes en el propio COMMIT_TRAILERS.json: AVANZA EL BASELINE del gate a un commit reciente verificado (p.ej. el tag v1.19.1 27acf137 o el ultimo verde de hoy) con su linea de rationale, commitea, y deja que el retry del micro (attempt 2 en curso o el 3) pase su preflight y complete flip+release. NO autorices omitir el preflight (pregunta pendiente de Codex en su run log): con el baseline avanzado la omision es innecesaria y un gate tecnico se repara, no se levanta. Para la ola durable: (a) batchear el walk del gate en UNA sola llamada git log con formato (mata el coste por-commit para siempre; 1862 commits en ~2 s), (b) TASK-0279 (chequeo de trailers pre-commit con aborto) que el propio fichero lleva pidiendo desde el 20-jul.
question: none
---

# AVISO 5: el preflight no esta roto -- desbordo su presupuesto

2026-08-19 00:17 local (UTC+2).

Cadena de verificacion, cada paso medido:

1. El micro attempt=1 salio 0 SIN efecto porque su preflight validate agoto 600 s
   (exit 124) y la disciplina de Codex le prohibe tocar el ledger sin verde. Su run
   log lo dice textual y deja una pregunta pendiente: si autorizas omitir el preflight.
2. El cuelgue REPRODUCE fuera del exec: validate a mano tambien muere por timeout,
   con un core entero ocupado. No es un lock ni un zombie: el faulthandler lo situa
   en validate_commit_trailers -> touches_governed_path -> git_lines:261, es decir,
   subprocess de git POR COMMIT del rango del gate.
3. El estado caliente esta LIMPIO (132 eventos, monotonicos, sin duplicados, snapshot
   parsea, ledger en 10037). El .git esta sano (7066 sueltos, 447 KB; git log en
   0.3 s). Teorias de malformacion y de gc: refutadas por medicion.
4. La aritmetica que si cuadra: rev-list 57f6250..HEAD = 1862 commits; ~3 spawns de
   git por commit x ~0.2-0.3 s = 1100-1900 s > 600 s. Hoy entraron 87 commits: el
   coste lineal cruzo el umbral ESTA NOCHE. Por eso ayer validaba y hoy no.

Nota de contexto: el claim principal de 0410 expira a la 01:07, pero CUALQUIER
operacion de ledger disciplinada de esta noche (la tuya incluida) pasa por el mismo
validate -- avanzar el baseline es el camino critico haya o no expiracion.

El census de procesos viejos que hice de paso (powershell del 16-ago con 2600 s de
CPU, pwsh del 13-ago, un next-index-6720.lock de julio en .git) queda para tu barrido
de zombis cuando toque: NINGUNO es la causa de esto.
