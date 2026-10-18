# Sesión 6 — Requisitos del MVP

- Proyecto: Reserva de Salas de Estudio — UPB Santa Cruz (P02)
- Integrantes que participan: Raúl Vaca (Hugo Zúñiga se incorpora en la fase 7)
- Docente y cliente: Ing. Sergio Barrientos
- Fecha: 15/10/2026 · Fase 1 · Issue #2 · Milestone F1 Requisitos
- Plan: [Sesiones 8–9](sesion-08-09-plan.md) · Cambios: [cambios.md](cambios.md)
- Actualizado: 18/10/2026 · anexo con los datos del repositorio anterior (sección 9, C-12), administrador 10003 en el padrón (C-13) y glosario de siglas (C-14). Las reglas no cambian.

## 0. Cómo leer este documento

El significado de cada sigla de este documento (RF, HU, CU, FE, MW, P-xx, C-xx…) está en [glosario.md](glosario.md) (cambio C-14).

Cada requisito, y cada parte de un requisito cuando hace falta, lleva una de estas tres marcas:

| Marca | Significa |
|---|---|
| **[ACUERDO]** | Lo indicó o aprobó el docente. Se cita la fuente. |
| **[PROPUESTA]** | Lo decidió o propuso el equipo y el docente todavía no lo confirmó. |
| **[PROVISIONAL]** | Valor que usamos mientras el docente no responda una pregunta abierta (sección 6). Si responde distinto, se registra en `cambios.md` y se corrige. |

**Bloques horarios.** Las reservas se hacen por bloques fijos (RES-RF-09):

| Bloque | B1 | B2 | B3 | B4 | B5 | B6 |
|---|---|---|---|---|---|---|
| Horario | 07:45–09:45 | 10:00–12:00 | 12:15–14:15 | 14:30–16:30 | 16:45–18:45 | 19:00–21:00 |

**Personas del padrón usadas en los ejemplos** [PROPUESTA]. El padrón (`padron/padron.json`) tiene 24 entradas: 15 estudiantes reales del curso, el docente, tres administradores y las cinco personas ficticias de los ejemplos (cambios C-09 y C-13). Los ejemplos y las pruebas usan solo las personas de esta tabla; los datos de los estudiantes reales no se copian a los documentos.

| Código | Nombre | Correo | Rol | Matrícula al día | Activa | Nota |
|---|---|---|---|---|---|---|
| 31245 | Valeria Rojas | valeria.rojas@upb.example | Estudiante de pregrado | Sí | Sí | Ficticia |
| 31246 | Mateo Suárez | mateo.suarez@upb.example | Estudiante de pregrado | Sí | Sí | Ficticio |
| 31247 | Lucía Fernández | lucia.fernandez@upb.example | Estudiante de pregrado | **No** | Sí | Ficticia |
| 31248 | Diego Vargas | diego.vargas@upb.example | Estudiante de pregrado | Sí | **No** | Ficticio |
| 20101 | Ana Gutiérrez | ana.gutierrez@upb.example | Docente | — | Sí | Ficticia |
| 10001 | Sergio Barrientos | adminsergio@upb.example | Administrador | — | Sí | Cuenta de administrador del docente, aparte de su cuenta de docente; correo inventado |
| 10002 | Raúl Vaca | adminraul@upb.example | Administrador | — | Sí | Segundo administrador; correo inventado. No aparece en los ejemplos |
| 10003 | Hugo Zuñiga | adminhugo@upb.example | Administrador | — | Sí | Tercer administrador (C-13); correo inventado. No aparece en los ejemplos |

**Salas** [capacidades **[PROVISIONAL]**, ficticias y declaradas como tales]:

| Sala | A | B | C | D | E | F | H | J |
|---|---|---|---|---|---|---|---|---|
| Capacidad | 6 | 4 | 6 | 8 | 10 | 6 | 12 | 4 |
| Nivel | Posgrado | Pregrado | Pregrado | Pregrado | Posgrado | Pregrado | Pregrado | Pregrado |

Que pregrado no use A ni E es **[PROVISIONAL]** (P-16). Ver RF-11.

**Fechas de los ejemplos.** El lunes 19/10/2026 abre la semana que se usa en casi todos los ejemplos. Cada criterio fija su "hora actual".

## 1. Fuentes

| ID | Fuente | Qué aporta |
|---|---|---|
| ENC | Encargo P02 (sesión 2) | Necesidades RES-01 a RES-08, situaciones para analizar y condiciones comunes del curso |
| S4 | `sesion04.md` (repositorio anterior) | 15 min de desalojo, una sala por bloque, ejemplo 07:45–09:45 → 10:00 y "modificar hasta 10 min después de realizada" |
| S6 | `sesion-06-requisitos.md` (repositorio anterior), entrevista ENT-01 a ENT-08 | Reglas RES-RF-01 a 07 aprobadas por el docente |
| D07 | README del repositorio anterior, decisiones del 07/10/2026 | MongoDB aprobado; anticipación de pregrado desde las 18:00; recorridos de registro (FE → MW → Padrón → BD) e inicio de sesión (FE → MW → BD) |
| DR | Indicaciones del docente comunicadas por Raúl, **fecha no registrada** | (1) No reservar dos bloques seguidos el mismo día. (2) Los estudiantes de posgrado pueden reservar las salas A y E. |
| E15 | Decisiones del equipo (Raúl), 15/10/2026 | Valores provisionales y decisiones de alcance del MVP |

