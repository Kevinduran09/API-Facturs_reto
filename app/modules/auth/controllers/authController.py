
from datetime import timedelta
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from injector import Injector

from app.modules.auth.utils.authhelper import authenticate_user, create_access_token, es_admin, get_current_user
from ..services.authService import AuthService
from ..schemas.authSchema import LoginResponse,loginSchema
from ..module import AuthModule

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

injector = Injector([AuthModule()])

def get_service() -> AuthService:
    return injector.get(AuthService)


@router.post("/login", response_model=LoginResponse)
async def login(form_data: loginSchema, service: AuthService = Depends(get_service)):
    user = await authenticate_user(
        service, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={
            "sub": user.nombreUsuario,
            "iss":user.id
            },
        expires_delta=access_token_expires,
    )
    print(user.__dict__)
    current_user={
        "isClient": bool(user.cliente) and bool(user.cliente.nombre),
        "isAdmin": es_admin(user),
        "username": user.nombreUsuario,
        "iss": {
            "type": "emp" if user.cliente_id is None else "client",
            "iss": user.cliente_id if user.empleado_id is None else user.empleado_id
        }
    }
    return {"access_token": access_token, "token_type": "bearer", "current": current_user}


@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
