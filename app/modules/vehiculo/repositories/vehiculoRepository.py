from ..models.vehiculoModel import Vehiculo
from ..schemas.vehiculoSchema import VehiculoIn, VehiculoUpdate
from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.transactions import in_transaction


class VehiculoRepository:
    @classmethod
    async def get_all(cls):
        try:
            vehiculos = await Vehiculo.all()
            return vehiculos
        except Exception as e:
            print(f"Error fetching all vehiculos: {e}")
            return []

    @classmethod
    async def get_by_id(cls, id: int):
        try:
            vehiculo = await Vehiculo.get(id=id)
            return vehiculo
        except DoesNotExist:
            print(f"Vehiculo with id {id} does not exist.")
            return None
        except Exception as e:
            print(f"Error fetching vehiculo by id: {e}")
            return None

    @classmethod
    async def store(cls, vehiculo: VehiculoIn):
        try:
            async with in_transaction():
                vehiculo_data = vehiculo.model_dump()
                nuevo_vehiculo = await Vehiculo.create(**vehiculo_data)
                return nuevo_vehiculo
        except IntegrityError as e:
            print(f"IntegrityError while storing vehiculo: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error storing vehiculo: {e}")
            return None

    @classmethod
    async def update(cls, vehiculo: Vehiculo, update_data: dict):
        try:
            for field, value in update_data.items():
                setattr(vehiculo, field, value)
            await vehiculo.save(update_fields=list(update_data.keys()))
            return vehiculo
        except DoesNotExist:
            print(f"Vehiculo with id {vehiculo.id} does not exist.")
            return None
        except IntegrityError as e:
            print(f"IntegrityError while updating vehiculo: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error updating vehiculo: {e}")
            return None

    @classmethod
    async def delete(cls, id: int):
        try:
            vehiculo = await Vehiculo.get(id=id)
            await vehiculo.delete()
            return True
        except DoesNotExist:
            print(f"Vehiculo with id {id} does not exist.")
            return False
        except Exception as e:
            print(f"Unexpected error deleting vehiculo: {e}")
            return False

    @classmethod
    async def get_by_placa(cls, placa: str):
        try:
            vehiculo = await Vehiculo.get(placa=placa)
            return vehiculo
        except DoesNotExist:
            print(f"Vehiculo with placa {placa} does not exist.")
            return None
        except Exception as e:
            print(f"Unexpected error fetching vehiculo by placa: {e}")
            return None