El contenido de ENC, S4, S6 y D07 está copiado en el anexo de la sección 9, con enlaces al repositorio anterior.

## 2. Alcance del MVP

**Incluye:** registro con el padrón, inicio y cierre de sesión, consulta de salas libres, crear, ver, cancelar y modificar reservas, mantenimiento de salas por período y gestión de reservas ajenas por el administrador.

**Actores:** estudiante de pregrado, docente y administrador.

### Qué reglas aplican a quién

| Regla | Pregrado | Docente | Administrador (reserva propia) | Administrador modificando una reserva ajena |
|---|---|---|---|---|
| RF-01 Sala ocupada en el bloque (15 min) | Sí | Sí | Sí | Sí |
| RF-02 Una reserva por bloque | Sí | Sí | Sí | Las del dueño |
| RF-04 Capacidad | Sí | Sí | Sí | Sí |
| RF-05 Matrícula al día | Sí | No | No | Las del dueño |
| RF-06 Solo antes de que empiece (modificar) | Sí | Sí | Sí | Sí |
| RF-08 Bloques no seguidos | Sí | No **[PROVISIONAL]** | No **[PROVISIONAL]** | Las del dueño |
| RF-10 Anticipación | Sí | No **[PROVISIONAL]** | No **[PROVISIONAL]** | Las del dueño |
| RF-11 Salas A y E | No puede usarlas **[PROVISIONAL]** | Puede | Puede | Las del dueño |

"Las del dueño" significa que, cuando el administrador modifica una reserva ajena, se aplican las reglas de la persona dueña de la reserva **[PROPUESTA, E15]**. El administrador no puede dejarle a un estudiante una reserva que el propio estudiante no podría tener.

### Limitaciones del MVP (declaradas)

- El mantenimiento solo se registra en bloques que todavía no empezaron (RF-12).
- Un período de mantenimiento registrado no se puede quitar, y las reservas que canceló no se restauran.
- Al modificar una reserva no se puede cambiar de sala: para eso se cancela y se reserva de nuevo **[PROVISIONAL]**.
- El aviso por cancelación de mantenimiento no se envía por email ni WhatsApp: el estado "Cancelada por mantenimiento" se ve en el sistema. El encargo permite esto: "el estado debe poder consultarse en el sistema".
- El criterio de RF-07 prueba dos solicitudes seguidas, **no** dos solicitudes en el mismo instante (ver RF-07).

**Fuera del MVP:** historial de correcciones (RES-07), agenda por sala (RES-08), estudiantes de posgrado y doctorado, salas G e I, reservas recurrentes y pagos.

## 3. Requisitos funcionales

### RES-RF-01 — Sala ocupada en el bloque (15 min de desalojo)

- Origen: ENC (RES-04); S4 y S6 (ENT-01). Prioridad: alta, porque es el problema central del cliente.
- Estado: **[ACUERDO]** 15 min de desalojo entre dos reservas de la misma sala (S4, S6). La forma de expresarla con bloques es **[PROVISIONAL]** (ver RF-09 y el cambio C-01).
- Requisito: una sala puede tener como máximo **una reserva confirmada por fecha y bloque**. Como los bloques están separados por 15 min, dos reservas en bloques distintos de la misma sala siempre respetan el desalojo. Si el bloque pedido ya está reservado en esa sala, el sistema rechaza la solicitud y no registra nada.
- Criterio de aceptación:
  - Situación inicial: Mateo (31246) tiene la sala B el jueves 22/10 en B1 (07:45–09:45). Hoy es miércoles 21/10, 18:05.
  - Límite (se acepta): Valeria (31245) pide la sala B el jueves 22/10 en B2 (10:00–12:00), 3 asistentes. Se confirma, porque hay exactamente 15 min entre las 09:45 y las 10:00 (el mismo caso que S4). La sala B queda con dos reservas.
  - Rechazo: Valeria pide la sala B el jueves 22/10 en B1. Se rechaza por "sala ocupada en ese bloque" y la sala B conserva solo la reserva de Mateo en B1.

### RES-RF-02 — Una reserva por persona en el mismo bloque

- Origen: ENC (RES-04); S4 y S6 (ENT-02). Prioridad: alta.
- Estado: **[ACUERDO]** (S4, S6).
- Requisito: si la persona ya tiene una reserva confirmada en la misma fecha y bloque, en cualquier sala, el sistema rechaza la nueva y conserva la existente. Las reservas canceladas no cuentan.
- Criterio de aceptación:
  - Situación inicial: Valeria tiene la sala B el jueves 22/10 en B2. Hoy es miércoles 21/10, 18:05.
  - Acción: Valeria pide la sala C el jueves 22/10 en B2.
  - Resultado: se rechaza por "ya tienes una reserva en ese bloque". Solo existe su reserva de la sala B.

### RES-RF-03 — Modificación rechazada: "¿Deseas mantenerla?"

- Origen: ENC (RES-05); S6 (ENT-03). Prioridad: alta.
- Estado: **[ACUERDO]** (S6). Que **Esc** cancele la reserva es **[PROVISIONAL]** (pregunta P-02).
- Requisito: si el nuevo bloque, la nueva fecha o los nuevos asistentes de una modificación no cumplen las reglas de reserva, el sistema rechaza el cambio, no aplica nada e informa la causa. Luego pregunta al estudiante "¿Deseas mantenerla?":
  - Con **"Sí"**, la reserva original se conserva sin cambios.
  - Con **"No"** o **Esc**, la reserva original pasa a **Cancelada**. El registro se conserva con sus datos originales.

  Si quien modifica es el administrador (reserva ajena), el cambio se rechaza y la reserva queda intacta, **sin** la pregunta **[PROPUESTA, E15]**.
