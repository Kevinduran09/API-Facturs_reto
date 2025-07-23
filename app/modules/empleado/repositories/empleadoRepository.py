from app.modules.usuario.models.UsuarioModel import Usuario
from app.modules.puesto.models.puestoModel import Puesto
from ..models.empleadoModel import Empleado
from tortoise.exceptions import DoesNotExist, IntegrityError
from ..schemas.empleadoSchema import EmpleadoSchema,EmpleadoIn,EmpleadoUpdate
from tortoise.transactions import in_transaction
class EmpleadoRepository:
    @classmethod
    async def get_all(cls):
        try:
            empleados = await Empleado.all().select_related("puesto", "usuario")
            return empleados
        except Exception as e:
            print(f"Error fetching all empleados: {e}")
            return []

    @classmethod
    async def get_by_id(cls, id: int):
        try:
           empleado = await Empleado.get(id=id).select_related("puesto",'usuario')
           return empleado
        except DoesNotExist:
            print(f"Empleado with id {id} does not exist.")
            return None
        except Exception as e:
            print(f"Error fetching empleado by id: {e}")
            return None

    @classmethod
    async def store(cls, empleado: EmpleadoIn):
      
        try:
            async with in_transaction():
                # 1. Extraer el ID del puesto y eliminarlo del dump
                puesto_id = empleado.puesto
                empleado_data = empleado.model_dump(exclude={'usuario', 'puesto'})

                # 2. Obtener el objeto Puesto
                puesto = await Puesto.get_or_none(id=puesto_id)
                if not puesto:
                    raise ValueError("El puesto especificado no existe")

                # 3. Crear el empleado con el objeto Puesto
                emp = await Empleado.create(
                    **empleado_data,
                    puesto=puesto  # Pasamos el objeto, no el ID
                )

                # 4. Crear usuario si existe
                if empleado.usuario:
                    usuario = await Usuario.create(
                        **empleado.usuario.model_dump(exclude={'empleado'}),
                        empleado=emp  # Pasamos el objeto Empleado
                    )

                return emp
        except IntegrityError as e:
            print(f"IntegrityError while storing empleado: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error storing empleado: {e}")
            return None

    @classmethod
    async def update(cls, empleado: Empleado,update_data:dict):
        try:
            for field, value in update_data.items():
                setattr(empleado,field,value)
            await empleado.save(update_fields=list(update_data.keys()))
            return empleado
        except DoesNotExist:
            print(f"Empleado with id {empleado.id} does not exist.")
            return None
        except IntegrityError as e:
            print(f"IntegrityError while updating empleado: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error updating empleado: {e}")
            return None

    @classmethod
    async def delete(cls, id: int):
        try:
            emp = await Empleado.get(id=id)
            await emp.delete()
            return True
        except DoesNotExist:
            print(f"Empleado with id {id} does not exist.")
            return False
        except Exception as e:
            print(f"Unexpected error deleting empleado: {e}")
            return False

    @classmethod
    async def get_by_email(cls, email: str):
        try:
            emp = await Empleado.get(email=email)
            return emp
        except DoesNotExist:
            print(f"Empleado with email {email} does not exist.")
            return None
        except Exception as e:
            print(f"Unexpected error fetching empleado by email: {e}")
            return None
