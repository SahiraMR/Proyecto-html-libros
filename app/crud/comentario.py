from sqlalchemy.orm import Session
from app.models.comentario import Comentario

def obtener_comentarios(db: Session):
    return db.query(Comentario).filter(Comentario.eliminado == False).all()

def obtener_comentario_por_id(db: Session, comentario_id: int):
    return db.query(Comentario).filter(Comentario.id == comentario_id).first()

def crear_comentario(db: Session, comentario_data: dict):
    nuevo_comentario = Comentario(**comentario_data)
    db.add(nuevo_comentario)
    db.commit()
    db.refresh(nuevo_comentario)
    return nuevo_comentario

def actualizar_comentario(db: Session, comentario_id: int, nuevos_datos: dict):
    comentario = db.query(Comentario).filter(Comentario.id == comentario_id).first()
    if comentario:
        for key, value in nuevos_datos.items():
            setattr(comentario, key, value)
        db.commit()
        db.refresh(comentario)
    return comentario

def eliminar_comentario(db: Session, comentario_id: int):
    comentario = db.query(Comentario).filter(Comentario.id == comentario_id).first()
    if comentario:
        comentario.eliminado = True
        db.commit()
        db.refresh(comentario)
        return comentario
    return None

def obtener_comentarios_eliminados(db: Session):
    return db.query(Comentario).filter(Comentario.eliminado == True).all()

def obtener_comentarios_por_libro(db: Session, libro_id: int):
    return db.query(Comentario).filter(
        Comentario.libro_id == libro_id,
        Comentario.eliminado == False
    ).all()
