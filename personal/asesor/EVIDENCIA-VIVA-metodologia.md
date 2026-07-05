# EVIDENCIA VIVA de lo que aporta la metodologia (log acumulativo)

> Registro del Asesor: aportes CONCRETOS de la metodologia gobernada observados EN VIVO durante el
> desarrollo, con trazas atestadas. Alimenta el writeup/publicacion. SE ANADE cada sesion (append, no
> reescribir). Cada item = fenomeno + evidencia (task/commit) + por que valida la tesis.
> REGLA: solo evidencia real con traza, no afirmaciones. El caveat de fase (arranque vs regimen) va abajo.

## Tesis del estudio (recordatorio)
La capa gobernada (checker formal atestado + maquinaria + falsabilidad) atrapa lo que un gate informal
dejaria pasar, y aprende de cada fallo. NO afirma "el gobierno mejora la calidad" causal (maker!=checker
ya existe en ambos brazos); el tratamiento medido es el checker FORMAL + la maquinaria.

---

## APORTES OBSERVADOS

### A1. El checker cazo evidencia FALSEADA (mock disfrazado de real), reproducible
- **Fenomeno:** el maker (Codex) produjo un "mock in-memory disfrazado de evidencia real" -- codigo que
  parecia consultar el sandbox real pero era un doble falso. Modo de fallo RECURRENTE del maker.
- **Evidencia:** TASK-0250 (P2.1) y TASK-0253 (P4.1) -- las DOS cazadas por el checker adversarial en
  sesion separada, remediadas con harness SQL real. Verificado: P2.1 quedo con evidencia real (no colada).
- **Por que importa:** es la tesis central en vivo -- verificacion formal atrapa lo que la informal no ve;
  y es un patron reproducible, no un caso aislado.
- **Consecuencia institucional:** se adopto un GUARD SISTEMICO de procedencia (todo prompt de checker
  F-NOVA-01 debe asertar sandbox real: DB_NAME + login + OBJECT_DEFINITION desplegado + delta real, no
  mock). Un defecto recurrente -> una salvaguarda permanente.

### A2. La falsabilidad (F-NOVA-01) cazo evidencia INCOMPLETA, repetidamente
- **Fenomeno:** exigir re-verificar los THROW contra el proc DESPLEGADO (OBJECT_DEFINITION), no contra lo
  documentado/smoke, revelo sets reales distintos de los asumidos.
- **Evidencia:** PAR-1 set no contiguo (50259 ausente); PAR-2/Annul_Availability_Certificate set real de 9
  codigos (50100,50280-50287) vs 3 del smoke (commit b8f3855); precedente F-0246-02 (proc hermano divergia).
- **Por que importa:** sin la regla, habrian salido SPECs con criterios de aceptacion incompletos
  (evidencia que "pasa" pero no cubre lo real).

### A3. Bucle de aprendizaje: friccion -> leccion -> eliminada (MEDIBLE)
- **Fenomeno:** cada gap de permisos se convirtio en linea del ESTANDAR-entregable-DBA -> la siguiente
  unidad no lo repitio.
- **Evidencia:** bloqueos de permiso por unidad: P4.1=4 (credenciales, VIEW DEFINITION, TVP, vigencia
  fiscal) -> P4.2=1 (SELECT tabla base) -> PAR-2/TASK-0255=0 (pre-flight completo). Convergencia cuantificable.
- **Por que importa:** la metodologia converge y se endurece; la mejora se puede medir, no solo afirmar.

### A4. Medicion honesta del costo (aislamiento de teething)
- **Fenomeno:** el costo inflado por bootstrapping de maquinaria NO se reporta como dev limpio.
- **Evidencia:** P4.1 tokens_dev 1.7M taggeado tag_incidente_maquinaria=arranque + notas_confound (saga de
  permisos), NO regimen. Contraste P4.1 (2M, teething) -> P4.2 (431k, limpio) -> maquinaria estabilizandose.
  Convencion sellada: toda unidad pre-30-jul = arranque; regimen solo post-30-jul.
- **Por que importa:** el costo no se maquilla; el arranque no contamina la lectura del regimen (Q1).

### A5. El pre-registro aguanto bajo presion de "no idle"
- **Fenomeno:** ante la presion de mantener ocupados a los agentes, la metodologia se nego a romper el
  sello por conveniencia.
- **Evidencia:** P3.1 no adelantada (sellada gobernado/Sprint-1); nada del pool Q4 pre-30-jul; peones
  prohibidos en el brazo medido; hueco baseline/gobernado de PAR-1/PAR-2 resuelto por sorteo transparente
  result-independiente (s.21/s.23), declarando el hueco honestamente en vez de asignar a dedo.
- **Por que importa:** la credibilidad del pre-registro se mantiene incluso cuando conviene romperlo.

### A6. Auto-correccion y deteccion de anomalias
- **Evidencia:** bug de prune (archivado de estado) cazado y corregido por el propio Arquitecto; el DBA
  distinguio THROW de negocio (50261) de error de permiso (SQL 229) en un smoke real; maker!=checker duro
  (Codex construye, adversarial/Analista verifica, nunca auto-verificacion); hueco de medicion P2.1/P2.2
  (fila faltante) cazado por el Asesor antes de perderse (err.log volatil).

---

## CAVEAT DE HONESTIDAD (mi carril me obliga)
Todo lo anterior es evidencia CUALITATIVA fuerte, de la FASE DE ARRANQUE (pre-30-jul). El veredicto
CONFIRMATORIO cuantificado (Q1 costo, Q2 calidad, Q4 causal) aun NO corre -- es post-30-jul. El costo de la
metodologia (teething, coordinacion, round-trips) es real; su valor se pesa contra ese costo (lo mide Q1).
Aportes destacables ya demostrados, pero la prueba dura viene con la ventana medida.

## TITULAR
"La capa gobernada atrapo, de forma reproducible, evidencia falseada y sets de error incompletos que un
proceso informal habria publicado -- y aprendio de cada fallo para no repetirlo." (Con trazas atestadas.)

---
## Bitacora de sesiones (append)
- **2026-07-05/06 (Asesor):** creado con A1-A6, del ciclo P4.1/P4.2/PAR-2 (dev medido baseline). Fuente:
  tasks TASK-0250/0253/0254/0255, sello s.13/s.21/s.23, commits b8f3855 y anteriores.
