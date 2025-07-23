def generate_service(name: str):
    """Genera un servicio completo con los mismos métodos que tu ejemplo"""
    service_template = f"""from ..repositories.{name.lower()}Repository import {name.capitalize()}Repository
from ..models.{name.lower()}Model import {name.capitalize()}
from ..schemas.{name.lower()}Schema import {name.capitalize()}Schema, {name.capitalize()}Out, {name.capitalize()}In, {name.capitalize()}Update
from typing import List, Optional


class {name.capitalize()}Service:
    def __init__(self, repository: {name.capitalize()}Repository):
        self.repository = repository

    async def get_all(self) -> List[{name.capitalize()}Out]:
        \"\"\"Obtener todos los {name.lower()}s\"\"\"
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Optional[{name.capitalize()}Out]:
        \"\"\"Obtener un {name.lower()} por ID\"\"\"
        return await self.repository.get_by_id(id)

    async def store(self, {name.lower()}_schema: {name.capitalize()}In) -> Optional[{name.capitalize()}Out]:
        \"\"\"Crear un nuevo {name.lower()}\"\"\"
        return await self.repository.store({name.lower()}_schema)

    async def update(self, id: int, {name.lower()}_schema: {name.capitalize()}Update) -> Optional[{name.capitalize()}Out]:
        \"\"\"Actualizar un {name.lower()} existente\"\"\"
        {name.lower()} = await self.repository.get_by_id(id)
        update_data = {name.lower()}_schema.model_dump(exclude_unset=True)
        return await self.repository.update({name.lower()}, update_data)

    async def delete(self, id: int) -> bool:
        \"\"\"Eliminar un {name.lower()}\"\"\"
        return await self.repository.delete(id)

    async def get_by_email(self, email: str) -> Optional[{name.capitalize()}Out]:
        \"\"\"Obtener {name.lower()} por email (ejemplo de método adicional)\"\"\"
        return await self.repository.get_by_email(email)
"""
    return service_template
