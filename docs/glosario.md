# Glosario de siglas — Reserva de Salas (UPB Santa Cruz, P02)

Hecho para leer los `docs/` sin marearse. Busca la sigla, lee su significado y sigue.

## Ficha del documento

| Campo | Detalle |
|---|---|
| **Creado por** | Hugo Zúñiga, con asistencia de Claude (Anthropic). Hugo pidió el documento y definió qué debía incluir; Claude redactó el borrador y comprobó cada sigla contra `docs/`, contra el código y contra el repositorio anterior (commit `4353d1d`) |
| **Fecha** | 18/10/2026 |
| **Revisado por** | Raúl Vaca, en el PR #27 |
| **Issue** | #28 (H0: lectura de `docs/`, glosario y anexo de fuentes) |
| **Cambio que lo registra** | C-14 en [cambios.md](cambios.md) |
| **Por qué existe** | Los documentos de `docs/` usan decenas de siglas (RF, RC, RT, HU, CU, CA, E1, P-xx, C-xx, D-xx, F0–F9, B1–B6, FE, MW, BD…) y cada una se explica solo en el documento donde nace. Hugo entra al proyecto en la fase 7 y debe poder explicar las historias y el diseño (tarea H0 del plan), así que necesita un solo lugar donde consultarlas. Además, varias letras significan cosas distintas según el documento (sección 6) y eso confunde al leer |
| **Qué no es** | No crea reglas, no cambia ningún requisito y no reemplaza a los documentos. Si una sigla de este glosario contradice a un documento, **manda el documento** y este archivo se corrige |
| **Cómo se mantiene** **[PROPUESTA]** | Quien agregue una sigla nueva en `docs/` la suma aquí en el mismo commit. Si cambia el significado de una sigla existente, lo registra además en `cambios.md`. Raúl decide si adopta esta regla al revisar la pull request |

**Convenciones de este archivo**
- **(deducido)**: el repo no define la sigla; es la lectura más probable por el contexto.
- **(externo)**: significado general de la industria, no escrito en el repo.
- Las demás vienen definidas o usadas de forma explícita en `docs/` o en el código.

---

## 0. Cómo se arma un ID

| Forma | Se lee así | Ejemplo |
|---|---|---|
| `RES-RF-04` | proyecto · tipo · número | Requisito funcional 4 |
| `HU04-CA2` | historia 4 · criterio 2 | Segundo criterio de la historia 4 |
| `test_HU04_CA2_…` | un test = un criterio | Cada criterio de aceptación se convierte en exactamente un test |
| `CU-07 E1` | caso de uso 7 · excepción 1 | Primer camino de error del CU-07 |
| `F5` | fase 5 del plan | Reglas |

En el texto suelen abreviar `RES-RF-04` como `RF-04`. Es lo mismo.

---

## 1. IDs de documentación (los que más aparecen)

| Sigla | Significa | Ejemplo | Dónde se define |
|---|---|---|---|
| **RES** | Reservas: prefijo del proyecto (deducido) | `RES-RF-01` | `sesion-06` |
| **RF** | Requisito Funcional: una regla del sistema | `RF-01` sala ocupada | `sesion-06`, sección 3 |
| **RC** | Requisito de Calidad (deducido) | `RC-01` causa concreta | `sesion-06`, sección 4 |
| **RT** | Restricción técnica (deducido) | `RT-03` MongoDB | `sesion-06`, sección 5 |
| **HU** | Historia de Usuario | `HU-07` modificar | `sesion-07`, sección 1 |
| **CA** | Criterio de Aceptación (formato Dado / Cuando / Entonces) | `HU07-CA2` | `sesion-07`, sección 2 |
| **CU** | Caso de Uso | `CU-07` | `sesion-07`, sección 3 |
| **E1, E2…** | Excepción: camino de error dentro de un caso de uso | `CU-07 E1` | `sesion-07`, sección 3 |
| **RES-MOD** | Modelo (diagrama) | `RES-MOD-01` | `sesion-07`, sección 4 |
| **P** | Pregunta abierta al docente | `P-02` (¿Esc cancela?) | `sesion-06`, sección 6 |
| **C** | Cambio aprobado | `C-04` | `cambios.md` |
| **D** | Decisión de diseño | `D-02` índices únicos | `sesion-13-14`, sección 1 |
| **B1–B6** | Bloque horario 1 a 6. Es el nombre que usan el código y los documentos | `B2` = 10:00–12:00 | `sesion-06`, sección 0 |
| **Horario A–F** | Nombre que ve el usuario en las pantallas para los bloques 1 a 6 (C-16): 1 = A, 2 = B, 3 = C, 4 = D, 5 = E, 6 = F. El código y la base siguen guardando el número | "Horario B" = bloque 2 = `B2` = 10:00–12:00 | `reservas/templatetags/horarios.py` (filtro `letra_horario`) |

