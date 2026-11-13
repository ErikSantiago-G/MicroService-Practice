CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    producto_id INT
);

INSERT INTO clientes (nombre, producto_id) VALUES
('Santiago', 1),
('Carlos', 2),
('Andres', 3);