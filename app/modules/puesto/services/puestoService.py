from ..repositories.puestoRepository import PuestoRepository
from ..models.puestoModel import Puesto
from ..schemas.puestoSchema import PuestoOut, PuestoCreate, PuestoUpdate
from typing import List, Optional


class PuestoService:
    def __init__(self, repository: PuestoRepository):
        self.repository = repository

    async def get_all(self) -> List[PuestoOut]:
        """Obtener todos los puestos"""
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Optional[PuestoOut]:
        """Obtener un puesto por ID"""
        return await self.repository.get_by_id(id)

    async def store(self, puesto_schema: PuestoCreate) -> Optional[PuestoOut]:
        """Crear un nuevo puesto"""
        return await self.repository.store(puesto_schema)

    async def update(self, id: int, puesto_schema: PuestoUpdate) -> Optional[PuestoOut]:
        """Actualizar un puesto existente"""
        puesto = await self.repository.get_by_id(id)
        update_data = puesto_schema.model_dump(exclude_unset=True)
        return await self.repository.update(puesto, update_data)

    async def delete(self, id: int) -> bool:
        """Eliminar un puesto"""
        return await self.repository.delete(id)

    async def get_by_email(self, email: str) -> Optional[PuestoOut]:
        """Obtener puesto por email (ejemplo de método adicional)"""
        return await self.repository.get_by_email(email)
