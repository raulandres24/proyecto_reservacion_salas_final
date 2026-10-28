# Trazabilidad de las pruebas

- Proyecto: Reserva de Salas de Estudio — UPB Santa Cruz (P02)
- Integrantes que participan: Raúl Vaca y Hugo Zúñiga (desde la fase 7)
- Fecha: 18/10/2026 · Fase 7 · Issue #22 · Milestone F7 Pruebas
- Requisitos: [Sesión 6](sesion-06-requisitos.md) · Historias, criterios y casos de uso: [Sesión 7](sesion-07-modelos.md) · Diseño: [Sesiones 13–14](sesion-13-14-diseno.md) · Plan: [Sesiones 8–9](sesion-08-09-plan.md) · Cambios: [cambios.md](cambios.md)

Este documento relaciona cada test con su requisito, su historia, su criterio de aceptación y su caso de uso, y dice en qué estado está. La lista de 26 tests se acordó en la fase 1 (sesión 7, sección 6); el 27/10/2026 se agregó HU01-CA3 (cambio C-15), así que son 27. **Lo que no se prueba** está declarado allí y no se copia aquí, para no tener dos listas que se contradigan.

## 1. Cómo se ejecutan

```
python -m pytest -v
```

Requisitos: el entorno virtual activo, `pip install -r requirements.txt` y MongoDB local corriendo como *replica set* (la misma base que usa la aplicación). pytest-django crea su propia base `test_reservacion_salas`; **no toca** la base `reservacion_salas` de la aplicación.

## 2. Los 27 tests

