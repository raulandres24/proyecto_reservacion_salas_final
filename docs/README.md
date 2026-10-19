# Reserva de Salas de Estudio — UPB Santa Cruz (P02)

- Docente y cliente: Ing. Sergio Barrientos
- Integrantes: Raúl Vaca y Hugo Zúñiga
- Tecnología: Django 5.2 con MongoDB (django-mongodb-backend), plantillas HTML y Tailwind CSS

## 1. Qué hace

Aplicación web para reservar las salas de estudio de la universidad por bloques fijos (B1 a B6, de lunes a viernes). Cubre las nueve historias del MVP ([sesion-07-modelos.md](docs/sesion-07-modelos.md), sección 1):

| Historia | Qué permite |
|---|---|
| HU-01 | Registrarse con el código y el correo del padrón, eligiendo una contraseña |
| HU-02 | Iniciar y cerrar sesión con correo y contraseña |
| HU-03 | Ver qué salas están libres en una fecha y un bloque |
| HU-04 | Reservar una sala (estudiante de pregrado) |
| HU-05 | Reservar una sala siendo personal (docente o administrador) |
| HU-06 | Ver mis reservas y cancelar una antes de que empiece |
| HU-07 | Modificar una reserva y decidir si la conservo cuando el cambio no es posible |
| HU-08 | Poner una sala en mantenimiento (administrador) |
| HU-09 | Modificar o cancelar reservas de otras personas con las mismas reglas (administrador) |

Las reglas de cada historia están en [sesion-06-requisitos.md](docs/sesion-06-requisitos.md) y el diseño en [sesion-13-14-diseno.md](docs/sesion-13-14-diseno.md).

## 2. Requisitos

- **Python 3.13** (la versión usada en el desarrollo).
- **MongoDB local como *replica set* de un nodo**, llamado `rs0`, en `localhost:27017`. La aplicación usa la base `reservacion_salas` (`config/settings.py`). El *replica set* es necesario porque el mantenimiento se guarda en una transacción (diseño, D-04).
- Las dependencias de [requirements.txt](requirements.txt), entre ellas Django 5.2.18, django-mongodb-backend 5.2.4, pymongo 4.19.0, pytest 9.1.1 y pytest-django 4.14.0.

**Configurar MongoDB como *replica set***: en el archivo de configuración de MongoDB (`mongod.cfg`; en una instalación normal de Windows está en la carpeta `bin` del servidor) se agrega:

```yaml
replication:
  replSetName: rs0
```

Después se reinicia el servicio de MongoDB y, una sola vez, se ejecuta en `mongosh`:

```
rs.initiate({_id: "rs0", members: [{_id: 0, host: "localhost:27017"}]})
```

Se indica `localhost:27017` para que el nodo quede con esa dirección, que es la que usa `config/settings.py`. Para comprobarlo, `db.hello().setName` en `mongosh` debe responder `rs0`.


## 3. Cómo ponerlo a andar (Windows, PowerShell)

Desde la carpeta del proyecto, con MongoDB corriendo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_salas
python manage.py runserver
```

| Paso | Qué hace |
|---|---|
| `python -m venv .venv` y `Activate.ps1` | Crea y activa el entorno virtual. Si PowerShell bloquea el script, antes se ejecuta `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`. |
| `pip install -r requirements.txt` | Instala las versiones exactas del proyecto. |
| `python manage.py migrate` | Crea las colecciones y los índices. Las migraciones de `cuentas` y `reservas` están en sus carpetas `migrations/`; las de `auth` y `contenttypes` están en `mongo_migrations/`, porque el conector de MongoDB las necesita con identificadores ObjectId (`MIGRATION_MODULES` en `config/settings.py`). |
| `python manage.py cargar_salas` | Carga las 8 salas (A, B, C, D, E, F, H y J). Se puede repetir sin duplicar: la primera vez dice `Sala A: creada` y las siguientes, `actualizada`. |
| `python manage.py runserver` | Arranca el servidor de desarrollo de Django en `http://127.0.0.1:8000/`. |

La aplicación se abre en **`http://127.0.0.1:8000/login/`** (o `/registro/` para crear una cuenta). La dirección raíz `/` no tiene página propia.

## 4. Cuentas para probar

No hay cuentas creadas de antemano ni `createsuperuser`: **toda cuenta se crea en `/registro/`** con una persona que figure en el padrón ([padron/padron.json](padron/padron.json), 24 personas, de solo lectura). El registro pide el código, el correo del padrón y una contraseña nueva, que debe cumplir las reglas de Django: al menos 8 caracteres, no solo números, no demasiado común y no parecida al correo ni al nombre.

| Para probar | Código | Correo | Qué se puede ver |
|---|---|---|---|
| Administrador | 10002 | `adminraul@upb.example` | Reservas del día (puede cancelar reservas ajenas) y mantenimiento |
| Estudiante | 31245 | `valeria.rojas@upb.example` | Consultar, reservar, modificar y cancelar |
| Estudiante sin matrícula al día | 31247 | `lucia.fernandez@upb.example` | Puede registrarse, pero no reservar |
| Persona inactiva | 31248 | `diego.vargas@upb.example` | El registro se rechaza |

