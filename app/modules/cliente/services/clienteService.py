from ..repositories.clienteRepository import ClienteRepository
from ..schemas.clienteSchema import ClientIn, CLienteUpdate, ClientResponse
from ..models.clienteModel import Cliente


class ClienteService:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    async def get_all(self) -> list[ClientResponse]:
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> ClientResponse | None:
        return await self.repository.get_by_id(id)

    async def store(self, cliente: ClientIn) -> ClientResponse | None:
        return await self.repository.store(cliente)

    async def update(self, id: int, cliente_schema: CLienteUpdate) -> ClientResponse | None:
        cliente = await self.get_by_id(id)
        update_data = cliente_schema.model_dump(exclude_unset=True)
        return await self.repository.update(cliente, update_data)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)

    async def get_by_email(self, email: str) -> ClientResponse | None:
        return await self.repository.get_by_email(email)
