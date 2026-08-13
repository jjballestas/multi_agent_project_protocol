---
id: TASK-0370
title: La invariante que sostiene el detector de marcadores vive solo en un comentario, y su incumplimiento seria mudo
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0370-la-invariante-clave-a-gramatica-vive-solo-en-un-comentario.md
created: 2026-08-13
intake:
  type: fix
  goal: >
    Residuo 1 del veredicto formal de TASK-0350. El instanciador estrecho su detector de marcadores a
    la gramatica `^[A-Z][A-Z0-9_]*$`, y la misma expresion gobierna DETECCION y SUSTITUCION. De ahi se
    sigue una invariante implicita: toda clave que `build_replacements` produce tiene que casar esa
    gramatica. Si alguna no la casara, esa clave **no se sustituye y ademas no se detecta**: sale
    literal a la instancia generada, en silencio. Bajo el patron anterior se sustituia bien, asi que
    para esa clase de entrada el cambio convierte un fallo RUIDOSO en uno MUDO. Hoy la fuga no es
    alcanzable -- el checker extrajo las 28 claves del fuente y las 28 casan --, pero la invariante
    que lo garantiza vive UNICAMENTE en un comentario: no hay asercion, ni caso de runner, ni gate que
    la compruebe. La proxima clave que alguien anada con otra forma no encuentra nada que la pare.
  acceptance:
    - "AC1 (la invariante deja de ser un comentario): existe una comprobacion ejecutable que falla si
      alguna clave producida por `build_replacements` no casa la gramatica del detector. Se acredita
      por conducta anadiendo una clave que no la case y observando el rojo con su exit code, no
      leyendo el codigo."
    - "AC2 (la poblacion se DERIVA del productor, no se enumera): la comprobacion obtiene el conjunto
      de claves de `build_replacements` en tiempo de ejecucion. Una lista de 28 nombres escrita a mano
      no acredita: el dia que se anada la 29 la lista miente y la comprobacion pasa igual."
    - "AC3 (una sola fuente para las dos caras): se declara si deteccion y sustitucion siguen atadas a
      la MISMA expresion o si el arreglo las separa, y por que. Si quedan separadas, la comprobacion
      tiene que cubrir la divergencia entre ambas, que es donde renaceria el fallo mudo."
    - "AC4 (el negativo discrimina): con la comprobacion en su sitio, el conjunto actual de claves
      sigue pasando. Un cambio que ponga rojo tambien el estado sano no acredita: se mide con el par."
  verification_cmd:
    - "python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/new_instance.py
    - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
  out_of_scope:
    - "Revertir o reabrir el criterio de TASK-0350: el checker lo dio PASS en los seis AC y la
      gramatica no esta en cuestion. Esta tarea le pone el guardia que le faltaba, no lo discute."
    - "El banco de 72 tests que el motor embarca rojo en una instancia recien parida: es TASK-0371."
  risk: low
  estimate: S
---

# TASK-0370 -- la invariante sin guardia

## De donde sale

Veredicto formal de TASK-0350 (OK-CLOSABLE), residuo 1. El checker lo dice sin adornarlo:

> Una clave que el instanciador POSEE y que no case la gramatica no se sustituye **y ademas no se
> detecta**: sale literal a la instancia, en silencio. Bajo el patron viejo se sustituia bien. Para
> esa clase de entrada el fix convierte un fallo ruidoso en uno mudo.

Y acto seguido acota su alcance con honestidad: las 28 claves actuales casan, asi que **la fuga no es
alcanzable sin cambiar codigo**. No es un fallo de 0350 y por eso no emitio CHANGE-REQUIRED.

## Por que merece tarea propia

Porque lo que falta no es un caso: es el guardia de una invariante que hoy solo esta escrita en
prosa. `grep` del arbol y no hay asercion, ni caso de runner, ni gate. La garantia se sostiene sobre
que nadie anada una clave con otra forma -- y eso es disciplina, no mecanismo.

Es la forma que esta instancia lleva persiguiendo: **una propiedad verdadera hoy, sin nada que la
mantenga verdadera manana**.
