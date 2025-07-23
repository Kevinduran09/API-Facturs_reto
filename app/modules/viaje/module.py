
from injector import Module, provider, singleton
from .repositories.viajeRepository import ViajeRepository
from .services.viajeService import ViajeService

class ViajeModule(Module):
    @singleton
    @provider
    def provide_repository(self) -> ViajeRepository:
        return ViajeRepository()

    @singleton
    @provider
    def provide_service(self, repository: ViajeRepository) -> ViajeService:
        return ViajeService(repository)
    