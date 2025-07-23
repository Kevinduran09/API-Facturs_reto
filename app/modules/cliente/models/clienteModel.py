
from tortoise.models import Model
from tortoise import fields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.usuario.models.UsuarioModel import Usuario
class Cliente(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=60)
    apellido = fields.CharField(max_length=60)
    cedula = fields.CharField(max_length=20, unique=True)
    telefonoFijo = fields.CharField(max_length=20, null=True)
    telefonoMovil = fields.CharField(max_length=20, null=True)
    telefonoTrabajo = fields.CharField(max_length=20, null=True)
    correoElectronico = fields.CharField(max_length=80)
    fechaIngreso = fields.DatetimeField(auto_now_add=True)
    usuario = fields.ReverseRelation["Usuario"]


    