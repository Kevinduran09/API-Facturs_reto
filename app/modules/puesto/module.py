
from injector import Module, provider, singleton
from .repositories.puestoRepository import PuestoRepository
from .services.puestoService import PuestoService

class PuestoModule(Module):
    @singleton
    @provider
    def provide_repository(self) -> PuestoRepository:
        return PuestoRepository()

    @singleton
    @provider
    def provide_service(self, repository: PuestoRepository) -> PuestoService:
        return PuestoService(repository)
    