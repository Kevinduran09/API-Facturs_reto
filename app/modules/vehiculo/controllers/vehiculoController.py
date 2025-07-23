from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from injector import Injector
from ..services.vehiculoService import VehiculoService
from ..schemas.vehiculoSchema import VehiculoIn, VehiculoOut, VehiculoUpdate
from ..module import VehiculoModule

router = APIRouter()
injector = Injector([VehiculoModule()])


def get_service() -> VehiculoService:
    return injector.get(VehiculoService)


@router.get("/", response_model=List[VehiculoOut])
async def get_all_vehiculos(service: VehiculoService = Depends(get_service)):
    return await service.get_all()


@router.get("/{id}", response_model=VehiculoOut,summary='Consula vehiculo por numero de placa')
async def get_vehiculo_by_id(id: str, service: VehiculoService = Depends(get_service)):
    vehiculo = await service.get_by_placa(id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo


@router.post("/", response_model=VehiculoOut, status_code=status.HTTP_201_CREATED)
async def create_vehiculo(data: VehiculoIn, service: VehiculoService = Depends(get_service)):
    vehiculo = await service.store(data)
    if not vehiculo:
        raise HTTPException(
            status_code=400, detail="Error al crear el vehículo")
    return vehiculo


@router.put("/{id}", response_model=VehiculoOut)
async def update_vehiculo(id: int, data: VehiculoUpdate, service: VehiculoService = Depends(get_service)):
    vehiculo = await service.update(id, data)
    if not vehiculo:
        raise HTTPException(
            status_code=404, detail="Vehículo no encontrado o error al actualizar")
    return vehiculo


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehiculo(id: int, service: VehiculoService = Depends(get_service)):
    success = await service.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
