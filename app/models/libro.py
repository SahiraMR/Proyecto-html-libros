from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    autor_id = Column(Integer, ForeignKey("autores.id"), nullable=False)
    anio_publicacion = Column(String)
    genero = Column(String)
    plataforma = Column(String)
    viral_en_tiktok = Column(Boolean, default=False)
    portada = Column(String, default="sinportada.jpg")
    eliminado = Column(Boolean, default=False)
