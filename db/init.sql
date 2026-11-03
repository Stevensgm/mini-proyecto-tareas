-- Script de inicialización para la base de datos de PostgreSQL

CREATE TABLE IF NOT EXISTS tareas (
    id SERIAL PRIMARY KEY,
    tarea TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente'
);

-- Si el contenedor de la base de datos ya existía de antes (volumen con
-- datos previos a esta funcionalidad), esto agrega la columna sin perder
-- las tareas que ya estaban guardadas.
ALTER TABLE tareas ADD COLUMN IF NOT EXISTS estado TEXT NOT NULL DEFAULT 'pendiente';

-- Registros de prueba iniciales (docker-entrypoint-initdb.d solo corre
-- este script una vez, en un volumen de base de datos nuevo y vacío)
INSERT INTO tareas (tarea) VALUES
('Completar script de base de datos'),
('Revisar integracion con Flask y Docker Compose');