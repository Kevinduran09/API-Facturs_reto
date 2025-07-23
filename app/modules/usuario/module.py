
from injector import Module, provider, singleton
from .repositories.UsuarioRepository import UsuarioRepository
from .services.UsuarioService import UsuarioService

class UsuarioModule(Module):
    @singleton
    @provider
    def provide_repository(self) -> UsuarioRepository:
        return UsuarioRepository()

    @singleton
    @provider
    def provide_service(self, repository: UsuarioRepository) -> UsuarioService:
        return UsuarioService(repository)
    