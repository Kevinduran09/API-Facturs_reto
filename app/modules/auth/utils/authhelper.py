import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from injector import Injector
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.modules.auth.module import AuthModule
from app.modules.auth.services.authService import AuthService
load_dotenv()

load_dotenv()
injector = Injector([AuthModule()])


def get_service() -> AuthService:
    return injector.get(AuthService)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(db: AuthService, username: str, password: str):
    user = await db.geUserByUsername(username)
    if not user or not verify_password(password, user.contrasena):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    print(to_encode)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv("ALGORITHM"))


async def get_current_user(db: AuthService = Depends(get_service), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[
                             os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = await db.geUserByUsername(username)
        if user is None:
            raise credentials_exception
        return user.__dict__
    except JWTError:
        raise credentials_exception


def es_admin(user):
    try:
        return user.empleado.puesto.cargo == "Administrador"
    except AttributeError:
        return False