**Mismo número, misma funcionalidad:** `HU-n` y `CU-n` hablan de lo mismo (HU-07 y CU-07 = modificar).

### 1.1 Fuentes citadas en los requisitos

| Sigla | Significa |
|---|---|
| **ENC** | Encargo del proyecto P02 (sesión 2). Trae las necesidades `RES-01` a `RES-08` |
| **ENT** | Entrevista con el docente (`ENT-01` a `ENT-08`). El texto completo está en `sesion-06`, sección 9.3 |
| **S4, S6** | Documentos de las sesiones 4 y 6 del repositorio anterior |
| **D07** | Decisiones del 07/10/2026 (README del repositorio anterior). **No es D-07** |
| **DR** | Indicaciones del docente comunicadas por Raúl, sin fecha registrada |
| **E15** | Decisiones del equipo (Raúl) del 15/10/2026. **No es E1 ni E5** |
| **P02** | Proyecto 02: Reserva de Salas de Estudio (deducido) |
| **Repo anterior** | `campus-challenge-equipo-01`. Lo que usamos de él está copiado en `sesion-06-requisitos.md`, **sección 9 (anexo, C-12)**, con enlaces al commit `4353d1d` |
| **PB-01 a PB-05** | Ítems del backlog de la sesión 4 del repo anterior: PB-01 crear reserva, PB-02 consultar espacios, PB-03 validar código, PB-04 modificar reserva, PB-05 cancelar reserva. PB = Product Backlog (deducido) |
| **TDD** | Test-Driven Development: desarrollo guiado por pruebas. Es el método que usó la sesión 4 (S4) |
| **P1–P12** (sin guion) | Preguntas abiertas del README del repo anterior. Sus equivalentes con P-01 a P-17 están en `sesion-06`, sección 9.5. Ejemplo: P10 (anterior) = **P-13** (actual) |

---

## 2. Plan y gestión (`sesion-08-09-plan.md`)

| Sigla | Significa |
|---|---|
| **F0–F9** | Fases del plan en cascada: F0 Planificación, F1 Requisitos, F2 Diseño, F3 Entorno, F4 Datos, F5 Reglas, F6 Vistas, F7 Pruebas y CI, F8 Interfaz, F9 Entrega |
| **H0** | Tarea de Hugo: leer `docs/` (deducido: H de Hugo) |
| **E** (sola) | Ensayo de la demo |
| **R1–R4** | Recortes aprobados si el tiempo no alcanza (sección 9 del plan) |
| **h-p** | Horas-persona (esfuerzo) |
| **IT / FT** | Inicio temprano / Fin temprano (deducido; método de ruta crítica) |
| **ITa / FTa** | Inicio tardío / Fin tardío (deducido) |
| **Holgura** | Cuánto se puede retrasar una tarea sin mover la entrega (`FTa − FT`) |
| **MVP** | Minimum Viable Product: producto mínimo viable (externo) |
| **CI** | Continuous Integration: integración continua. Aquí, GitHub Actions corre los tests en cada push (externo) |
| **SHA** | Código hash que identifica un commit, por ejemplo `dab355c` (externo) |
| **MD** | Markdown: formato de los archivos `.md` (externo) |
| **IA** | Inteligencia Artificial (la asistencia de Claude citada en cada sesión) |
| **UPB** | Universidad Privada Boliviana (no lo define el repo; externo) |

---

## 3. Arquitectura y técnicas

