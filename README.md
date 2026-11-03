# Mini Proyecto de Tareas

Aplicación web desarrollada con Flask para gestionar una lista de tareas. Equipo 3

## Integrantes

- Jose Manuel Martinez Gallego
- James David Ortiz Muñoz
- Carlos Steven Giraldo Medina
- Helen Orejuela Mancilla

## Descripción

La aplicación permite gestionar tareas: crearlas, modificarlas, eliminarlas y filtrarlas por estado. Los registros se almacenan en una base de datos PostgreSQL. La interfaz es simple y funcional, no requiere de autenticación ni funcionalidades adicionales a lo requerido dentro del parcial.

Este proyecto evolucionó a partir de la primera entrega (CRUD básico con Docker, Docker Compose, PostgreSQL y pruebas automatizadas) agregando, para el Segundo Parcial, dos nuevas funcionalidades y un flujo de Integración y Entrega Continua completo (CI + CD con publicación de imagen en GHCR).

## Tecnologías utilizadas

- Python 3.11
- Flask
- psycopg2 (driver de PostgreSQL)
- HTML / CSS
- PostgreSQL 16
- Docker y Docker Compose
- pytest (pruebas automatizadas)
- GitHub Actions (CI/CD)
- GitHub Container Registry (GHCR)
- Git y GitHub

## Arquitectura

La aplicación web (`web`) y la base de datos (`db`) corren en contenedores separados, comunicados mediante una red de Docker. El contenedor `web` se construye a partir del `dockerfile` del proyecto (o se descarga ya construido desde GHCR, ver más abajo) y expone el puerto `8080`. El contenedor `db` usa la imagen oficial `postgres:16` y se inicializa con el script `db/init.sql`.

## Funcionalidades

### CRUD base

- Crear tareas (texto, fecha límite y estado).
- Listar todas las tareas.
- Modificar una tarea existente.
- Eliminar una tarea.

### Funcionalidad A — Filtro por estado

Cada tarea tiene un estado: `pendiente`, `en_progreso` o `completada` (por defecto `pendiente`). Desde la página principal se puede filtrar la lista por estado usando los enlaces "Filtrar por estado" o visitando directamente `/?estado=en_progreso`. También existe un endpoint JSON equivalente en `/api/tareas?estado=completada` que devuelve el total y el listado filtrado.

El filtrado se implementó como una función pura y aislada (`filtrar_tareas_por_estado` en `app.py`), sin dependencias de Flask ni de la base de datos, lo que permite probarla con pruebas unitarias simples y rápidas (ver `tests/test_filtro_estado.py`).

### Funcionalidad B — Validación de fecha límite

Cada tarea ahora exige una `fecha_limite`. Al crear o editar una tarea, el backend valida (función `validar_fecha_limite` en `app.py`) que la fecha tenga un formato válido (`AAAA-MM-DD`) y que sea igual o posterior a la fecha actual. Si la validación falla, la aplicación responde con el código HTTP `400` y el mensaje `"Fecha límite inválida. Debe ser hoy o una fecha futura."`.

## Estructura del proyecto

```
mini-proyecto-tareas/
├── app.py
├── db/
│   └── init.sql
├── requirements.txt
├── requirements-dev.txt
├── dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── ci.yml                (CI: "Pruebas")
│       └── docker-publish.yml    (CD: "Publicar imagen Docker en GHCR")
├── templates/
│   ├── index.html
│   └── editar.html
├── tests/
│   ├── conftest.py
│   ├── test_crud.py
│   ├── test_integracion.py
│   └── test_filtro_estado.py
└── README.md
```

## Configuración

La conexión entre la aplicación y PostgreSQL se configura mediante variables de entorno:

- `DB_HOST`: host de PostgreSQL (por defecto `db`, el nombre del servicio en Docker Compose)
- `DB_NAME`: nombre de la base de datos (`tareas_db`)
- `DB_USER`: usuario de PostgreSQL (`tareas_user`)
- `DB_PASSWORD`: contraseña del usuario (`tareas_pass`)

Estas variables ya vienen definidas en `docker-compose.yml` para desarrollo local.

## Cómo ejecutar el proyecto

