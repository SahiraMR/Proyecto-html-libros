from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación
app = FastAPI(debug=os.getenv("DEBUG", "false").lower() == "true")

# Montar archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.templates = templates  # Para usar templates en otros routers

# Páginas principales
@app.get("/", response_class=HTMLResponse)
def mostrar_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/objetivo", response_class=HTMLResponse)
def objetivo(request: Request):
    return templates.TemplateResponse("objetivo.html", {"request": request})

@app.get("/planeacion", response_class=HTMLResponse)
def planeacion(request: Request):
    return templates.TemplateResponse("planeacion.html", {"request": request})

@app.get("/diseno", response_class=HTMLResponse)
def diseno(request: Request):
    return templates.TemplateResponse("diseno.html", {"request": request})

@app.get("/desarrollador", response_class=HTMLResponse)
def desarrollador(request: Request):
    return templates.TemplateResponse("desarrollador.html", {"request": request})

# Incluir routers
from app.routes import libros, autores, comentarios
app.include_router(libros.router)
app.include_router(autores.router)
app.include_router(comentarios.router)
