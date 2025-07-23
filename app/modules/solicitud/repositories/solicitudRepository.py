from datetime import datetime
from app.modules.cliente.models.clienteModel import Cliente
from app.modules.servicio.models.servicioModel import Servicio
from helpers.calculate_duration import caltculateDurationAndDistance
from helpers.formatearTiempo import formatear_tiempo
from ..models.solicitudModel import Solicitud
from typing import List, Optional
from ..schemas.solicitudSchema import SolicitudCreate, SolicitudOut, SolicitudIn
from tortoise.exceptions import DoesNotExist, IntegrityError
from ...direccion.models.direccionModel import Direccion
from tortoise.transactions import in_transaction


class SolicitudRepository:

    async def get_all(self):
        """
        Obtener todas las solicitudes.
        """
        solicitudes = await Solicitud.all().select_related('cliente', "servicio", "direccionOrigen", "direccionDestino")
        print(f'solicitudes: {solicitudes}')
        return solicitudes

    async def get_by_id(self, id_solicitud: int)->SolicitudOut:
        """
        Obtener una solicitud por su ID.
        """
        try:
            solicitud = await Solicitud.get(id=id_solicitud).select_related('cliente', "servicio", "direccionOrigen", "direccionDestino")
            print(solicitud.__dict__)
            return solicitud
        except DoesNotExist:
            print(f"Solicitud with id {id_solicitud} does not exist.")
            return None
        except Exception as e:
            print(f"Error fetching solicitud by id: {e}")
            return None

    async def get_by_ids(self, idsList: List[int]):
        """
        Obtener lista de solicitudes por id
        """
        print(f'lista en repositorio: {idsList} ')
        # Orden ascendente por fecha
        solicitudes = await Solicitud.filter(id__in=idsList).order_by('fecha').select_related('cliente', "servicio", "direccionOrigen", "direccionDestino")
        return solicitudes

    async def store_test(self, solicitud: SolicitudIn):
        """
        Crear una nueva solicitud desde swagger o pra pruebas, solamente utiliza id's de direcciones existentes
        """
        solicitud_data = solicitud.model_dump(
            exclude={'direccionOrigen', 'direccionDestino', 'servicio', 'cliente'})

        try:

            if solicitud.direccionOrigen:
                dic_origen = await Direccion.get(id=solicitud.direccionOrigen)

            if solicitud.direccionDestino:
                dic_des = await Direccion.get(id-solicitud.direccionDestino)
            servicio = await Servicio.get(idServicio=solicitud.servicio)
            cliente = await Cliente.get(id=solicitud.cliente)

            solicitud = await Solicitud.create(**solicitud_data,
                                               direccionOrigen=dic_origen,
                                               direccionDestino=dic_des,
                                               cliente=cliente,
                                               servicio=servicio
                                               )
            print(solicitud.__dict__)
            return solicitud
        except IntegrityError as e:
            print(f"IntegrityError while creating solicitud: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error creating solicitud: {e}")
            return None

    async def store(self, solicitud: SolicitudCreate):
        """
        Crear una nueva solicitud.
        """
        solicitud_data = solicitud.model_dump(
            exclude={'direccionOrigen', 'direccionDestino', 'servicio', 'cliente'})

        try:

            dic_origen = None
            dic_des = None
            if solicitud.direccionOrigen:
                dic_origen = await Direccion.create(**solicitud.direccionOrigen.model_dump())

            if solicitud.direccionDestino:
                dic_des = await Direccion.create(**solicitud.direccionDestino.model_dump())

            servicio = await Servicio.get(idServicio=solicitud.servicio)

            cliente = await Cliente.get(id=solicitud.cliente)

            solicitud = await Solicitud.create(**solicitud_data,
                                               direccionOrigen=dic_origen,
                                               direccionDestino=dic_des,
                                               cliente=cliente,
                                               servicio=servicio
                                               )

            origen_coord, destino_coord = (
                dic_origen.lat, dic_origen.lon), (dic_des.lat, dic_des.lon)
            try:
                duration_solicitud_info = await caltculateDurationAndDistance(origen_coord, destino_coord)
                print(duration_solicitud_info)
                solicitud.kilometros = duration_solicitud_info['distancia_km']
                solicitud.tiempo_estimado = formatear_tiempo(
                    duration_solicitud_info["tiempo_estimado"])
                await solicitud.save()
            except Exception as e:
                print(f"Error obteniendo distancia y duración: {e}")
            return solicitud

        except IntegrityError as e:
            print(f"IntegrityError while creating solicitud: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error creating solicitud: {e}")
            return None

    async def update(self, solicitud: Solicitud, update_data: dict) -> SolicitudOut:
        """
        Actualizar una solicitud existente.
        """
        try:
            for field, value in update_data.items():
                setattr(solicitud, field, value)
            await solicitud.save(update_fields=list(update_data.keys()))
            return solicitud
        except DoesNotExist:
            print(f"Solicitud with id {solicitud.idSolicitud} does not exist.")
            return None
        except IntegrityError as e:
            print(f"IntegrityError while updating solicitud: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error updating solicitud: {e}")
            return None

    async def delete(self, id_solicitud: int) -> bool:
        """
        Eliminar una solicitud por su ID.
        """
        deleted_count = await Solicitud.filter(idSolicitud=id_solicitud).delete()
        return deleted_count > 0

    async def cancel_solicitud_by_id(self, id: int):
        """
        Cancelar Solicitud por id
        """
        try:
            solicitud = await self.get_by_id(id)
            solicitud.estado = 'cancelado'
            await solicitud.save(update_fields=["estado"])
            return solicitud
        except Exception as ex:
            print('Error cancel solicitud: {ex}')

    async def change_status_solicitud(self, id: int, status: str):
        """
        Cambiar el estado de una solicitud.
        """
        try:
            solicitud = await self.get_by_id(id)
            if not solicitud:
                raise DoesNotExist(f"Solicitud con ID {id} no encontrada.")

            if solicitud.estado == 'cancelado':
                raise SolicitudCanceladaError()

            solicitud.estado = status
            await solicitud.save(update_fields=["estado"])
            return solicitud
        except SolicitudCanceladaError as ex:
            print(f"Error: {ex}")
            raise
        except Exception as ex:
            print(f"Error cambiando el estado de la solicitud: {ex}")
            raise

    async def get_details_to_billing(self, id: int):
        """
        Obtener solo los datos básicos del cliente y del servicio para facturación.
        """
        try:
            print(f"ID de la solicitud: {id}")
            async with in_transaction() as conn:
                solicitud = await Solicitud.get(id=id).select_related('cliente', "servicio")
                if not solicitud:
                    raise DoesNotExist(f"Solicitud con ID {id} no encontrada.")

                details = {
                    "cliente": {
                        "nombre": solicitud.cliente.nombre,
                        "identificacion": solicitud.cliente.cedula,
                        "telefonoMovil": solicitud.cliente.telefonoMovil,
                        "correoElectronico": solicitud.cliente.correoElectronico,
                    },
                    "servicio": {
                        "tipoServicio": solicitud.servicio.tipoServicio,
                        "precioKilometro": solicitud.servicio.precioKilometro,
                    }
                }
                print(f"details: {details}")
                return details
        except DoesNotExist:
            print(f"Solicitud with id {id} does not exist.")
            return None
        except Exception as e:
            print(f"Error fetching details for billing: {e}")
            return None

    async def get_by_date(self, date_str: datetime):
        """
        Obtener solicitudes por fecha.
        """
        try:

            start_datetime = datetime.combine(date_str, datetime.min.time())
            end_datetime = datetime.combine(date_str, datetime.max.time())

            solicitudes = await Solicitud.filter(
                fecha__gte=start_datetime,
                fecha__lte=end_datetime
            ).select_related('cliente', "servicio", "direccionOrigen", "direccionDestino")

            return solicitudes
        except Exception as e:
            print(f"Error fetching solicitudes by date: {e}")
            return []

    

class SolicitudCanceladaError(Exception):
    """Excepción personalizada para solicitudes canceladas."""

    def __init__(self, message="No se puede cambiar el estado de una solicitud cancelada."):
        self.message = message
        super().__init__(self.message)

