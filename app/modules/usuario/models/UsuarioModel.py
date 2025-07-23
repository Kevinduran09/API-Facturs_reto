
from tortoise.models import Model
from tortoise import fields
from tortoise.exceptions import ValidationError
from app.modules.cliente.models.clienteModel import Cliente
from app.modules.empleado.models.empleadoModel import Empleado


class Usuario(Model):
    id = fields.IntField(pk=True)
    nombreUsuario = fields.CharField(max_length=255)
    contrasena = fields.CharField(max_length=255)
    cliente = fields.ForeignKeyField(
        'models.Cliente', related_name="usuario", on_delete=fields.CASCADE, null=True)
    empleado = fields.ForeignKeyField(
        'models.Empleado', related_name="usuario", on_delete=fields.CASCADE,null=True)

    async def clean(self):
        # Validación: un Usuario no puede estar asignado a un Cliente y a un Empleado al mismo tiempo
        if self.cliente and self.empleado:
            raise ValidationError(
                "Un usuario no puede ser asignado a un cliente y a un empleado al mismo tiempo.")

        # Validación: un Usuario debe estar asignado a al menos uno, no a ninguno
        if not self.cliente and not self.empleado:
            raise ValidationError(
                "Un usuario debe estar asignado a un cliente o a un empleado, pero no a ninguno.")
