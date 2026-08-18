DRAFT (no rutear hasta EXEC_EXIT de Codex). Medicion propia en clon limpio
D:/Aegis_Scratch/protocol/r5warn sobre 9ba1bbbc + un DECISION-PROBE anadido
(status ausente, superseded_by: [DECISION-0081]), borrado al terminar:

    CLASSIFY DECISION-0071    -> superseded | status= accepted | superseded_by= ['DECISION-0081']
    CLASSIFY DECISION-PROBE   -> superseded | status= None    | superseded_by= ['DECISION-0081']
    WARN: DECISION-0059-...md : decision currentness status is missing; attested policy treats it as current
    WARN: DECISION-PROBE.md   : decision currentness status is missing; attested policy treats it as current

Dos hechos:
1. El arreglo FUNCIONA y funciona con la forma REAL del corpus (lista), no solo con
   la escalar que usa la fixture nueva. DECISION-0059 (sin puntero) sigue vigente:
   el censo no se mueve.
2. El aviso de la linea 987 sigue diciendo "attested policy treats it as current"
   para un caso que produccion acaba de clasificar SUPERSEDED. El unico rastro
   visible del caso afirma lo contrario de lo que hace el motor.

Eso toca AC4 (decirlo RUIDOSAMENTE): un humano triando la lista de avisos lee
"treated as current" y no investiga -- exactamente el desenlace que la tarea existe
para impedir. Es la mitad observable de la MISMA propiedad, no un frente nuevo.
