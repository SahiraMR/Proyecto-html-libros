from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base

class Comentario(Base):
    __tablename__ = "comentarios"  # corregido __tablename__

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    usuario = Column(String, nullable=False)
    contenido = Column(String, nullable=False)
    fecha = Column(String, nullable=False)
    eliminado = Column(Boolean, default=False)  # lógica de eliminado lógico
