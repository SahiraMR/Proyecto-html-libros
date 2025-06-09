from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.autor import AutorCreate, Autor as AutorSchema
from app.crud.autor import (
    obtener_autores,
    obtener_autor_por_id,
    obtener_autor_por_nombre,
    crear_autor,
    actualizar_autor,
    eliminar_autor,
    obtener_autores_eliminados
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ----------------------------
# 🌐 Rutas HTML
# ----------------------------

@router.get("/autores", response_class=HTMLResponse)
def listar_autores(request: Request, db: Session = Depends(get_db)):
    autores = obtener_autores(db)
    return templates.TemplateResponse("autores.html", {"request": request, "autores": autores})

@router.get("/autores/crear", response_class=HTMLResponse)
def mostrar_formulario_crear_autor(request: Request):
    return templates.TemplateResponse("crear_autor.html", {"request": request})

@router.post("/autores/crear")
def crear_autor_html(
    request: Request,
    nombre: str = Form(...),
    nombre_libro: str = Form(...),
    genero: str = Form(...),
    db: Session = Depends(get_db)
):
    nuevo_autor = crear_autor(db, nombre, genero)
    nuevo_autor.nombre_libro = nombre_libro
    db.commit()
    db.refresh(nuevo_autor)
    return RedirectResponse("/autores", status_code=303)

@router.get("/autores/delete/{id}")
def eliminar_autor_html(id: int, db: Session = Depends(get_db)):
    eliminar_autor(db, id)
    return RedirectResponse("/autores", status_code=303)

@router.get("/autores/eliminados", response_class=HTMLResponse)
def ver_autores_eliminados(request: Request, db: Session = Depends(get_db)):
    eliminados = obtener_autores_eliminados(db)
    return templates.TemplateResponse("autores_eliminados.html", {"request": request, "autores": eliminados})

@router.get("/autores/editar/{id}", response_class=HTMLResponse)
def formulario_editar_autor(id: int, request: Request, db: Session = Depends(get_db)):
    autor = obtener_autor_por_id(db, id)
    if not autor:
        return RedirectResponse("/autores", status_code=303)
    return templates.TemplateResponse("editar_autor.html", {"request": request, "autor": autor})

@router.post("/autores/editar/{id}")
def actualizar_autor_html(
    id: int,
    nombre: str = Form(...),
    genero: str = Form(...),
    nombre_libro: str = Form(...),
    db: Session = Depends(get_db)
):
    actualizar_autor(db, id, nombre, genero, nombre_libro)
    return RedirectResponse("/autores", status_code=303)

# ----------------------------
# 📘 Rutas REST API para Swagger
# ----------------------------

@router.get("/api/autores", response_model=List[AutorSchema])
def api_listar_autores(db: Session = Depends(get_db)):
    return obtener_autores(db)

@router.get("/api/autores/{autor_id}", response_model=AutorSchema)
def api_obtener_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = obtener_autor_por_id(db, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

@router.post("/api/autores", response_model=AutorSchema)
def api_crear_autor(autor: AutorCreate, db: Session = Depends(get_db)):
    return crear_autor(
        db,
        nombre=autor.nombre,
        genero=autor.genero,
        nombre_libro=autor.nombre_libro or "Desconocido"
    )

@router.put("/api/autores/{autor_id}", response_model=AutorSchema)
def api_actualizar_autor(autor_id: int, autor_data: AutorCreate, db: Session = Depends(get_db)):
    autor = actualizar_autor(db, autor_id, autor_data.nombre, autor_data.genero, autor_data.nombre_libro)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

@router.delete("/api/autores/{autor_id}")
def api_eliminar_autor(autor_id: int, db: Session = Depends(get_db)):
    eliminar_autor(db, autor_id)
    return {"mensaje": "Autor eliminado correctamente"}
