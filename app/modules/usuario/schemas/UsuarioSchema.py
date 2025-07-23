
from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    nombreUsuario:str
    contrasena:str
    
    