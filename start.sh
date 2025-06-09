#!/bin/bash

# Cargar puerto dinámico si existe (por defecto 10000)
PORT=${PORT:-10000}

# Iniciar la app FastAPI con Uvicorn
uvicorn app.main:app --host=0.0.0.0 --port=$PORT
