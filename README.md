# 📊 API Empresarial Segura (ERP / POS Contable)

API RESTful desarrollada con **FastAPI** y **SQLAlchemy**, diseñada como el núcleo backend de un sistema ERP / Punto de Venta (POS) adaptado a la normativa contable y tributaria colombiana. Automatiza el registro de operaciones comerciales, el control de inventario y la generación de asientos contables basados en el **Plan Único de Cuentas (PUC)**.

---

## 🚀 Características Principales

* **Inicialización Automática del PUC:** Precarga de cuentas contables esenciales según el estándar colombiano (Caja/Bancos, Inventarios, Costo de Ventas, Ingresos Operacionales e IVA por Pagar).
* **Gestión de Inventario en Tiempo Real:** Creación y consulta de productos con control estricto de stock disponible y validación de existencias antes de procesar ventas.
* **Motor Contable Automatizado:** Al registrar una venta, la API calcula automáticamente el subtotal, el **IVA del 19%**, el costo de mercancía vendida y descuenta las unidades del inventario en una sola transacción atómica.
* **Validación de Datos y Seguridad:** Esquemas estrictos con **Pydantic** para garantizar integridad en las peticiones y respuestas, además de estructura modular preparada para autenticación y control de acceso.
* **Documentación Interactiva:** Interfaz Swagger UI y ReDoc integradas de forma nativa para pruebas rápidas.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.14+
* **Framework Web:** FastAPI
* **Servidor ASGI:** Uvicorn
* **ORM y Base de Datos:** SQLAlchemy + SQLite (escalable a PostgreSQL)
* **Validación de Datos:** Pydantic

---

## 📁 Estructura del Proyecto

```text
api-empresarial-segura/
├── database.py      # Configuración de conexión y sesión con la base de datos
├── main.py          # Punto de entrada de la API, rutas (endpoints) e inicialización
├── models.py        # Modelos relacionales SQLAlchemy (Cuentas PUC, Productos, Ventas)
├── schemas.py       # Esquemas Pydantic para validación de entrada y salida (DTOs)
├── security.py      # Utilidades de seguridad y protección de endpoints
└── .gitignore       # Exclusión de archivos locales, caché y bases de datos
