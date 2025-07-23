
from typing import Optional
from pydantic import BaseModel
from ...puesto.schemas.puestoSchema import PuestoOut
from datetime import datetime
from ...usuario.schemas.UsuarioSchema import UsuarioSchema
class EmpleadoSchema(BaseModel):
    nombre: str
    apellido:str
    cedula:str
    correoElectronico: str
    telefono:str
    direccion:str
    puesto: int
    fecha_Nacimiento: datetime
    fecha_contratacion: datetime
    
    class Config:
        from_attributes = True
    

class EmpleadoOut(EmpleadoSchema):
    id:int
    puesto: PuestoOut
    puesto_id:int

class EmpleadoIn(EmpleadoSchema):
    usuario: UsuarioSchema
    
class EmpleadoUpdate(BaseModel):
    nombre: Optional[str]
    apellido:Optional[str]
    cedula:Optional[str]
    correoElectronico: Optional[str]
    telefono:Optional[str]
    direccion:Optional[str]