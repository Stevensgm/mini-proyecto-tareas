-- Script de inicialización para la base de datos de PostgreSQL

CREATE TABLE IF NOT EXISTS tareas (
    id SERIAL PRIMARY KEY,
    tarea TEXT NOT NULL
);

-- Registros de prueba iniciales
INSERT INTO tareas (tarea) VALUES
('Completar script de base de datos'),
('Revisar integracion con Flask y Docker Compose');