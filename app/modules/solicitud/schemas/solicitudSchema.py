from pydantic import BaseModel, field_validator
from datetime import datetime, time, timedelta
from typing import List, Optional
from ..models.solicitudModel import EstadoSolicitudEnum
from ...cliente.schemas.clienteSchema import ClientResponse
from ...servicio.schemas.servicioSchema import ServicioOut
from ...direccion.schemas.direccionSchema import DireccionOut, DireccionSchema
# Asegúrate de que este schema exista
from ...viaje.schemas.viajeSchema import ViajeOut


class SolicitudSchema(BaseModel):
    cliente: int
    servicio: int
    direccionOrigen: int
    direccionDestino: int
    fecha: datetime
    observacion: Optional[str] = None

    class Config:
        from_attributes = True


class SolicitudIn(SolicitudSchema):
    pass


class SolicitudCambioEstado(BaseModel):
    estado: EstadoSolicitudEnum


class SolicitudCreate(BaseModel):
    cliente: int
    servicio: int
    direccionOrigen: DireccionSchema
    direccionDestino: DireccionSchema
    tiempo_estimado: Optional[time] = None
    kilometros: Optional[float] = None
    fecha: datetime
    observacion: Optional[str] = None

    class Config:
        from_attributes = True


class multiSolicitudes(BaseModel):
    solicitudes: List[int]


class SolicitudOut(BaseModel):
    id: int
    estado: EstadoSolicitudEnum
    anotaciones: Optional[str] = None
    tiempo_estimado: Optional[time] = None
    kilometros: Optional[float] = None
    cliente: ClientResponse
    servicio: ServicioOut
    direccionOrigen: DireccionOut
    direccionDestino: DireccionOut
    fecha: datetime
    observacion: Optional[str] = None
    direccionOrigen_id: int
    direccionDestino_id: int
    servicio_id: int
    cliente_id: int

    class Config:
        from_attributes = True

    @field_validator('tiempo_estimado', mode='before')
    def convertir_tiempo_estimado(cls, v):
        if isinstance(v, timedelta):
            return (datetime.min + v).time()
        return v


class SolicitudForViajeSchema(SolicitudOut):
    horaSalida: Optional[time] = None
    horaLlegada: Optional[time] = None
    horaReal: Optional[time] = None
    order: Optional[int] = None
    viaje: Optional[ViajeOut] = None
    viaje_id: Optional[int] = None


class SolicitudUpdate(BaseModel):
    idCliente: Optional[int] = None
    idServicio: Optional[int] = None
    direccionOrigen: Optional[int] = None
    direccionDestino: Optional[int] = None
    fecha: Optional[datetime] = None
    observacion: Optional[str] = None
    anotaciones: Optional[str] = None
    horaSalida: Optional[time] = None
    horaLlegada: Optional[time] = None
    horaReal: Optional[time] = None
    order: Optional[int] = None
    tiempo_estimado: Optional[time] = None
    kilometros: Optional[float] = None
