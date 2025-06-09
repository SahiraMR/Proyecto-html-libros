from pydantic import BaseModel
from typing import Optional

# Base común
class LibroBase(BaseModel):
    titulo: str
    autor_id: int
    anio_publicacion: Optional[str]
    genero: Optional[str]
    plataforma: Optional[str]
    viral_en_tiktok: Optional[bool]
    portada: Optional[str] = "sinportada.jpg"

# Para crear libro
class LibroCreate(LibroBase):
    pass

# Para actualizar libro (campos opcionales)
class LibroUpdate(BaseModel):
    titulo: Optional[str]
    autor_id: Optional[int]
    anio_publicacion: Optional[str]
    genero: Optional[str]
    plataforma: Optional[str]
    viral_en_tiktok: Optional[bool]
    portada: Optional[str]

# Para mostrar libro
class LibroOut(LibroBase):
    id: int
    eliminado: Optional[bool]

    class Config:
        from_attributes = True
