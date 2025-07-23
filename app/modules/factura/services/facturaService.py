from dotenv import load_dotenv
from fastapi import Depends
import httpx
import os

from app.modules.factura.middlewares.authFactusMiddleware import auth_factus_middleware
from ..repositories.facturaRepository import FacturaRepository
from ..models.facturaModel import Factura
from ..schemas.facturaSchema import FacturaSchema, FacturaOut, FacturaIn, FacturaUpdate
from typing import List, Optional


load_dotenv()

url_factus = os.getenv("URL_FACTUS")


class FacturaService:
    def __init__(self, repository: FacturaRepository):
        self.repository = repository

    async def get_all(self) -> List[FacturaOut]:
        """Obtener todos los facturas"""
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Optional[FacturaOut]:
        """Obtener un factura por ID"""
        return await self.repository.get_by_id(id)

    async def store(self, factura_schema: FacturaIn) -> Optional[FacturaOut]:
        """Crear un nuevo factura"""
        return await self.repository.store(factura_schema)

    async def update(self, id: int, factura_schema: FacturaUpdate) -> Optional[FacturaOut]:
        """Actualizar un factura existente"""
        factura = await self.repository.get_by_id(id)
        update_data = factura_schema.model_dump(exclude_unset=True)
        return await self.repository.update(factura, update_data)

    async def delete(self, id: int) -> bool:
        """Eliminar un factura"""
        return await self.repository.delete(id)

    async def get_by_email(self, email: str) -> Optional[FacturaOut]:
        """Obtener factura por email (ejemplo de método adicional)"""
        return await self.repository.get_by_email(email)

    async def get_rangos_enumeracion(self, credentials):
        """Obtener rangos de enumeración desde Factus"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url_factus}/v1/numbering-ranges?filter[id]&filter[document]&filter[resolution_number]&filter[technical_key]&filter[is_active]",
                                        headers={
                                            "Authorization": f"Bearer {credentials['access_token']}",
                                        }
                                        )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Error al obtener los rangos de enumeración"}

    async def emitir_y_guardar_factura(self, credentials, factura_data):
        """Emitir factura en Factus y guardar copia local"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{url_factus}/v1/bills/validate",
                headers={
                    "Authorization": f"Bearer {credentials['access_token']}",
                    "Content-Type": "application/json"
                },
                json=factura_data
            )
            if response.status_code in [200, 201]:
                data = response.json()
                # Extrae los datos relevantes para guardar localmente
                factura_local = {
                    "number": data["data"]["bill"]["number"],
                    "reference_code": data["data"]["bill"]["reference_code"],
                    "total": data["data"]["bill"]["total"],
                    "customer_name": data["data"]["customer"]["names"],
                }
                await self.repository.store(FacturaIn(**factura_local))
                return data
            else:
                return {
                    "error": "Error al emitir la factura",
                    "detalle": response.text
                }
