
-- Script de inicialización para la base de datos de PostgreSQL

CREATE TABLE IF NOT EXISTS tareas (
    id SERIAL PRIMARY KEY,
    tarea TEXT NOT NULL,
    fecha_limite DATE NOT NULL DEFAULT CURRENT_DATE,
    estado TEXT NOT NULL DEFAULT 'pendiente'
);

-- Agregar fecha_limite si la tabla ya existía.
ALTER TABLE tareas
ADD COLUMN IF NOT EXISTS fecha_limite DATE NOT NULL DEFAULT CURRENT_DATE;

-- Agregar estado si la tabla ya existía.
ALTER TABLE tareas
ADD COLUMN IF NOT EXISTS estado TEXT NOT NULL DEFAULT 'pendiente';

-- Registros de prueba iniciales
INSERT INTO tareas (tarea) VALUES
('Completar script de base de datos'),
('Revisar integracion con Flask y Docker Compose');
