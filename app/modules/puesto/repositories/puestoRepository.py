from ..models.puestoModel import Puesto
from typing import List, Optional
from ..schemas.puestoSchema import PuestoCreate, PuestoOut
from tortoise.exceptions import DoesNotExist, IntegrityError

class PuestoRepository:

    async def get_all(self) -> List[Puesto]:
        """Obtener todos los puestos"""
        return await Puesto.all()

    async def get_by_id(self, id_puesto: int) -> Optional[Puesto]:
        """Obtener puesto por ID"""
        try:
            puesto = await Puesto.get(id=id_puesto)
            return puesto
        except DoesNotExist:
            print(f"Puesto with id {id_puesto} does not exist.")
            return None
        except Exception as e:
            print(f"Error fetching puesto by id: {e}")
            return None

    async def store(self, puesto_data: PuestoCreate) -> PuestoOut:
        """Crear nuevo puesto"""
        try:
            return await Puesto.create(**puesto_data.model_dump())
        except IntegrityError as e:
            print(f"IntegrityError while creating puesto: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error creating puesto: {e}")
            return None

    async def update(self, puesto: Puesto, update_data: dict) -> PuestoOut:
        """Actualizar puesto existente"""
        try:
            for field, value in update_data.items():
                setattr(puesto, field, value)
            await puesto.save(update_fields=list(update_data.keys()))
            return puesto
        except DoesNotExist:
            print(f"Puesto with id {puesto.id} does not exist.")
            return None
        except IntegrityError as e:
            print(f"IntegrityError while updating puesto: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error updating puesto: {e}")
            return None

    async def delete(self, id_puesto: int) -> bool:
        """Eliminar puesto por ID"""
        try:
            deleted_count = await Puesto.filter(id=id_puesto).delete()
            return deleted_count > 0
        except Exception as e:
            print(f"Error deleting puesto: {e}")
            return False
