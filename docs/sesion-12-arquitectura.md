# Sesión 12 — Arquitectura y verificación del flujo

> **BORRADOR (fase 2).** Las secciones 1 a 5 se escriben en el diseño. Las secciones 6 y 7 (cambio real, pruebas y CI) se completan con resultados reales en la fase 7 (domingo 18/10) y la fase 9. Lo que todavía no existe dice **pendiente**: no se presenta como hecho.

- Proyecto e integrantes: Reserva de Salas de Estudio — UPB Santa Cruz (P02); Raúl Vaca y Hugo Zúñiga (Hugo desde la fase 7).
- Fecha real de la actividad: 16/10/2026 (borrador del diseño).
- Requisitos: [Sesión 6](sesion-06-requisitos.md) · Modelos: [Sesión 7](sesion-07-modelos.md) · Plan: [Sesiones 8–9](sesion-08-09-plan.md) · Diseño: [Sesiones 13–14](sesion-13-14-diseno.md)
- Operación seleccionada: **modificar una reserva** (HU-07, CU-07).
- IDs vigentes: RES-RF-03 y RES-RF-06 **[ACUERDO]** (Esc en RF-03, **[PROVISIONAL]**, P-02); además las reglas de reserva que se vuelven a comprobar (RF-01, 02, 04, 05, 08, 09, 10, 11, 12). Cada una tiene su estado en los requisitos.
- Tarea/issue que continúa: #5 (este borrador); en la fase 7: #19 (tests de Hugo, que incluyen los de la sesión 12) y #21 (workflow de CI).
- Retroalimentación que atiende: la revisión de las sesiones 13–14 del repositorio anterior, en `docs/sesion-13-14-revision (Raul).md` ([enlace permanente](https://github.com/raulandres24/campus-challenge-equipo-01/blob/4353d1df2b5ecf3f3debd4a5c67290e9b2296fa7/docs/sesion-13-14-revision%20(Raul).md), commit `4353d1d`) (punto 4 del diagnóstico y sección 4, "Correcciones prioritarias"). La revisión encontró que la regla del margen y del choque estaba repetida en dos capas. El 16/10/2026, leyendo el código, se comprobó que la constante de 15 min tenía tres definiciones: `reservas/models.py:106`, `proyecto/clases/horarios.py:13` y `proyecto/clases/sistema_reservas.py:30`. Además, `proyecto/clases/reserva.py:221` tenía un valor por defecto fijo de 15. Por otro lado, el endpoint del administrador (`api_editar_reserva`) guardaba sin pasar por las reglas. Eso se comprobó el 15/10/2026 leyendo el código, con asistencia de IA, y Raúl lo confirmó (plan, sección 1).

## 1. Punto de partida y alcance

- **Qué ya funcionaba:** en este repositorio, nada todavía. Está en la fase 2 (diseño) y no tiene código. El repositorio anterior no se usa como base.
- **Problema que abordamos:** la revisión de las sesiones 13–14 encontró que la regla de los 15 min estaba repetida en dos capas, y que crear y modificar usaban capas distintas. La lectura del código del 16/10/2026 confirmó tres definiciones de la constante (`reservas/models.py:106`, `proyecto/clases/horarios.py:13` y `proyecto/clases/sistema_reservas.py:30`), más un valor por defecto fijo de 15 en `proyecto/clases/reserva.py:221`. Además, el administrador podía guardar sin pasar por las reglas.
- **Incluimos:** una sola capa de reglas (`reservas/reglas.py`), una capa que orquesta (`servicios.py`) y vistas sin reglas. El administrador modifica por la misma operación que el estudiante.
- **Queda pendiente:** el código (fases 4 a 6), las pruebas y el CI (fase 7).
- **Comando y resultado inicial real:** no ejecutado. Todavía no hay código ni pruebas en este repositorio.

## 2. Responsabilidades y dependencias

| Grupo/componente | Responsabilidad | Código (estado) | Usa qué interfaz de otro grupo |
|---|---|---|---|
| Recepción (FE → MW) | Recibir el formulario de modificar, llamar a la operación y mostrar el resultado o la causa del rechazo | `reservas/views.py` (propuesto, fase 6) | `servicios.modificar_reserva` y la clase `Rechazo` que ofrece `servicios` |
| Orquestación | Leer los datos necesarios, preguntar a las reglas, guardar si no hubo rechazo y traducir la clave duplicada | `reservas/servicios.py` (propuesto, fase 5) | Las funciones de `reglas.py` y los modelos |
| Reglas | Decidir si la modificación se permite y con qué causa se rechaza | `reservas/reglas.py` (propuesto, fase 5) | Ninguna: recibe datos ya leídos |
| Datos | Guardar la reserva y los índices únicos | `reservas/models.py` (propuesto, fase 4) | — |

- **Cohesión:** cada grupo tiene un solo propósito. `reglas` solo decide, `servicios` solo coordina, la vista solo recibe y responde.
- **Acoplamiento:**
  - `servicios` conoce los nombres de las funciones de `reglas` y los modelos.
  - Si cambia una regla (por ejemplo, la anticipación, P-04/P-05), solo cambia `reglas.py`.
  - Si cambia un campo de la reserva, cambian `models.py` y la lectura en `servicios`.
- **Frontera separada:** las vistas no importan `reglas` (tabla 5.4 del diseño).

## 3. Interfaz seleccionada

La interfaz completa está en el diseño, sección 6.3. Resumen:

- **Proveedor y consumidor:** `reservas/servicios.py` → `reservas/views.py`.
- **Firma propuesta:** `modificar_reserva(usuario, reserva_id, fecha, bloque, asistentes, ahora)`.
- **Entradas:**
  - `usuario` es la cuenta que entrega Django;
  - `reserva_id` es el texto del ObjectId;
  - `bloque` va de 1 a 6;
  - `asistentes` es un entero ≥ 1;
  - `ahora` es la fecha y hora en America/La_Paz.
- **Resultado aceptado:** la misma reserva (mismo `_id`) con los datos nuevos. Ninguna otra cambia.
- **Resultado de rechazo:** `Rechazo` con `causa` y `preguntar_si_mantener`. Este último es "sí" solo si se rechazó la propuesta (E1) y modifica el dueño.
- **Datos que deben conservarse:** ante un rechazo, todos. "No" a "¿Deseas mantenerla?" es otra operación (`no_mantener_reserva`).
- **Consulta y escritura:** `servicios` lee la reserva, la ocupación de la sala, los mantenimientos y las reservas del dueño ese día, **sin contar la propia reserva**. Escribe una sola vez y solo si no hubo rechazo.
- **Restricción para pruebas:** `ahora` es un parámetro, así que ningún test depende de la hora real. Nada pide datos por teclado. Las pruebas usan MongoDB real (una base de pruebas separada), porque los índices únicos son parte del diseño.

## 4. Vistas del mismo flujo

### Responsabilidades y dependencias

El diagrama de componentes está en el diseño, sección 5.2 (FE → views → servicios → reglas; servicios → BD).
- **Las flechas significan:** quién llama a quién, en el orden de una petición.
- **Pregunta que responde:** ¿quién recibe, quién decide y quién guarda?
- **Implementado o propuesto:** todo está **propuesto**; el código empieza en la fase 4.

### Ejecución: éxito y rechazo

- **Modelo reutilizado:** el diagrama de actividad de `sesion-07-modelos.md` (sección 4) y la secuencia del diseño (sección 6.1).
- **Recorrido de éxito:**
  1. Buscar la reserva.
  2. `verificar_puede_modificar`.
  3. Leer los datos sin la propia reserva.
  4. `comprobar_reserva`.
  5. Actualizar la misma reserva y responder "Reserva modificada".
- **Recorrido de rechazo:**
  - Se decide en `reglas`, o en el índice único si dos solicitudes llegan al mismo instante.
  - Se responde con la causa. Si el rechazo es de la propuesta y modifica el dueño, se pregunta "¿Deseas mantenerla?".
  - No se escribe nada.
- **Cambio respecto al modelo de la sesión 7 anterior:** ahora se trabaja con bloques fijos (C-01). El camino del administrador va sin pregunta (HU-09), y se agregó el índice único como última barrera (D-02).

### Ubicación

| Componente/datos | Dónde se ejecuta o almacena hoy | Ubicación prevista |
|---|---|---|
| Vistas, servicios y reglas | Pendiente: un proceso de Django con `runserver` (servidor de desarrollo) en la computadora del estudiante | Sin cambio en el MVP: no se despliega |
| Reservas e índices | Pendiente: MongoDB local como *replica set* de un nodo | Sin cambio |
| Pruebas de CI | Pendiente: GitHub Actions, con MongoDB en un contenedor | Fase 7 |

- **Dónde ejecuta las pruebas el CI:** en una máquina de GitHub. No es el servidor de la aplicación.

## 5. Decisión arquitectónica y calidad

- **Objetivo y contexto:** que crear, modificar (estudiante y administrador) y cancelar apliquen **las mismas reglas desde un solo lugar**. Atributos de calidad: mantenibilidad (una regla, un lugar), facilidad de prueba y seguridad (el administrador no se salta reglas).
- **Observación que permitiría evaluar la mejora:**
  - Buscar en el código dónde se define el margen de los bloques: tiene que aparecer **una sola vez**, en `BLOQUES`.
  - Buscar `reglas` en `views.py`: no debe aparecer.
  - Comprobar que HU09-CA2 (el administrador con las reglas del dueño) pasa.

| Alternativa | Beneficio | Trabajo adicional o límite |
|---|---|---|
| A: Las reglas dentro de cada operación de `servicios` (o de la vista), sin un archivo de reglas | Menos archivos; cada operación se lee de corrido | Crear y modificar repiten comprobaciones; es fácil que el administrador tenga su propia versión sin reglas, que fue lo que pasó en el repositorio anterior |
| B: Un solo archivo de reglas (`reglas.py`) que no toca la base, más `servicios` que orquesta y un índice único en la base | Cada regla existe una vez; crear y modificar (estudiante y administrador) usan la misma `comprobar_reserva`; el índice cubre el caso del mismo instante (RF-07) | Un archivo más y una capa más que explicar; `servicios` tiene que leer y pasar los datos a las reglas |

- **Elección y razones:** **B** (D-02, D-03 y D-10 del diseño). Ataca directamente los dos defectos de la revisión de las sesiones 13–14.
- **Estado:** propuesta en el diseño; se implementa en la fase 5.
- **Qué nueva evidencia podría obligarnos a revisarla:** que django-mongodb-backend no cree el índice único parcial (se comprueba en la fase 4), o que una regla nueva del docente necesite datos que hoy no se leen.

## 6. Cambio y trazabilidad de las pruebas

- **Cambio real o frontera comprobada:** pendiente (fases 5 y 6).
- **Cómo se conservan las reglas acordadas:** las de la sesión 6 se implementan una vez en `reglas.py` (D-10).
- **Si se corrigió un requisito o modelo:** C-01 a C-07 en [cambios.md](cambios.md).

| Requisito | Ruta del caso de uso | Función/contrato | Test real y caso | Respuesta y estado esperados |
|---|---|---|---|---|
| RF-03 | Éxito (CU-07, paso 5) | `modificar_reserva` | `test_HU07_CA1_modifica_el_bloque_de_la_misma_reserva`: Valeria mueve su reserva de B2 a B4 en la sala B, con Mateo en B3 | La misma reserva queda en B4, Confirmada, con 3 asistentes; la de Mateo no cambia |
| RF-03, RF-01 | Rechazo (CU-07, E1) y "Sí" | `modificar_reserva` | `test_HU07_CA2_rechazo_y_si_conserva_ambas_reservas`: mover a B3, ocupado por Mateo | Rechazo "sala ocupada en ese bloque" con la pregunta; las dos reservas quedan como estaban |
| RF-06 | Límite (CU-07, E2) | `modificar_reserva` | `test_HU07_CA4_rechaza_modificar_reserva_ya_comenzada`: el jueves 22/10 a las 10:00 exactas, B2 | Rechazo "la reserva ya comenzó", sin pregunta; la reserva sigue en B2 |

- **El límite de la guía no se usa.** La guía propone "R1 comienza justo cuando termina R2". En este proyecto rige el desalojo de 15 min (RES-RF-01, acuerdo con el docente). Por eso el límite que se prueba es el de RF-06, decidido el 15/10/2026.
- **Pruebas nuevas:** las 3 de arriba, escritas por Hugo en la fase 7.
- **Comando y resultado final local:** pendiente (fase 7).
- **Suite completa:** pendiente (fase 7; 26 tests).
- **Alcance no comprobado:** dos solicitudes en el mismo instante (RF-07 y las limitaciones de la sección 1 del diseño), Esc (P-02) y el reinicio del servidor.

## 7. Evidencia de CI y versión

Todo pendiente hasta la fase 7 (domingo 18/10, de 18:00 a 19:00, Hugo):

- **Archivo de workflow:** `.github/workflows/ci-sesion12.yml`, el nombre que indica la guía, adaptado del material de la sesión 12:
  - **Python 3.13** en lugar de 3.12;
  - las pruebas en `tests/` en lugar de `tests/sesion12`;
  - un contenedor de **MongoDB como *replica set*** (diseño, sección 5.5, [A CONFIRMAR EN F7]).
- **Dependencias instaladas:** pendiente.
- **Comando que ejecuta:** pendiente.
- **Ejecución de Actions (URL):** pendiente.
- **Commit probado (SHA):** pendiente.
- **Estado real:** no ejecutado: todavía no hay código.
- **Resultado:** pendiente.
- **Reporte de pruebas:** pendiente.
- **Candidato de código fuente:** pendiente.
- **Qué falta para una entrega en el entorno destino:** el MVP no se despliega; se demuestra en la computadora del estudiante.

## 8. Plan actualizado y participación

- **Tarea/issue y estado real:** #5, en curso. Este borrador se completa en la fase 7.
- **Dependencia o riesgo que cambió:** el CI pasó al domingo (cambio del plan del 15/10). Además, el CI necesita MongoDB como *replica set*.
- **Siguiente acción:**
  - fase 3 (entorno), Raúl, viernes 16/10 a las 17:00;
  - las tres pruebas y el workflow: Hugo, domingo 18/10.
- **Aportes individuales:** Raúl aprobó las decisiones de diseño y revisó los documentos. Hugo escribirá las pruebas y el workflow (fase 7).
- **Asistencia de IA:** se usó Claude (Anthropic) para proponer las decisiones de diseño y redactar este borrador a partir del diseño y de la guía de la sesión 12. Raúl las revisó y aprobó.

## 9. Enlaces de entrega

- Este MD en GitHub: `docs/sesion-12-arquitectura.md` (borrador subido al cerrar la fase 2; URL final: pendiente).
- Pull request: no se usa.
- **Hallazgo del diseño, a comprobar en F4:** según la documentación de MongoDB, una transacción sola no garantizaría "gana la primera", porque dos solicitudes que escriben documentos distintos no chocan. Por eso el diseño agrega un índice único como última barrera. En la fase 4 se comprueba insertando dos reservas Confirmadas iguales: la segunda debe fallar. **Eso comprueba el índice, no una carrera real entre dos solicitudes simultáneas**, que no se prueba (ver "Lo que no se prueba" en `sesion-07-modelos.md`).
