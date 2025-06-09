from pydantic import BaseModel
from typing import Optional

class AutorBase(BaseModel):
    nombre: str
    nombre_libro: Optional[str] = "Desconocido"
    genero: Optional[str] = "N/A"

class AutorCreate(AutorBase):
    pass

class Autor(AutorBase):
    id: int

    class Config:
        from_attributes = True  # ✅ para compatibilidad con Pydantic v2