| Sigla | Significa | Dónde está en el proyecto |
|---|---|---|
| **FE** | Frontend: lo que ve la persona en el navegador | `templates/` |
| **MW** | Middleware: la capa del medio, o sea el servidor | `urls.py`, `views.py`, `servicios.py`, `reglas.py` |
| **BD** | Base de Datos (MongoDB) | `models.py` |
| **Padrón** | Lista de la universidad, solo lectura (no es sigla, pero va en el recorrido) | `padron/padron.json` |
| **MVT** | Model – View – Template: el patrón de Django | Model = BD · View = entrada del MW · Template = FE |
| **CSRF** | Cross-Site Request Forgery: ataque que Django frena con un token | `{% csrf_token %}` en cada formulario |
| **HTTP** | Protocolo del navegador al servidor (externo) | — |
| **GET / POST** | Métodos HTTP: GET consulta, POST envía datos que cambian algo | `request.method`, `@require_POST` |
| **URL** | Dirección web de cada pantalla | `urls.py` |
| **HTML** | Lenguaje de las pantallas | `templates/*.html` |
| **CSS** | Estilos; en F8 llega Tailwind | `static/` (todavía no existe) |
| **JSON** | Formato de datos en texto | `padron.json` |
| **WSGI** | Web Server Gateway Interface: puerta de entrada del servidor (externo) | `config/wsgi.py` (la usa `runserver`) |
| **ASGI** | Asynchronous Server Gateway Interface: versión asíncrona (externo) | `config/asgi.py` |
| **UTC** | Hora universal; Mongo guarda las fechas así | Mongo |
| **UTF-8** | Codificación de texto con tildes y ñ | `open(..., encoding="utf-8")` |
| **I18N** | Internationalization: idioma y formato regional (externo) | `USE_I18N` en `settings.py` |
| **PK / pk** | Primary Key: clave primaria de un registro | `reserva.pk` |
| **ID / _id** | Identificador; en Mongo es un `ObjectId` | `reserva_id` |
| **API** | Application Programming Interface; aparece solo al criticar el repo anterior (`api_editar_reserva`) | repo anterior |

> **MW no es la lista `MIDDLEWARE` de `settings.py`.** Esa lista son piezas internas de Django (sesiones, CSRF, autenticación). Cuando el docente dice MW, se refiere a toda la capa del servidor.

**Recorridos:** Registro = FE → MW → Padrón → BD. Resto de operaciones = FE → MW → BD.

---

## 4. Las marcas entre corchetes

| Marca | Significa |
|---|---|
| **[ACUERDO]** | Lo indicó o aprobó el docente |
| **[PROPUESTA]** | Lo propuso el equipo; el docente no lo confirmó |
| **[PROVISIONAL]** | Valor temporal mientras el docente no responda. Si responde distinto, se anota en `cambios.md` |
| **[DECISIÓN F2]** | Decisión de diseño de Raúl en la fase 2 |
| **[A CONFIRMAR EN F3 / F4 / F7]** | Detalle técnico que se comprueba en esa fase |

Estados en `cambios.md`: **Aplicado** (ya está en el documento) y **Aplicado (provisional)** (depende de una pregunta abierta).

---

## 5. Índice rápido de los IDs

### 5.1 Requisitos funcionales (RF)

| ID | Qué exige |
|---|---|
| RF-01 | Una sola reserva confirmada por sala, fecha y bloque (15 min de desalojo) |
| RF-02 | Una reserva por persona en el mismo bloque |
| RF-03 | Si la modificación se rechaza: "¿Deseas mantenerla?" |
| RF-04 | Los asistentes no superan la capacidad de la sala |
| RF-05 | Solo estudiantes con matrícula al día reservan |
| RF-06 | Modificar o cancelar solo antes de que empiece; solo el dueño |
| RF-07 | Solicitudes casi simultáneas: gana la primera |
| RF-08 | No reservar dos bloques seguidos el mismo día (estudiantes) |
| RF-09 | Bloques fijos, de lunes a viernes |
| RF-10 | Anticipación: el día siguiente desde las 18:00 del día de clase anterior (estudiantes) |
| RF-11 | Pregrado no usa las salas A y E |
| RF-12 | Mantenimiento de una sala por período |
| RF-13 | Registro validado con el padrón |
| RF-14 | Inicio y cierre de sesión con mensaje de error único |

### 5.2 Calidad y restricciones

| ID | Qué exige |
|---|---|
| RC-01 | Cada rechazo muestra su causa concreta |
| RC-02 | Una consulta no modifica datos |
| RC-03 | Un rechazo no deja la operación a medias |
| RT-01 | Las reglas de negocio se escriben en Python |
| RT-02 | Todas las horas en la zona `America/La_Paz` |
| RT-03 | Persistencia en MongoDB vía `django-mongodb-backend` |

### 5.3 Historias y casos de uso (mismo número = misma funcionalidad)

| HU / CU | Funcionalidad | Actor |
|---|---|---|
| 01 | Registrarse con el padrón | Persona sin cuenta |
| 02 | Iniciar y cerrar sesión | Usuario registrado |
| 03 | Consultar salas libres | Cualquier usuario con cuenta |
| 04 | Reservar una sala | Estudiante de pregrado |
| 05 | Reserva del personal (incluye A y E) | Docente o administrador |
| 06 | Ver mis reservas y cancelar | Estudiante de pregrado |
| 07 | Modificar mi reserva | Estudiante de pregrado |
| 08 | Poner una sala en mantenimiento | Administrador |
| 09 | Gestionar reservas ajenas | Administrador |

