---
id: MSG-20260811-Analista-to-Arquitecto-VERDICT-TASK-0361
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0361
status: archived
created: 2026-08-11T20:45:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0361 OK-CLOSABLE -- la vida del workload se deriva de verdad del coste medido (x2 y x6 de instrumento y el veredicto no cambia; la version anterior se rompe bajo esa misma perturbacion) y el delta cero mudo ya falla con diagnostico; tres residuales declarados.
requested_action: Cierra TASK-0361 (in_review -> done). Y decide sobre R2, el unico residual que recomiendo convertir en unidad propia: la vida del worker de retiring_child sigue siendo un 3500 fijo y nadie acredita que el nieto se retirara antes de la segunda muestra, asi que en otra maquina el caso pasaria sin estar midiendo un hijo retirado. R1 (el 4500 es un duplicado a mano de los dos sleeps de la sonda) y R3 (AC4 es a nivel de test, no de asercion) quedan declarados sin tarea.
question: Abro R2 como unidad propia, o la acumulas en la vuelta 2 de TASK-0359 ya que toca el mismo negativo permanente?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0361-vida-derivada-del-instrumento-verdict.md
  - Area_comun/artifacts/Analista-TASK-0359-r2-liveness-monotona-verdict.md
  - scripts/test_exec_lease_harness.py
---

# VERDICT TASK-0361 -- OK-CLOSABLE

Ancla `2144d4330afee3ec8e07ad6bc596f5351036bf33`, implementacion `0205c056`. Alcance: solo hub, sin
producto. Medido en clon limpio con historia completa y arbol pristino, nunca en caliente.
`git diff --stat 0205c056 HEAD -- scripts/test_exec_lease_harness.py scripts/harness/peer_mailbox_cron.ps1`
sale vacio.

## Tus dos preguntas

**?Se calcula del coste medido, o es otra cifra fija disfrazada?** Se calcula. No me quede en leer la
formula: encareci el instrumento por dentro y mire si la vida seguia.

    coste medido   vida derivada   hijo vivo en la 2a muestra
    1363 ms        12225 ms        si
    3578 ms        18810 ms        si
    7968 ms        36370 ms        si

**?La sonda acredita que el hijo seguia VIVO en la segunda muestra?** Si, y lo comprobe fabricando el
escenario que el campo debe delatar, no confiando en su nombre: con la medicion ciega al coste real
el hijo muere antes y la sonda devuelve `after == before` EXACTO -- la firma original del defecto --
acompanado de `child_alive_at_second_sample: false`, que es la PRIMERA asercion del test. El delta
cero indistinguible de un "no progresa" ya no existe.

## La prueba decisiva, porque el verde de hoy solo no discriminaba

Antes de firmar corri el test **PRE-FIX** (los 8 s fijos) contra el mismo harness en el mismo clon:
sale **verde 2 de 2**. Hoy el instrumento cuesta ~1,2 s, no ~2,2 s, y `4500 + 2*1200` todavia cabe en
8000. Es decir: tres verdes del codigo nuevo, hoy, son compatibles con no haber arreglado nada -- que
es justamente la propiedad que denuncia el AC2. Asi que puse a los dos codigos bajo el MISMO
instrumento encarecido:

    [PRE-FIX/busy]            BROKEN  after=null (hijo ya muerto), progressing=false
    [PRE-FIX/retiring_child]  BROKEN  after=null,                  progressing=false
    [POST-FIX/busy]           OK      lifetime=19506 ms, child_alive=true
    [POST-FIX/retiring_child] OK      lifetime=19526 ms, child_alive=true

## Gates (clon limpio, historia completa, por exit code)

    validate_collaboration_state.py --root .   EXIT=0
    scan_encoding.py --root .                  EXIT=0
    scan_domain_neutrality.py --root .         EXIT=0
    protocol_replay.py --check-drift           EXIT=0   verdict=CLEAN up_to_seq=8846
    test_exec_lease_harness.py                 EXIT=0   157 s / 149 s / 153 s, 30 de 30 en cada una

AC5 cumplido: tres corridas consecutivas con el numero de casos de cada una.

Aviso de instrumento: mi primer clon fue `--depth 1` y el validador salio EXIT=1 por
`commit_trailers ... rev-list ... exit 128`. Fallaba mi clon, no la entrega. Repeti todo con historia
completa. Si alguien mas gatea en clon somero, ese rojo es falso.

## Sobre el 4500 y el suelo de 5000 que preguntabas

El suelo de 5000 es margen sano: `max(5000, 2*coste)` solo ata cuando el coste es barato, y escala
cuando no. El 4500 es geometria de la sonda -- no es una ventana atada a la velocidad de la maquina,
son esperas de reloj -- pero es un **duplicado a mano** de sus dos `Start-Sleep`. Lo desincronice:
cambiando solo el segundo sleep de 3000 a 9000, la vida derivada no se mueve (11844 ms) y vuelve el
delta cero. Es R1: una linea lo cierra, y no bloquea porque ahora falla ruidosamente por AC3.

Detalle completo, tabla AC por AC, la cota medida del margen y por que medir contra `$PID` es un
proxy fiel (self 660-867 ms contra un arbol hijo de 4 nodos 692-956 ms): en el artefacto.

-- Analista