La contraseña la elige cada uno al registrarse; este README no publica ninguna. Las personas de los ejemplos (Valeria, Mateo, Lucía, Diego y Ana) son ficticias. El padrón incluye también a los estudiantes del curso, con su aprobación y la del docente (cambio C-09 en [cambios.md](docs/cambios.md)).

## 5. Cómo correr las pruebas

Con el entorno virtual activo y MongoDB corriendo como *replica set*:

```powershell
python -m pytest
```

Son **26 tests, uno por criterio de aceptación**. [docs/trazabilidad.md](docs/trazabilidad.md) relaciona cada uno con su requisito, su historia y su caso de uso, y dice su estado. Los tests usan el MongoDB real, pero en una **base aparte, `test_reservacion_salas`**, que crea pytest-django: no tocan la base `reservacion_salas` de la aplicación. Ningún test depende de la hora del sistema: cada operación recibe la hora (`ahora`) que dice su criterio.

## 6. Estilos (Tailwind CSS)

Los estilos usan Tailwind CSS con su **ejecutable independiente, sin Node**. El CSS compilado está en el repositorio (`static/css/estilos.css`), así que **para usar la aplicación no hace falta el ejecutable**.

Solo para cambiar los estilos:

1. Descargar el ejecutable de Windows de las [Releases de tailwindlabs/tailwindcss](https://github.com/tailwindlabs/tailwindcss/releases) (usamos la v4.3.3) y guardarlo como `tools/tailwindcss.exe`. La carpeta `tools/` está en `.gitignore`, por eso no viene en el repositorio.
2. Compilar:

```powershell
.\tools\tailwindcss.exe -i .\static\src\entrada.css -o .\static\css\estilos.css
```

Con `--watch` al final, vuelve a compilar cada vez que cambian los archivos.

## 7. Estructura del proyecto

```
config/            configuración de Django (settings, URLs principales)
cuentas/           cuenta de usuario propia, registro contra el padrón e inicio de sesión
reservas/          salas, reservas y mantenimiento: reglas, servicios y vistas
  reglas.py        todas las reglas del sistema; no lee ni escribe en la base
  servicios.py     cada operación de los casos de uso: lee, pregunta a reglas y guarda
  management/      comando cargar_salas
padron/            padron.json, el padrón de la universidad (solo lectura)
templates/         plantillas HTML
static/            entrada de Tailwind (src/) y CSS compilado (css/)
tests/             los 26 tests y conftest.py
mongo_migrations/  migraciones de auth y contenttypes para MongoDB
docs/              requisitos, historias, plan, diseño, cambios, trazabilidad y glosario
```

**Regla de arquitectura:**

- Las **vistas** solo llaman a **servicios**: nunca importan `reglas` ni deciden nada.
- Los **servicios** leen y guardan con los **modelos**, y le preguntan a **reglas** si la operación se permite.
- **`reglas.py` es el único lugar de las reglas**: recibe datos ya leídos, no toca la base y, si algo no se cumple, lanza `Rechazo` con la causa.
- **`ahora` es un parámetro** de toda operación que depende del tiempo; la vista le pasa la hora real y los tests, la de su criterio.

El detalle está en el diseño, secciones 4 y 5.

## 8. Lo que no se hizo o queda provisional

- **Limitaciones del MVP y lo que queda fuera:** [sesion-06-requisitos.md, "Limitaciones del MVP"](docs/sesion-06-requisitos.md#limitaciones-del-mvp-declaradas).
- **Valores provisionales:** las reglas marcadas **[PROVISIONAL]** dependen de preguntas abiertas al docente (P-01 a P-17), con el valor que se usa mientras no haya respuesta: [sesion-06-requisitos.md, sección 6](docs/sesion-06-requisitos.md#6-preguntas-abiertas-para-el-docente).
- **Lo que no se prueba:** [sesion-07-modelos.md, "Lo que no se prueba"](docs/sesion-07-modelos.md#lo-que-no-se-prueba-declarado).
- **Cambios a lo acordado:** [cambios.md](docs/cambios.md).
- **Solo para desarrollo:** la `SECRET_KEY` de `config/settings.py` es una clave de desarrollo (`django-insecure-…`) y `DEBUG` está activado. El MVP corre con el servidor de desarrollo de Django y no está preparado para desplegarse en un servidor real.

## 9. Declaración de uso de IA

**[COMPLETAR POR CADA INTEGRANTE]**

Cada integrante escribe su propio párrafo, solo con lo que es cierto. Guía de qué contar:

- **Qué herramienta** usó (nombre y, si lo sabe, el modelo).
- **Para qué parte del trabajo**: por ejemplo, documentos (requisitos, plan, diseño), código (qué archivos o qué fases), tests, estilos o revisión.
- **Qué hizo la IA y qué hizo el integrante**: si la IA explicó, propuso estructura, propuso código o revisó, y si el integrante lo escribió, lo copió, lo adaptó, lo probó o lo subió.
- **Que revisó y puede explicar** el código y los documentos que llevan su nombre.

**Raúl Vaca:** [COMPLETAR POR CADA INTEGRANTE]

**Hugo Zúñiga:** [COMPLETAR POR CADA INTEGRANTE]

El registro de participación por fase está en [sesion-08-09-plan.md](docs/sesion-08-09-plan.md), sección 13.
