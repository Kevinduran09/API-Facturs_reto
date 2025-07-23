
from enum import Enum
from tortoise.models import Model
from tortoise import fields


class EstadoSolicitudEnum(str, Enum):
    pendiente = "pendiente"
    en_proceso = "en proceso"
    cancelado = "cancelado"
    realizada = "realizada"
    aprobada = "aprobada"

class Solicitud(Model):
    id = fields.IntField(pk=True)
    cliente = fields.ForeignKeyField(
        'models.Cliente', related_name='cliente', on_delete=fields.CASCADE,null=False
    )
    servicio = fields.ForeignKeyField(
        "models.Servicio", related_name='servicio',on_delete=fields.CASCADE,null=False
    )
    direccionOrigen = fields.ForeignKeyField(
        'models.Direccion',related_name='solicitudes_origen',on_delete=fields.CASCADE,null=True
    )
    direccionDestino = fields.ForeignKeyField(
        'models.Direccion', related_name='solicitudes_destino', on_delete=fields.CASCADE, null=True
    )
    viaje = fields.ForeignKeyField('models.Viaje', related_name='solicitud_viaje', null=True)
    fecha = fields.DatetimeField()
    anotaciones = fields.TextField(null=True)
    estado = fields.CharEnumField(
        enum_type=EstadoSolicitudEnum, null=True, default=EstadoSolicitudEnum.pendiente)
    observacion = fields.TextField(null=True)
    horaSalida = fields.TimeField(null=True)
    horaLlegada = fields.TimeField(null=True)
    kilometros = fields.FloatField(null=True)
    tiempo_estimado = fields.TimeField(null=True)
    orden = fields.IntField(null=True)
    horaReal = fields.TimeField(null=True)
        