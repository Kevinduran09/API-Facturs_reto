
from injector import Module, provider, singleton
from .repositories.solicitudRepository import SolicitudRepository
from .services.solicitudService import SolicitudService

class SolicitudModule(Module):
    @singleton
    @provider
    def provide_repository(self) -> SolicitudRepository:
        return SolicitudRepository()

    @singleton
    @provider
    def provide_service(self, repository: SolicitudRepository) -> SolicitudService:
        return SolicitudService(repository)
    