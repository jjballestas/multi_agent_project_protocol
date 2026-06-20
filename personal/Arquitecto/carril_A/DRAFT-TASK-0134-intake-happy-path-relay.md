# DRAFT - TASK-0134: Fix camino feliz del intake (RF-14) - relay-signer + happy-path test + UX project-first

> DRAFT en personal/Arquitecto; NO promovido. Espera ratificacion de DECISION-0052 + ext2 SPEC-0086.
> maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol. Sucesor de TASK-0133 (done pero con el camino
> feliz NO demostrado = falla de verificacion del checker; ver REPLY al operador).

## Por que TASK nueva y no reabrir 0133
TASK-0133 quedo `done`; reabrir un done complica el ledger. La correccion (write real + relay + test del
happy path + UX) entra como TASK-0134, encadenada a 0133 y a DECISION-0052. (Si el operador prefiere reabrir
0133, lo ajusto.)

## Alcance
1. **Relay-signer (DECISION-0052):** el front emite EXECUTE con `actorId:"Arquitecto"` (no `Operador`); el
   payload requirement lleva `author:"Operador"`, `origin:"front-intake"`, `relayed_by:"Arquitecto"`. La
   transaccion envuelve `claim acquire (Arquitecto) -> task_upsert requirement -> claim release`.
2. **CAMINO FELIZ (AC15 revisado):** test de comportamiento que prueba `execute+confirm` -> escritura REAL
   por submit_intent (requirement en TASK_INDEX/PROJECT_STATE, seq, drift 0). NO solo dry_run/409.
3. **Atribucion honesta (AC18):** la UI declara "firmado por el Arquitecto en nombre del Operador"; evento
   con author=Operador + relayed_by=Arquitecto.
4. **UX (Claude Design):** project-first (selector de proyecto primero; demas campos habilitados tras elegir
   proyecto) + tipografia del selector destacada. Construir contra el rework de `components/intake/`.
5. Mantener AC14/AC16/AC17 + carry AC11/AC12/AC13.

## DoD
- AC15 (negativo **y** camino feliz) + AC18 verdes con tests de comportamiento; AC14/16/17 + AC11/12/13 verdes.
- node --test/CI verde; npm start ejecutable; la vista Intake navega y el intake ESCRIBE de verdad (demostrado).
- validate exit 0 CON y SIN secretos (clon limpio, DECISION-0046); drift 0; #4 epoca 1.14.0 intacta;
  neutralidad limpia (codigo solo en Zeus-protocol).
- Reproducido por el checker (Arquitecto) desde clon limpio, **incluyendo el write real** (no se cierra sin
  ejecutar el happy path); maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Operador como firmante criptografico propio (opcion (c) re-genesis -> ceremonia RF-9 roster, DIFERIDA).
- Otros intent kinds desde el front. DEF-PII vivo (TASK-0118 sigue gate).
