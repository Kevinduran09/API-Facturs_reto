from ..models.vehiculoModel import TrasmisionEnum, CombustibleEnum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date
class VehiculoIn(BaseModel):
   tipoVehiculo: str
   placa: str
   capacidad: int = Field(gt=0)
   modelo: str
   fechaCompra: date
   anoVehiculo: int = Field(ge=1900, le=date.today().year)
   potencia: int = Field(ge=0)
   transmision: TrasmisionEnum
   combustible: CombustibleEnum
   color: str
   numeroPuertas: int = Field(..., ge=2, le=5)
   kilometraje: Optional[int] = Field(default=None, ge=0)
   fechaUltimoMantenimiento: Optional[date] = None
   carnetCirculacion: Optional[str] = None

class VehiculoOut(VehiculoIn):
    id: int

    class Config:
        from_attributes = True 


class VehiculoUpdate(BaseModel):
    tipoVehiculo: Optional[str] = None
    placa: Optional[str] = None
    capacidad: Optional[int] = Field(default=None, gt=0)
    modelo: Optional[str] = None
    fechaCompra: Optional[date] = None
    anoVehiculo: Optional[int] = Field(
        default=None, ge=1900, le=date.today().year)
    potencia: Optional[int] = Field(default=None, ge=0)
    transmision: Optional[TrasmisionEnum] = None
    combustible: Optional[CombustibleEnum] = None
    color: Optional[str] = None
    numeroPuertas: Optional[int] = Field(default=None, ge=2, le=5)
    kilometraje: Optional[int] = Field(default=None, ge=0)
    fechaUltimoMantenimiento: Optional[date] = None
    carnetCirculacion: Optional[str] = None
