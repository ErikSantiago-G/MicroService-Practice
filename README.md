#  Laboratorio de Microservicios con Docker y FastAPI

Laboratorio práctico de arquitectura distribuida basado en microservicios independientes, comunicación mediante API REST y persistencia de datos con PostgreSQL. El entorno utiliza Docker y Docker Compose para desplegar y administrar todos los componentes de manera aislada.

##  Descripción del proyecto

El objetivo de este proyecto es implementar una arquitectura de microservicios en la que un cliente pueda realizar consultas a través de un servicio principal (M1), el cual se comunica con un segundo microservicio (M2) para obtener información adicional.

Cada microservicio tiene su propia base de datos PostgreSQL, evitando el acoplamiento directo entre los datos de los servicios.

Toda la infraestructura se ejecuta mediante contenedores Docker, conectados a través de una red interna que permite la comunicación entre ellos.

##  Objetivos

- Implementar una arquitectura basada en microservicios.
- Crear API REST independientes utilizando FastAPI.
- Establecer comunicación HTTP entre microservicios.
- Implementar bases de datos independientes con PostgreSQL.
- Configurar redes internas mediante Docker.
- Administrar los servicios utilizando Docker Compose.
- Implementar persistencia de datos mediante Docker Volumes.
- Comprobar el comportamiento del sistema ante la caída de un microservicio.

##  Arquitectura del sistema

El laboratorio está compuesto por cuatro contenedores principales:

| Contenedor | Responsabilidad |
|---|---|
| M1 | API de clientes y comunicación con M2. |
| M2 | API de productos y consulta de su base de datos. |
| DB-M1 | Almacenamiento de información de clientes. |
| DB-M2 | Almacenamiento de información de productos. |

### Diagrama de arquitectura

```text
                    CLIENTE
                       |
                       | HTTP
                       v
              +------------------+
              |  MICROSERVICIO M1 |
              |     FastAPI       |
              |    Puerto 8000    |
              +------------------+
                       |
              +--------+---------+
              |                  |
              v                  |
       +-------------+           |
       | PostgreSQL  |           |
       |    DB-M1    |           |
       +-------------+           |
                                  |
                       HTTP       |
                       v          |
              +------------------+
              |  MICROSERVICIO M2 |
              |     FastAPI       |
              |    Puerto 8000    |
              +------------------+
                       |
                       v
               +-------------+
               | PostgreSQL  |
               |    DB-M2    |
               +-------------+

          RED INTERNA DE DOCKER
```

**Nota:** M2 utiliza internamente el puerto 8000, pero se publica en el puerto 8001 de la máquina anfitriona. M1 se publica en el puerto 8000.

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.11 | Lenguaje de programación. |
| FastAPI | Desarrollo de API REST. |
| HTTPX | Comunicación HTTP entre servicios. |
| PostgreSQL 16 | Sistemas de gestión de bases de datos. |
| Docker | Contenedorización de aplicaciones. |
| Docker Compose | Orquestación de contenedores. |
| PowerShell | Administración del entorno en Windows. |
| Visual Studio Code | Entorno de desarrollo. |

##  Estructura del proyecto

```text
laboratorio-microservicios/
│
├── docker-compose.yml
│
├── microservicio-m1/
│   ├── Dockerfile
│   ├── requirements.txt
│   │
│   ├── app/
│   │   └── main.py
│   │
│   └── database/
│       └── init.sql
│
├── microservicio-m2/
│   ├── Dockerfile
│   ├── requirements.txt
│   │
│   ├── app/
│   │   └── main.py
│   │
│   └── database/
│       └── init.sql
│
└── README.md
```

### Descripción de los archivos

- `docker-compose.yml`: define los cuatro servicios, sus configuraciones, dependencias, puertos, redes y volúmenes.
- `Dockerfile`: establece la imagen y las instrucciones necesarias para construir cada microservicio.
- `requirements.txt`: contiene las dependencias de Python.
- `main.py`: implementa los endpoints y la lógica de cada API.
- `init.sql`: crea las tablas e inserta los registros iniciales.

