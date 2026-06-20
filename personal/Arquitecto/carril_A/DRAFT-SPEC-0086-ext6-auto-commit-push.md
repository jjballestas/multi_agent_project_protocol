# DRAFT - Extension 6 de SPEC-0086: cerrar el ciclo en la app (auto commit+push gobernado) [RF-14]

> DRAFT en personal/Arquitecto; NO promovido. Triage del REQ-444E0DE5 (semilla del operador, intake).
> SUPERFICIE DE TRANSPORTE -> bajo DECISION-0054. maker=Codex / checker=Arquitecto + pasada del Analista.
> Codigo en Zeus-protocol (server). OFF BY DEFAULT.

## Origen (REQ-444E0DE5, author=Operador)
"Tras confirmar un EXECUTE no quiero bajar a la terminal a git add/commit/push; quiero que la app aterrice el
cambio en canonico." Aceptacion: la app commitea SOLO lo que escribio submit_intent (seed + ledger/state) con
mensaje claro y pushea al remote configurado, como parte de la transaccion; resultado atomico "enviado +
aterrizado (HEAD, seq)"; push fallido -> error NO verde; NO commitea working-tree arbitrario (add acotado;
prueba negativa: sucio ajeno no entra).

## AC27 (NUEVO) - Auto commit+push gobernado, acotado, atomico y honesto [comportamiento PERMANENTE; DECISION-0054]
- Tras un EXECUTE gobernado EXITOSO (requirement-intake / mailbox-archive), si la capacidad esta habilitada, el
  server hace `git add` de EXACTAMENTE las rutas reportadas por la transaccion submit_intent (task/seed file +
  `events.jsonl`/`snapshot.json`/`CLAIMS`/`PROJECT_STATE`/`TASK_INDEX`(+slim)), `git commit` con mensaje TEMPLADO
  server-side (ASCII; deriva de actionId+id+seq), y `git push` al remote/branch PRE-CONFIGURADO.
- **Resultado HONESTO (hereda AC11):** solo con push OK se reporta "enviado + aterrizado en canonico" con el
  **HEAD (sha)** y el **seq** REALES; si el push FALLA (red/auth/non-fast-forward) -> error real visible, NO
  verde, resultado = NO-aterrizado (el commit local puede existir, pero no se afirma aterrizado).
- **OFF BY DEFAULT:** capacidad deshabilitada por defecto; flag + remote/branch en registro FUERA del config
  pinned (#4 epoca 1.14.0). Push vivo contra el remote real = GO posterior del operador.
- **Snapshot consistente:** commitea exactamente los outputs -> el clon limpio valida desde git HEAD (regresion-
  proof estilo AC22: tras el auto-commit+push, el HEAD pusheado valida exit 0).

## AC28 (NUEVO) - Anti-commit-arbitrario y anti-egress inseguro (prueba negativa PERMANENTE) [CRITICO; DECISION-0054]
Tests permanentes (no reabrir):
- un archivo **SUCIO AJENO** en el working tree (no escrito por la transaccion) NO entra al commit (add explicito
  de rutas derivadas server-side; NUNCA `git add -A`/`.`).
- el cliente **NO puede inyectar** rutas ni el mensaje de commit (ambos server-side).
- **NO force-push:** `--force`/`--force-with-lease` ausentes; non-fast-forward -> error SEGURO "remote advanced"
  (nunca sobrescribe el remote).
- el front **NUNCA** recibe/almacena credenciales (git las resuelve via el credential helper del entorno).
- el commit+push NO emite eventos ni muta el ledger (solo persiste en git lo que submit_intent escribio);
  **#4 byte-identica** (config/genesis/keys sin cambio; se asierta antes/despues).

## test_plan (anadido)
- **Server (Zeus):** camino feliz (capacidad ON contra un remote/clon de prueba): add acotado -> commit templado
  -> push -> resultado con HEAD+seq reales; el HEAD pusheado valida exit 0 (clon limpio). Negativos: sucio ajeno
  no entra; inyeccion de ruta/mensaje rechazada; push fallido -> error NO verde; non-fast-forward -> error
  seguro sin force.
- **Front:** tras EXECUTE OK con capacidad ON, la UI muestra "aterrizado (HEAD, seq)"; con push fallido muestra
  error y NO verde. Con capacidad OFF (default), el flujo actual no cambia.
- **Gates protocolo:** validate con/sin secretos exit 0; drift 0; #4 byte-identica; neutralidad/encoding 0.

## Carry permanentes
AC11 / AC17 (no-bypass: el commit+push NO es un 2o escritor del ledger) / AC19-AC20 disciplina (cuelga del
execute gobernado, no accion arbitraria). #4 epoca 1.14.0 byte-identica. OFF by default; uso vivo = GO operador.
