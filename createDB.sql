-- 1. Crear la base de datos
CREATE DATABASE transporte_db;
GO -- <--- ESENCIAL: Detiene la ejecución aquí para crear la BD

-- 2. Cambiar al contexto de la nueva base de datos
USE transporte_db;
GO

-- 3. Crear la tabla
CREATE TABLE transportes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    posicion INT NOT NULL,
    valor INT NOT NULL
);
GO -- <--- ESENCIAL: Detiene la ejecución para que la tabla exista antes del INSERT

-- 4. Insertar los datos (Corregí la posición de 'Micros' a 5)
INSERT INTO transportes (nombre, posicion, valor) VALUES 
('Caminar', 1, 1), 
('Bicicletas', 2, 4), 
('Motos', 3, 10), 
('Trufis', 4, 16), 
('Micros', 5, 25), -- <--- Cambiado de 4 a 5 para mantener el orden
('Buses', 6, 30), 
('Telefericos', 7, 34), 
('Tren', 8, 40), 
('Taxis', 9, 45), 
('Aviones', 10, 60);
GO

-- Verificación
SELECT * FROM transportes ORDER BY posicion ASC;