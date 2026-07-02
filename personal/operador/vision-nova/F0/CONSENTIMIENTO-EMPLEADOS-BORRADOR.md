# Consentimiento informado y autorizacion de tratamiento de datos - Estudio Nova Budget

BORRADOR v0.1 (paquete F0). Tres decisiones marcadas [DECIDE EL OPERADOR].
RECOMENDACION FIRME: revision de 30 minutos con abogado laboral/de datos local
(Ley 1581 de 2012, habeas data, Colombia) ANTES de la primera firma.

---

## Acuerdo de participacion en el estudio de metodologia Nova

Entre: [EMPRESA] (el "Empleador") y ____________________ (el "Participante").
Fecha: __________. Vigencia: duracion del estudio (estimada jul-2026 a dic-2026).

### 1. Que es esto

El Empleador va a desarrollar software interno (suite Nova, empezando por Nova
Budget) usando una metodologia de trabajo con agentes de IA. Queremos MEDIR SI LA
METODOLOGIA FUNCIONA — no evaluar a las personas. El estudio esta pre-registrado:
las metricas y reglas se fijan y sellan ANTES de empezar, para que nadie (tampoco
el Empleador) pueda moverlas despues.

### 2. Que se mide, exactamente

Datos derivados del registro de tareas (ledger), del historial de codigo (git) y de
la integracion continua (CI), a nivel de TAREA:

- costo de computo/tokens de IA gastados por tarea;
- ciclos de revision y veredictos (aprobado / cambio requerido) por tarea;
- defectos ligados a tareas y su remediacion;
- tiempos de ciclo de las tareas;
- eventos de ayuda/des-atasco/excepcion registrados en el sistema.

### 3. Que NO se mide

- NO captura de pantalla, NO registro de teclado, NO software de vigilancia.
- NO contenido de comunicaciones privadas (chat, llamadas, correo personal).
- NO ubicacion, NO horarios fuera de los metadatos normales de git/CI.

### 4. Para que se usa

- Evaluar la METODOLOGIA (procesos, herramientas, agentes) y mejorarla.
- Posible publicacion como caso de estudio industrial (ver punto 6).

### 5. Compromiso central del Empleador

**LAS METRICAS DE ESTE ESTUDIO NO SE USARAN PARA EVALUACION DE DESEMPENO
INDIVIDUAL, COMPENSACION, NI DECISIONES DISCIPLINARIAS.** Este compromiso es
incondicional durante la vigencia del estudio y sobre los datos recogidos en el.

### 6. Que se publicaria

[DECISION DEL OPERADOR 2026-07-02] Se publicaria el dataset COMPLETO SEUDONIMIZADO:
eventos a nivel de tarea con etiqueta de rol (por ejemplo dev-1, dev-2), sin nombres
ni datos de contacto. El contenido del punto 3 (pantalla, teclado, comunicaciones
privadas) NUNCA forma parte del dataset.

ADVERTENCIA QUE EL PARTICIPANTE ACEPTA EXPRESAMENTE: en un equipo pequeno, una
persona que conozca la empresa podria inferir que rol corresponde a que persona
(riesgo de re-identificacion). Precisamente por eso los compromisos de los puntos
5 (no uso punitivo), 7 (retencion y acceso) y 8 (disputa) son incondicionales.

Cambiar el nivel de publicacion despues de la firma requiere nuevo consentimiento.

### 7. Retencion y acceso

- Datos crudos atribuibles: se conservan 24 MESES desde el cierre del estudio
  [DECISION DEL OPERADOR 2026-07-02]; despues se eliminan o se anonimizan de
  forma irreversible. (Nota: lo ya publicado bajo el punto 6 no puede retirarse;
  la retencion aplica al corpus crudo interno.)
- Acceso a datos crudos: solo el operador del estudio y el auditor tecnico.
- Cada Participante puede CONSULTAR SUS PROPIOS DATOS en cualquier momento y
  solicitar correccion de errores de atribucion.

### 8. Canal de disputa

Si el Participante considera que un defecto o metrica le fue mal atribuido, lo
reporta por [canal interno]; la disputa se registra como evento firmado en el
sistema (arbitrated:true) y su resolucion queda auditable. Disputar no tiene
ninguna consecuencia negativa.

### 9. Si decides no participar

[DECISION DEL OPERADOR 2026-07-02] Trabajas exactamente igual, con las mismas
herramientas y flujo; tus tareas simplemente se EXCLUYEN del dataset publicado y
de todo reporte externo. Solo se usan en el analisis interno de la metodologia,
bajo los mismos limites de los puntos 3, 5 y 7.

No participar, o retirar el consentimiento despues (efecto hacia adelante), NO
afecta tu empleo, salario ni asignacion de trabajo.

### 10. Autorizacion de tratamiento de datos (Ley 1581 de 2012)

El Participante AUTORIZA al Empleador a tratar los datos descritos en el punto 2
con la finalidad del punto 4, bajo los limites de los puntos 3, 5, 6 y 7. Derechos
de conocer, actualizar, rectificar y revocar: [canal interno / correo del
responsable de tratamiento].

### 11. Firma y acuse

Firma del Participante: ____________________  Fecha: __________
Firma del Empleador:    ____________________  Fecha: __________

El acuse puede registrarse ademas como EVENTO FIRMADO en el ledger de la instancia
(consent.acknowledged, sin datos personales en el evento: solo id de agente y hash
del documento firmado), sellando el consentimiento con la misma maquinaria que el
resto del estudio.
