---
decision_id: DECISION-0115
title: Que significa "verificado" -- toda afirmacion de verificacion declara su alcance, y un gate que no se repite no es un gate
status: accepted
date: 2026-08-14
ratified_at: 2026-08-14
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0099, DECISION-0101, DECISION-0113]
phase: P2
---

# DECISION-0115 - Que significa "verificado"

## Origen

Informe de campo del Arquitecto de la instancia NOVA, sesion 2026-08-13/14. Cuatro de sus seis
lecciones son la misma en cuatro niveles distintos: **una afirmacion de verificacion vale lo que su
alcance declarado, y hoy el alcance se sobreentiende.**

## Las cuatro clausulas

### 1. El ancla se declara POR CLASE DE EVIDENCIA

Un veredicto puede anclarse con rigor -- commit, seq del ledger, hash de cabeza, gates por exit code
en clon limpio -- y aun asi juzgar artefactos que **no viven en el repositorio**. Ocurrio: el SQL
juzgado no estaba en el arbol y las citas apuntaban a ficheros que el commit anclado no contiene. El
hallazgo nacio obsoleto y ni el checker ni el coordinador podian verlo desde el ancla.

**Regla:** si parte del juicio recae sobre artefactos fuera del repositorio, esa parte se ancla con su
propio identificador -- hash de la definicion desplegada, ruta y version del script -- o se declara
NO REPRODUCIBLE. Un ancla parcial se lee como si todo estuviera anclado.

### 2. Lo desplegado se verifica POR ENTORNO, con hash

"Verificado" sin nombrar el entorno no significa nada cuando el artefacto vive en N sitios. Ocurrio:
se leyo la definicion viva de un procedimiento en la unica de tres bases donde la guarda existia, y se
concluyo que el checker se equivocaba. Peor: esa guarda la injertaba un script por **reemplazo de
texto sobre la definicion**, de modo que si las cadenas literales cambian el objeto se recrea SIN
guarda y el script **termina en exito**.

**Regla:** para todo artefacto desplegado en varios entornos, la verificacion es por entorno y con
hash de lo desplegado. Y su corolario, que es el que mas veces salva: **una verificacion que CONFIRMA
lo que esperabas es exactamente donde hay que pedir la segunda fuente.**

### 3. "Mecanismo probado" no es "camino probado"

"Una prueba que falle si se revierte el arreglo" es necesario y NO basta. Ocurrio: una prueba con un
doble que lanza los codigos que la propia prueba eligio pasa, y falla al revertir -- pero el camino
real lanza otros codigos, ninguno mapeado, y el endpoint sigue devolviendo 500 con el detalle del
motor dentro. **La prueba confirma la hipotesis de su autor.**

**Regla:** los criterios de aceptacion distinguen las dos cosas. *Mecanismo probado* admite un doble.
*Camino probado de punta a punta* exige el contrato real. Para un hallazgo de seguridad, solo el
segundo cierra.

### 4. La exigencia es GATE REPRODUCIBLE, no solo gate por exit code

Esta metodologia descansa en "gatea por exit code, nunca por grep". Ocurrio que el exit code **no es
estable**: la misma suite sobre el MISMO commit dio 106/106 y despues 104/106, por arneses que
consumen su propio estado. Toda "suite verde" declarada bajo esa condicion es una primera corrida.

**Regla:** un gate acredita si repite. Dos corridas consecutivas sobre el mismo commit, o el arnes se
declara no idempotente y **se excluye del gate**. Un verbo central que no se repite no es un verbo
central.

## Por que van juntas y no como cuatro decisiones

Porque son cuatro caras de un unico contrato: **quien afirma haber verificado, declara sobre que y
bajo que condiciones**. Separarlas invita a cumplir una y creer que se cumplieron las otras, que es
la forma exacta del defecto que las cuatro describen.

## Alcance

Vinculante para veredictos de checker, handoffs de maker y encargos del coordinador. No cambia
esquema ni ledger: cambia lo que un artefacto de verificacion **debe declarar** para contar como tal.

## Autoria

Las cuatro clausulas y sus cuatro medidas de campo son del **Arquitecto de la instancia NOVA**. Tres
de ellas las descubrio contra su propio trabajo, incluida la que le corrige a el.