- Criterio de aceptación:
  - Situación inicial: Valeria tiene la sala B el jueves 22/10 en B2; Mateo tiene la sala B el jueves 22/10 en B3. Hoy es miércoles 21/10, 19:00.
  - Acción: Valeria intenta mover su reserva a B3.
  - Resultado: se rechaza por "sala ocupada en ese bloque" y aparece "¿Deseas mantenerla?".
    - Con "Sí": la reserva de Valeria sigue en B2, con sus mismos asistentes.
    - Con "No": la reserva de Valeria queda Cancelada, todavía en B2.
    - En los dos casos, la reserva de Mateo no cambia.

### RES-RF-04 — Capacidad de la sala

- Origen: ENC (RES-03, RES-04; "el número de asistentes coincide exactamente con la capacidad"). Prioridad: alta.
- Estado: rechazar si se supera la capacidad es **[ACUERDO]** (S6). Aceptar si los asistentes son iguales a la capacidad es **[PROVISIONAL]** (P-03). Las capacidades son **[PROVISIONAL]** (P-11).
- Requisito: los asistentes son un número entero de 1 o más, que incluye a quien reserva y no registra nombres. Si superan la capacidad de la sala, el sistema rechaza la reserva o la modificación y no registra cambios.
- Criterio de aceptación:
  - Situación inicial: la sala B (capacidad 4) está libre el jueves 22/10 en B2. Hoy es miércoles 21/10, 18:05.
  - Límite (se acepta): Valeria pide la sala B para **4** asistentes y se confirma.
  - Rechazo: con la misma situación, Valeria pide la sala B para **5** asistentes. Se rechaza por "capacidad superada" y no se crea ninguna reserva.

### RES-RF-05 — Solo reservan estudiantes con matrícula al día

- Origen: ENC (RES-01, RES-04); S6 (ENT-04). Prioridad: alta.
- Estado: la regla es **[ACUERDO]** (S6). Que el dato se lea del padrón lo indicó Raúl al listar los acuerdos (15/10/2026). En la fase 2 se decidió copiarlo del padrón a la cuenta al registrarse (diseño, D-01); la limitación que resulta es la pregunta P-17 (cambio C-06).
- Requisito: un estudiante sin la matrícula al día puede tener cuenta (RF-13), pero el sistema rechaza todas sus reservas con el motivo "matrícula no vigente" y no registra nada. Esta regla no se aplica al docente ni al administrador.
- Criterio de aceptación:
  - Situación inicial: Lucía (31247, matrícula no al día) tiene cuenta. La sala C está libre el jueves 22/10 en B2. Hoy es miércoles 21/10, 18:05.
  - Acción: Lucía pide la sala C el jueves 22/10 en B2.
  - Resultado: se rechaza por "matrícula no vigente" y la sala C sigue libre.

### RES-RF-06 — Modificar o cancelar solo antes de que la reserva empiece

- Origen: ENC (RES-05); S6 (ENT-08). Prioridad: alta.
- Estado:
  - Modificar solo antes de que empiece: **[ACUERDO]** (S6).
  - La regla de S4, "hasta 10 minutos después de realizada", queda como pregunta abierta (P-01) y por ahora no se aplica.
  - Que el estudiante solo cancele antes de que empiece es **[PROVISIONAL]** (P-10).
  - Que el administrador pueda cancelar en cualquier momento es **[PROPUESTA, E15]**.
  - Que solo el dueño de la reserva pueda cancelarla o modificarla es **[PROPUESTA]** (cambio C-04).
- Requisito: una reserva **ya comenzó** cuando la hora actual es igual o posterior al inicio de su bloque. Una reserva que ya comenzó no se puede modificar, y el estudiante tampoco puede cancelarla: el sistema informa "la reserva ya comenzó" y la conserva sin cambios.
- **[PROPUESTA]** Solo el dueño de la reserva puede cancelarla o modificarla (el administrador, en cualquier momento). Para **modificar**, el administrador también respeta lo de arriba: solo antes de que la reserva empiece.
- Criterio de aceptación:
  - Situación inicial: Valeria tiene la sala B el jueves 22/10 en B2 (10:00–12:00). Hoy es **jueves 22/10, 10:00** (justo el inicio).
  - Acción: Valeria intenta mover su reserva a B4.
  - Resultado: se rechaza por "la reserva ya comenzó" y la reserva sigue en B2.
- Criterio de aceptación (dueño) **[PROPUESTA]**:
  - Situación inicial: Mateo tiene la sala D el jueves 22/10 en B3. Hoy es miércoles 21/10, 19:00.
  - Acción: Valeria intenta cancelar la reserva de Mateo.
  - Resultado: se rechaza por "la reserva no es tuya" y la reserva de Mateo sigue Confirmada.
  - La parte de **modificar** una reserva ajena no tiene criterio ni test propio. Se declara así en la trazabilidad.

### RES-RF-07 — Solicitudes casi simultáneas: gana la primera

