from datetime import timedelta, datetime


def formatear_tiempo(tiempo_estimado_min):
    tiempo_segundos = tiempo_estimado_min * 60
    return (datetime.min + timedelta(seconds=tiempo_segundos)).time()
