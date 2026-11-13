import os
import psycopg
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Microservicio M1 - Clientes")

DATABASE_URL = os.getenv("DATABASE_URL")
M2_URL = os.getenv("M2_URL")

@app.get("/")
def inicio():
    return {"servicio": "M1", "estado": "activo"}

@app.get("/clientes/{cliente_id}")
def consultar_cliente(cliente_id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, nombre, producto_id FROM clientes WHERE id = %s",
                (cliente_id,)
            )
            cliente = cur.fetchone()

    if not cliente:
        raise HTTPException(404, "Cliente no encontrado")

    try:
        respuesta = httpx.get(
            f"{M2_URL}/productos/{cliente[2]}",
            timeout=5
        )
        respuesta.raise_for_status()
        producto = respuesta.json()
    except httpx.HTTPError:
        raise HTTPException(503, "Microservicio M2 no disponible")

    return {
        "cliente": {
            "id": cliente[0],
            "nombre": cliente[1]
        },
        "producto": producto
    }