- Origen: ENC ("dos personas intentan reservar el mismo intervalo"); S6 (ENT-07). Prioridad: media.
- Estado: **[ACUERDO]** (S6).
- Requisito: si dos personas piden la misma sala, fecha y bloque casi al mismo tiempo, la reserva queda solo a nombre de quien envió primero; la segunda se rechaza por "sala ocupada en ese bloque".
- Criterio de aceptación:
  - Situación inicial: la sala D está libre el jueves 22/10 en B3. Hoy es miércoles 21/10, 18:05.
  - Acción: Valeria envía la solicitud y, enseguida, Mateo envía la misma.
  - Resultado: existe una sola reserva de la sala D en B3, a nombre de Valeria, y la de Mateo se rechaza.
- **Limitación del criterio:** prueba dos solicitudes **seguidas**, no dos solicitudes en el **mismo instante**. El mismo instante se resuelve en el diseño con un índice único parcial (D-02).

### RES-RF-08 — No reservar dos bloques seguidos el mismo día

- Origen: DR (indicación del docente, comunicada por Raúl, fecha no registrada), para evitar el uso excesivo de las salas. Prioridad: media.
- Estado: la regla para estudiantes es **[ACUERDO]** (DR). Que **no** se aplique al docente ni al administrador es **[PROVISIONAL]** (P-08). Se agregó como cambio C-02.
- Requisito: un estudiante no puede tener reservas confirmadas en dos bloques contiguos de la misma fecha, en ninguna sala. Sí puede tener bloques alternados (B1 y B3, o B1, B3 y B5).
- Criterio de aceptación:
  - Situación inicial: Valeria tiene la sala B el jueves 22/10 en B2. Hoy es miércoles 21/10, 18:05.
  - Rechazo: Valeria pide la sala C el jueves 22/10 en **B3**. Se rechaza por "no puedes reservar dos bloques seguidos", aunque sea en otra sala.
  - Límite (se acepta): Valeria pide la sala C el jueves 22/10 en **B4** (alternado) y se confirma.

### RES-RF-09 — Bloques fijos, horario y días de atención

- Origen: ENC ("horario de apertura", "días sin servicio", "unidad fija de tiempo"). Prioridad: alta, porque las demás reglas dependen de los bloques.
- Estado: **[PROVISIONAL]** (P-06, P-07). S4 respalda solo en parte: su ejemplo de 07:45–09:45 y la siguiente a las 10:00 coincide con B1 y B2.
- Requisito: solo se reserva en uno de los seis bloques de la sección 0, de lunes a viernes. No hay duración libre. Nadie, ni docente ni administrador, puede reservar ni mover una reserva a un bloque que ya empezó o ya pasó **[PROPUESTA, E15]**.
- Criterio de aceptación:
  - Situación inicial: hoy es viernes 23/10, 10:00. Ana (docente, sin límite de anticipación) tiene cuenta.
  - Acción: Ana pide la sala C el **sábado 24/10** en B2.
  - Resultado: se rechaza por "no hay atención ese día" y no se crea ninguna reserva.

### RES-RF-10 — Anticipación para reservar

- Origen: ENC; D07 (decisión del 07/10/2026). Prioridad: alta.
- Estado:
  - Pregrado reserva el día siguiente desde las 18:00: **[ACUERDO]** (D07).
  - Pregrado también reserva el mismo día, en bloques que aún no empezaron: **[PROVISIONAL]** (P-04).
  - Después de un viernes viene el lunes, porque cuenta el día de clase anterior: **[PROVISIONAL]** (P-05).
  - El docente y el administrador no tienen límite de anticipación: **[PROVISIONAL]** (P-13).
- Requisito: un estudiante de pregrado puede reservar:
  - **hoy**, en bloques que aún no empezaron;
  - el **siguiente día de clase**, solo desde las 18:00 del día de clase anterior.

  Nada más allá de eso. La consulta de salas (HU-03) muestra solo las fechas y bloques que el usuario puede reservar en ese momento; si pide otra fecha, recibe el motivo **[PROPUESTA, E15]**.
- Criterio de aceptación:
  - Rechazo: hoy es miércoles 21/10, **17:59**. Valeria pide la sala C el jueves 22/10 en B1. Se rechaza con "las reservas para el jueves se abren el miércoles a las 18:00".
  - Límite (se acepta): la misma solicitud a las **18:00** se confirma.
  - Viernes → lunes **[PROVISIONAL]**: hoy es viernes 16/10, 18:00. Valeria pide la sala C el lunes 19/10 en B1 y se confirma.

### RES-RF-11 — Salas A y E no disponibles para pregrado

- Origen: DR (indicación del docente comunicada por Raúl, fecha no registrada). Prioridad: media.
- Estado:
  - Los estudiantes de posgrado pueden reservar A y E: **[ACUERDO]** (DR).
  - Los estudiantes de pregrado **no** pueden usar A ni E: **[PROVISIONAL]** (P-16).
  - En el MVP, posgrado sigue fuera y solo el docente y el administrador reservan A y E: **[PROPUESTA, E15]**.
- Requisito: un estudiante de pregrado no puede reservar las salas A ni E, y la consulta no se las muestra. El docente y el administrador sí pueden.
- Criterio de aceptación:
  - Situación inicial: la sala A está libre el jueves 22/10 en B2. Hoy es miércoles 21/10, 18:05.
  - Rechazo: Valeria pide la sala A. Se rechaza por "sala no disponible para tu nivel" y no se crea ninguna reserva.
  - Aceptación: Ana (docente) pide la sala A y se confirma.

### RES-RF-12 — Mantenimiento de una sala por período

