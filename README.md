# mini-proyecto-tareas


# Mini Proyecto de Tareas

Aplicación web desarrollada con Flask para gestionar una lista de tareas.
Equipo 3

## Integrantes 
Jose Manuel Martinez Gallego
James David Ortiz Muñoz
Carlos Steven Giraldo Medina
Helen Orejuela Mancilla

##Descripcion
la aplicacion permite gestionar tareas: crear, modificar y eliminar registros almacenados en un una base de datos postgreSQL. La interfaz es simple y funcional, no requiere de autenticacion ni funcionalidades adicionales a lo requerido dentro del parcial.

## Tecnologías utilizadas

- Python
- Flask
- HTML
- postgreSQL 16 
- Docker
- Docker compose
- Git y Github

## Arquitectura
La aplicacion web (web) y la base de datos (db) corren en contenedores seprados, comunicados mediante una red de Docker.

## Estructura del proyecto

mini-proyecto-tareas/
├── app.py
├── db/
  └── init.sql.
├── requirements.txt      
├── Dockerfile            
├── docker-compose.yml   
├── templates/
│   └── index.html       
└── README.md
## configuracion

La conexion entre la aplicacion y postgresSQL se configura mediante variables de entorno definidas en el archivo docker-compose.yml:

DB_HOST: Host de postgreSQL
DB_NAME: Nombre de la base de datos
DB_USER: usuario de postgreSQL
DB_PASSWORD: Contraseña del usuario de postgreSQL

## como ejecutar el proyecto

1. clona el repositorio: 
git clone https://github.com/Stevensgm/mini-proyecto-tareas.git
cd mini-proyecto-tareas
2. Levantar los servicios con Docker compose:
docker compose up --build

3. abrir wl navegador en:
   http://localhost:8080

4. usar la interfaz para crear, modificar y eliminar tareas.
5. para detener los servicios se usa el siguiente comando:
docker compose down
no se requiere instalar python o alguna otra depencia, docker compose se encarga de ejecutar todo.

Aquí tienes el README completo, corregido y listo para copiar y pegar (mantuve toda la estructura y el contenido de tu compañera, solo corregí la sección de Git, completé los Pull Requests, y arreglé un par de detalles menores):

markdown
# Mini Proyecto de Tareas

Aplicación web desarrollada con Flask para gestionar una lista de tareas. Equipo 3

## Integrantes

- Jose Manuel Martinez Gallego
- James David Ortiz Muñoz
- Carlos Steven Giraldo Medina
- Helen Orejuela Mancilla

## Descripción

La aplicación permite gestionar tareas: crear, modificar y eliminar registros almacenados en una base de datos PostgreSQL. La interfaz es simple y funcional, no requiere de autenticación ni funcionalidades adicionales a lo requerido dentro del parcial.

## Tecnologías utilizadas

- Python
- Flask
- HTML
- PostgreSQL 16
- Docker
- Docker Compose
- Git y GitHub

## Arquitectura

La aplicación web (`web`) y la base de datos (`db`) corren en contenedores separados, comunicados mediante una red de Docker.

## Estructura del proyecto

mini-proyecto-tareas/
├── app.py
├── db/
│ └── init.sql
├── requirements.txt
├── dockerfile
├── docker-compose.yml
├── templates/
│ ├── index.html
│ └── editar.html
└── README.md


## Configuración

La conexión entre la aplicación y PostgreSQL se configura mediante variables de entorno definidas en el archivo `docker-compose.yml`:

- `DB_HOST`: Host de PostgreSQL
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`: Usuario de PostgreSQL
- `DB_PASSWORD`: Contraseña del usuario de PostgreSQL

## Cómo ejecutar el proyecto

1. Clona el repositorio:

git clone https://github.com/Stevensgm/mini-proyecto-tareas.git
cd mini-proyecto-tareas

2. Levanta los servicios con Docker Compose:

docker compose up --build

3. Abre el navegador en:

http://localhost:8080

4. Usa la interfaz para crear, modificar y eliminar tareas.
5. Para detener los servicios:

docker compose down


No se requiere instalar Python ni ninguna otra dependencia; Docker Compose se encarga de ejecutar todo.

## Git y trabajo colaborativo

Cada integrante trabajó en su propia rama (`feature/...`), con commits descriptivos de su avance, y abrió un Pull Request hacia `main`, revisado y aprobado por otro compañero del equipo antes de mergear.

Ramas utilizadas:
- `feature-aplicacion`
- `feature/docker`
- `feature/base-datos`
- `feature/compose`
- `feature/mejora-interfaz-tareas`
- `fix/conexion-db`

Pull Requests:
- [PR #11 — Docker Compose (servicios web y db)](https://github.com/Stevensgm/mini-proyecto-tareas/pull/11)
- [PR #13 — Base de datos (init.sql)](https://github.com/Stevensgm/mini-proyecto-tareas/pull/13)
- [PR #14 — Interfaz de tareas](https://github.com/Stevensgm/mini-proyecto-tareas/pull/14)
- [PR #16 — Dockerfile](https://github.com/Stevensgm/mini-proyecto-tareas/pull/16)
- [PR #17 — Conexión a PostgreSQL](https://github.com/Stevensgm/mini-proyecto-tareas/pull/17)
- [PR #18 — README del proyecto](https://github.com/Stevensgm/mini-proyecto-tareas/pull/18)
## persistencia 

se comprobo la persistencia de la siguiente manera: 

1. se crearon tareas desde la interfaz web.
2. se ejecuto docker compose up nuevamente.
3. se verifico que las tareas creadas anteriormente seguian disponibles en http://localhost:8080
