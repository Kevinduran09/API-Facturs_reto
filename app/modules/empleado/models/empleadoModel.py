
from tortoise.models import Model
from tortoise import fields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.usuario.models.UsuarioModel import Usuario
class Empleado(Model):
   id = fields.IntField(pk=True)
   nombre = fields.CharField(max_length=255)
   apellido = fields.CharField(max_length=255)
   cedula = fields.CharField(max_length=20, unique=True)
   correoElectronico = fields.CharField(max_length=255, unique=True)
   telefono = fields.CharField(max_length=20, null=True)
   direccion = fields.TextField(null=True)
   puesto = fields.ForeignKeyField("models.Puesto", related_name="empleados", on_delete=fields.CASCADE)
   fecha_Nacimiento = fields.DateField(null=True)
   fecha_contratacion = fields.DateField(null=True)
   usuario = fields.ReverseRelation["Usuario"]
