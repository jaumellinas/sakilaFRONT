# sakilaFRONT

**Frontend web**  
Acceso a Datos — 2º DAM  
Jaume Llinàs Sansó

## Índice

1. [Descripción general](#descripción-general)
2. [Estructura del proyecto](#estructura-del-proyecto)
3. [Requisitos](#requisitos)
4. [Variables de entorno (.env)](#variables-de-entorno-env)
5. [Vistas principales](#vistas-principales)
   1. [Autenticación](#1-autenticación)
   2. [Clientes](#2-clientes)
   3. [Reservas](#3-reservas)
6. [Despliegue en local](#despliegue-en-local)
7. [Despliegue en entorno cloud](#despliegue-en-entorno-cloud)
8. [Uso de IA y recursos](#uso-de-ia-y-recursos)

## Descripción general

> [!NOTE]  
> Esta aplicación está desarrollada con **Django**, un framework de **Python**.

El proyecto **sakilaFRONT** tiene como objetivo proporcionar una **interfaz web** para interactuar con la **API RESTful sakilaAPI**, permitiendo a un usuario autenticado realizar operaciones CRUD sobre **clientes (customers)** y **reservas (rentals)**.

El acceso a la aplicación se controla mediante autenticación con **tokens JWT**, que se obtienen al iniciar sesión con credenciales válidas en la API sakilaAPI.

> [!IMPORTANT]  
> Esta aplicación requiere una instancia activa de **sakilaAPI** para funcionar correctamente. Todos los datos se gestionan a través de las peticiones HTTP a dicha API.

## Estructura del proyecto

```
sakilaFRONT/
├── sakilaAPI_frontend/
│   ├── api/
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── templates/
│   │   │   ├── customers/
│   │   │   │   ├── delete.html
│   │   │   │   ├── detail.html
│   │   │   │   ├── form.html
│   │   │   │   └── list.html
│   │   │   ├── rentals/
│   │   │   │   ├── detail.html
│   │   │   │   ├── form.html
│   │   │   │   └── list.html
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── api_client.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── sakilaAPI_frontend/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── db.sqlite3
│   └── manage.py
├── Dockerfile
├── README.md
├── docker-compose.yml
└── requirements.txt
```

## Requisitos

* Python 3.12+
  * django
  * djangorestframework
  * requests
  * python-dotenv
  * pyjwt

> [!IMPORTANT]  
> Esta guía de instalación asume que el usuario ya dispone de una instancia activa de **sakilaAPI** a la que conectarse.

## Variables de entorno (.env)

* API_BASE_URL
* DEBUG
* SECRET_KEY

## Vistas principales

### 1. **Autenticación**  
`api/views.py`

| Vista | URL | Descripción |
|--------|-----|-------------|
| `RegisterView` | `/register/` | Formulario de registro de nuevo usuario |
| `LoginView` | `/login/` | Formulario de inicio de sesión |
| `LogoutView` | `/logout/` | Cierre de sesión |

---

**a] - Página de registro**

```
GET /register/
```

Muestra un formulario con los campos:
- `username`: Nombre de usuario
- `email`: Correo electrónico
- `password`: Contraseña
- `password_confirm`: Confirmación de contraseña

---

**b] - Página de inicio de sesión**

```
GET /login/
```

Muestra un formulario con los campos:
- `username`: Nombre de usuario
- `password`: Contraseña

---

### 2. **Clientes**  
`api/views.py`

| Vista | URL | Descripción |
|--------|-----|-------------|
| `CustomerListView` | `/customers/` | Lista todos los clientes |
| `CustomerDetailView` | `/customers/<id>/` | Muestra detalles de un cliente |
| `CustomerCreateView` | `/customers/create/` | Formulario para crear cliente |
| `CustomerUpdateView` | `/customers/<id>/edit/` | Formulario para editar cliente |
| `CustomerDeleteView` | `/customers/<id>/delete/` | Confirmación de eliminación |

---

**c] - Lista de clientes**

```
GET /customers/
```

Muestra una tabla con todos los clientes y botones para ver, editar y eliminar.

---

**d] - Crear nuevo cliente**

```
GET /customers/create/
```

Muestra formulario con campos:
- `store_id`: ID de la tienda
- `first_name`: Nombre
- `last_name`: Apellido
- `email`: Correo electrónico
- `address_id`: ID de dirección
- `active`: Estado activo

---

### 3. **Reservas**  
`api/views.py`

| Vista | URL | Descripción |
|--------|-----|-------------|
| `RentalListView` | `/rentals/` | Lista todas las reservas |
| `RentalDetailView` | `/rentals/<id>/` | Muestra detalles de una reserva |
| `RentalCreateView` | `/rentals/create/` | Formulario para crear reserva |
| `RentalDeleteView` | `/rentals/<id>/delete/` | Confirmación de eliminación |

---

**e] - Crear nueva reserva**

```
GET /rentals/create/
```

Muestra formulario con campos:
- `rental_date`: Fecha de alquiler
- `inventory_id`: ID del inventario
- `customer_id`: ID del cliente
- `staff_id`: ID del personal

---

## Despliegue en local

Para documentar el despliegue de nuestra aplicación, asumiremos que el usuario tiene instalada una versión reciente de Python y acceso a una instancia activa de sakilaAPI.

El proceso para llevar a cabo el despliegue en local consiste en:

1. Instalar la última versión de [Python](https://www.python.org/downloads/).
2. Clonar nuestro proyecto de GitHub en la máquina.
3. Abrir una terminal y navegar hasta el directorio donde se encuentra nuestra app.
4. En dicho directorio, crear un `venv` y activarlo.
5. Instalar los requisitos con `pip install -r requirements.txt`
6. Rellenar el archivo `.env` del proyecto con las variables necesarias.
7. Ejecutar migraciones con `python manage.py migrate`
8. Ejecutar el comando `python manage.py runserver`.

Este proceso levantará nuestra aplicación en la URL `http://127.0.0.1:8000`.

## Despliegue en entorno cloud

De forma extra y siendo realizada esta parte tras haber acabado la actividad en sí, he dockerizado y desplegado la aplicación en un servidor VPS propio. Mi entorno de despliegue consiste en tres contenedores:

* ```sakila-web```
* ```sakila-api```
* ```nginx-proxy-manager```

Para lograr conexión entre todas las partes, todos los contenedores mencionados están conectados a una red interna llamada ```inter```, permitiéndome interconectar todos los contenedores entre sí sin exponer todo el tráfico hacia Internet. Además, usando Nginx agilizo la generación de certificados SSL a través del Certbot de Let's Encrypt.

Explicado esto, el proceso de despliegue es el siguiente:

1. Clonar nuestro proyecto de GitHub en el servidor.
2. Abrir una terminal y navegar hasta el directorio donde se encuentra nuestra app.
3. En dicho directorio, crear un archivo `.env` y rellenarlo con nuestras variables de entorno.
4. Ejecutar el comando `docker compose build --no-cache`.
5. Cuando el proyecto termine de descargarse y configurarse, deployear la aplicación con el comando `docker compose up`.

Con estos pasos, tendríamos nuestra aplicación corriendo en el puerto 8000 de nuestro Docker. Para acceder a la aplicación en sí, accederemos al dashboard de Nginx Proxy Manager y crearemos una redirección de la URL `http://sakila-web:8000` a la URL de nuestra elección.

En mi caso, y aprovechando un dominio que reservo para este tipo de experimentos, mi contenedor con el frontend apunta a https://frontsakila.jaume.wtf.

## Uso de IA y recursos

Este proyecto ha sido mayoritariamente elaborado guiándome por la documentación oficial de Django y posts de foros del estilo StackOverflow. No obstante, para funciones específicas como la integración con la API externa, manejo de tokens JWT o el afinado de ciertos elementos de CSS con Bulma se ha usado la inteligencia artificial Claude a modo de corrector, pasándole el script entero y comentando (no corrigiendo directamente) las partes que no le gustaban.