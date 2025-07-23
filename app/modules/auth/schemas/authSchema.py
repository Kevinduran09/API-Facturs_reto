
from pydantic import BaseModel

class loginSchema(BaseModel):
    username:str
    password:str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    current: dict
