from ..models.facturaModel import Factura
from typing import List, Optional
from ..schemas.facturaSchema import FacturaIn, FacturaOut
from tortoise.exceptions import DoesNotExist, IntegrityError

class FacturaRepository:

    async def get_all(self) -> List[Factura]:
        """Obtener todos los facturas"""
        return await Factura.all()

    async def get_by_id(self, id_factura: int) -> Optional[Factura]:
        """Obtener factura por ID"""
        try:
            factura = await Factura.get(id=id_factura)
            return factura
        except DoesNotExist:
            print(f"Factura with id {id_factura} does not exist.")
            return None
        except Exception as e:
            print(f"Error fetching factura by id: {e}")
            return None

    async def store(self, factura_data: FacturaIn) -> FacturaOut:
        """Crear nuevo factura"""
        try:
            return await Factura.create(**factura_data.model_dump())
        except IntegrityError as e:
            print(f"IntegrityError while creating factura: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error creating factura: {e}")
            return None

    async def update(self, factura: Factura, update_data: dict) -> FacturaOut:
        """Actualizar factura existente"""
        try:
            for field, value in update_data.items():
                setattr(factura, field, value)
            await factura.save(update_fields=list(update_data.keys()))
            return factura
        except DoesNotExist:
            print(f"Factura with id {factura.id} does not exist.")
            return None
        except IntegrityError as e:
            print(f"IntegrityError while updating factura: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error updating factura: {e}")
            return None

    async def delete(self, id_factura: int) -> bool:
        """Eliminar factura por ID"""
        try:
            deleted_count = await Factura.filter(id=id_factura).delete()
            return deleted_count > 0
        except Exception as e:
            print(f"Error deleting factura: {e}")
            return False
