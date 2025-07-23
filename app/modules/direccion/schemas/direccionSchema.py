from pydantic import BaseModel

class DireccionSchema(BaseModel):
    lat: float
    lon: float
    nombreDireccion: str
    pais: str
    estado: str
    ciudad:str
    distrito:str
    class Config:
        from_attributes = True


class DireccionOut(DireccionSchema):
    id:int
