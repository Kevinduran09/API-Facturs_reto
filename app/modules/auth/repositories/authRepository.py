
from app.modules.auth.schemas.authSchema import loginSchema
from app.modules.usuario.models.UsuarioModel import Usuario
from tortoise.exceptions import DoesNotExist, IntegrityError


class AuthRepository:
    @classmethod
    async def login(cls, credentials: loginSchema):
        try:
            user = Usuario.get(
                nombreUsuario=credentials.nombreUsuario, contrasena=credentials.contrasena)

            if user:
                return user

        except DoesNotExist as ex:
            print(f'error user not exists: ${ex}')
            return None
        except Exception as ex:
            print(f'error login: ${ex}')
            return None

    @classmethod
    async def getUser(cls,username: str):
        try:
            user = await Usuario.get(
                nombreUsuario=username).prefetch_related('cliente', 'empleado__puesto')
            
            if user:
                return user

        except DoesNotExist as ex:
            print(f'error user not exists: ${ex}')
            return None
        except Exception as ex:
            print(f'error login: ${ex}')
            return None
