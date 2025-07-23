
from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from injector import Injector
from ..services.clienteService import ClienteService
from ..schemas.clienteSchema import ClientResponse, ClientIn, CLienteUpdate
from ..module import ClienteModule

router = APIRouter()

injector = Injector([ClienteModule()])

def get_service() -> ClienteService:
    return injector.get(ClienteService)


def get_service() -> ClienteService:
    return injector.get(ClienteService)


@router.get("/", response_model=List[ClientResponse])
async def get_all(service: ClienteService = Depends(get_service)):
    return await service.get_all()


@router.get("/{id}", response_model=ClientResponse)
async def get_by_id(id: int, service: ClienteService = Depends(get_service)):
    cliente = await service.get_by_id(id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create(cliente: ClientIn, service: ClienteService = Depends(get_service)):
    result = await service.store(cliente)
    if not result:
        raise HTTPException(status_code=400, detail="Error al crear cliente")
    return result


@router.put("/{id}", response_model=ClientResponse)
async def update(id:int,cliente: CLienteUpdate, service: ClienteService = Depends(get_service)):
    updated = await service.update(id,cliente)
    if not updated:
        raise HTTPException(
            status_code=404, detail="Cliente no encontrado para actualizar")
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, service: ClienteService = Depends(get_service)):
    success = await service.delete(id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Cliente no encontrado para eliminar")
    return
