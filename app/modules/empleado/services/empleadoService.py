
from ..repositories.empleadoRepository import EmpleadoRepository
from ..models.empleadoModel import Empleado
from ..schemas.empleadoSchema import EmpleadoSchema, EmpleadoOut, EmpleadoIn, EmpleadoUpdate
from typing import List, Optional


class EmpleadoService:
    def __init__(self, repository: EmpleadoRepository):
        self.repository = repository

    async def get_all(self) -> List[EmpleadoOut]:
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Optional[EmpleadoOut]:
        return await self.repository.get_by_id(id)

    async def store(self, empleado_schema: EmpleadoIn) -> Optional[EmpleadoOut]:

        return await self.repository.store(empleado_schema)

    async def update(self, id: int, empleado_schema: EmpleadoUpdate) -> Optional[EmpleadoOut]:
        empleado = await self.repository.get_by_id(id)
        update_data = empleado_schema.model_dump(exclude_unset=True)
        return await self.repository.update(empleado, update_data)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)

    async def get_by_email(self, email: str) -> Optional[EmpleadoOut]:
        return await self.repository.get_by_email(email)
