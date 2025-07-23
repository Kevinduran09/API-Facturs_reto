import asyncio
# Ajusta al nombre real del archivo
from helpers.calculate_duration import caltculateDurationAndDistance


async def main():
    # Coordenadas de ejemplo (San José, Costa Rica → Cartago, Costa Rica)
    origen = (9.9281, -84.0907)    # San José
    destino = (9.8644, -83.9194)   # Cartago

    resultado = await caltculateDurationAndDistance(origen, destino)
    print("Resultado del cálculo:", resultado)

if __name__ == "__main__":
    asyncio.run(main())