- Origen: ENC (RES-06, "bloquear períodos"); S6 (ENT-05: cancelar y avisar; ENT-06: el encargado inhabilita). Prioridad: media.
- Estado:
  - Cancelar las reservas afectadas y avisar: **[ACUERDO]** (S6). El canal (email o WhatsApp) queda pendiente (P-12).
  - Que se registre por período (fecha y bloques), que el aviso sea un estado visible en el sistema y que solo se pueda en bloques que aún no empezaron: **[PROPUESTA, E15]**.
- Requisito: el administrador registra un mantenimiento indicando sala, fecha y uno o más bloques que todavía no empezaron. El sistema:
  - cancela las reservas confirmadas de esa sala en esos bloques, que el dueño ve como "Cancelada por mantenimiento";
  - rechaza cualquier reserva o modificación nueva en ese período.
- Criterio de aceptación:
  - Situación inicial: Valeria tiene la sala C el jueves 22/10 en B2. Hoy es miércoles 21/10, 20:00.
  - Acción: Sergio (10001, administrador) registra mantenimiento de la sala C el jueves 22/10 en B2 y B3.
  - Resultado: la reserva de Valeria queda "Cancelada por mantenimiento". Si Mateo pide luego la sala C el jueves 22/10 en B3, se rechaza por "sala en mantenimiento".
  - Rechazo: hoy es jueves 22/10, 10:30. Sergio intenta registrar mantenimiento en B2, que ya empezó. Se rechaza y no se cancela nada.

### RES-RF-13 — Registro con el padrón

- Origen: arquitectura indicada por el docente (D07: registro FE → MW → Padrón → BD). Prioridad: alta.
- Estado:
  - El recorrido del registro: **[ACUERDO]** (D07).
  - Los cuatro rechazos, que la matrícula vencida no impida registrarse, y que la contraseña siga las reglas por defecto de Django: **[PROPUESTA, E15]**.
- Requisito: una persona sin cuenta escribe su código y su correo. El sistema los busca en el padrón, y si cumplen todo, la persona elige su contraseña y se crea su cuenta en la BD. Se rechaza si:
  1. el código no existe en el padrón;
  2. el correo no es el de ese código;
  3. la persona está inactiva;
  4. la persona ya tiene cuenta.

  El padrón es de solo lectura: el sistema nunca lo modifica y no guarda contraseñas en él.
- Criterio de aceptación:
  - Aceptación: Valeria (31245, valeria.rojas@upb.example), sin cuenta, se registra con una contraseña válida. Se crea su cuenta y el padrón no cambia.
  - Rechazo: Diego (31248, inactivo) intenta registrarse. Se rechaza por "persona no activa en el padrón" y no se crea ninguna cuenta.

### RES-RF-14 — Inicio y cierre de sesión

- Origen: arquitectura indicada por el docente (D07: inicio de sesión FE → MW → BD, sin consultar el padrón). Prioridad: alta.
- Estado:
  - El recorrido: **[ACUERDO]** (D07).
  - Entrar con correo y contraseña, y un único mensaje de error: **[PROPUESTA, E15]**.
- Requisito: el usuario entra con su correo y su contraseña, que se comparan con su cuenta en la BD. Si algo falla, el mensaje es siempre "Correo o contraseña incorrectos", sin decir cuál de los dos. Al cerrar sesión, las operaciones vuelven a pedir inicio de sesión.
- Criterio de aceptación:
  - Situación inicial: Valeria tiene cuenta.
  - Aceptación: entra con su correo y su contraseña, y el sistema la identifica.
  - Rechazo: con una contraseña incorrecta recibe "Correo o contraseña incorrectos", el mismo mensaje que con un correo inexistente.

## 4. Requisitos de calidad

### RES-RC-01 — El rechazo muestra la causa concreta

- Estado: **[PROPUESTA]** del equipo (S6), pendiente de confirmar (P-15).
- Requisito: cada rechazo nombra su causa: sala ocupada, ya tiene una reserva en ese bloque, bloques seguidos, capacidad superada, matrícula no vigente, ya comenzó, anticipación, sala no disponible para su nivel, sala en mantenimiento, día sin atención o la reserva no es tuya. Un mensaje genérico como "Error" no cumple.
- Comprobación: los criterios de rechazo de este documento ya indican el mensaje esperado.

### RES-RC-02 — Una consulta no modifica datos

- Estado: **condición del encargo** (ENC, "Condiciones comunes del curso").
- Requisito: consultar salas libres (HU-03) o ver "mis reservas" no crea, cambia ni borra nada en la BD.

### RES-RC-03 — Un rechazo no deja la operación a medias

- Estado: **condición del encargo** (ENC: "Un error debe producir un mensaje comprensible y no dejar una operación incompleta").
- Requisito: cuando una operación se rechaza, los datos quedan exactamente como estaban antes. Cada criterio de rechazo comprueba qué se conserva.
- El encargo también pide que la misma operación no se duplique por un reintento. Esto ya lo cubre RF-02: si se reenvía la misma reserva, se rechaza por "ya tienes una reserva en ese bloque".

## 5. Restricciones

| ID | Restricción | Estado |
|---|---|---|
| RES-RT-01 | Las reglas de negocio se implementan en Python | **Condición del encargo** |
| RES-RT-02 | Todas las fechas y horas se interpretan en la zona horaria America/La_Paz | **Condición del encargo** ("una zona horaria local acordada") |
| RES-RT-03 | La persistencia usa MongoDB, a través de Django (django-mongodb-backend), en lugar de MySQL o MariaDB | **[ACUERDO]** (D07, aprobado por el docente el 07/10/2026) |

