
from tortoise.models import Model
from tortoise import fields
from enum import Enum

class TrasmisionEnum(str,Enum):
    manual = "Manual"
    automatica = "Automática"
    semi_automatica = "Semi-automática"
    
class CombustibleEnum(str, Enum):
    gasolina = "Gasolina"
    diesel = "Diésel"
    electrico = "Eléctrico"
    hibrido = "Híbrido"
    
       
class Vehiculo(Model):
    id = fields.IntField(pk=True)
    tipoVehiculo = fields.CharField(max_length=40)
    placa = fields.CharField(max_length=20, unique=True)
    capacidad = fields.IntField()  
    modelo = fields.CharField(max_length=45)
    fechaCompra = fields.DateField()
    anoVehiculo = fields.IntField()  
    potencia = fields.IntField() 
    transmision = fields.CharField(max_length=20) 
    combustible = fields.CharField(max_length=20)  
    color = fields.CharField(max_length=30)
    numeroPuertas = fields.IntField() 
    kilometraje = fields.IntField(null=True)  
    fechaUltimoMantenimiento = fields.DateField(null=True)
    carnetCirculacion = fields.CharField(max_length=50, null=True)
    