##  Funcionamiento de los microservicios

### 1. Microservicio M1 - Clientes

M1 es el punto de entrada principal del sistema.

Sus responsabilidades son:

- Recibir solicitudes HTTP del cliente.
- Consultar la información de clientes en PostgreSQL.
- Obtener el identificador del producto asociado al cliente.
- Enviar una solicitud HTTP a M2.
- Recibir la respuesta de M2.
- Construir y devolver una respuesta combinada.

**Endpoint principal:**

```http
GET /clientes/{cliente_id}
```

### 2. Microservicio M2 - Productos

M2 es responsable de administrar y consultar la información de productos.

Sus responsabilidades son:

- Recibir solicitudes HTTP provenientes de M1.
- Consultar la base de datos PostgreSQL de productos.
- Recuperar la información solicitada.
- Devolver los resultados en formato JSON.

**Endpoint principal:**

```http
GET /productos/{producto_id}
```

### 3. Comunicación entre microservicios

La comunicación se realiza mediante HTTP utilizando la biblioteca HTTPX.

M1 utiliza la siguiente dirección:

```python
M2_URL = "http://m2:8000"
```

El nombre `m2` corresponde al nombre del servicio definido en Docker Compose.

Docker proporciona resolución DNS interna, permitiendo que los contenedores se comuniquen sin necesidad de utilizar direcciones IP fijas.

### Flujo de una solicitud

1. El cliente solicita información de un cliente a M1.
2. M1 consulta PostgreSQL DB-M1.
3. M1 obtiene el identificador del producto asociado.
4. M1 realiza una petición HTTP a M2.
5. M2 consulta PostgreSQL DB-M2.
6. M2 devuelve la información del producto.
7. M1 combina ambas respuestas.
8. El cliente recibe la información en formato JSON.

##  Bases de datos

El sistema utiliza dos instancias independientes de PostgreSQL.

### DB-M1: clientes_db

Tabla principal:

| Campo | Tipo | Descripción |
|---|---|---|
| id | SERIAL | Identificador del cliente. |
| nombre | VARCHAR(100) | Nombre del cliente. |
| producto_id | INT | Identificador del producto asociado. |

### DB-M2: productos_db

Tabla principal:

| Campo | Tipo | Descripción |
|---|---|---|
| id | SERIAL | Identificador del producto. |
| nombre | VARCHAR(100) | Nombre del producto. |
| precio | DECIMAL(10,2) | Precio del producto. |

Cada microservicio accede exclusivamente a su propia base de datos. La información del otro servicio se obtiene mediante su API REST.

##  Instalación y ejecución

### Requisitos previos

- Windows 10 u 11 compatible.
- Docker Desktop.
- WSL 2.
- Visual Studio Code.
- Git (opcional).

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

Ingresar al directorio:

```bash
cd laboratorio-microservicios
```

### 2. Construir e iniciar los contenedores

Ejecutar desde la raíz del proyecto:

```bash
docker compose up -d --build
```

Este comando construye las imágenes y levanta los cuatro contenedores.

### 3. Verificar los contenedores

```bash
docker compose ps
```

Se deben encontrar activos:

- microservicio-m1
- microservicio-m2
- db-m1
- db-m2

### 4. Consultar los registros

```bash
docker compose logs -f
```

### 5. Detener el laboratorio

```bash
docker compose down
```

Este comando detiene y elimina los contenedores, pero conserva los volúmenes de datos.

##  Endpoints disponibles

| Microservicio | Método | Endpoint | Descripción |
|---|---|---|---|
| M1 | GET | `/` | Estado de M1. |
| M1 | GET | `/clientes/{cliente_id}` | Consultar cliente y su producto. |
| M2 | GET | `/` | Estado de M2. |
| M2 | GET | `/productos/{producto_id}` | Consultar producto. |

