# Registro de cambios aprobados

Aquí se registra todo cambio a algo ya escrito o acordado: un requisito, una historia, el plan o una regla. Cada cambio tiene motivo, fuente y fecha, para que nada cambie en silencio (plan de las sesiones 8–9, sección 3).

- Requisitos vigentes: [sesion-06-requisitos.md](sesion-06-requisitos.md)
- Plan: [sesion-08-09-plan.md](sesion-08-09-plan.md)

**Estados posibles:**
- **Aplicado:** el cambio ya está en el documento afectado.
- **Aplicado (provisional):** está aplicado, pero depende de una pregunta abierta al docente; si responde distinto, se registra un cambio nuevo.

| ID | Fecha | Qué cambia | Antes | Después | Motivo | Fuente | Respuesta del docente (fecha y texto) | Estado | Afecta |
|---|---|---|---|---|---|---|---|---|---|
| C-01 | 15/10/2026 | Forma de expresar RES-RF-01 (15 min de desalojo) | Horarios libres. Criterio de la sesión 6 anterior: "Sala A con reserva de 10:00 a 12:00; se pide de 12:10 a 13:00 → rechazo". | Reservas por bloques fijos B1 a B6, separados por 15 min. La regla queda como "una reserva por sala, fecha y bloque". Nuevo límite: B1 ocupado → B2 en la misma sala se acepta. **El margen de 15 min no cambia.** | Las reservas pasan a hacerse por bloques fijos (RES-RF-09). | Decisión del equipo (Raúl), 15/10/2026. Respaldo parcial: ejemplo 07:45–09:45 → 10:00 de `sesion04.md`. | Sin respuesta todavía: pregunta P-07 (bloques y horario). | Aplicado (provisional) | RES-RF-01, RES-RF-09; criterios de HU-04, HU-05 y HU-07 |
| C-02 | 15/10/2026 | Se agrega la regla RES-RF-08: no reservar dos bloques seguidos el mismo día | No existía. | Un estudiante no puede tener reservas en dos bloques contiguos de la misma fecha, en ninguna sala. Sí puede tener bloques alternados (B1 y B3). No se aplica al docente ni al administrador **[PROVISIONAL]**. | Evitar el uso excesivo de las salas. | Indicación del docente comunicada por Raúl, fecha no registrada. | Indicación sin fecha registrada. Sobre si aplica al docente y al administrador: pregunta P-08, sin respuesta. | Aplicado (la parte del docente y del administrador, provisional) | RES-RF-08; criterios de HU-04 y HU-07 |
| C-03 | 15/10/2026 | Actor de la historia HU-05 | "Docente". El plan de la fase 0 (sección 2) dejaba pendiente que ninguna historia cubría que el administrador reserve. | "Personal: docente o administrador", con las mismas reglas. Sin historia nueva y sin tests extra. | Resolver el pendiente de la fase 0 sin aumentar el alcance. | Decisión del equipo (Raúl), 15/10/2026. | No aplica: es una decisión de alcance del equipo. | Aplicado en los requisitos. La historia se escribe en `sesion-07-modelos.md`, y el pendiente del plan se marca como resuelto al cerrar la fase 1. | HU-05; plan, sección 2 |
