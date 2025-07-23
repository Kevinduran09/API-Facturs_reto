
from ..repositories.UsuarioRepository import UsuarioRepository

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository
    
    async def get_all(self):
        return await self.repository.get_all()
    