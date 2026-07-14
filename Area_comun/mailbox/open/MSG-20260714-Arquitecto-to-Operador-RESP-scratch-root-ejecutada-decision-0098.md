---
message_id: MSG-20260714-Arquitecto-to-Operador-RESP-scratch-root-ejecutada-decision-0098
from: Arquitecto
to: Operador
type: RESP
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-14
context_refs:
  - Area_comun/mailbox/answered/MSG-20260714-Operador-to-Arquitecto-DIRECTIVA-scratch-root-policy.md
  - Area_comun/decisions/DECISION-0098-scratch-root-unico-por-proyecto.md
one_line_summary: "DIRECTIVA scratch-root EJECUTADA COMPLETA: (1) DECISION-0098 draft PARA FIRMA; (2) ordenamiento hecho con tu autorizacion (raiz limpia de nova-*; 3 dirs reapeados tras verificar integracion+duplicados, 2 archivos residuales no listados movidos a D:/Aegis_Scratch/NOVA-Suite/residue/); (3) cableado template+new_instance+validador py/ps1+test+gitignore."
requested_action: "FIRMA DECISION-0098 (al firmar la sello via submit_intent). Opcional: decide reap final de los 2 residuales en residue/ (nova-9310-tx.json = tx ya aplicada; nova-a2-events.bak = ledger 2-eventos del staging A2, verificado NO presente en historia git de NOVA)."
question: "Firmas DECISION-0098?"
---

# RESP - Scratch root unico: regla formalizada + ordenamiento ejecutado + cableado

## 1. La regla -> DECISION-0098 (draft para firma)
`Area_comun/decisions/DECISION-0098-scratch-root-unico-por-proyecto.md`: 6 clausulas (regla
todos-los-proyectos con paraguas D:/Aegis_Scratch/<proyecto>/<proposito>/ y ~/Aegis_Scratch en
POSIX; fuera del arbol atestado + nunca unica copia; declarado al nacer via campo OPCIONAL
`scratch_root` -- configs PINEADOS exentos, sin re-genesis; chequeo condicional del validador;
ciclo de vida = limpieza al stand-down DECISION-0057; ordenamiento inicial documentado).

## 2. Ordenamiento (ejecutado ~17:22 con tu autorizacion explicita)
- VERIFICACION previa: nova-a2 y nova-enc = 0 commits/ramas/stash fuera de origin/main (fdeb99d);
  TODOS los secretos hallados (6 en inst-tmp + 6 en a2) = duplicados byte-identicos sha256 de los
  vivos en NOVA-Suite/NOVA/Aegis/protocol-secrets/; inst-tmp = scaffold consumido.
- REAP de los 3 dirs. Paraguas D:/Aegis_Scratch/ creado con README de convencion.
- HALLADOS 2 archivos sueltos NO listados en la DIRECTIVA: D:/nova-9310-tx.json (tx TASK-9310 ya
  aplicada) y D:/nova-a2-events.bak (respaldo del ledger 2-eventos del staging A2; verificado por
  blob-hash que NO esta en la historia git de NOVA). MOVIDOS sin destruir a
  D:/Aegis_Scratch/NOVA-Suite/residue/ -- su reap final es tuyo.
- Raiz del disco LIMPIA de nova-*.

## 3. Cableado (aditivo, compatible con pineados; gates verdes por exit-code)
- `protocol.config.template.json`: campo `scratch_root` ({{SCRATCH_ROOT}}).
- `scripts/new_instance.py`: `--scratch-root` (default <drive-del-target>/Aegis_Scratch/
  <proyecto>/ en Windows, ~/Aegis_Scratch/<proyecto>/ en POSIX); .gitignore de instancia
  attested gana guards `Aegis_Scratch/` + `.protocol-tmp/`.
- Validador `.py` Y `.ps1` (paridad): si `scratch_root` existe -> absoluta Y FUERA del arbol de
  la instancia, si no FAIL; ausente/vacio = no-op (hub pineado 2E35F26E intacto y verde).
- `scripts/test_scratch_root.py`: 7 casos (ausente/vacio/relativa/dentro/fuera + paridad ps1) = OK.
- `.gitignore` del hub: guard `Aegis_Scratch/`.
- validate + scan_encoding + neutralidad + validate(examples/minimal_instance) +
  test_attested_instancing = exit 0. Checker adversarial subagent paso previo al commit.

FONDO INTOCABLE verificado: config hub 2E35F26E / epoch 1.14.0 / dataset N=500 sin tocar.
