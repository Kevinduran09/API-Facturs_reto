
from fastapi import APIRouter, Depends
from injector import Injector
from ..services.UsuarioService import UsuarioService
from ..schemas.UsuarioSchema import UsuarioSchema
from ..module import UsuarioModule

router = APIRouter()

injector = Injector([UsuarioModule()])

def get_service() -> UsuarioService:
    return injector.get(UsuarioService)

@router.get("/")
async def get_all(service: UsuarioService = Depends(get_service)):
    return await service.get_all()
    