
from injector import Module, provider, singleton
from .repositories.empleadoRepository import EmpleadoRepository
from .services.empleadoService import EmpleadoService

class EmpleadoModule(Module):
    @singleton
    @provider
    def provide_repository(self) -> EmpleadoRepository:
        return EmpleadoRepository()

    @singleton
    @provider
    def provide_service(self, repository: EmpleadoRepository) -> EmpleadoService:
        return EmpleadoService(repository)
    