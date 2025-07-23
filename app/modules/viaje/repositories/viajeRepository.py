from datetime import date

from app.modules.empleado.models.empleadoModel import Empleado
from app.modules.solicitud.models.solicitudModel import Solicitud
from ..models.viajeModel import EstadoViajeEnum, Tripulacion, Viaje
from typing import List, Optional
from ..schemas.viajeSchema import ViajeIn, ViajeOut, ViajeSchema
from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.functions import Count


class ViajeRepository:

    async def get_all(self)-> List[ViajeOut]:
        """Obtener todos los viajes"""
        return await Viaje.all().prefetch_related(
            "tripulaciones__Empleado__puesto"
        ).annotate(
            TotalSolicitudes=Count("tripulaciones")
        ).filter(
            tripulaciones__Empleado__puesto__codigo='trp390'
        ).values(
            "id", "TotalSolicitudes",
            "tripulaciones__Empleado__nombre", "tripulaciones__Empleado__puesto__cargo","fechaViaje","estado"
        )
    async def get_by_id(self, id_viaje: int) -> Optional[ViajeOut]:
        return await Viaje.get(id=id_viaje)
    
    async def get_full_by_id(self, id_viaje: int) -> Optional[dict]:
        """Obtener viaje por ID con solicitudes, vehículo y encargado"""
        try:
            viaje = await Viaje.get(id=id_viaje).prefetch_related(
                "tripulaciones__Empleado__puesto",
                "solicitud_viaje__cliente",
                "solicitud_viaje__servicio",
                "solicitud_viaje__direccionOrigen",
                "solicitud_viaje__direccionDestino",
                "vehiculo"
            )

            # Buscar el encargado (empleado con puesto transportista)
            encargado = None
            for tripulacion in viaje.tripulaciones:
                if tripulacion.Empleado.puesto and tripulacion.Empleado.puesto.codigo == "trp390":
                    encargado = {
                        "id": tripulacion.Empleado.id,
                        "nombre": tripulacion.Empleado.nombre,
                        "cargo": tripulacion.Empleado.puesto.cargo
                    }
                    break

            # Mapear las solicitudes
            solicitudes = []
            for solicitud in await viaje.solicitud_viaje.order_by('fecha').prefetch_related(
                "cliente", "servicio", "direccionOrigen", "direccionDestino"
            ):
                solicitudes.append({
                    "id": solicitud.id,
                    "cliente_nombre": solicitud.cliente.nombre if solicitud.cliente else None,
                    "tipo_servicio": solicitud.servicio.tipoServicio if solicitud.servicio else None,
                    "lat_origen": solicitud.direccionOrigen.lat if solicitud.direccionOrigen else None,
                    "lon_origen": solicitud.direccionOrigen.lon if solicitud.direccionOrigen else None,
                    "lat_destino": solicitud.direccionDestino.lat if solicitud.direccionDestino else None,
                    "lon_destino": solicitud.direccionDestino.lon if solicitud.direccionDestino else None,
                    "estado_solicitud": solicitud.estado if solicitud.estado else None,
                })

            return {
                "id": viaje.id,
                "fechaViaje": viaje.fechaViaje,
                "estado": viaje.estado,
                "vehiculo": {
                    "tipoVehiculo": viaje.vehiculo.tipoVehiculo if viaje.vehiculo else None,
                    "placa": viaje.vehiculo.placa if viaje.vehiculo else None,
                    "color": viaje.vehiculo.color if viaje.vehiculo else None
                },
                "encargado": encargado,
                "solicitudes": solicitudes
            }

        except DoesNotExist:
            print(f"Viaje with id {id_viaje} does not exist.")
            return None
        except Exception as e:
            print(f"Error fetching full viaje by id: {e}")
            return None

    async def store(self, viaje_data: ViajeIn) -> ViajeSchema:
        """Crear nuevo viaje"""
        
        
        try:
     
            viaje = await Viaje.create(**viaje_data.model_dump(exclude={'selectedRequests', 'tripulaciones'}), estado=EstadoViajeEnum.pendiente,vehiculo_id=viaje_data.vehicleId)
            
            # Aginar viaje a solicitudes
            await Solicitud.filter(id__in=viaje_data.selectedRequests).update(viaje=viaje, estado="en proceso")
            
            # Asignar tripulaciones al viaje
            tripulacion_viaje = [await Tripulacion.create(Viaje_id=viaje.id,Empleado_id=emp_id) for emp_id in viaje_data.employeeIds]
            
            #Guardar registros de la tripulacion
            await Tripulacion.bulk_create(tripulacion_viaje)
            return viaje
        except IntegrityError as e:
            print(f"IntegrityError while creating viaje: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error creating viaje: {e}")
            return None




    async def update(self, viaje: Viaje, update_data: dict) :
        """Actualizar viaje existente"""
        try:
            for field, value in update_data.items():
                setattr(viaje, field, value)
            await viaje.save(update_fields=list(update_data.keys()))
            return viaje
        except DoesNotExist:
            print(f"Viaje with id {viaje.id} does not exist.")
            return None
        except IntegrityError as e:
            print(f"IntegrityError while updating viaje: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error updating viaje: {e}")
            return None

    async def delete(self, id_viaje: int) -> bool:
        """Eliminar viaje por ID"""
        try:
            deleted_count = await Viaje.filter(id=id_viaje).delete()
            return deleted_count > 0
        except Exception as e:
            print(f"Error deleting viaje: {e}")
            return False

    async def get_available_employees(self, fecha: date) -> List[Viaje]:
        """
        Obtener empleados disponibles para asignar a un viaje.
        """
        try:
            unavailable_employees = await Tripulacion.filter(
                Viaje__fechaViaje=fecha
            ).values_list('Empleado_id', flat=True)
         
            available_employees = await Empleado.exclude(
                id__in=unavailable_employees
            ).exclude(
                puesto__codigo="adm23"
            ).values(
                "id", "nombre", "puesto__cargo"
            )
           
            return available_employees
        except DoesNotExist:
            print(f"Fecha {fecha} does not exist.")
            return []
        except IntegrityError as e:
            print(f"IntegrityError while fetching available employees: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error fetching available employees: {e}")
            return []
