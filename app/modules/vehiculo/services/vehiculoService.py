from ..repositories.vehiculoRepository import VehiculoRepository
from ..models.vehiculoModel import Vehiculo
from ..schemas.vehiculoSchema import VehiculoOut, VehiculoIn, VehiculoUpdate
from typing import List, Optional


class VehiculoService:
    def __init__(self, repository: VehiculoRepository):
        self.repository = repository

    async def get_all(self) -> List[VehiculoOut]:
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Optional[VehiculoOut]:
        return await self.repository.get_by_id(id)

    async def store(self, vehiculo_schema: VehiculoIn) -> Optional[VehiculoOut]:
        return await self.repository.store(vehiculo_schema)

    async def update(self, id: int, vehiculo_schema: VehiculoUpdate) -> Optional[VehiculoOut]:
        vehiculo = await self.repository.get_by_id(id)
        if not vehiculo:
            return None
        update_data = vehiculo_schema.model_dump(exclude_unset=True)
        return await self.repository.update(vehiculo, update_data)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)

    async def get_by_placa(self, placa: str) -> Optional[VehiculoOut]:
        return await self.repository.get_by_placa(placa)
