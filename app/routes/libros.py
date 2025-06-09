from fastapi import APIRouter, Request, Form, Depends, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.libro import Libro
from app.models.autor import Autor
from app.schemas.libros import LibroCreate, LibroUpdate, LibroOut
from app.crud.libro import (
    obtener_libros,
    obtener_libro_por_id,
    crear_libro,
    actualizar_libro,
    eliminar_libro,
    obtener_libros_eliminados,
    filtrar_libros_por_genero,
    obtener_generos_unicos
)
from app.crud.comentario import obtener_comentarios_por_libro

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# HTML PRINCIPAL
@router.get("/libros", response_class=HTMLResponse)
def listar_libros(request: Request, db: Session = Depends(get_db)):
    libros = obtener_libros(db)
    for libro in libros:
        autor = db.query(Autor).filter(Autor.id == libro.autor_id).first()
        libro.autor_nombre = autor.nombre if autor else "Desconocido"
        libro.comentarios = obtener_comentarios_por_libro(db, libro.id)
    return templates.TemplateResponse("libros.html", {"request": request, "libros": libros})

# FORMULARIO CREAR
@router.get("/libros/crear", response_class=HTMLResponse)
def mostrar_formulario_crear_libro(request: Request, db: Session = Depends(get_db)):
    autores = db.query(Autor).all()
    return templates.TemplateResponse("crear_libro.html", {"request": request, "autores": autores})

@router.post("/libros/crear")
async def crear_libro_post(
    titulo: str = Form(...),
    autor_id: int = Form(...),
    anio_publicacion: str = Form(...),
    genero: str = Form(...),
    plataforma: str = Form(...),
    viral_en_tiktok: str = Form(...),
    portada: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    nombre_portada = "sinportada.jpg"
    if portada and portada.filename:
        ruta = f"static/portadas/{portada.filename}"
        with open(ruta, "wb") as f:
            f.write(await portada.read())
        nombre_portada = portada.filename

    nuevo_libro = Libro(
        titulo=titulo,
        autor_id=autor_id,
        anio_publicacion=anio_publicacion,
        genero=genero,
        plataforma=plataforma,
        viral_en_tiktok=(viral_en_tiktok == "True"),
        portada=nombre_portada,
        eliminado=False
    )
    crear_libro(db, nuevo_libro)
    return RedirectResponse("/libros", status_code=303)

# EDITAR
@router.get("/libros/editar/{libro_id}", response_class=HTMLResponse)
def mostrar_formulario_editar_libro(libro_id: int, request: Request, db: Session = Depends(get_db)):
    libro = obtener_libro_por_id(db, libro_id)
    autores = db.query(Autor).all()
    return templates.TemplateResponse("editar_libro.html", {"request": request, "libro": libro, "autores": autores})

@router.post("/libros/editar/{libro_id}")
async def editar_libro(
    libro_id: int,
    titulo: str = Form(...),
    autor_id: int = Form(...),
    anio_publicacion: str = Form(...),
    genero: str = Form(...),
    plataforma: str = Form(...),
    viral_en_tiktok: str = Form(...),
    portada: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    libro = obtener_libro_por_id(db, libro_id)
    if not libro:
        return HTMLResponse(content="Libro no encontrado", status_code=404)

    if portada and portada.filename:
        ruta = f"static/portadas/{portada.filename}"
        with open(ruta, "wb") as f:
            f.write(await portada.read())
        libro.portada = portada.filename

    datos = {
        "titulo": titulo,
        "autor_id": autor_id,
        "anio_publicacion": anio_publicacion,
        "genero": genero,
        "plataforma": plataforma,
        "viral_en_tiktok": (viral_en_tiktok == "True"),
        "portada": libro.portada
    }

    actualizar_libro(db, libro_id, datos)
    return RedirectResponse("/libros", status_code=303)

# ELIMINAR
@router.get("/libros/eliminar/{libro_id}")
def eliminar_libro_html(libro_id: int, db: Session = Depends(get_db)):
    eliminar_libro(db, libro_id)
    return RedirectResponse("/libros", status_code=303)

# VER LIBROS ELIMINADOS
@router.get("/libros/eliminados", response_class=HTMLResponse)
def ver_libros_eliminados(request: Request, db: Session = Depends(get_db)):
    libros = obtener_libros_eliminados(db)
    for libro in libros:
        autor = db.query(Autor).filter(Autor.id == libro.autor_id).first()
        libro.autor_nombre = autor.nombre if autor else "Desconocido"
    return templates.TemplateResponse("libros_eliminados.html", {"request": request, "libros": libros})

# NUEVAS FUNCIONES DE BÚSQUEDA Y FILTRADO
@router.get("/libros/buscar", response_class=HTMLResponse)
def mostrar_formulario_busqueda(request: Request, db: Session = Depends(get_db)):
    generos = [g[0] for g in obtener_generos_unicos(db)]
    return templates.TemplateResponse("busqueda_libros.html", {"request": request, "generos": generos})

@router.get("/libros/filtrar", response_class=HTMLResponse)
def filtrar_libros_genero(request: Request, genero: str, db: Session = Depends(get_db)):
    libros = filtrar_libros_por_genero(db, genero)
    for libro in libros:
        autor = db.query(Autor).filter(Autor.id == libro.autor_id).first()
        libro.autor_nombre = autor.nombre if autor else "Desconocido"
    return templates.TemplateResponse("filtro_resultado.html", {"request": request, "libros": libros, "genero": genero})

@router.get("/libros/buscar_por_id", response_class=HTMLResponse)
def buscar_libro_por_id(request: Request, id: int, db: Session = Depends(get_db)):
    libro = obtener_libro_por_id(db, id)
    if libro:
        autor = db.query(Autor).filter(Autor.id == libro.autor_id).first()
        libro.autor_nombre = autor.nombre if autor else "Desconocido"
        libro.comentarios = obtener_comentarios_por_libro(db, libro.id)
    return templates.TemplateResponse("buscar_resultado.html", {"request": request, "libro": libro})

# API PARA DOCS
@router.get("/api/libros", response_model=list[LibroOut])
def api_obtener_libros(db: Session = Depends(get_db)):
    return obtener_libros(db)

@router.get("/api/libros/{libro_id}", response_model=LibroOut)
def api_obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = obtener_libro_por_id(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.post("/api/libros", response_class=HTMLResponse)
def api_crear_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    nuevo = Libro(**libro.dict(), eliminado=False)
    crear_libro(db, nuevo)
    return HTMLResponse(content="<h2>✅ Libro creado correctamente</h2><a href='/libros'>Volver</a>")

@router.put("/api/libros/{libro_id}", response_class=HTMLResponse)
def api_actualizar_libro(libro_id: int, libro: LibroUpdate, db: Session = Depends(get_db)):
    libro_existente = obtener_libro_por_id(db, libro_id)
    if not libro_existente:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    actualizar_libro(db, libro_id, libro.dict(exclude_unset=True))
    return HTMLResponse(content="<h2>✅ Libro actualizado</h2><a href='/libros'>Volver</a>")

@router.delete("/api/libros/{libro_id}", response_class=HTMLResponse)
def api_eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    eliminar_libro(db, libro_id)
    return HTMLResponse(content="<h2>🗑️ Libro eliminado</h2><a href='/libros'>Volver</a>")
