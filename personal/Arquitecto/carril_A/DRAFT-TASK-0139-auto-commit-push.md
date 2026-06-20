# DRAFT - TASK-0139: Auto commit+push gobernado del intake (cerrar el ciclo en la app) (SPEC-0086 ext6, AC27/AC28)

> DRAFT en personal/Arquitecto; NO promovido. Espera ratificacion (REQ-444E0DE5 -> DECISION-0054 + ext6 SPEC-0086).
> maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA (transporte/egress) antes de cerrar. Codigo en Zeus
> (server). OFF BY DEFAULT; push vivo = GO posterior del operador.

- spec: SPEC-0086 (ext6, AC27/AC28; carry AC11/AC17)
- decision: DECISION-0054 (superficie de transporte)
- origen: REQ-444E0DE5 (semilla del operador via intake)
- status propuesto al promover: ready (Codex)
- code_repo: D:/Agentes/Zeus/Zeus-protocol

## Alcance
1. **Server (Zeus):** tras un EXECUTE gobernado EXITOSO, si la capacidad esta ON: `git add` de EXACTAMENTE las
   rutas reportadas por submit_intent (task/seed + ledger/state +slim); `git commit` con mensaje TEMPLADO
   server-side (ASCII, deriva de actionId+id+seq); `git push` al remote/branch pre-configurado. Sin `git add -A`,
   sin texto libre del cliente, sin force-push.
2. **Resultado honesto:** solo push OK -> "enviado + aterrizado en canonico (HEAD sha, seq)" reales; push fallido
   (red/auth/non-fast-forward) -> error real, NO verde, resultado=NO-aterrizado; non-fast-forward -> error seguro.
3. **Config OFF-by-default** en registro FUERA del config pinned (estilo connectors.config.json): flag enabled +
   remote + branch. Default disabled.
4. **Front:** con capacidad ON, la UI refleja el aterrizaje (HEAD, seq) o el error; con OFF (default) el flujo no
   cambia.

## DoD
- AC27 (commit+push acotado/atomico/honesto; el HEAD pusheado valida exit 0) + AC28 (anti-commit-arbitrario +
  anti-egress: sucio ajeno no entra, cliente no inyecta rutas/mensaje, no force-push, front sin credenciales)
  verdes como tests de COMPORTAMIENTO permanentes. Carry AC11/AC17.
- Camino feliz contra un remote/clon de PRUEBA (no el remote vivo): add acotado -> commit -> push -> HEAD+seq
  reales; clon limpio del HEAD pusheado valida exit 0.
- #4 epoca 1.14.0 BYTE-IDENTICA; validate con/sin secretos exit 0; drift 0; node --test/CI verde; npm start
  ejecutable; neutralidad/encoding limpio.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. PASADA DEL ANALISTA (bounding del
  transporte + egress de credenciales) ANTES de cerrar (la activa el operador). Commit como Arquitecto +
  Co-Authored-By: Codex.

## Fuera de alcance
- Push VIVO contra el remote real (gateado por GO posterior del operador; esta task entrega la capacidad OFF y
  probada contra remote de prueba).
- Manejo automatico de merges/conflictos mas alla de "non-fast-forward -> error seguro".
- Cualquier `git add -A` / commit de working-tree arbitrario / force-push / texto libre del cliente en el mensaje.
