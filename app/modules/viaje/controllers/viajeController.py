from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from injector import Injector

from app.modules.factura.middlewares.authFactusMiddleware import auth_factus_middleware
from ..services.viajeService import ViajeService
from ..schemas.viajeSchema import ViajeDetalleOut, ViajeSchema, ViajeOut, ViajeIn, ViajeUpdate
from ..module import ViajeModule
from ...solicitud.schemas.solicitudSchema import multiSolicitudes
router = APIRouter()

injector = Injector([ViajeModule()])

def get_service() -> ViajeService:
    return injector.get(ViajeService)


@router.get("/available-employees/{fecha}")
async def get_available_employees(fecha: date, service: ViajeService = Depends(get_service)):
    """
    Endpoint para obtener empleados disponibles para asignar a un viaje.
    """
    try:
        employees = await service.get_available_employees(fecha)
        return {"available_employees": employees}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=List[ViajeOut])
async def get_all_viajes(service: ViajeService = Depends(get_service)):
    """Obtener todos los viajes"""
    return await service.get_all()

@router.get("/{id}", response_model=ViajeDetalleOut)
async def get_viaje_by_id(id: int, service: ViajeService = Depends(get_service)):
    """Obtener un viaje por ID"""
    viaje = await service.get_full_by_id(id)
    if not viaje:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viaje no encontrado")
    return viaje


@router.post('/alcanzables')
async def validate_routes(solicitudes: multiSolicitudes, service: ViajeService = Depends(get_service)):
    """Verificar el alcance de las solicitudes para construir una ruta"""
    return await service.validate_availability(solicitudes.solicitudes)


@router.post("/", response_model=ViajeSchema, status_code=status.HTTP_201_CREATED)
async def create_viaje(data: ViajeIn, service: ViajeService = Depends(get_service)):
    """Crear un nuevo viaje"""
    viaje = await service.store(data)
    if not viaje:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Error al crear el viaje")
    return viaje


@router.put("/{id}")
async def update_viaje(id: int, data: ViajeUpdate, service: ViajeService = Depends(get_service)):
    """Actualizar un viaje existente"""
    print(data)
    viaje = await service.update(id, data)
    if not viaje:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Viaje no encontrado o error al actualizar")
    return viaje


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_viaje(id: int, service: ViajeService = Depends(get_service)):
    """Eliminar un viaje"""
    success = await service.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Viaje no encontrado")
