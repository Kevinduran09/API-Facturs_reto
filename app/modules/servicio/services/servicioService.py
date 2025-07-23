
from ..repositories.servicioRepository import ServicioRepository
from typing import List, Optional
from ..schemas.servicioSchema import *
class ServicioService:
    def __init__(self, repository: ServicioRepository):
        self.repository = repository
    
    async def get_all(self) -> List[ServicioOut]:
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Optional[ServicioOut]:
        return await self.repository.get_by_id(id)
    async def store(self,servicio:ServicioCreate)->Optional[ServicioOut]:
        return await self.repository.store(servicio)
    async def update(self, id:int,servicio_schema:ServicioUpdate) ->Optional[ServicioOut]:
        servicio = await self.repository.get_by_id(id)
        update_data = servicio_schema.model_dump(exclude_unset=True)
        return await self.repository.update(servicio,update_data)
    async def delete(self,id:int)->bool:
        return await self.repository.delete(id)