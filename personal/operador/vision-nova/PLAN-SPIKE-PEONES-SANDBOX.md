# PLAN SPIKE PEONES EN SANDBOX (ensayo F6.0 propuesto)

- fecha: 2026-07-02
- emite: Asesor a peticion del Operador ("quiero colocar los peones a funcionar y medirlos")
- estado: PLAN OPERATIVO listo (ejecuta el Operador con guia del Asesor)
- base: DECISION-0074 (D3 backend hibrido: peones keyless NUNCA firman) + DECISION-0078
  ajustada por DECISION-0083 (brazo C = fase condicional; sandbox como ensayo)
- regla de oro: PARALELO y fuera del camino critico F1->F4; cero impacto en el gate 30-jul

## 1. Que da y que NO da este spike (honestidad primero)

- SI da: peones FUNCIONANDO esta semana; contrato de asignacion calibrado con datos
  reales; numeros EXPLORATORIOS de ahorro (tokens del firmante con/sin peon); setup
  tecnico resuelto (Ollama+modelos) antes de que F6.1 lo necesite; y aprender donde
  los peones fallan.
- NO da: evidencia confirmatoria de Q1. Sin pre-registro SELLADO (F3.4), cualquier
  numero es anecdota (tu propio veredicto adversarial lo dice). Los numeros del spike
  se declaran en el pre-registro como PILOTO DE CALIBRACION y quedan fuera de Q1.
  La medicion confirmatoria (>=15 tareas/brazo, tareas reales Nova Budget, gobierno
  completo) sigue siendo F6.1 post-sello.

## 2. Setup (30-60 min, maquina del Operador)

1. Instalar Ollama (https://ollama.com/download, Windows).
2. `ollama pull qwen2.5-coder:7b` (peon principal segun D3). Opcional segundo peon:
   `ollama pull deepseek-coder:6.7b`.
3. Sandbox: `D:/Agentes/Zeus/piloto-peones/` (ruta ya reservada por DECISION-0074/0078).
   `git init` local, SIN remoto, SIN conexion al hub. Estructura: `tareas/`,
   `entregas/`, `registro/`.
4. Verificacion: `ollama run qwen2.5-coder:7b "escribe un test pytest para una
   funcion suma"` responde coherente.

## 3. Contrato de asignacion (plantilla; los 9 puntos de DECISION-0078 son ley)

Cada tarea a peon se envia SOLO con este bloque completo (archivo en `tareas/`):

```text
OBJETIVO: <concreto, 1-2 lineas>
RUTAS PERMITIDAS: <lista>   RUTAS PROHIBIDAS: <lista>
ENTRADA: <exacta>           SALIDA ESPERADA: <exacta>
PASOS/PATRON PERMITIDO: <si aplica>
RESTRICCIONES DURAS: no ledger, no submit_intent, no commits, no secretos, no PII,
  no decisiones, no cambios de protocolo, no reglas de negocio
VERIFICACION OBJETIVA: <comando/test/lint/diff esperado>
CRITERIO DE ACEPTACION: <binario>
SI FALTA CONTEXTO: devuelve BLOCKED + una pregunta concreta; no inventes alcance
PROVENANCE: peon=<modelo>, prompt_id=<archivo>, ts=<ISO>, rutas=<tocadas>, gates=<resultado>
```

## 4. Tanda de ensayo (5 tareas B + 3 tareas A, elegibles segun 0078)

Solo tareas acotadas, repetitivas, gate-verificables (scaffolding de tests,
transformaciones mecanicas, fixtures, runbooks iniciales, reemplazos de texto).
Sugeridas: (1) tests unitarios de un modulo utilitario; (2) conversion de un doc a
plantilla parametrizada; (3) fixtures JSON de casos limite; (4) borrador de runbook
de instalacion; (5) tabla de mapeo i18n. Brazo A (control): el firmante hace 3 de
esas tareas SOLO, cronometrado, misma hoja de registro.
Si la salida es funcion mecanica de la entrada: codegen/script antes que LLM (0078).

## 5. Hoja de registro (una fila por tarea; `registro/medicion.csv`)

```text
tarea_id, brazo(A|B), tokens_prompt_delegacion, tokens_revision, tokens_integracion,
tokens_rework, tokens_peon_in, tokens_peon_out, tiempo_pared_min, fallos_gate,
ciclos_correccion, calidad(aceptada|corregida|rechazada), incidentes
```

La metrica que decide: `tokens_firmante_total = delegacion + revision + integracion
+ rework` comparado contra el brazo A. El costo de ESCRIBIR EL CONTRATO cuenta como
costo del firmante (regla 0078; es la trampa clasica del "ahorro" con peones).

## 6. Reglas duras del spike

- MANUAL y SERIALIZADO: un peon a la vez, sin crons ni concurrencia (el contrato
  exec-lease de 0235 no aplica al sandbox; no multiplicar riesgos).
- El sandbox JAMAS toca el hub ni Zeus-protocol: cero submit_intent, cero commits
  fuera de `piloto-peones/`, cero PII/datos reales de la empresa.
- STOP inmediato si un peon intenta escribir fuera de rutas permitidas: se registra
  como incidente y la tarea se descarta.
- Timebox: 1-2 sesiones del Operador. Si engancha mas tiempo, es senal de exito:
  se corta y se vuelca lo aprendido a F6.1, no se alarga el juguete.

## 7. Salidas del spike (lo que alimenta F6.1 y el pre-registro)

1. Contrato de asignacion CALIBRADO (v1 -> v1.1 con lo aprendido).
2. `registro/medicion.csv` con la tanda completa (numeros exploratorios).
3. Nota de 10 lineas: donde ahorran, donde revientan, config elegida (modelo/params).
4. Declaracion en el pre-registro F3.4: "piloto de calibracion ejecutado en sandbox
   (fechas, N tareas); sus datos NO entran a Q1".

## 8. Encaje en el tablero (decision del Operador pendiente)

Si el Operador quiere trackearlo: ordenar al Arquitecto agregar item "F6.0 ensayo
sandbox de peones (timebox, paralelo, exploratorio)" al tablero. Alternativa: queda
como actividad de sandbox fuera del tablero (el tablero solo mide el camino critico).
