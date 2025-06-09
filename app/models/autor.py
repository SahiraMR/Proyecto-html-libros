from sqlalchemy import Column, Integer, String
from app.database import Base

class Autor(Base):
    __tablename__ = "autores"  # corregido __tablename__

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False, unique=True)
    nombre_libro = Column(String, default="Desconocido", nullable=False)
    genero = Column(String, default="N/A", nullable=False)
    eliminado = Column(String, default="no", nullable=False)