Hay dos formas de levantar la aplicación: construyendo la imagen localmente a partir del código fuente, o usando la imagen ya publicada en GHCR por el pipeline de CD.

### Opción 1 — Desde el código fuente (build local)

1. Clona el repositorio:

```
git clone https://github.com/Stevensgm/mini-proyecto-tareas.git
cd mini-proyecto-tareas
```

2. El archivo `docker-compose.yml` del repositorio está configurado para usar la imagen publicada en GHCR (ver Opción 2). Para construir la imagen en tu propia máquina a partir del `dockerfile`, usa `docker compose` indicando el build directamente:

```
docker compose up --build web
```

Si lo anterior no reconstruye porque el servicio `web` referencia `image:` en vez de `build:`, puedes construir y levantar el contenedor manualmente:

```
docker build -t mini-proyecto-tareas:local .
docker compose up -d db
docker run --rm -p 8080:8080 --network mini-proyecto-tareas_default \
  -e DB_HOST=db -e DB_NAME=tareas_db -e DB_USER=tareas_user -e DB_PASSWORD=tareas_pass \
  mini-proyecto-tareas:local
```

(El nombre de la red puede variar; revísalo con `docker network ls` después de levantar `db`, normalmente es `<carpeta>_default`.)

3. Abre el navegador en `http://localhost:8080`.
4. Para detener los servicios: `docker compose down` (agrega `-v` solo si quieres borrar también los datos de la base de datos).

### Opción 2 — Usando la imagen publicada en GHCR (recomendado)

Cada vez que se integran cambios a `main`/`master` y las pruebas pasan, el pipeline de CD publica automáticamente una imagen lista para usar en GitHub Container Registry. No es necesario tener el código fuente ni construir nada:

```
docker pull ghcr.io/stevensgm/mini-proyecto-tareas:latest
```

Luego, con la base de datos levantada (puedes usar el `docker-compose.yml` del repo solo para el servicio `db`, o tu propio PostgreSQL), ejecuta:

```
docker run --rm -p 8080:8080 \
  -e DB_HOST=db \
  -e DB_NAME=tareas_db \
  -e DB_USER=tareas_user \
  -e DB_PASSWORD=tareas_pass \
  --network mini-proyecto-tareas_default \
  ghcr.io/stevensgm/mini-proyecto-tareas:latest
```

O, de forma más simple, usando directamente `docker compose` (el `docker-compose.yml` del repositorio ya referencia `ghcr.io/stevensgm/mini-proyecto-tareas:latest` para el servicio `web`, por lo que descarga la imagen en vez de construirla):

```
docker compose up
```

Abre el navegador en `http://localhost:8080`.

No se requiere instalar Python ni ninguna otra dependencia en ninguna de las dos opciones; Docker (o Docker Compose) se encarga de todo.

## Pruebas automatizadas

Para instalar las dependencias de desarrollo y ejecutar las pruebas localmente:

```
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Todas las pruebas sustituyen la conexión a PostgreSQL por una base de datos falsa en memoria (`tests/conftest.py`), por lo que no es necesario levantar Docker para ejecutarlas.

La suite actual (22 pruebas) se organiza en tres categorías:

- **Pruebas unitarias** (`tests/test_filtro_estado.py`, 8 pruebas): prueban la función pura `filtrar_tareas_por_estado` de forma aislada, sin depender de Flask ni de la base de datos (filtrado por cada estado válido, estado vacío/ausente/inválido, sin coincidencias, lista vacía).
- **Pruebas de integración** (`tests/test_integracion.py`, 1 prueba): simulan un flujo completo a través de la aplicación Flask (crear → listar → editar → eliminar una tarea) usando el cliente de pruebas de Flask y la base de datos falsa.
- **Pruebas de regresión del CRUD** (`tests/test_crud.py`, 13 pruebas): cubren las rutas existentes (crear, listar, editar, eliminar) y la validación de fecha límite (fecha de hoy válida, fecha futura válida, fecha pasada inválida, fecha vacía inválida, formato incorrecto inválido), garantizando que las nuevas funcionalidades no rompan el comportamiento previo del CRUD.

## Integración y Entrega Continua (CI/CD)

### CI — `.github/workflows/ci.yml` ("Pruebas")

Se ejecuta automáticamente:
- En cada `pull_request` (abierto o actualizado), contra cualquier rama destino.
- En cada `push` a `main` o `master`.

El workflow instala las dependencias de `requirements-dev.txt` y corre `pytest -q`. Un Pull Request no puede fusionarse de forma segura a `main` si esta comprobación falla.

### CD — `.github/workflows/docker-publish.yml` ("Publicar imagen Docker en GHCR")

Se ejecuta automáticamente cuando el workflow "Pruebas" termina en `main` o `master`, y solo continúa si ese workflow terminó exitosamente (`workflow_run` + `if: conclusion == 'success'`). Es decir: solo se publica una imagen nueva si las pruebas pasaron.

Pasos del workflow:
1. Descarga el código del commit exacto que pasó las pruebas.
2. Inicia sesión en GHCR usando el `GITHUB_TOKEN` del propio repositorio (no requiere credenciales adicionales).
3. Construye la imagen Docker a partir del `dockerfile`.
4. Publica la imagen en GHCR con dos etiquetas: `latest` y el hash del commit (`<sha>`).

### Imagen publicada

- Registro: GitHub Container Registry (GHCR)
- Nombre completo de la imagen: `ghcr.io/stevensgm/mini-proyecto-tareas`
- Etiquetas disponibles: `latest` (siempre la versión más reciente que pasó CI en main) y una etiqueta por cada commit (`ghcr.io/stevensgm/mini-proyecto-tareas:<sha>`), útil para desplegar una versión específica.

```
docker pull ghcr.io/stevensgm/mini-proyecto-tareas:latest
```

## Persistencia

Se comprobó la persistencia de la siguiente manera:

1. Se crearon tareas desde la interfaz web.
2. Se ejecutó `docker compose down` (sin `-v`) y luego `docker compose up` nuevamente.
3. Se verificó que las tareas creadas anteriormente seguían disponibles en `http://localhost:8080`, incluyendo su estado y fecha límite.

## Git y trabajo colaborativo

Cada integrante trabajó en su propia rama (`feature/...`), con commits descriptivos de su avance, y abrió un Pull Request hacia `main`, revisado antes de mergear.

Ramas y Pull Requests de la primera entrega:
- `feature-aplicacion`
- `feature/docker` — [PR #11](https://github.com/Stevensgm/mini-proyecto-tareas/pull/11), [PR #22](https://github.com/Stevensgm/mini-proyecto-tareas/pull/22), [PR #23](https://github.com/Stevensgm/mini-proyecto-tareas/pull/23), [PR #24](https://github.com/Stevensgm/mini-proyecto-tareas/pull/24)
- `feature/base-datos` — [PR #13](https://github.com/Stevensgm/mini-proyecto-tareas/pull/13)
- `feature/compose` — [PR #14](https://github.com/Stevensgm/mini-proyecto-tareas/pull/14)
- `feature/mejora-interfaz-tareas` — [PR #16](https://github.com/Stevensgm/mini-proyecto-tareas/pull/16)
- `fix/conexion-db` — [PR #17](https://github.com/Stevensgm/mini-proyecto-tareas/pull/17)
- README y CI — [PR #18](https://github.com/Stevensgm/mini-proyecto-tareas/pull/18), [PR #20](https://github.com/Stevensgm/mini-proyecto-tareas/pull/20)

Ramas y Pull Requests del Segundo Parcial:
- `feature/filtro-estado` — [PR #25](https://github.com/Stevensgm/mini-proyecto-tareas/pull/25): endpoint y lógica de filtro por estado, pruebas unitarias nuevas (`tests/test_filtro_estado.py`) y actualización de `tests/conftest.py` para reconocer las nuevas consultas SQL sin romper las pruebas existentes.
- `feature/validacion-fecha-limite` — [PR #26](https://github.com/Stevensgm/mini-proyecto-tareas/pull/26): validación de fecha límite al crear/editar tareas, nuevas pruebas de regresión en `tests/test_crud.py`.

Ambas ramas se integraron a `main` y la suite completa (22 pruebas) pasa sin regresiones sobre el estado combinado.
