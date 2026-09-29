# mini-proyecto-tareas


# Mini Proyecto de Tareas

Aplicación web desarrollada con Flask para gestionar una lista de tareas.
Equipo 3

## Integrantes 
- Jose Manuel Martinez Gallego
- James David Ortiz Muñoz
- Carlos Steven Giraldo Medina
- Helen Orejuela Mancilla

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

## Git y trabajo colaborativo
El equipo trabajo con la rama develop como rama intermedia entre las ramas individuales y la rama main: 
main
 └── develop
      ├── feature/docker         
      ├── feature/mejora-interfaz-tareas    
      ├── feature-base-datos     
      └── fix/conexion-db      
    
cada integrante trabajo en su propia rama, hizo commits descriptivos de su avance y abrio un pull request hacia develop para revision antes de subir a main.
pull request final hacia main
- https://github.com/Stevensgm/mini-proyecto-tareas/pull/17#issue-5623353473

- https://github.com/Stevensgm/mini-proyecto-tareas/pull/15#issue-5622330323

- https://github.com/Stevensgm/mini-proyecto-tareas/pull/14#issue-5622242368

- https://github.com/Stevensgm/mini-proyecto-tareas/pull/13#issue-5620955444

## persistencia 

se comprobo la persistencia de la siguiente manera: 

1. se crearon tareas desde la interfaz web.
2. se ejecuto docker compose up nuevamente.
3. se verifico que las tareas creadas anteriormente seguian disponibles en http://localhost:8080