
from injector import Module, provider, singleton
from .repositories.clienteRepository import ClienteRepository
from .services.clienteService import ClienteService

class ClienteModule(Module):
    @singleton
    @provider
    def provide_repository(self) -> ClienteRepository:
        return ClienteRepository()

    @singleton
    @provider
    def provide_service(self, repository: ClienteRepository) -> ClienteService:
        return ClienteService(repository)
    