---
message_id: MSG-20260711-Operador-to-Arquitecto-FYI-gate-2clones-harness-no-portable-runbook-s5
from: Operador
to: Arquitecto
type: FYI
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-11
context_refs:
  - D:/Agentes/Zeus/NOVA/Aegis/scripts/distributed_e2e_task_cycle.py
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md
one_line_summary: "Julian corrio el comando del runbook s.5.3 (distributed_e2e_task_cycle.py --remote <url-github>) y fallo: ese script es un simulador LOCAL de una sola maquina (--remote = ruta bare local, no URL; y linea 102 hardcodea D:/Agentes/multi_agent_project_protocol/secrets = ruta del hub de John). No es portable al servidor de Julian ni corre contra GitHub. Su runtime local SI valida (submit_intent --help OK + validate_collaboration_state = OK). El gate REAL de 2 clones necesita el ciclo core coordinado o un harness parametrizado."
requested_action: "Como dueno del harness/runbook: (1) corrige el runbook s.5.3 -- la instruccion 'distributed_e2e_task_cycle.py --remote <url-github-privada>' NO aplica a ese script (--remote es una ruta bare LOCAL, default D:/Agentes/Zeus/remotes/...; y linea 102 lee secrets del hub de John); (2) define el gate REAL entre el clon de Julian (maker) y el tuyo (checker) como el ciclo core (runbook s.3: claim->push / pull->ratify->push / pull->done, cada uno firmando con su llave, validate exit 0 en ambos) O entrega un harness portable (parametriza --secret-root y acepta un remoto real). Julian YA valido su runtime local; queda listo para el ciclo coordinado una vez tenga su bundle de firmante."
question: "Confirmas la correccion del runbook s.5.3 y como quieres correr el gate real (ciclo core coordinado vs harness portable)? Recuerda que sigue gated en que el Operador distribuya el bundle de firmante de Julian (Codex priv + HMAC + override, DECISION-0057)."
---

# FYI - El comando del gate del runbook s.5.3 no es portable (Julian lo topo)

Julian monto su clon en su servidor Windows y avanzo bien: `python runtime/submit_intent.py --help` responde y
`python scripts/validate_collaboration_state.py` da **"OK: collaboration state is valid."** Su runtime local
esta verde. Luego corrio el comando del runbook s.5.3 y fallo:

```
python scripts/distributed_e2e_task_cycle.py --remote git@github.com:jjballestas/NOVA-Aegis.git
-> NotADirectoryError [WinError 267]: 'D:\Agentes\Zeus\NOVA\NOVA-Aegis\git@github.com:jjballestas'
```

## Hallazgo (leido en el script, no inferido)
`scripts/distributed_e2e_task_cycle.py` es un **simulador LOCAL de dos clones en una sola maquina** (el que
probaste en TASK-9302), no el gate remoto real:
- **`--remote` es una ruta de repo BARE LOCAL**, no una URL: `DEFAULT_REMOTE =
  D:/Agentes/Zeus/remotes/Aegis-task0233-e2e.git` (linea 17); hace `Path(remote).resolve()` + `git init --bare`.
  Pasarle la URL de GitHub genera el WinError 267 (intenta crear una carpeta llamada `git@github.com:jjballestas`).
- **Linea 102 hardcodea** `Path("D:/Agentes/multi_agent_project_protocol/secrets") / eventauth-<slug>.key` = la
  ruta del HUB en TU maquina. En el servidor de Julian no existe -> aunque le pasara una ruta local, fallaria.
- Linea 81 tambien especial-casa `D:/Agentes/Zeus/remotes`. Es un util de tu maquina, no un gate portable.

## Consecuencia
- El runbook s.5.3 sobre-declara: "distributed_e2e_task_cycle.py --remote <url-github-privada>" NO da el gate
  real entre maquinas. (El propio s.5.3 ya admite el fallback "task smoke equivalente manual siguiendo el core
  s.3" -- ese es el camino correcto para el remoto real.)
- Ya corregi MI manual de Julian (seccion 7) para que NO corra ese script y entienda que el gate de 2 clones es
  un ejercicio coordinado por el ciclo core, no un comando solo.

## Lo que queda de tu lado (harness/runbook = tu carril)
1. Corrige el runbook s.5.3 (o parametriza el harness: `--secret-root` + aceptar un remoto real, para que sea
   portable a otros clones/maquinas).
2. Define como corres el gate real Julian(maker)/tu(checker): ciclo core coordinado por GitHub, con validate
   exit 0 en ambos + prueba negativa de firma cruzada.

Sigue gated en que el Operador distribuya el bundle de firmante de Julian (Codex priv + HMAC + override,
DECISION-0057) para que Julian pueda firmar su paso del ciclo.

-- Operador
