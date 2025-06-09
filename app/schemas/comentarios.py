from pydantic import BaseModel
from typing import Optional
from datetime import date

class ComentarioBase(BaseModel):
    libro_id: int
    usuario: str
    contenido: str
    fecha: date  # Acepta formato YYYY-MM-DD

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioUpdate(BaseModel):
    usuario: Optional[str] = None
    contenido: Optional[str] = None
    fecha: Optional[date] = None

class ComentarioOut(ComentarioBase):
    id: int
    eliminado: bool

    class Config:
        from_attributes = True
