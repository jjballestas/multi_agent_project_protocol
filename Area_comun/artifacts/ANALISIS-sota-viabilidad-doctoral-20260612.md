# ANALISIS - Estado del arte y viabilidad doctoral de la metodologia (2026-06-12)

> Estado: ANALISIS / cerrado (ejecutado en sesion Claude/Cowork 2026-06-12; este artifact es el registro
> formal del trabajo, encolado retroactivamente como TASK-0104 tipo analysis). Autor: Claude
> (arquitecto), con aprobaciones del operador en la misma sesion. Neutral (proceso/investigacion sobre el
> protocolo mismo); las referencias a instancias de dominio se citan por ruta externa, sin contenido de
> dominio en este repo.

## Pregunta

El protocolo (v1.1.0, runtime v0.11.0) ocupa la interseccion de seis areas activas del estado del arte.
Tres preguntas: (1) que dice la literatura 2015-2026 en cada area y donde estan los gaps; (2) puede la
metodologia elevarse a nivel de investigacion doctoral; (3) que correcciones necesita el plan para
sobrevivir revision academica.

## Respuesta corta

(1) Cada pilar tiene literatura madura pero fragmentada; **la interseccion de los seis esta vacia** -
nadie ha publicado un protocolo integrado y evaluado empiricamente. (2) **Como artefacto, hoy NO; como
programa de investigacion, SI** - el artefacto es solido pero faltaba diseno experimental: hipotesis
falsable, adversario definido y dataset publicable. (3) Las tres carencias se corrigieron en papel
(documentos 01-05 del caso de estudio) y la primera se materializo en este repo como DECISION-0029 +
TASK-0101..0103.

## Metodo

Busqueda paralela en 6 frentes (6 subagentes), ~85 referencias con URL de descarga verificada
(spot-check por fetch directo de arXiv en 4 anclas), clasificadas peer-reviewed / preprint / literatura
gris. Veredicto critico adversarial sobre la hoja de ruta del caso de estudio. Verificacion de cada
afirmacion sobre el repo contra el repo real (codigo y ledger).

## Hallazgos principales

1. **Gaps del campo donde el protocolo ya esta posicionado:** G1.2 (log operativo unificado con
   provenance normativa W3C PROV), G3.1 (provenance de AUTORIA de cambios por agentes - SLSA/in-toto
   atestan builds, no autoria; el gap esta vacio), G4.1 (cost-attribution por handoff), G5.1 (semantica
   formal de handoffs), G5.2 (coordinacion persistente de agentes heterogeneos - exactamente el modo de
   operacion de este repo), G6.2 (parada en cascada N-agente, sin teoria publicada).
2. **Defecto critico 1 - hipotesis circular:** "con atestacion se atesta mas que sin atestacion" es
   verdadera por construccion. Corregida por H1 (solidez: deteccion >=95%, FPR <=1%), H2 (coste: <=5%
   tokens, <=10% latencia), H3 (verificabilidad externa >=90%), con pre-registro congelado antes de medir.
3. **Defecto critico 2 - auto-atestacion:** el runtime (escritor unico, DECISION-0022) firmaba con HMAC
   simetrico lo que el mismo escribia: sin adversario, sin contribucion. Corregido por el modelo de
   amenaza A1/A2/A3-restringido/A4 y la adopcion de firmantes cruzados sin consenso (firma por agente +
   prev_hash + anclaje externo). El operador APROBO la politica el 2026-06-12.
4. **Defecto critico 3 - dataset no examinado:** las fuentes de produccion contienen datos personales
   bajo RGPD y Ley 1581/2012. Corregido por esquema de captura en dos planos (protocolo publicable sin
   texto libre / carga util por hash), niveles T1/T2/T3 y GATE-DATASET legal bloqueante previo a
   instrumentar.
5. **Hallazgo transversal del SOTA relevante para DECISION-0005/0008:** el coste dominante en ingenieria
   de software agentica esta en la revision/verificacion entre agentes (aprox. 59% de tokens en code
   review segun Tokenomics 2026), no en la generacion - valida la prioridad de eficiencia de comunicacion
   del protocolo.

## Acciones derivadas (trazabilidad)

| Derivado | Donde | Estado |
|---|---|---|
| DECISION-0029 firmantes cruzados | `Area_comun/decisions/DECISION-0029-firmantes-cruzados.md` | accepted 2026-06-12 |
| TASK-0101 prev_hash encadenado | `Area_comun/tasks/TASK-0101-codex-eventlog-prev-hash.md` | proposed |
| TASK-0102 firma por agente | `Area_comun/tasks/TASK-0102-codex-firma-por-agente.md` | proposed |
| TASK-0103 anclaje externo | `Area_comun/tasks/TASK-0103-codex-anclaje-externo.md` | proposed |
| Handoff de continuidad de sesion | `Area_comun/handoffs/HANDOFF-SESION-20260612-claude-analisis-doctoral.md` | publicado |
| Pendiente: Fase 0 del pipeline (E5, E6, #1) | por encolar | no iniciado |
| Pendiente: GATE-DATASET (consulta juridica) | por iniciar (mayor latencia del camino critico) | no iniciado |

## Documentos fuente (fuera de este repo - caso de estudio, contiene contexto de dominio)

Carpeta `D:\Agentes\Estudio\Case_Studies\loops_agenticos\`:
`01_Sources/Documents/SOTA_sistemas_multiagente_2026-06.md` (informe SOTA completo con las ~85
referencias y URLs); `01_Sources/Documents/01..05_*.md` (paquete de correcciones: hipotesis, modelo de
amenaza, publicabilidad, integracion, resumen ejecutivo);
`04_Learning_Output/Final_Deliverables/sintesis_hoja_de_ruta.md|.html` (hoja de ruta revisada
2026-06-12).

## Reglas de criterio fijadas por este analisis (vigentes para sesiones futuras)

1. Toda afirmacion de seguridad cita clase de adversario (A1/A2/A3r/A4); sin clase, no se afirma.
2. "Capability" del registry = habilidad (RBAC), NO object-capability; no presentar como CaMeL.
3. Umbrales experimentales se congelan en pre-registro antes de medir; no se ajustan a posteriori.
4. Los gaps se "abordan" o "instrumentan", nunca se "resuelven" sin medicion que lo respalde.
5. La ventaja del dataset es de publicabilidad estructurada, no de existencia unica.
