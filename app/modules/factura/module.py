
from injector import Module, provider, singleton
from .repositories.facturaRepository import FacturaRepository
from .services.facturaService import FacturaService

class FacturaModule(Module):
    @singleton
    @provider
    def provide_repository(self) -> FacturaRepository:
        return FacturaRepository()

    @singleton
    @provider
    def provide_service(self, repository: FacturaRepository) -> FacturaService:
        return FacturaService(repository)
    