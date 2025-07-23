
from tortoise.models import Model
from tortoise import fields


class Servicio(Model):
    idServicio = fields.IntField(pk=True)
    tipoServicio = fields.CharField(max_length=100)
    descripcionServicio = fields.TextField()
    precioKilometro = fields.FloatField()
    requiere_origen = fields.BooleanField(default=False)
    requiere_destino = fields.BooleanField(default=False)
