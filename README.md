# 🏍️ Moto Parts API

API RESTful desarrollada con **Django REST Framework** para la gestión de un sistema de repuestos de motocicletas.  
Incluye autenticación JWT, gestión de usuarios, catálogo de productos, categorías, marcas y clientes.

---

## 📦 Tecnologías principales

- **Python 3.12**
- **Django 4.2**
- **Django REST Framework**
- **drf-spectacular** → documentación OpenAPI/Swagger
- **PostgreSQL**
- **Docker & Docker Compose**
- **pytest** → pruebas automáticas

---

## ⚙️ Instalación local (sin Docker)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/juanCamilo2002/moto-parts-backend.git
   cd moto-parts-backend
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate   # En linux / Mac
   venv\Scripts \activate     # En Windows
   ```
3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno** 

   Crea un archivo .env `.env` en la raiz del proyecto, hay uno de ejemplo `.env.example`
   ```bash
   SECRET_KEY=django-insecure-tu-clave-secreta
   DEBUG=True
   DJANGO_ALLOWED_HOSTS=*

   POSTGRES_DB=moto_parts
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

5. **Aplicar migraciones y ejecutar servidor**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## 🐳 Ejecución con Docker
1. **Asegúrate de tener Docker y Docker Compose instalados.**
2. **Levantar los servicios**
   ```bash
   docker-compose up --build
   ```
3. **variables de entornos extras (Dokcer) pgadmin**
   ```bash
   # credentials pgadmin (Docker)
   PGADMIN_EMAIL=admin@gmail.com  
   PGADMIN_PASSWORD=admin1234
   ```
3. **El backend estará disponible en:**

   👉 http://localhost:8000

## 📜 Documentación de la API

Una vez en ejecución, puedes acceder a la documentación generada automáticamente:
* Swagger UI → http://localhost:8000/api/docs/
* Redoc UI → http://localhost:8000/api/redoc/

## 🧩 Estructura de módulos
| Módulo      | Descripción                                                     |
| ----------- | --------------------------------------------------------------- |
| `users`     | Gestión de usuarios, autenticación y roles (`admin`, `seller`). |
| `auth`      | Registro, login, logout y perfil de usuario autenticado.        |
| `catalog`   | CRUD de productos, marcas y categorías.                         |
| `customers` | Gestión de clientes (personas naturales o empresas).            |
| `orders` | Gestión de pedidos y carrito de compras (`Cart`, `CartItem`, `Order`).            |

## 🛒 Módulo de Pedidos y Carrito
**Funcionalidades:**

* Creación y gestión de carritos por cliente.
* Agregar, eliminar o listar productos en el carrito.
* Creación de órdenes con múltiples productos (`Order` y `OrderItem`).`


| Endpoint             | Método  | Descripción                                               |
| -------------------- | ------- | --------------------------------------------------------- |
| `/api/orders/carts/` | `POST`  | Crear carrito con productos                               |
| `/api/orders/`       | `POST`  | Crear orden con items                                     |
| `/api/orders/`       | `GET`   | Listar órdenes del vendedor                               |
| `/api/orders/{id}/`  | `PATCH` | Actualizar estado de orden (`PENDING`, `COMPLETED`, etc.) |


## 🧪 Pruebas automáticas
Para ejecutar todos los tests con `pytest`
   ```bash
   pytest -v
   ````
Puedes usar `pytest --disable-warnings` para una salida más limpia

## 🌱 Seeders (Datos iniciales)
El proyecto incluye seeders divididos por módulo para poblar la base de datos con datos de prueba.

**Comandos disponibles:**

```bash
# sin docker 
python manage.py seed_users
python manage.py seed_customers
python manage.py seed_catalog
python manage.py seed_all

# con docker
docker exec -it python manage.py seed_users
docker exec -it python manage.py seed_customers
docker exec -it python manage.py seed_catalog
docker exec -it python manage.py seed_all
```
`seed_all ejecuta todos los seeders en order (usuarios → clientes → catálogo )`

## 🔐 Autenticación
El sistema utiliza **JWT (JSON Web Tokens)** con el paquete `djangorestframework-simplejwt`.

**Enpoints Principales**
* `POST /api/auth/register/` → Registro de usuario (por defecto rol seller).
* `POST /api/auth/token/` → Inicio de sesión (Devuelve tokens `access` y `refresh`)
* `POST /api/auth/logout/` → Cierre de sesión (Invalida refresh token).
* `GET /api/auth/me` → Perfil de usuario autenticado.
* `POST /api/auth/token/refresh` → Renueva el token `access`.

## 🧱 Ejemplo de flujo (usuarios)
```bash 
   # Registro
   curl -X POST http://localhost:8000/api/auth/register/ \
   -H "Content-Type: application/json" \
   -d '{"email": "user@test.com", "password": "12345"}'

   # Login
   curl -X POST http://localhost:8000/api/auth/token/ \
   -H "Content-Type: application/json" \
   -d '{"email": "user@test.com", "password": "12345"}'
   ```
## 🗂️ Endpoints principales
| Recurso                    | Método | Descripción                              |
| -------------------------- | ------ | ---------------------------------------- |
| `/api/catalog/products/`   | GET    | Listar productos                         |
| `/api/catalog/products/`   | POST   | Crear producto (solo admin)              |
| `/api/catalog/categories/` | CRUD   | Gestión de categorías                    |
| `/api/catalog/brands/`     | CRUD   | Gestión de marcas                        |
| `/api/customers/`          | CRUD   | Gestión de clientes (admin y vendedores) |

## 🧰 Variables útiles de entorno
| Variable            | Descripción                | Valor por defecto |
| ------------------- | -------------------------- | ----------------- |
| `POSTGRES_DB`       | Nombre de la base de datos | moto_parts        |
| `POSTGRES_USER`     | Usuario de Postgres        | postgres          |
| `POSTGRES_PASSWORD` | Contraseña de Postgres     | postgres          |
| `POSTGRES_HOST`     | Host de la BD              | db                |
| `POSTGRES_PORT`     | Puerto de la BD            | 5432              |

## 👨‍💻 Autor
Juan Camilo Ordoñez Morea

Desarrollador Backend — Python / Django / Node.js

📧 juan.ordonez.dev@gmail.com

🌐  [LinkedIn](www.linkedin.com/in/juancamiloordonezmorea-desarrolladorfullstack)

## 🏁 Licencia
Este proyecto se distribuye bajo la licencia MIT.

Consulta el archivo `LICENSE` para más información.