### 5.4 Las letras a–i del CU-04 (paso 2) y su función en el código

Son las 9 comprobaciones de `comprobar_reserva`, en este orden:

| Letra | Regla | Función en `reglas.py` |
|---|---|---|
| a | RF-05 matrícula | `verificar_matricula` |
| b | RF-09 día y bloque | `verificar_dia_y_bloque` |
| c | RF-10 anticipación | `verificar_anticipacion` |
| d | RF-11 nivel de sala | `verificar_nivel_de_sala` |
| e | RF-12 mantenimiento | `verificar_sin_mantenimiento` |
| f | RF-04 capacidad | `verificar_capacidad` |
| g | RF-01 / RF-07 sala libre | `verificar_sala_libre` |
| h | RF-02 una por bloque | `verificar_un_bloque_por_persona` |
| i | RF-08 bloques seguidos | `verificar_bloques_no_seguidos` |

---

## 6. Trampas: la misma letra significa cosas distintas

| Letra | Significados (según dónde aparezca) |
|---|---|
| **B** | Sala B **o** Bloque B1–B6 **o** "Horario B" en pantalla, que es el bloque 2 (C-16). `B2` es un bloque; "sala B" es una sala; "Horario B" es `B2` |
| **C** | Sala C **o** Cambio `C-01` |
| **D** | Sala D **o** Decisión `D-01` **o** fuente `D07` (no es `D-07`, que es el comando `cargar_salas`) |
| **E** | Sala E **o** Excepción `E1` **o** Ensayo (`E`) **o** fuente `E15` |
| **F** | Sala F **o** Fase `F5` |
| **H** | Sala H **o** `H0` (tarea de Hugo) **o** prefijo `HU` |
| **P** | Pregunta `P-02` **o** proyecto `P02` **o** Padrón **o** `P1`–`P12` (sin guion): preguntas del repo anterior. Equivalencias en `sesion-06`, sección 9.5 |
| **R** | Recorte `R1` **o** prefijos `RF`, `RC`, `RT` **o** "R1 / R2" como dos reservas en la guía de la sesión 12 |
| **S** | Fuente `S4` / `S6` **o** `servicios` |
| **Sesión N** | **No** es la fase **FN**. Sesión 6 = requisitos; F6 = vistas |
| **RES-HU-01** | En el repo anterior era "modificar una reserva". Hoy es `HU-07` |

**Salas:** A, B, C, D, E, F, H, J (no existen G ni I). A y E son de posgrado.

---

## 7. Términos que no son siglas pero marean

| Término | Qué es |
|---|---|
| **Padrón** | Archivo JSON con 24 entradas: 15 compañeros reales, el docente, 3 administradores y 5 personas ficticias de los ejemplos (23 antes de C-13). Solo se lee, y solo al registrarse. El repo anterior y el docente lo llaman también **DB estática** |
| **Cuentas de administrador** | Códigos `10001` (Sergio), `10002` (Raúl) y `10003` (Hugo, C-13): 5 dígitos, correo inventado `@upb.example` y entrada aparte de la del estudiante o docente de la misma persona |
| **Dueño** | Quien creó la reserva (`dueno`, sin ñ en el código) |
| **Bloque** | Franja fija de 2 h; hay 6 al día, separadas por 15 min. En pantalla se llama "Horario A" a "Horario F" (C-16) |
| **Desalojo de 15 min** | El margen entre un bloque y el siguiente; por eso no hace falta una regla aparte |
| **Rechazo** | Excepción de `reglas.py` con `causa` y `preguntar_si_mantener` |
| **Índice único parcial** | Restricción de MongoDB: no permite dos reservas *confirmadas* iguales. Es la última barrera (D-02) |
| **Replica set** | Modo de MongoDB necesario para las transacciones |
| **Transacción atómica** | Todo o nada: el mantenimiento y sus cancelaciones ocurren juntos (D-04) |
| **ObjectId** | Tipo del `_id` de cada documento en MongoDB |
| **Dado / Cuando / Entonces** | Formato de cada criterio de aceptación: situación, acción, resultado |
| **Cascada** | Método del plan: se cierra una fase antes de empezar la siguiente |
| **Trazabilidad** | Tabla que une requisito → HU → CA → CU → test (`sesion-07`, sección 6) |
| **Ruta crítica** | Cadena de tareas sin holgura; aquí, todas las fases |
