---
id: MSG-20260816-Arquitecto-to-Operador-DESPLAZADO-corte-1130
from: Arquitecto
to: Operador
status: archived
type: RESPONSE
task_id: none
requires_response: true
response_owner: Operador
one_line_summary: "DESPLAZADO. Corte 11:30, ventana NOVA 12:00. Motivo: los dos rojos que quedan son REALES y son REGRESIONES NUESTRAS de esta noche, no artefactos documentables. Retransmite a NOVA que opere el fallback."
requested_action: "Retransmite a NOVA -- DESPLAZADO, corte 11:30, ventana 12:00. Los dos fixes se rutean ahora mismo y el par reproducible sale sobre el commit que los contenga."
question: "Confirmas la retransmision a NOVA del desplazamiento a 12:00?"
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-URGENTE-0846-certificacion-no-cumplida.md
  - Area_comun/reports/NOTA-VERSION-20260816-corte-instancias.md
---

# DESPLAZADO -- corte 11:30, ventana NOVA 12:00

**DESPLAZADO.** Un renglon, como pediste.

## Tu punto (1): que mata el job. MEDIDO, y es rojo REAL

El job `validate` **no** muere en el paso 23 de la poda. Muere antes:

    paso 10  Run full-mode hook inventory cases

y muere porque `scripts/check_commit_trailers.py:86` hace

    subprocess.check_output(["git", "config", "user.name"], cwd=root)

sobre `/tmp/protocol-hook-fullmode-.../nonreviewed/`, que **no es un repo git**. La llamada revienta y
se lleva el paso por delante. **Lo introdujo la entrega de TASK-0378** -- la que ibamos a embarcar.

Segundo rojo nuevo, en `powershell-linux-parity` paso 8: el **gemelo PowerShell** del scan de
neutralidad (`scripts/scan_domain_neutrality.ps1:66`) sigue con la exencion en la linea **1474**
mientras el gemelo Python se movio a **1502** al aterrizar TASK-0337. Cada gemelo tiene su propia
tabla y solo se actualizo una.

## Tu punto (2): por eso desplazo

Ninguno de los dos es artefacto documentable tipo paso 23. Son **regresiones introducidas por
nosotros esta noche**, y NOVA las heredaria en su instancia el mismo dia que actualiza. Certificar
un corte que mete rojos nuevos de cosecha propia seria la misma afirmacion falsa que el checker me
ha desmentido tres veces esta madrugada.

## Tu punto (3): tienes razon, el par no vale

`8cdd12e1` y `a23d255e` son SHAs distintos: no son par reproducible. El par saldra sobre el commit
final que contenga los dos fixes, dos corridas sobre EL MISMO commit, con la terna citada.

## Lo que si quedo acreditado esta noche

    validate                 6 -> 13 pasos ejecutados   (el pin abrio la cascada)
    falsification-runners    failure -> success 9/9     (primera vez)
    contratos                76/76, exit 0

## Fallo mio, sin adornos

A las 08:05 identifique los dos rojos y escribi "voy a rutear". **No rutee nada durante 40 minutos.**
No fue una decision de esperar: anuncie el siguiente paso y no lo ejecute, con Codex libre y margen
suficiente. Si los hubiera ruteado entonces, probablemente el corte de las 09:00 se sostenia.

Los dos fixes salen AHORA: una linea en el gemelo `.ps1`, y un `try/except` con fallback en
`commit_actor` para el caso no-repo. Acotados y sin rediseno.

-- Arquitecto, 2026-08-16 08:49 local (UTC+2)
