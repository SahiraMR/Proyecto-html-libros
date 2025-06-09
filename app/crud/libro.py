from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.libro import Libro

def obtener_libros(db: Session):
    return db.query(Libro).filter_by(eliminado=False).all()

def obtener_libro_por_id(db: Session, libro_id: int):
    return db.query(Libro).filter_by(id=libro_id).first()

def crear_libro(db: Session, libro: Libro):
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro

def actualizar_libro(db: Session, libro_id: int, datos_actualizados: dict):
    libro = db.query(Libro).filter_by(id=libro_id).first()
    if libro:
        for clave, valor in datos_actualizados.items():
            setattr(libro, clave, valor)
        db.commit()
        db.refresh(libro)
    return libro

def eliminar_libro(db: Session, libro_id: int):
    libro = db.query(Libro).filter_by(id=libro_id).first()
    if libro:
        libro.eliminado = True
        db.commit()

def obtener_libros_eliminados(db: Session):
    return db.query(Libro).filter_by(eliminado=True).all()

def filtrar_libros_por_genero(db: Session, genero: str):
    return db.query(Libro).filter(
        and_(
            Libro.genero.ilike(f"%{genero.strip()}%"),
            Libro.eliminado == False
        )
    ).all()

def obtener_generos_unicos(db: Session):
    generos = db.query(Libro.genero).filter(Libro.eliminado == False).distinct().all()
    return sorted(set([
        g[0].strip().capitalize()
        for g in generos
        if g[0] and len(g[0].strip()) >= 3  # solo géneros de al menos 3 letras
    ]))