## 5.1 Resumen de casos límite

Son los casos que más se discuten en una defensa.

| Requisito | Límite | Resultado |
|---|---|---|
| RF-01 | B1 ocupado; otra persona pide B2 en la misma sala (15 min exactos) | Se acepta |
| RF-04 | Asistentes = capacidad (4 en la sala B) | Se acepta **[PROVISIONAL]** |
| RF-06 | Modificar justo a la hora de inicio (10:00 en B2) | Se rechaza: ya comenzó |
| RF-08 | B2 y luego B4 el mismo día (alternado) | Se acepta |
| RF-10 | Pregrado pide el día siguiente a las 18:00 exactas | Se acepta (a las 17:59 se rechaza) |

## 6. Preguntas abiertas para el docente

Se siguen en el issue #26. Mientras no haya respuesta, rige el valor provisional. La numeración P-01 a P-17 es de este repositorio; la del repositorio anterior (P1 a P12) y sus equivalencias están en la sección 9.5.

| ID | Pregunta | Valor provisional | Afecta |
|---|---|---|---|
| P-01 | Además de "solo antes de que empiece", ¿rige la regla de S4: "modificar hasta 10 minutos después de realizada"? | No se aplica | RF-06 |
| P-02 | Al presionar Esc en "¿Deseas mantenerla?", ¿la reserva se cancela? | Sí, se cancela | RF-03 |
| P-03 | Si los asistentes son iguales a la capacidad, ¿se acepta? | Sí | RF-04 |
| P-04 | ¿Pregrado puede reservar el mismo día, en bloques que aún no empezaron? | Sí | RF-10 |
| P-05 | Fin de semana: ¿el lunes se abre el viernes a las 18:00 (día de clase anterior) o el domingo a las 18:00 (día de calendario)? | Viernes a las 18:00 | RF-10 |
| P-06 | ¿Los días de atención son solo de lunes a viernes? | Sí | RF-09 |
| P-07 | ¿Las reservas son por bloques fijos de 2 h (B1 a B6), con horario de 07:45 a 21:00? | Sí | RF-09, RF-01 |
| P-08 | ¿La regla de bloques no seguidos aplica también al docente y al administrador? | No | RF-08 |
| P-09 | ¿Se puede cambiar de sala al modificar una reserva? | No: se cancela y se reserva de nuevo | RF-03, HU-07 |
| P-10 | ¿Un estudiante puede cancelar una reserva que ya comenzó? | No | RF-06 |
| P-11 | ¿Qué capacidad tiene cada sala? | Las ficticias de la sección 0 | RF-04 |
| P-12 | Ante una cancelación por mantenimiento, ¿se avisa por email, por WhatsApp o por ambos? | Solo el estado visible en el sistema | RF-12 |
| P-13 | ¿El docente y el administrador quedan fuera de la regla de anticipación? (Era la pregunta P10 del repositorio anterior, sin respuesta) | Sí, quedan fuera | RF-10 |
| P-14 | Posgrado: ¿puede usar también las salas de pregrado? | Aplazado: posgrado está fuera del MVP | RF-11 |
| P-15 | ¿Se aprueba que cada rechazo muestre su causa concreta? | Sí | RC-01 |
| P-16 | ¿Los estudiantes de pregrado pueden usar las salas A y E? | No | RF-11 |
| P-17 | La matrícula al día, el rol y el nivel se copian del padrón a la cuenta al registrarse, y al reservar ya no se consulta el padrón. ¿Es aceptable que, si el padrón cambiara después del registro, la cuenta no se actualice? (En el MVP el padrón es estático y de solo lectura.) Agregada el 15/10/2026, cambio C-06 | Sí, es aceptable; queda como limitación declarada | RF-05, RF-13 |

## 7. Siguiente paso

