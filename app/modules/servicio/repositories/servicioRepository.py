
from ..models.servicioModel import Servicio
from typing import List, Optional
from ..schemas.servicioSchema import ServicioCreate,ServicioOut
from tortoise.exceptions import DoesNotExist, IntegrityError

class ServicioRepository:

    async def get_all(self) -> List[Servicio]:
        return await Servicio.all()

    async def get_by_id(self, id_servicio: int) -> Optional[Servicio]:
       try:
           servicio = await Servicio.get(id=id_servicio)
           return servicio
       except DoesNotExist:
           print(f"Servicio with id {id} does not exist.")
           return None
       except Exception as e:
           print(f"Error fetching servicio by id: {e}")
           return None

    async def store(self, servicio_data: ServicioCreate) -> ServicioOut:
        return await Servicio.create(**servicio_data.model_dump())

    async def update(self, servicio: Servicio,update_data:dict) -> ServicioOut:
        try:
            for field, value in update_data.items():
                setattr(servicio, field, value)
            await servicio.save(update_fields=list(update_data.keys()))
            return servicio
        except DoesNotExist:
            print(f"Servicio with id {servicio.id} does not exist.")
            return None
        except IntegrityError as e:
            print(f"IntegrityError while updating servicio: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error updating servicio: {e}")
            return None

    async def delete(self, id_servicio: int) -> bool:
        deleted_count = await Servicio.filter(idServicio=id_servicio).delete()
        return deleted_count > 0
