from datetime import date, timedelta
from app.modules.solicitud.repositories.solicitudRepository import SolicitudRepository
from app.modules.solicitud.services.solicitudService import SolicitudService
from helpers.calculate_duration import caltculateDurationAndDistance
from ..repositories.viajeRepository import ViajeRepository
from ..schemas.viajeSchema import ViajeOut, ViajeIn, ViajeSchema, ViajeUpdate
from typing import List, Optional


class ViajeService:
    def __init__(self, repository: ViajeRepository):
        self.repository = repository

    async def get_all(self)-> List[ViajeOut]:
        """Obtener todos los viajes"""
        return await self.repository.get_all()

    async def get_full_by_id(self, id: int) -> Optional[dict]:
        """Obtener un viaje por ID"""
        return await self.repository.get_full_by_id(id)

    async def store(self, viaje_schema: ViajeIn) -> Optional[ViajeSchema]:
        """Crear un nuevo viaje"""
        return await self.repository.store(viaje_schema)

    async def update(self, id: int, viaje_schema: ViajeUpdate) :
        """Actualizar un viaje existente"""
        viaje = await self.repository.get_by_id(id)
        update_data = viaje_schema.model_dump(exclude_unset=True)
        return await self.repository.update(viaje, update_data)

    async def delete(self, id: int) -> bool:
        """Eliminar un viaje"""
        return await self.repository.delete(id)

    async def get_by_email(self, email: str) -> Optional[ViajeOut]:
        """Obtener viaje por email (ejemplo de método adicional)"""
        return await self.repository.get_by_email(email)

    async def get_available_employees(self,fecha: date):
        """
        Obtener empleados disponibles para asignar a un viaje.
        """
        return await self.repository.get_available_employees(fecha)
    
    async def validate_availability(self, list_ids_solicitudes: List[int]):
        solicitud_service = SolicitudService(SolicitudRepository())
        solicitudes = await solicitud_service.get_multiSolicitudes_by_id(list_ids_solicitudes)

        resultado = []
        global total_alcanzadas
        total_alcanzadas = True
        global tiempo_finalizacion_estimado
        ultima_solicitud_alcanzable = None

        for i, solicitud in enumerate(solicitudes):

            fecha_inicio_actual = solicitud.fecha
           

            if i == 0:
                # Si es el primer viaje, no hay viajes anteriores para comparar
                resultado.append({
                    "id": solicitud.id,
                    "alcanzable": True,
                })
                # Obtenemos el tiempo estimado de finalizacion para la solicitud sumando la fecha de inicio y el tiempo estimado de llegada entre sus direcciones
                # ejemplo: 2023-10-01 12:00:00 + 30 minutos = 2023-10-01 12:30:00
                tiempo_finalizacion_estimado = fecha_inicio_actual + solicitud.tiempo_estimado
                # Guardamos la primera solicitud alcanzable
                ultima_solicitud_alcanzable = solicitud
                
                continue

            # Si la solicitud anterior fue descartada, compararemos con la última solicitud alcanzable
            if ultima_solicitud_alcanzable:
                origen_anterior = (ultima_solicitud_alcanzable.direccionDestino.lat,
                                ultima_solicitud_alcanzable.direccionDestino.lon)
            else:
                # En caso de que no haya solicitud alcanzable previa, seguimos con la primera
                origen_anterior = (solicitudes[i-1].direccionDestino.lat,
                                solicitudes[i-1].direccionDestino.lon)

            destino_actual = (solicitud.direccionOrigen.lat,
                            solicitud.direccionOrigen.lon)
          

            # Calculamos la duración y distancia entre el destino anterior y el origen actual
            distancia = await caltculateDurationAndDistance(origen_anterior, destino_actual)
         

            # Tiempo estimado entre rutas al tiempo estimado de la solicitud actual le sumamos el tiempo estimado de la distancia entre el destino del anterior y el origen del actual
            # ejemplo: 2023-10-01 12:00:00 + 30 minutos + 20 minutos = 2023-10-01 12:50:00
            tiempo_entre_rutas = tiempo_finalizacion_estimado + \
                timedelta(minutes=distancia["tiempo_estimado"])
           

            # Verificamos si hay suficiente tiempo para la solicitud actual
        
            if tiempo_entre_rutas > fecha_inicio_actual:
                total_alcanzadas = False
                resultado.append({
                    "id": solicitud.id,
                    "alcanzable": False,
                    "mensaje": "Se solapa o no hay tiempo suficiente entre solicitudes"
                })
               
            else:
                resultado.append({
                    "id": solicitud.id,
                    "alcanzable": True,
                    "mensaje": "Solicitud alcanzable"
                })
             
                # Actualizamos el tiempo de finalización estimado para la próxima solicitud
                tiempo_finalizacion_estimado = fecha_inicio_actual + solicitud.tiempo_estimado
               
                # Guardamos la solicitud alcanzable para la próxima comparación
                ultima_solicitud_alcanzable = solicitud

        return {
            "todas_alcanzables": total_alcanzadas,
            "solicitudes": resultado
        }

                
