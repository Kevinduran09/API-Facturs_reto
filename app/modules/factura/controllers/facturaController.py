from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from injector import Injector

from app.modules.factura.middlewares.authFactusMiddleware import auth_factus_middleware
from ..services.facturaService import FacturaService
from ..schemas.facturaSchema import FacturaSchema, FacturaOut, FacturaIn, FacturaUpdate
from ..module import FacturaModule

router = APIRouter()

injector = Injector([FacturaModule()])

def get_service() -> FacturaService:
    return injector.get(FacturaService)


@router.get('/token')
async def get_token(credentials=Depends(auth_factus_middleware)):
    """Obtener token de factus"""
    return credentials
@router.get('/rangosEnumeracion')
async def get_rangos_enumeracion(service: FacturaService = Depends(get_service), credentials=Depends(auth_factus_middleware)):
    """Obtener token de factus"""
    return await service.get_rangos_enumeracion(credentials)

@router.get("/", response_model=List[FacturaOut])
async def get_all_facturas(service: FacturaService = Depends(get_service)):
    """Obtener todos los facturas"""
    return await service.get_all()


@router.get("/{id}", response_model=FacturaOut)
async def get_factura_by_id(id: int, service: FacturaService = Depends(get_service)):
    """Obtener un factura por ID"""
    factura = await service.get_by_id(id)
    if not factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrado")
    return factura


@router.post("/", response_model=FacturaOut, status_code=status.HTTP_201_CREATED)
async def create_factura(data: FacturaIn, service: FacturaService = Depends(get_service)):
    """Crear un nuevo factura"""
    factura = await service.store(data)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Error al crear el factura")
    return factura


@router.put("/{id}", response_model=FacturaOut)
async def update_factura(id: int, data: FacturaUpdate, service: FacturaService = Depends(get_service)):
    """Actualizar un factura existente"""
    factura = await service.update(id, data)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Factura no encontrado o error al actualizar")
    return factura


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_factura(id: int, service: FacturaService = Depends(get_service)):
    """Eliminar un factura"""
    success = await service.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Factura no encontrado")

@router.post("/emitir", status_code=201)
async def emitir_factura(
    factura_data: dict = Body(...),
    credentials=Depends(auth_factus_middleware),
    service: FacturaService = Depends(get_service)
):
    """Emite una factura a Factus y guarda una copia local."""
    resultado = await service.emitir_y_guardar_factura(credentials, factura_data)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return resultado
