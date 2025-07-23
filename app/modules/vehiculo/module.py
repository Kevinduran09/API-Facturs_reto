
from injector import Module, provider, singleton
from .repositories.vehiculoRepository import VehiculoRepository
from .services.vehiculoService import VehiculoService

class VehiculoModule(Module):
    @singleton
    @provider
    def provide_repository(self) -> VehiculoRepository:
        return VehiculoRepository()

    @singleton
    @provider
    def provide_service(self, repository: VehiculoRepository) -> VehiculoService:
        return VehiculoService(repository)
    