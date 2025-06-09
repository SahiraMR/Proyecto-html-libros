from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.schemas.comentarios import ComentarioCreate, ComentarioUpdate, ComentarioOut
from app.crud.comentario import (
    obtener_comentarios,
    obtener_comentario_por_id,
    crear_comentario,
    actualizar_comentario,
    eliminar_comentario,
    obtener_comentarios_eliminados,
)
from app.models.libro import Libro

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/comentarios", response_class=HTMLResponse)
def listar_comentarios(request: Request, db: Session = Depends(get_db)):
    comentarios = obtener_comentarios(db)
    return templates.TemplateResponse("comentarios.html", {"request": request, "comentarios": comentarios})

@router.get("/comentarios/crear", response_class=HTMLResponse)
def mostrar_formulario_crear_comentario(request: Request, db: Session = Depends(get_db)):
    libros = db.query(Libro).filter(Libro.eliminado == False).all()
    return templates.TemplateResponse("crear_comentario.html", {
        "request": request,
        "libros": libros
    })

@router.post("/comentarios/crear", response_class=HTMLResponse)
def crear_comentario_html(
    request: Request,
    libro_id: int = Form(...),
    usuario: str = Form(...),
    contenido: str = Form(...),
    fecha: str = Form(...),
    db: Session = Depends(get_db)
):
    comentario_data = {
        "libro_id": libro_id,
        "usuario": usuario,
        "contenido": contenido,
        "fecha": date.fromisoformat(fecha),
        "eliminado": False
    }
    crear_comentario(db, comentario_data)
    return RedirectResponse("/comentarios", status_code=303)

@router.get("/comentarios/editar/{comentario_id}", response_class=HTMLResponse)
def mostrar_formulario_editar_comentario(comentario_id: int, request: Request, db: Session = Depends(get_db)):
    comentario = obtener_comentario_por_id(db, comentario_id)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    libros = db.query(Libro).filter(Libro.eliminado == False).all()
    return templates.TemplateResponse("editar_comentario.html", {
        "request": request,
        "comentario": comentario,
        "libros": libros
    })

@router.post("/comentarios/editar/{comentario_id}", response_class=HTMLResponse)
def actualizar_comentario_html(
    comentario_id: int,
    libro_id: int = Form(...),
    usuario: str = Form(...),
    contenido: str = Form(...),
    fecha: str = Form(...),
    db: Session = Depends(get_db)
):
    datos = {
        "libro_id": libro_id,
        "usuario": usuario,
        "contenido": contenido,
        "fecha": date.fromisoformat(fecha)
    }
    comentario_actualizado = actualizar_comentario(db, comentario_id, datos)
    if not comentario_actualizado:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return RedirectResponse("/comentarios", status_code=303)

@router.get("/comentarios/eliminar/{comentario_id}", response_class=HTMLResponse)
def eliminar_comentario_html(comentario_id: int, db: Session = Depends(get_db)):
    comentario = eliminar_comentario(db, comentario_id)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return RedirectResponse("/comentarios", status_code=303)

@router.get("/comentarios/eliminados", response_class=HTMLResponse)
def mostrar_eliminados(request: Request, db: Session = Depends(get_db)):
    comentarios = obtener_comentarios_eliminados(db)
    return templates.TemplateResponse("comentarios_eliminados.html", {
        "request": request,
        "comentarios": comentarios
    })

@router.post("/api/comentarios", response_model=ComentarioOut)
def crear_comentario_api(comentario: ComentarioCreate, db: Session = Depends(get_db)):
    return crear_comentario(db, comentario.dict())

@router.put("/api/comentarios/{comentario_id}", response_model=ComentarioOut)
def actualizar_comentario_api(comentario_id: int, datos: ComentarioUpdate, db: Session = Depends(get_db)):
    comentario = actualizar_comentario(db, comentario_id, datos.dict(exclude_unset=True))
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return comentario

@router.delete("/api/comentarios/{comentario_id}", response_model=ComentarioOut)
def eliminar_comentario_api(comentario_id: int, db: Session = Depends(get_db)):
    comentario = eliminar_comentario(db, comentario_id)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return comentario