Estado al 27/10/2026: **27 de 27 implementados y en verde**, en local y en GitHub Actions. Última corrida completa, en la copia local de Raúl, con el código que se subió en `ff7c3d6`: 27 passed, en unos 48 segundos. En GitHub Actions, el CI de `ff7c3d6` pasó en verde: [run #15](https://github.com/raulandres24/proyecto_reservacion_salas_final/actions/runs/40613061505), en 44 s. La corrida anterior, con los 26 tests de la fase 1, fue a las 22:55 del 18/10/2026 sobre `29b817a` (`26 passed in 30.68s`). De los 16 tests de Raúl, 15 siguen el issue #18 y HU01-CA3, el #34; los 11 de Hugo siguen el #19; los de Hugo se fusionaron en `main` con el PR #30 (merge `ec1a354`). La base de pytest (`pytest.ini`, `pytest` y `pytest-django` en `requirements.txt`) está en `8e83913`.

| Requisito | HU | Criterio | Paso o excepción del CU | Test | Archivo | Responsable | Estado |
|---|---|---|---|---|---|---|---|
| RF-13 | HU-01 | CA1 aceptación | CU-01 paso 7 | `test_HU01_CA1_registra_cuenta_con_codigo_y_correo_del_padron` | `test_hu01_registro.py` | Raúl | Pasa (`60eda5d`) |
| RF-13 | HU-01 | CA2 rechazo | CU-01 E3 | `test_HU01_CA2_rechaza_registro_de_persona_inactiva` | `test_hu01_registro.py` | Raúl | Pasa (`60eda5d`) |
| RF-13 | HU-01 | CA3 rechazo (C-15) | CU-01 E6 | `test_HU01_CA3_rechaza_si_las_contrasenas_no_coinciden` | `test_hu01_registro.py` | Raúl | Pasa (`ff7c3d6`, local y Actions) |
| RF-14 | HU-02 | CA1 aceptación | CU-02 paso 3 | `test_HU02_CA1_inicia_sesion_con_correo_y_contrasena` | `test_hu02_sesion.py` | Raúl | Pasa (`154d7c9`) |
| RF-14 | HU-02 | CA2 rechazo | CU-02 E1 | `test_HU02_CA2_contrasena_incorrecta_da_mensaje_unico` | `test_hu02_sesion.py` | Raúl | Pasa (`154d7c9`) |
| RF-01, RF-11, RC-02 | HU-03 | CA1 aceptación | CU-03 paso 4 | `test_HU03_CA1_muestra_salas_libres_sin_a_ni_e_y_no_modifica_datos` | `test_hu03_consulta.py` | Raúl | Pasa (`640e63a`) |
| RF-10 | HU-03 | CA2 rechazo | CU-03 E2 | `test_HU03_CA2_antes_de_las_18_no_muestra_el_dia_siguiente` | `test_hu03_consulta.py` | Raúl | Pasa (`640e63a`) |
| RF-10 | HU-04 | CA1 aceptación + límite | CU-04 pasos 2c–4 | `test_HU04_CA1_reserva_a_las_18_en_punto_para_el_dia_siguiente` | `test_hu04_reserva.py` | Raúl | Pasa (`d27383a`) |
| RF-01, RF-07 | HU-04 | CA2 rechazo | CU-04 E1 (2g) | `test_HU04_CA2_rechaza_si_choca_con_otra_reserva` | `test_hu04_reserva.py` | Raúl | Pasa (`d27383a`) |
| RF-01 | HU-04 | CA3 límite | CU-04 paso 2g | `test_HU04_CA3_acepta_bloque_siguiente_con_15_min_de_desalojo` | `test_hu04_reserva.py` | Raúl | Pasa (`d27383a`) |
| RF-02 | HU-04 | CA4 rechazo | CU-04 E1 (2h) | `test_HU04_CA4_rechaza_segunda_reserva_en_el_mismo_bloque` | `test_hu04_reserva.py` | Raúl | Pasa (`d27383a`) |
| RF-08 | HU-04 | CA5 rechazo | CU-04 E1 (2i) | `test_HU04_CA5_rechaza_bloques_seguidos_en_otra_sala` | `test_hu04_reserva.py` | Raúl | Pasa (`d27383a`) |
| RF-05 | HU-04 | CA6 rechazo | CU-04 E1 (2a) | `test_HU04_CA6_rechaza_si_matricula_no_esta_al_dia` | `test_hu04_reserva.py` | Raúl | Pasa (`d27383a`) |
| RF-04 | HU-04 | CA7 rechazo | CU-04 E1 (2f) | `test_HU04_CA7_rechaza_si_supera_la_capacidad` | `test_hu04_reserva.py` | Raúl | Pasa (`d27383a`) |
| RF-11, RF-10 | HU-05 | CA1 aceptación | CU-05 | `test_HU05_CA1_docente_reserva_sala_a_sin_limite_de_anticipacion` | `test_hu05_personal.py` | Raúl | Pasa (`8082d80`) |
| RF-09 | HU-05 | CA2 rechazo | CU-05 E1 (2b) | `test_HU05_CA2_rechaza_reserva_en_sabado` | `test_hu05_personal.py` | Raúl | Pasa (`8082d80`) |
| RF-06 | HU-06 | CA1 aceptación | CU-06 paso 5 | `test_HU06_CA1_cancela_antes_de_que_empiece_y_conserva_el_registro` | `test_hu06_cancelar.py` | Hugo | Pasa (`19513ea`) |
| RF-06 | HU-06 | CA2 rechazo + límite | CU-06 E2 | `test_HU06_CA2_rechaza_cancelar_reserva_ya_comenzada` | `test_hu06_cancelar.py` | Hugo | Pasa (`19513ea`) |
| RF-06 (C-04) | HU-06 | CA3 rechazo | CU-06 E1 | `test_HU06_CA3_rechaza_cancelar_reserva_ajena` | `test_hu06_cancelar.py` | Hugo | Pasa (`19513ea`) |
| RF-03 | HU-07 | CA1 aceptación (sesión 12) | CU-07 paso 5 | `test_HU07_CA1_modifica_el_bloque_de_la_misma_reserva` | `test_hu07_modificar.py` | Hugo | Pasa (`76fb03a`) |
| RF-03, RF-01 | HU-07 | CA2 rechazo + "Sí" (sesión 12) | CU-07 E1 | `test_HU07_CA2_rechazo_y_si_conserva_ambas_reservas` | `test_hu07_modificar.py` | Hugo | Pasa (`76fb03a`) |
| RF-03 | HU-07 | CA3 rechazo + "No" | CU-07 E1 | `test_HU07_CA3_rechazo_y_no_cancela_la_original` | `test_hu07_modificar.py` | Hugo | Pasa (`76fb03a`) |
| RF-06 | HU-07 | CA4 límite (sesión 12) | CU-07 E2 | `test_HU07_CA4_rechaza_modificar_reserva_ya_comenzada` | `test_hu07_modificar.py` | Hugo | Pasa (`76fb03a`) |
| RF-12 | HU-08 | CA1 aceptación | CU-08 pasos 3–4 | `test_HU08_CA1_mantenimiento_cancela_reservas_y_bloquea_el_periodo` | `test_hu08_mantenimiento.py` | Hugo | Pasa (`c1c4dbe`) |
| RF-12 | HU-08 | CA2 rechazo | CU-08 E1 | `test_HU08_CA2_rechaza_mantenimiento_en_bloque_ya_empezado` | `test_hu08_mantenimiento.py` | Hugo | Pasa (`c1c4dbe`) |
| RF-03 | HU-09 | CA1 rechazo sin pregunta | CU-09 E1 | `test_HU09_CA1_admin_rechazado_sin_pregunta_conserva_ambas` | `test_hu09_gestion_ajena.py` | Hugo | Pasa (`a398910`) |
| RF-08 (reglas del dueño) | HU-09 | CA2 rechazo | CU-09 paso 3, E1 | `test_HU09_CA2_admin_aplica_reglas_del_dueno` | `test_hu09_gestion_ajena.py` | Hugo | Pasa (`a398910`) |

RC-01 (causa concreta) y RC-03 (un rechazo no deja la operación a medias) no tienen tests propios: los comprueba cada test de rechazo, que verifica el mensaje exacto y lo que quedó guardado.

## 3. Cómo están escritos los tests

- **Qué se prueba:** las reglas y los servicios (`reservas/servicios.py`, `cuentas/servicios.py`), que son los que deciden. Solo los tests de HU-02 pasan por la vista (`iniciar_sesion`), porque el mensaje "Correo o contraseña incorrectos" se genera ahí.
- **El reloj:** ningún test lee la hora del sistema. Cada operación recibe `ahora`, y el test pasa la fecha y la hora que dice el criterio (por ejemplo, miércoles 21/10/2026 a las 18:05). Los fixtures `hora` y `fecha` arman esos valores en la zona America/La_Paz.
- **Datos de partida:** `tests/conftest.py` crea las cuentas de los ejemplos (Valeria, Mateo, Lucía, Ana, Sergio), carga las 8 salas con el mismo comando `cargar_salas` y ofrece `dar_reserva`, que deja armada la situación del "Dado" sin pasar por las reglas.
- **Aislamiento:** cada test que usa datos lleva `django_db(transaction=True)`. Con esa marca, pytest-django **borra los datos** al terminar cada test, así que cada test empieza con la base vacía. Se eligió porque `django.db.transaction.atomic()` no hace nada con este conector (el mantenimiento usa `django_mongodb_backend.transaction.atomic()`), así que no se confía en que Django deshaga los cambios de un test.
- **Comprobación:** antes de escribir los tests se corrió una prueba de humo con dos tests temporales (no se conservaron). El primero creaba un usuario y el segundo comprobaba que la base estaba vacía; los dos pasaron.

## 4. Precisiones sobre lo que verifica cada test implementado

Estas precisiones dicen qué comprueba exactamente el test, para que nadie lea en el criterio más de lo que se prueba.

| Test | Precisión |
|---|---|
| HU01-CA1 | "Puede iniciar sesión" se comprueba con `authenticate` (correo y contraseña), no con el navegador. "El padrón no cambia" compara el contenido de `padron.json` antes y después. |
| HU02-CA1 | "Su cuenta no cambia" compara correo, código, nombre, rol, nivel, matrícula y contraseña. **No** compara `last_login`: Django lo actualiza solo en cada inicio de sesión. |
| HU02-CA2 | Se comprueban las dos peticiones (contraseña incorrecta y correo inexistente): el mismo mensaje y ningún usuario autenticado. |
| HU03-CA1, HU03-CA2 | "La base queda igual" compara una foto de las reservas y de los mantenimientos antes y después. |
| HU04-CA2, CA4, CA5 | "Solo existe la reserva…" compara la lista completa de reservas con la reserva que se había dejado armada. |
| HU04-CA3 | El desalojo de 15 minutos se prueba por su resultado (B1 y B2 de la sala B quedan reservadas), no calculando la diferencia de horas. |
| HU05-CA1 | La falta de límite de anticipación para el docente sigue siendo **[PROVISIONAL]** (P-13). |

## 5. Pruebas de Hugo

Hugo escribió los 11 tests de HU-06 a HU-09 (issue #19), uno por criterio, en cuatro commits: HU-06 en `19513ea`, HU-07 en `76fb03a`, HU-08 en `c1c4dbe` y HU-09 en `a398910`. Se fusionaron en `main` con el PR #30 (merge `ec1a354`).

El plan (sección 4) pedía esos tests antes de las 18:00 del domingo 18/10. No se cumplió: los cuatro commits de Hugo son de las 19:29. Raúl corrió la suite de 26 tests sobre su rama a las 19:41 (todos en verde) y los fusionó en main a las 19:45.