- Documento siguiente de la fase 1: `docs/sesion-07-modelos.md`, con las historias HU-01 a HU-09, sus criterios Dado/Cuando/Entonces, los casos de uso CU-01 a CU-09 y el diagrama de actividad de HU-07 (issue #3).
- Los criterios de este documento se reutilizan allí con los mismos datos, para que cada test salga de un criterio y no de un detalle del código.

## 8. Participación y asistencia utilizada

- **Raúl Vaca:** respondió las preguntas de la fase 1, definió los valores provisionales y las limitaciones, y revisó el documento antes del commit.
- **Asistencia de IA:** se usó Claude (Anthropic) para comparar las respuestas con las sesiones 4 y 6 y el README del repositorio anterior, proponer la estructura y redactar el borrador.
- **Hugo Zúñiga (18/10/2026):** sumó a este documento las entrevistas y los datos del repositorio anterior (C-12), se agregó al padrón como administrador con el código 10003 (C-13) y creó el glosario de siglas (C-14), en el issue #28 (H0).
- **Asistencia de IA (18/10/2026):** se usó Claude (Anthropic) para copiar las entrevistas del repositorio anterior sin cambiar su texto, comprobar los datos citados contra el commit `4353d1d`, redactar el glosario y aplicar C-12, C-13 y C-14.

## 9. Anexo — Datos adjuntos del repositorio anterior

Los IDs **ENC**, **S4**, **S6** y **D07** (sección 1) apuntan al repositorio anterior, [campus-challenge-equipo-01](https://github.com/raulandres24/campus-challenge-equipo-01), que queda solo como referencia y no se modifica. Este anexo copia lo que usamos de él para poder leerlo sin salir de este repositorio. **No crea reglas**: las reglas vigentes siguen en la sección 3, con el estado de cada una. Se agregó el 18/10/2026 (cambio C-12).

**Versión citada:** commit `4353d1d` del 14/10/2026. Los enlaces apuntan a ese commit y no a la rama, para que sigan mostrando lo mismo aunque el repositorio anterior cambie.

| Sigla | Archivo en el repositorio anterior | Enlace |
|---|---|---|
| S4 | `docs/sesion04.md` | [ver](https://github.com/raulandres24/campus-challenge-equipo-01/blob/4353d1df2b5ecf3f3debd4a5c67290e9b2296fa7/docs/sesion04.md) |
| S6 | `docs/sesion-06-requisitos.md` (entrevista del 01/10/2026) | [ver](https://github.com/raulandres24/campus-challenge-equipo-01/blob/4353d1df2b5ecf3f3debd4a5c67290e9b2296fa7/docs/sesion-06-requisitos.md) |
| D07 | `README.md` (bitácora de decisiones y preguntas P1 a P12) | [ver](https://github.com/raulandres24/campus-challenge-equipo-01/blob/4353d1df2b5ecf3f3debd4a5c67290e9b2296fa7/README.md) |
| ENC | El encargo no está en ese repositorio; solo un resumen de RES-01 a RES-08 en `docs/BRECHA_REQUISITOS.md` | [ver](https://github.com/raulandres24/campus-challenge-equipo-01/blob/4353d1df2b5ecf3f3debd4a5c67290e9b2296fa7/docs/BRECHA_REQUISITOS.md) |
| — | `docs/sesion-13-14-revision (Raul).md`, la revisión que cita la sesión 12 | [ver](https://github.com/raulandres24/campus-challenge-equipo-01/blob/4353d1df2b5ecf3f3debd4a5c67290e9b2296fa7/docs/sesion-13-14-revision%20(Raul).md) |
| — | `docs/TRAZABILIDAD_PRUEBAS.md`, donde figuran las 129 pruebas que cita el plan | [ver](https://github.com/raulandres24/campus-challenge-equipo-01/blob/4353d1df2b5ecf3f3debd4a5c67290e9b2296fa7/docs/TRAZABILIDAD_PRUEBAS.md) |

### 9.1 ENC — Necesidades del encargo (RES-01 a RES-08)

El encargo del curso (P02, sesión 2) lo compartió el docente aparte. La tabla es el resumen que hizo el equipo en `docs/BRECHA_REQUISITOS.md`, **no el texto original**.

| ID | Qué pide el encargo | Dónde aparece aquí |
|---|---|---|
| RES-01 | Registrar espacios (id, capacidad, estado) y solicitantes | RF-05 |
| RES-02 | Consultar disponibilidad por fecha, horario y capacidad | HU-03 (consulta de salas libres) |
| RES-03 | Crear una reserva (solicitante, espacio, intervalo, asistentes) | RF-04 |
| RES-04 | Aplicar reglas de horario, capacidad y conflictos antes de confirmar | RF-01, RF-02, RF-04, RF-05, RF-07 |
| RES-05 | Modificar o cancelar una reserva | RF-03, RF-06 |
| RES-06 | Registrar bloqueos administrativos o de mantenimiento | RF-12 |
| RES-07 | Corregir una operación administrativa conservando motivo e historial | Fuera del MVP |
| RES-08 | Mostrar agenda por espacio, reservas activas y cancelaciones | Fuera del MVP |

### 9.2 S4 — Aclaraciones del cliente en la sesión 4

Entrevista al docente en la sesión 4 (`docs/sesion04.md`; el documento no registra la fecha). El backlog de esa sesión tenía cinco ítems **PB** (PB-01 crear reserva, PB-02 consultar espacios, PB-03 validar código, PB-04 modificar reserva, PB-05 cancelar reserva) y se trabajó PB-01.

| Pregunta | Respuesta del docente | Efecto en S4 | Dónde queda aquí |
|---|---|---|---|
| ¿Existe un intervalo de tiempo entre reservas para el desalojo? | Se propone un intervalo de 15 minutos. | Diferencia obligatoria de 15 min entre el fin de una reserva y el inicio de la siguiente de la misma sala. | RF-01 (ENT-01) |
| ¿Cuántas salas puede reservar un alumno por horario? | Una sola sala. | Si ya tiene una reserva activa en ese bloque, se rechaza la nueva. | RF-02 (ENT-02) |
| ¿Hasta cuánto tiempo antes se permite modificar? | Hasta 10 minutos después de haber sido realizada. | Se aplicaría al programar PB-04. | Pregunta P-01: por ahora no se aplica |

**Ejemplo límite de S4** (el que respalda C-01 y RF-09): hay una reserva en la sala A de 07:45 a 09:45 y se pide la misma sala de 10:00 a 12:00. Resultado: CONFIRMADA, porque el fin y el inicio respetan exactamente los 15 minutos. Es el caso de B1 y B2.

### 9.3 S6 — Entrevistas ENT-01 a ENT-08

Fuente: sesión 6 del repositorio anterior (entrevista del 01/10/2026). ENT-01 y ENT-02 vienen de la entrevista de la sesión 4. El docente es el Ing. Sergio Barrientos. El texto es el original; la columna "Estado" es la que tenían allí.

| ID | Pregunta | Respuesta del docente | Estado en el repositorio anterior | Alimenta |
|---|---|---|---|---|
| ENT-01 | ¿Cuánto tiempo debe pasar entre el fin de una reserva y el inicio de la siguiente en la misma sala? | Se propone un intervalo de 15 minutos de desalojo. | Confirmado | RF-01 (C-01) |
| ENT-02 | ¿Un estudiante puede tener dos reservas activas en el mismo bloque horario? | Una sola sala por horario, aunque sean salas distintas. | Confirmado | RF-02 |
| ENT-03 | Si un cambio de reserva es rechazado (ej.: sala A 10:00–12:00 movida a 12:30–13:50 con otra reserva a las 14:00), ¿la reserva original se mantiene o se pierde? | El sistema debe mostrar un mensaje preguntando "¿Deseas mantenerla?". Si responde que no o presiona Esc, la reserva original se cancela. | Confirmado | RF-03 (Esc: P-02) |
| ENT-04 | ¿Es coherente exigir en los términos y condiciones que solo puedan reservar estudiantes con matrícula al día? | Sí, es coherente: no puede reservar quien no tenga su matrícula al día. | Confirmado (falta definir cómo se verifica) | RF-05 (D-01, P-17) |
| ENT-05 | Si mantenimiento bloquea una sala y ya había una reserva en ese horario, ¿qué debe hacer el sistema con esa reserva? | La reserva se cancela y se avisa al estudiante por email o por mensaje de WhatsApp que su reservación fue cancelada. | Confirmado (falta definir el canal: email, WhatsApp o ambos) | RF-12 (P-12) |
| ENT-06 | ¿Qué pasa con las reservas existentes si se registra un bloqueo de mantenimiento en esa sala y horario? | La persona encargada de la gestión de las salas puede inhabilitarlas. | Confirmado | RF-12 |
| ENT-07 | Si dos personas reservan la misma sala a la misma hora, en el mismo segundo, ¿a nombre de quién queda la reserva? | A nombre de quien presionó primero el botón. | Confirmado | RF-07 |
| ENT-08 | ¿Se puede modificar o cancelar una reserva que ya comenzó? | No se puede modificar una vez que empezó; solo se puede modificar antes de que empiece. | Confirmado para modificar (cancelar: pendiente) | RF-06 (P-10) |

Los ejemplos de esas preguntas usan horarios libres (10:00–12:00, 12:30–13:50). Desde C-01 las reservas son por bloques, pero las respuestas del docente no cambian.

### 9.4 D07 — Respuestas del docente registradas en el README anterior

| Fecha | Respuesta o aclaración | Dónde queda aquí |
|---|---|---|
| 02/10/2026 | No usar el padrón real: usar una base estática con los estudiantes del aula. El docente explicó en la pizarra el recorrido FE → MW → DB estática → DB del proyecto. | RF-13, D-08 |
| 07/10/2026 | Se puede usar MongoDB junto con Django, en lugar de MySQL o MariaDB. | RT-03 |
| 07/10/2026 | Pregrado: las reservas de un día se abren a las 18:00 del día de clase anterior. Reemplaza dos respuestas anteriores del docente: "24 horas antes" y "desde las 21:00". | RF-10 |
| 07/10/2026 | Aclaración al recorrido: el padrón se consulta solo al registrarse; iniciar sesión no vuelve a consultarlo. | RF-13, RF-14, D-01 |

### 9.5 Preguntas P1 a P12 del repositorio anterior y su equivalente

El README anterior numeraba sus preguntas sin guion (P1 a P12). Aquí son P-01 a P-17. Solo la equivalencia P10 → P-13 está escrita en la sección 6; las demás se deducen del texto de cada pregunta.

| Anterior | Pregunta (resumen) | Equivalente aquí |
|---|---|---|
| P1 | ¿Sigue vigente "modificar hasta 10 minutos después de crearla" o rige "hasta que empiece"? | P-01 |
| P2 | Esc en "¿Deseas mantenerla?": ¿pierde la reserva? | P-02 |
| P3 | ¿Se acepta una reserva con asistentes igual a la capacidad? | P-03 |
| P4 | ¿Se puede cancelar una reserva ya iniciada? ¿Se puede mover a un horario pasado? | P-10 (cancelar). Mover a un bloque pasado: RF-09 [PROPUESTA] |
| P5 | Aviso de mantenimiento: ¿correo o WhatsApp? | P-12 |
| P6 | ¿Posgrado y doctorado reservan también las salas de pregrado? | P-14 |
| P7 | ¿Se registra la carrera de quien reserva? | Sin equivalente: el padrón nuevo no tiene el campo `carrera` |
| P8 | Pizarra "Reserva 10:00 / llega 10 am / 11 am": ¿qué significa "llega"? | Sin equivalente en el MVP |
| P9 | ¿Se pueden reservar sábado y domingo? | P-06 (aquí se atiende solo de lunes a viernes) |
| P10 | ¿Administradores y docente quedan fuera de la regla de anticipación? | P-13 |
| P11 | Si el padrón cambia después del registro, ¿cada cuánto se actualiza? | P-17 |
| P12 | Pregrado: ¿se reserva el mismo día antes de que empiece el bloque? | P-04 |

Preguntas nuevas de este repositorio, sin equivalente anterior: P-05, P-07, P-08, P-09, P-11, P-15 y P-16.
