from datetime import date, datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from injector import Injector

from app.modules.solicitud.repositories.solicitudRepository import SolicitudCanceladaError
from ..services.solicitudService import SolicitudService
from ..schemas.solicitudSchema import SolicitudIn, multiSolicitudes, SolicitudCambioEstado, SolicitudOut, SolicitudUpdate, SolicitudCreate
from ..module import SolicitudModule

router = APIRouter()

injector = Injector([SolicitudModule()])

def get_service() -> SolicitudService:
    return injector.get(SolicitudService)


@router.get('/getByDate', response_model=List[SolicitudOut])
async def get_by_date(date: date = Query(..., description="Fecha en formato YYYY-MM-DD"), service: SolicitudService = Depends(get_service)):
    """
    Endpoint para obtener solicitudes por fecha.
    """
    solicitudes = await service.get_by_date(date)
    if not solicitudes:
        raise HTTPException(
            status_code=404, detail="No se encontraron solicitudes para la fecha proporcionada")
    return solicitudes

@router.get('/detailsToBilling/{id}')
async def get_details_to_billing(id:int,service: SolicitudService = Depends(get_service)):
    """
    Endpoint para obtener detalles de solicitudes para facturación.
    """
    try:
        details = await service.get_details_to_billing(id)
        return details
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Error interno del servidor {ex}")
    
@router.get("/", response_model=List[SolicitudOut])
async def get_all_solicitudes(service: SolicitudService = Depends(get_service)):
    return await service.get_all()


@router.get("/{id}", response_model=SolicitudOut)
async def get_solicitud_by_id(id: int, service: SolicitudService = Depends(get_service)):
    solicitud = await service.get_by_id(id)
    if not solicitud.__dict__['id']:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud


@router.post('/get_multiSolicitudes')
async def get_solicitudes_by_ids(solicitudes: multiSolicitudes, service: SolicitudService = Depends(get_service)):
    return await service.get_multiSolicitudes_by_id(solicitudes.solicitudes)

@router.post("/", response_model=SolicitudOut, status_code=status.HTTP_201_CREATED)
async def create_solicitud(data: SolicitudCreate, service: SolicitudService = Depends(get_service)):
    solicitud = await service.store(data)
    if not solicitud:
        raise HTTPException(
            status_code=400, detail="Error al crear la solicitud")
    return solicitud

@router.post("/test", summary="Version test de crear solicitud, solamente solicita ids de direcciones en db", response_model=SolicitudOut, status_code=status.HTTP_201_CREATED)
async def create_solicitud_test(data: SolicitudIn, service: SolicitudService = Depends(get_service)):
    solicitud = await service.store_test(data)
    if not solicitud:
        raise HTTPException(
            status_code=400, detail="Error al crear la solicitud")
    return solicitud
@router.post('/cancelar/{id}',summary="Cancelar una solicitud")
async def cancel_solicitud(id:int, service:SolicitudService = Depends(get_service)):
    result = await service.cancel_solicitud_by_id(id)
    if not result:
        raise HTTPException(
            status_code=400, detail="Error al cancelar la solicitud")
    return result

@router.post('/estado/{id}',summary="Cambiar estado solicitud")
async def change_status(id: int, status: SolicitudCambioEstado, service: SolicitudService = Depends(get_service)):
    """
    Endpoint para cambiar el estado de una solicitud.
    """
    try:
       
        solicitud = await service.change_status_solicitud(id, status)
        return {"message": "Estado actualizado correctamente", "solicitud": solicitud}
    except SolicitudCanceladaError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail="Error interno del servidor {ex}")



@router.put("/{id}", response_model=SolicitudOut)
async def update_solicitud(id: int, data: SolicitudUpdate, service: SolicitudService = Depends(get_service)):
    solicitud = await service.update(id, data)
    if not solicitud:
        raise HTTPException(
            status_code=404, detail="Solicitud no encontrada o error al actualizar")
    return solicitud


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_solicitud(id: int, service: SolicitudService = Depends(get_service)):
    success = await service.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
