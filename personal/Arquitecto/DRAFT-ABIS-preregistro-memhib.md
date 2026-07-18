## CELDA A-BIS (2026-07-18, DIRECTIVA de reencuadre del Operador; pre-registro EX-ANTE)

Motivo: A refuto el ahorro de re-derivacion en el SUELO overhead-bound (sello: umbral
inalcanzable por diseno). El Operador reencuadra al regimen correcto: en FRIO la
alternativa a la memoria no es re-derivar trivial sino RE-ESTABLECER el contexto
completo (caro). A-bis mide la CAPACIDAD (contexto sobrevive el frio + se comparte) y
el COSTO transparente. No sustituye el registro de A (queda tal cual); ANADE el regimen.

ESCENARIO (por trial): un agente PRODUCTOR establece un CONTEXTO RICO desde material
bruto sintetico (cuerpo de trabajo caro de reconstruir: >= 12 documentos fuente
sinteticos extensos de los que se derivan >= 25 decisiones interdependientes con
rationale + una tabla de parametros derivados) y lo escribe a la memoria (artefactos
gobernados + commit + build; autor logico declarado). Un agente EN FRIO (exec fresco
del cron = sesion cold real, DISTINTO del productor) debe completar una TAREA
DEPENDIENTE (responder/validar 20 items que exigen el contexto destilado).

ADDENDUM DEL OPERADOR INCORPORADO (ex-ante): CONTEXTO RICO = REGIMEN 2
(no-re-derivable / solo-recuperable): el corpus imita una SESION DE INVESTIGACION --
cadena de DECISIONES SELLADAS + RESULTADOS MEDIDOS + derivaciones con referencias
cruzadas (una conclusion depende de otra). NO cuenta re-derivable trivial ni relleno.
La pregunta del cold EXIGE las conclusiones acumuladas (sin memoria: rehacer las
mediciones o fallar). Fidelidad cotejada CAMPO A CAMPO (>=95 pct).

BRAZOS (por trial; execs separados, cold por construccion; TRES brazos):
- CON memoria: el cold recupera el contexto destilado (query + retrieve + verificacion
  sha) y completa la tarea. Mide: exito + fidelidad + costo.
- SIN-a (RE-COMUNICACION): al cold se le re-alimenta el cuerpo CRUDO COMPLETO; costo =
  re-leer todo. CON vs SIN-a lee el AHORRO en el regimen caro.
- SIN-b (COLD PURO): el cold no tiene nada (ni memoria ni re-feed). CON vs SIN-b lee la
  CAPACIDAD ("no se pierde el contexto": el cold-nada falla o degrada donde CON
  recupera). El reporte SEPARA "ahorra" (SIN-a) de "habilita" (SIN-b).

METRICAS + CRITERIOS EX-ANTE (a congelar con el ACK del Asesor):
1. CAPACIDAD: el cold CON recupera el contexto con fidelidad >= 95 pct del set de
   verificacion Y completa la tarea (>= 18/20 items correctos). EXITO si ademas el SIN
   degrada (menos items correctos) o exige el re-establecimiento completo.
2. COMPARTIR EN FRIO: productor != cold (autores/credenciales distintas; proxy jball si
   el nodo logico es Asesor). EXITO: el cold-distinto recupera el contexto del otro.
3. COSTO TRANSPARENTE: total del exec por brazo (mismo instrumento de la serie) +
   overhead fijo ~115k DECLARADO APARTE + marginales estimados (patron del sello de A).
   CRITERIO DE VALOR: total CON < total SIN (ambos cold; el delta es el efecto del
   regimen). El numero sale tal cual.
4. APORTE A LA METODOLOGIA (declarativo con dato): continuidad de contexto a traves de
   cold-start/compactacion/handoff CON atestacion (drift 0 + procedencia + round-trip),
   que la metodologia pierde sin memoria.

N: 2 trials (2 contextos ricos independientes, productores logicos distintos) x 3
brazos (CON, SIN-a, SIN-b) = 6 execs de medicion + 2 execs productores (medidos como setup del trial,
reportados aparte). SET DE VERIFICACION: lo sella el ARQUITECTO tras el exec productor
y ANTES de los brazos cold (20 items por trial derivados del contexto guardado; ni el
cold-CON ni el cold-SIN lo ven antes).

GATE DE INTEGRIDAD transversal identico (round-trip + drift 0 + procedencia + 0 PII).
Regla anti-hueco: si el material bruto no da para derivar las >= 25 decisiones o la
tarea dependiente queda subdeterminada -> BLOCKED del maker (no inventar).
Secuencia: NO compite con D/C (A-bis se ejecuta despues de cerrar D y C, o en huecos
de ventana si el Asesor lo pide). Celda(s): TASK-0027+ (post C).
