# 📦 Inventario Backend - Exploración de Frameworks

Este proyecto es una iniciativa personal para explorar distintos frameworks de backend a través de la construcción de un sistema de inventario sencillo. Con el objetivo de comparar tecnologías, ver como funcionan las rutas, parámetros, entre otros temas.

## 🚀 Tecnologías exploradas

Este repositorio contendrá versiones del sistema construidas con diferentes frameworks, tales como:

- **Node.js (Express.js)**
- **Python (Flask, FastAPI, Django)**
- **Java (Spring Boot)**
- **Go (Gin / Fiber)**
- **Rust (Actix Web / Rocket)**
- **C# (.NET Core Web API)**

Cada implementación estará organizada en carpetas separadas dentro del repositorio.

## 🧾 Funcionalidades del sistema

El sistema de inventario incluirá funcionalidades básicas como:

- Gestión de productos:
  - Crear / Leer / Actualizar / Eliminar producto
- Autenticación de usuarios (opcional según framework)
- API RESTful para consumo por frontend o terceros (Se verifica con Postman)

## 📁 Estructura del repositorio

```bash
inventario-backend/
│
├── express/            # Implementación en Express.js
├── flask/              # Implementación en Flask
├── fastapi/            # Implementación en FastAPI
├── django/             # Implementación en Django
├── springboot/         # Implementación en Spring Boot
├── .NET/               # Implementación en .NET Core
├── postman.json        # Archivo de rutas exportadas en postman
└── README.md           # Este archivo
```

## Comandos

- Express
  - Instala las dependencias creando el node_modules de acuerdo a lo que esté en el package.json. El segundo comando es cuando se quiere crear un nuevo proyecto de cero:
  ```
    npm install
    npm install express
  ```
  - Para iniciar o levantar el servidor:
  ```
    node server.js
    npm start
  ```
- Flask
  - Primero se instalan las dependencias necesarias:
  ```
    pip install flask PyJWT bcrypt
  ```
  - Para levantar el servidor:
  ```
    python server.py
  ```
- FastAPI
  - Instala fastapi y uvicorn (para leventar el servidor)
  ```
    pip install fastapi uvicorn
  ```
- Levanta el servidor
  ```
    python -m uvicorn server:app --reload --port 4002
  ```