### Documentación Swagger

FastAPI genera automáticamente la documentación interactiva de las API.

**M1:**

http://localhost:8000/docs

**M2:**

http://localhost:8001/docs

##  Pruebas del laboratorio

### Prueba 1: consultar un producto directamente en M2

```http
GET http://localhost:8001/productos/1
```

Respuesta esperada:

```json
{
  "id": 1,
  "nombre": "Teclado",
  "precio": 80000.0
}
```

### Prueba 2: consultar un cliente desde M1

```http
GET http://localhost:8000/clientes/1
```

Respuesta esperada:

```json
{
  "cliente": {
    "id": 1,
    "nombre": "Santiago"
  },
  "producto": {
    "id": 1,
    "nombre": "Teclado",
    "precio": 80000.0
  }
}
```

Esta prueba permite comprobar la comunicación entre M1 y M2 y la consulta independiente de ambas bases de datos.

### Prueba 3: simular la caída de M2

Detener M2:

```bash
docker compose stop m2
```

Consultar nuevamente M1:

```http
GET http://localhost:8000/clientes/1
```

Respuesta esperada:

```json
{
  "detail": "Microservicio M2 no disponible"
}
```

Código HTTP:

```text
503 Service Unavailable
```

Esto demuestra que M1 puede detectar la indisponibilidad de M2 y gestionar el error de comunicación.

### Prueba 4: recuperar M2

```bash
docker compose start m2
```

Volver a consultar M1:

```http
GET http://localhost:8000/clientes/1
```

La respuesta debe volver a funcionar correctamente.

### Prueba 5: verificar persistencia

Detener el entorno:

```bash
docker compose down
```

Iniciar nuevamente:

```bash
docker compose up -d
```

Consultar los datos nuevamente. Los registros deben permanecer almacenados gracias a los volúmenes persistentes de Docker.

##  Redes y volúmenes Docker

### Red interna

Docker Compose crea automáticamente una red compartida para los servicios.

Esto permite que M1 se comunique con M2 utilizando su nombre DNS:

```text
http://m2:8000
```

No es necesario conocer la dirección IP interna del contenedor.

### Volúmenes

Se utilizan dos volúmenes independientes:

```yaml
volumes:
  datos-m1:
  datos-m2:
```

Estos permiten conservar la información de PostgreSQL incluso después de detener y eliminar los contenedores.

**Importante:** el comando `docker compose down -v` elimina también los volúmenes y, por tanto, los datos persistidos.

##  Conceptos de arquitectura aplicados

- **Separación de responsabilidades:** cada microservicio tiene una función específica.
- **Autonomía:** cada servicio administra su propia lógica y base de datos.
- **Comunicación distribuida:** los servicios intercambian información mediante HTTP.
- **Service Discovery:** Docker DNS permite localizar los servicios por nombre.
- **Contenedorización:** cada componente se ejecuta en un entorno aislado.
- **Orquestación:** Docker Compose administra el ciclo de vida de los contenedores.
- **Persistencia:** Docker Volumes conserva los datos.
- **Tolerancia básica a fallos:** M1 gestiona la indisponibilidad de M2 mediante respuestas HTTP 503.


## Este laboratorio puede evolucionar incorporando:

- API Gateway para centralizar las solicitudes.
- Autenticación y autorización mediante JWT.
- Balanceo de carga entre réplicas de microservicios.
- Circuit Breaker para mejorar la tolerancia a fallos.
- RabbitMQ o Apache Kafka para comunicación asíncrona.
- Redis para almacenamiento en caché.
- Prometheus y Grafana para monitoreo.
- Kubernetes para orquestación avanzada.
- Pruebas automatizadas con Pytest.


**Desarrollado como laboratorio práctico de arquitectura de software**

Tecnologías principales: Python, FastAPI, PostgreSQL y Docker.

---

 Si este proyecto te resulta útil para aprender arquitectura de microservicios, puedes darle una estrella al repositorio.
