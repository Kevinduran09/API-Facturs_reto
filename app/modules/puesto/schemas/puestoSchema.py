
from typing import Optional
from pydantic import BaseModel

class PuestoSchema(BaseModel):
    cargo: str
    salario:float
    descripcion: Optional[str]=None
    codigo: str
    class Config:
        from_attributes = True
        
class PuestoOut(PuestoSchema):
    id: int


class PuestoCreate(PuestoSchema):
    pass


class PuestoUpdate(BaseModel):
    cargo: Optional[str]=None
    salario: Optional[float]=None
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True
