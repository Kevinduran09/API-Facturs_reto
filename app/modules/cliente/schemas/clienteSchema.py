from typing import Optional
from ...usuario.schemas.UsuarioSchema import UsuarioSchema
from pydantic import BaseModel, EmailStr
from datetime import datetime


class ClienteSchema(BaseModel):
    nombre: str
    apellido: str
    correoElectronico: EmailStr
    cedula: str
    telefonoFijo: Optional[str] = None
    telefonoMovil: Optional[str] = None
    telefonoTrabajo: Optional[str] = None

    class Config:
        from_attributes = True


class ClientResponse(ClienteSchema):
    id: int
    fechaIngreso: datetime


class ClientIn(ClienteSchema):
    usuario: UsuarioSchema


class CLienteUpdate(BaseModel):
    nombre: Optional[str]
    apellido: Optional[str]
    correoElectronico: Optional[EmailStr]
    cedula: Optional[str]
    telefonoFijo: Optional[str] = None
    telefonoMovil: Optional[str] = None
    telefonoTrabajo: Optional[str] = None
