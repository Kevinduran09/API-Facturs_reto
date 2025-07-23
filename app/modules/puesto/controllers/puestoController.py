from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from injector import Injector
from ..services.puestoService import PuestoService
from ..schemas.puestoSchema import  PuestoOut, PuestoCreate, PuestoUpdate
from ..module import PuestoModule

router = APIRouter()

injector = Injector([PuestoModule()])

def get_service() -> PuestoService:
    return injector.get(PuestoService)


@router.get("/", response_model=List[PuestoOut])
async def get_all_puestos(service: PuestoService = Depends(get_service)):
    """Obtener todos los puestos"""
    return await service.get_all()


@router.get("/{id}", response_model=PuestoOut)
async def get_puesto_by_id(id: int, service: PuestoService = Depends(get_service)):
    """Obtener un puesto por ID"""
    puesto = await service.get_by_id(id)
    if not puesto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Puesto no encontrado")
    return puesto


@router.post("/", response_model=PuestoOut, status_code=status.HTTP_201_CREATED)
async def create_puesto(data: PuestoCreate, service: PuestoService = Depends(get_service)):
    """Crear un nuevo puesto"""
    puesto = await service.store(data)
    if not puesto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Error al crear el puesto")
    return puesto


@router.put("/{id}", response_model=PuestoOut)
async def update_puesto(id: int, data: PuestoUpdate, service: PuestoService = Depends(get_service)):
    """Actualizar un puesto existente"""
    puesto = await service.update(id, data)
    if not puesto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Puesto no encontrado o error al actualizar")
    return puesto


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_puesto(id: int, service: PuestoService = Depends(get_service)):
    """Eliminar un puesto"""
    success = await service.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Puesto no encontrado")
