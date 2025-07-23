
from ..models.UsuarioModel import Usuario

class UsuarioRepository:
    async def get_all(self):
        return await Usuario.all()
    