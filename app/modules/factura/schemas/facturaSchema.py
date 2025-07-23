from pydantic import BaseModel

class FacturaSchema(BaseModel):
    number: str
    reference_code: str
    total: str
    customer_name: str
    
class FacturaOut(FacturaSchema):
    id: int
    
class FacturaIn(FacturaSchema):
    pass
    
class FacturaUpdate(FacturaSchema):
    pass
    