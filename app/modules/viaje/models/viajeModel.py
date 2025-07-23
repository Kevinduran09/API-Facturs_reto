
from enum import Enum
from tortoise.models import Model
from tortoise import fields

from app.modules.solicitud.models.solicitudModel import Solicitud


class EstadoViajeEnum(str, Enum):
    pendiente = "pendiente"
    en_proceso = "en proceso"
    cancelado = "cancelado"
    realizado = "realizado"
    completado = "completado"

class Tripulacion(Model):
    id = fields.IntField(pk=True)
    Empleado = fields.ForeignKeyField(
        "models.Empleado", related_name="tripulacion_empleado")
    Viaje = fields.ForeignKeyField(
        "models.Viaje", related_name="tripulaciones")

class Viaje(Model):
    id = fields.IntField(pk=True)
    fechaViaje = fields.DateField()
    vehiculo = fields.ForeignKeyField(
        "models.Vehiculo", related_name="viajes")
    estado = fields.CharEnumField(enum_type=EstadoViajeEnum,null=True,default=EstadoViajeEnum.pendiente)
    tripulaciones = fields.ReverseRelation["Tripulacion"]
    solicitudes = fields.ReverseRelation["Solicitud"]

