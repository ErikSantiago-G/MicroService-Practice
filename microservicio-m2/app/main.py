import os
import psycopg
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Microservicio M2 - Productos")

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def inicio():
    return {"servicio": "M2", "estado": "activo"}

@app.get("/productos/{producto_id}")
def consultar_producto(producto_id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, nombre, precio FROM productos WHERE id = %s",
                (producto_id,)
            )
            producto = cur.fetchone()

    if not producto:
        raise HTTPException(404, "Producto no encontrado")

    return {
        "id": producto[0],
        "nombre": producto[1],
        "precio": float(producto[2])
    }
