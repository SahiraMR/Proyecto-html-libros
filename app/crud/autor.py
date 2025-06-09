from sqlalchemy.orm import Session
from app.models.autor import Autor

def obtener_autores(db: Session):
    return db.query(Autor).filter(Autor.eliminado == "no").all()

def obtener_autor_por_id(db: Session, autor_id: int):
    return db.query(Autor).filter(Autor.id == autor_id).first()

def obtener_autor_por_nombre(db: Session, nombre: str):
    return db.query(Autor).filter(Autor.nombre == nombre).first()

def crear_autor(db: Session, nombre: str, genero: str, nombre_libro: str = "Desconocido"):
    nuevo_autor = Autor(nombre=nombre, genero=genero, nombre_libro=nombre_libro)
    db.add(nuevo_autor)
    db.commit()
    db.refresh(nuevo_autor)
    return nuevo_autor

def actualizar_autor(db: Session, autor_id: int, nuevo_nombre: str, nuevo_genero: str, nuevo_libro: str):
    autor = obtener_autor_por_id(db, autor_id)
    if autor:
        autor.nombre = nuevo_nombre
        autor.genero = nuevo_genero
        autor.nombre_libro = nuevo_libro
        db.commit()
        db.refresh(autor)
    return autor

def eliminar_autor(db: Session, autor_id: int):
    autor = obtener_autor_por_id(db, autor_id)
    if autor:
        autor.eliminado = "si"
        db.commit()

def obtener_autores_eliminados(db: Session):
    return db.query(Autor).filter(Autor.eliminado == "si").all()
