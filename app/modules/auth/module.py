
from injector import Module, provider, singleton
from .repositories.authRepository import AuthRepository
from .services.authService import AuthService

class AuthModule(Module):
    @singleton
    @provider
    def provide_repository(self) -> AuthRepository:
        return AuthRepository()

    @singleton
    @provider
    def provide_service(self, repository: AuthRepository) -> AuthService:
        return AuthService(repository)
    