# Reserva de Salas de Estudio — UPB Santa Cruz (P02)

- Docente y cliente: Ing. Sergio Barrientos
- Integrantes: Raúl Vaca y Hugo Zúñiga
- Tecnología: Django 5.2 con MongoDB (django-mongodb-backend), plantillas HTML y Tailwind CSS

## 1. Qué hace

Aplicación web para reservar las salas de estudio de la universidad por bloques fijos (B1 a B6, que en pantalla se llaman "Horario A" a "Horario F"; de lunes a viernes). Cubre las nueve historias del MVP ([sesion-07-modelos.md](docs/sesion-07-modelos.md), sección 1):

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

No hay cuentas creadas de antemano ni `createsuperuser`: **toda cuenta se crea en `/registro/`** con una persona que figure en el padrón ([padron/padron.json](padron/padron.json), 24 personas, de solo lectura). El registro pide el código, el correo del padrón y una contraseña nueva escrita dos veces ("Contraseña" y "Confirmar contraseña"), que debe cumplir las reglas de Django: al menos 8 caracteres, no solo números, no demasiado común y no parecida al correo ni al nombre.

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

Son **27 tests, uno por criterio de aceptación**. [docs/trazabilidad.md](docs/trazabilidad.md) relaciona cada uno con su requisito, su historia y su caso de uso, y dice su estado. Los tests usan el MongoDB real, pero en una **base aparte, `test_reservacion_salas`**, que crea pytest-django: no tocan la base `reservacion_salas` de la aplicación. Ningún test depende de la hora del sistema: cada operación recibe la hora (`ahora`) que dice su criterio.

## 6. Estilos (Tailwind CSS)

Los estilos usan Tailwind CSS con su **ejecutable independiente, sin Node**. El CSS compilado está en el repositorio (`static/css/estilos.css`), así que **para usar la aplicación no hace falta el ejecutable**.

**Tailwind solo lee `templates/`.** `static/src/entrada.css` empieza con `@import "tailwindcss" source(none);` y `@source "../../templates";`. Sin esas dos líneas, Tailwind busca nombres de clase en todos los archivos del repositorio y genera clases que ninguna pantalla usa: pasaba con `.contents` y `.visible`, porque esas palabras aparecían en otros archivos. Por eso, si una plantilla nueva no está dentro de `templates/`, sus clases no se generan.

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
tests/             los 27 tests y conftest.py
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

Cada integrante escribe su propio párrafo, solo con lo que es cierto. Guía de qué contar:

- **Qué herramienta** usó (nombre y, si lo sabe, el modelo).
- **Para qué parte del trabajo**: por ejemplo, documentos (requisitos, plan, diseño), código (qué archivos o qué fases), tests, estilos o revisión.
- **Qué hizo la IA y qué hizo el integrante**: si la IA explicó, propuso estructura, propuso código o revisó, y si el integrante lo escribió, lo copió, lo adaptó, lo probó o lo subió.
- **Que revisó y puede explicar** el código y los documentos que llevan su nombre.

**Raúl Vaca:** Usé Claude (Anthropic) durante todo el proyecto: para la documentación (requisitos, plan y diseño), para proponer el código y los tests, para los estilos y para revisar. Claude propuso; yo analicé cada propuesta, comprobé que la entendía y decidí si convenía ponerla en el código o no. Los commits y los cambios subidos al repositorio los hice yo, después de esa revisión con criterio humano. Comprobé lo que subí con pruebas automáticas (pytest) mientras escribía el código, con pruebas de humo y después con pruebas en vivo, con el frontend y el backend funcionando juntos, para verificar que cada caso de uso se cumple. Puedo explicar línea por línea: las apps cuentas y reservas (modelos, servicios, reglas y vistas), el padrón (padron/padron.json y cómo se lee), config/settings.py y, en distintos grados, el funcionamiento de MongoDB y de Django con MongoDB. Todavía estoy repasando: cómo funciona cada test en detalle y dónde se ve cada caso de uso en el código. A veces me quedan dudas sobre el funcionamiento de algunas partes del código que sí puedo explicar; me falta afinarlo. En el rediseño de las pantallas de inicio de sesión y registro (issue #36, PR #40) usé Claude Code siguiendo mis instrucciones: yo elegí el diseño, le di los textos exactos y le indiqué qué no podía tocar. También usé Claude en un chat aparte para revisar el resultado contra el repositorio. El encabezado nuevo y la línea de la fecha de hoy los escribí yo con la guía de Claude en ese chat, paso a paso. Revisé el diff, probé las pantallas en el navegador del celular y de la computadora, corrí los 27 tests e hice los commits y el pull request.

**Hugo Zúñiga:** Usé Claude (Anthropic) en el chat de claude.ai para entender los documentos y la estructura del proyecto (incluidas la sesión 6 y el repositorio anterior), para redactar documentación de apoyo, para proponer los tests de HU-06 a HU-09 y para proponer el workflow de CI. Claude explicó y propuso borradores: el glosario de siglas (`docs/glosario.md`), el anexo de fuentes del repositorio anterior (sesión 6, sección 9, con sus datos comprobados contra el commit 4353d1d), los 11 tests de `tests/test_hu06_cancelar.py` a `tests/test_hu09_gestion_ajena.py` y `.github/workflows/ci-sesion12.yml`. Yo revisé cada propuesta antes de usarla, apliqué los ajustes de la revisión de Raúl (solo comentarios Dado/Cuando/Entonces, solo fixtures de `conftest.py` y un commit por archivo) y la probé: instalé el entorno, levanté MongoDB como replica set, corrí pytest hasta obtener 26 passed y ejecuté el CI en GitHub Actions. Los commits, los push y los pull requests (#27, #30 y #31) los hice yo. Probé el CI en ubuntu-26.04: falló porque el contenedor de MongoDB no arranca con el kernel 7.0 de esa imagen, así que lo dejé fijado en ubuntu-24.04. Puedo explicar los tests de HU-06, HU-07 y HU-08, el workflow de CI y por qué necesita MongoDB como replica set (la transacción de HU-08), y el glosario y el anexo que llevan mi nombre.

El registro de participación por fase está en [sesion-08-09-plan.md](docs/sesion-08-09-plan.md), sección 13.
