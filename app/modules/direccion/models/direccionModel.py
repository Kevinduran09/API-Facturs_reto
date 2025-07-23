from tortoise.models import Model
from tortoise import fields


class Direccion(Model):
    id =fields.IntField(pk=True)
    lat = fields.FloatField(null=False)
    lon = fields.FloatField(null=False)
    nombreDireccion = fields.CharField(max_length=40,null=False)
    pais = fields.CharField(max_length=20, null=False)
    estado = fields.CharField(max_length=20, null=False)
    ciudad = fields.CharField(max_length=20, null=False)
    distrito = fields.CharField(max_length=20, null=False)
