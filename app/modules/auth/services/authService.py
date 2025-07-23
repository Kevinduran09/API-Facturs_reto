
from app.modules.auth.schemas.authSchema import loginSchema
from ..repositories.authRepository import AuthRepository

class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository
    
    async def get_all(self):
        return await self.repository.get_all()
    
    async def login(self,credentials:loginSchema):
        return await self.repository.login(credentials)
    async def geUserByUsername(self,username:str):
        return await self.repository.getUser(username)