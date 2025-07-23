
from injector import Module, provider, singleton
from .repositories.servicioRepository import ServicioRepository
from .services.servicioService import ServicioService

class ServicioModule(Module):
    @singleton
    @provider
    def provide_repository(self) -> ServicioRepository:
        return ServicioRepository()

    @singleton
    @provider
    def provide_service(self, repository: ServicioRepository) -> ServicioService:
        return ServicioService(repository)
    