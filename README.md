# Proyecto Transporte

Sistema de registro de transporte con interfaz gráfica y SQL Server.

## Base de datos
La creacion de base de datos mas la inyeccion para que todos los usuarios tengan la misma base de datos

CREATE DATABASE transporte_db;

CREATE TABLE transportes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    posicion INT NOT NULL,
    valor INT NOT NULL
);

INSERT INTO Transportes (nombre, posicion, valor ) VALUES
('Caminar', 1, 1),
('Bicicletas', 2, 4),
('Motos', 3, 10),
('Trufis', 4, 16),
('Micros', 4, 25),
('Buses', 6, 30),
('Telefericos', 7, 34),
('Tren', 8, 40),
('Taxis', 9, 45),
('Aviones', 10, 60);

## Archivos
- main.py → arranca el programa
- interfaz.py → ventana y botones
- database.py → conexión a base de datos

## Cómo ejecutar
python main.py
