
from tortoise.models import Model
from tortoise import fields

class Puesto(Model):
    id = fields.IntField(pk=True)
    cargo = fields.CharField(max_length=255)
    salario = fields.DecimalField(max_digits=10, decimal_places=2)
    descripcion = fields.CharField(max_length=255)
    codigo = fields.CharField(max_length=25)
