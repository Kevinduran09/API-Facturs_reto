from pydantic import BaseModel
from typing import Optional


class ServicioBase(BaseModel):
    tipoServicio: str
    descripcionServicio: str
    precioKilometro: float
    requiere_origen: bool
    requiere_destino: bool


class ServicioCreate(ServicioBase):
    pass


class ServicioUpdate(BaseModel):
    tipoServicio: Optional[str] = None
    descripcionServicio: Optional[str] = None
    precioKilometro: Optional[float] = None
    requiere_origen: Optional[bool]
    requiere_destino: Optional[bool]


class ServicioOut(ServicioBase):
    idServicio: int

    class Config:
        from_attributes = True
