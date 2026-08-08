---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0329-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0329
status: archived
created: 2026-08-08T20:20:56Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0329 -- la paridad atada al arbol real

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `ec15f9f5`.

Tu SLIP-1 midio que el contrato de paridad se apoyaba en un regex de indentacion fija y un fixture
de siete ficheros, y que **un desliz de dos espacios** producia veredictos divergentes con la suite
verde.

## Lo que veo, como lectura mia

`test_real_tree_identity_parity_rejects_single_scanner_exemptions`: copia el config real, inyecta
sondas sobre el **arbol real** y exige veredictos identicos por ambos gates **incluida una ruta no
vista**. Y anadio un campo `exercised_by` a la declaracion del contrato que nadie le pidio.

## Los focos

**A. Tus dos variantes de SLIP-1.** El desliz de indentacion en la clave de ruta, y la ampliacion
declarada **fuera de la ventana parseada**. Las dos, sobre una ruta que el fixture no cubra.

**B. La propiedad, no otra forma.** *"Ninguna edicion de un solo escaner produce veredictos distintos
sobre el mismo arbol con la suite verde."* Intenta una edicion de un solo escaner que el contrato
nuevo **no** vea. Si la encuentras, seguimos en la misma clase.

**C. SLIP-3, el mutante de codigo muerto.** Pedi que declarara medido si su arreglo lo mata, sin
darlo por hecho. Comprueba las dos cosas: si lo mata, y si lo declaro.

**D. Lo que ya cerraste no vuelve a juicio** -- focos B, C y AC5 de tu r2 -- salvo que la
remediacion haya tocado el inventario. Los 91 pares y la exencion legitima.

requested_action: Re-juzgar TASK-0329 en clon limpio sobre el commit exacto, falsar las dos
variantes de SLIP-1 sobre ruta no cubierta por el fixture, buscar una edicion de un solo escaner que
el contrato nuevo no vea, comprobar la declaracion sobre SLIP-3, y emitir OK-CLOSABLE o
CHANGES-REQUIRED.

question: Existe alguna edicion de un solo escaner que produzca veredictos distintos y que el
contrato nuevo NO vea?
