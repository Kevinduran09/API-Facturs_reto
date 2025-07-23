
from datetime import date
from typing import List, Optional
from pydantic import BaseModel

from app.modules.viaje.models.viajeModel import EstadoViajeEnum


class ViajeSchema(BaseModel):
    id: int
    vehiculo_id: int
    fechaViaje: date
    estado: EstadoViajeEnum


class ViajeOut(BaseModel):
    id: int
    TotalSolicitudes: int
    tripulaciones__Empleado__nombre: str
    tripulaciones__Empleado__puesto__cargo: str
    fechaViaje: date
    estado: EstadoViajeEnum

class ViajeIn(BaseModel):
    vehicleId: int
    fechaViaje:date
    selectedRequests:List[int]
    employeeIds:List[int]
    
    class config:
        from_attributes = True
    

class ViajeUpdate(BaseModel):
    estado: Optional[EstadoViajeEnum] = None

    
    
class VehiculoInfo(BaseModel):
    tipoVehiculo: str
    placa: str
    color: str


class SolicitudInfo(BaseModel):
    id: int
    cliente_nombre: str
    tipo_servicio: str
    lat_origen: float
    lon_origen: float
    lat_destino: float
    lon_destino: float
    estado_solicitud: str
class EncargadoInfo(BaseModel):
    id: int
    nombre: str
    cargo: str
class ViajeDetalleOut(BaseModel):
    id: int
    fechaViaje: date
    estado: str
    vehiculo: VehiculoInfo
    encargado: EncargadoInfo
    solicitudes: List[SolicitudInfo]
    
