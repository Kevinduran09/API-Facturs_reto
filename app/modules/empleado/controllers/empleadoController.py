
from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from injector import Injector
from ..services.empleadoService import EmpleadoService
from ..schemas.empleadoSchema import EmpleadoSchema, EmpleadoOut, EmpleadoIn, EmpleadoUpdate
from ..module import EmpleadoModule

router = APIRouter()

injector = Injector([EmpleadoModule()])

def get_service() -> EmpleadoService:
    return injector.get(EmpleadoService)


def get_service() -> EmpleadoService:
    return injector.get(EmpleadoService)


@router.get("/", response_model=List[EmpleadoOut])
async def get_all_empleados(service: EmpleadoService = Depends(get_service)):
    return await service.get_all()


@router.get("/{id}", response_model=EmpleadoOut)
async def get_empleado_by_id(id: int, service: EmpleadoService = Depends(get_service)):
    empleado = await service.get_by_id(id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@router.post("/", response_model=EmpleadoOut, status_code=status.HTTP_201_CREATED)
async def create_empleado(data: EmpleadoIn, service: EmpleadoService = Depends(get_service)):
    empleado = await service.store(data)
    if not empleado:
        raise HTTPException(
            status_code=400, detail="Error al crear el empleado")
    return empleado


@router.put("/{id}", response_model=EmpleadoOut)
async def update_empleado(id: int, data: EmpleadoUpdate, service: EmpleadoService = Depends(get_service)):
    print(data)
    empleado = await service.update(id, data)
    if not empleado:
        raise HTTPException(
            status_code=404, detail="Empleado no encontrado o error al actualizar")
    return empleado


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_empleado(id: int, service: EmpleadoService = Depends(get_service)):
    success = await service.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
