from app.modules.usuario.models.UsuarioModel import Usuario
from ..models.clienteModel import Cliente
from ..schemas.clienteSchema import ClientIn, ClienteSchema,ClientResponse
from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.transactions import in_transaction
class ClienteRepository:
    async def get_all(self) -> list[ClientResponse]:
        return await Cliente.all().prefetch_related('usuario')

    async def get_by_id(self, id: int) -> ClientResponse | None:
        try:
            return await Cliente.get(id=id).prefetch_related('usuario')
        except DoesNotExist:
            return None

    async def store(self, cliente: ClientIn) -> ClientResponse | None:
        
        try:
           async with in_transaction():
            #    crear cliente
            client = await Cliente.create(
                **cliente.model_dump(exclude={'usuario'})
            )
            # crear usuario
            if cliente.usuario:
                usuario = await Usuario.create(**cliente.usuario.model_dump(exclude={'cliente'}),
                                               cliente=client)
            return client 
        except IntegrityError as e:
            # Imprime el error de integridad
            print(f"IntegrityError occurred: {e}")
            return None
        except Exception as e:
            # Imprime cualquier otro tipo de error
            print(f"An error occurred: {e}")
            return None

    async def update(self, cliente: Cliente,update_data:dict) -> ClientResponse | None:
        try:
            for field, value in update_data.items():
                setattr(cliente, field, value)
            await cliente.save(update_fields=list(update_data.keys()))
            return cliente
        except DoesNotExist:
            print(f"Cliente with id {cliente.id} does not exist.")
            return None
        except IntegrityError as e:
            print(f"IntegrityError while updating cliente: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error updating cliente: {e}")
            return None

    async def delete(self, id: int) -> bool:
        try:
            cliente = await Cliente.get(id=id)
            await cliente.delete()
            return True
        except DoesNotExist:
            return False

    async def get_by_email(self, email: str) -> ClientResponse | None:
        try:
            return await Cliente.get(email=email)
        except DoesNotExist:
            return None
