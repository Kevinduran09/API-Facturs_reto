
from ..repositories.solicitudRepository import SolicitudRepository
from typing import List, Optional
from ..schemas.solicitudSchema import *


class SolicitudService:
    def __init__(self, repository: SolicitudRepository):
        self.repository = repository

    async def get_all(self) -> List[SolicitudOut]:
        solicitudes= await self.repository.get_all()
        return solicitudes

    async def get_by_id(self, id: int) -> Optional[SolicitudOut]:
        return await self.repository.get_by_id(id)
    
    async def get_multiSolicitudes_by_id(self, idsList: List[int]) -> List[SolicitudOut]:
        print(f'listas : {idsList}')
        return await self.repository.get_by_ids(idsList)
    
    async def store(self, solicitud: SolicitudCreate) -> Optional[SolicitudOut]:
        return await self.repository.store(solicitud)
    
    async def store_test(self, solicitud: SolicitudIn) -> Optional[SolicitudOut]:
        return await self.repository.store_test(solicitud)

    async def update(self, id: int, solicitud_schema: SolicitudUpdate) -> Optional[SolicitudOut]:
        solicitud = await self.repository.get_by_id(id)
        update_data = solicitud_schema.model_dump(exclude_unset=True)
        return await self.repository.update(solicitud, update_data)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)

    async def cancel_solicitud_by_id(self,id:int):
        return await self.repository.cancel_solicitud_by_id(id)

    async def change_status_solicitud(self, id: int, status: str):
        return await self.repository.change_status_solicitud(id, status)

    async def get_by_date(self, date: datetime) -> List[SolicitudOut]:
        return await self.repository.get_by_date(date)

    async def get_details_to_billing(self,id:int):
        return await self.repository.get_details_to_billing(id)