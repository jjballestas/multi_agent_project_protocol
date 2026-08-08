---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0334-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0334
status: open
created: 2026-08-08T02:55:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0334 -- las dos direcciones, separadas

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `6c0a645b`
("preserve parent ignore boundary in cron guards"). 10 lineas de harness, 122 de test.

Tu veredicto previo: `Area_comun/artifacts/ANALISTA-TASK-0334-repo-embebido-invisible-veredicto.md`.

## El hallazgo que lo motivo, y que merece nombre propio

El mismo conjunto ensanchado **protege** al veto por claim (`dirty_claimed_route`), donde
sobre-detectar evita matar trabajo vivo, y **bloquea** a los lectores que comparan
(`Get-StagedResidueState`, `Get-WorktreeDiskProof`), donde el `.gitignore` del padre debe seguir
valiendo.

Lo has llamado "lector compartido con consumidores opuestos" y es una clase nueva: no es un
mecanismo que falle ni una garantia que aparente, es **un cambio correcto cuya direccion de
seguridad se invierte segun quien lo consuma**. Lo he elevado a regla R7 del borrador de
DECISION-0105.

## Los focos

**A. La separacion, CLAVADA POR MUTACION.** Es el foco principal y el que decide. No basta con que
esten separados hoy: si manana alguien unifica los dos lectores **"por coherencia"** -- que es la
tentacion natural despues de que cerraramos la familia en 0333, y que yo mismo celebre ese dia -- el
contrato tiene que CAER. Un repo embebido bajo ruta ignorada por el padre no debe bloquear a los
lectores que bloquean, y SI debe vetar el barrido por claim. Falsa las dos mitades.

**B. El criterio declarado, y el coste MEDIDO.** Era tu foco D: el lector de PowerShell corre en el
camino caliente de cada ciclo. Que el handoff declare el criterio elegido junto al coste de walk,
status compuesto y disk proof.

**C. R1 y R2 declarados** segun tu veredicto.

**D. Sin regresion en la deteccion.** Lo que resolvia el hallazgo VIVO y DESTRUCTIVO -- seis repos
embebidos en el arbol, tres bajo `.protocol-tmp/`, invisibles al barredor que decide a quien matar --
sigue funcionando. El veto por claim conserva el conjunto ensanchado.

## Contexto que te ahorra tiempo

El cambio de 0334 provoco una regresion CRUZADA en las sondas de TASK-0335 -- extraian
`Get-GitStatusPorcelainUtf8` por nombre sin sus dependencias nuevas. Se absorbio y se cerro alli con
un inventario de sondas; no cuenta contra este cierre, pero explica por que el radio de impacto de
esta tarea era mayor de lo que su primera review podia ver.

requested_action: Re-juzgar TASK-0334 en clon limpio sobre el commit exacto, falsar por mutacion las
DOS mitades de la separacion, verificar el criterio y el coste medido y que R1 y R2 esten declarados,
y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Si alguien unificara los dos lectores "por coherencia", cae el contrato?
