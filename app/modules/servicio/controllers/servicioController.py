from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from injector import Injector
from ..services.servicioService import ServicioService
from ..schemas.servicioSchema import ServicioOut, ServicioUpdate, ServicioBase
from ..module import ServicioModule

router = APIRouter()

injector = Injector([ServicioModule()])


def get_service() -> ServicioService:
    return injector.get(ServicioService)


@router.get("/", response_model=List[ServicioOut], summary="Obtener todos los servicios")
async def get_all_servicios(service: ServicioService = Depends(get_service)):
    return await service.get_all()


@router.get("/{id}", response_model=ServicioOut, summary="Obtener un servicio por ID")
async def get_servicio_by_id(id: int, service: ServicioService = Depends(get_service)):
    servicio = await service.get_by_id(id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


@router.post("/", response_model=ServicioOut, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo servicio")
async def create_servicio(data: ServicioBase, service: ServicioService = Depends(get_service)):
    servicio = await service.store(data)
    if not servicio:
        raise HTTPException(
            status_code=400, detail="Error al crear el servicio")
    return servicio


@router.put("/{id}", response_model=ServicioOut, summary="Actualizar un servicio existente")
async def update_servicio(id: int, data: ServicioUpdate, service: ServicioService = Depends(get_service)):
    servicio = await service.update(id, data)
    if not servicio:
        raise HTTPException(
            status_code=404, detail="Servicio no encontrado o error al actualizar")
    return servicio


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un servicio")
async def delete_servicio(id: int, service: ServicioService = Depends(get_service)):
    success = await service.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
