from app.modules.factura.controllers.facturaController import router as factura_router
from app.modules.viaje.controllers.viajeController import router as viaje_router

from app.modules.puesto.controllers.puestoController import router as puesto_router
from app.modules.auth.controllers.authController import router as auth_router
from app.modules.solicitud.controllers.solicitudController import router as solicitud_router
from app.modules.servicio.controllers.servicioController import router as servicio_router
from app.modules.vehiculo.controllers.vehiculoController import router as vehiculo_router
from app.modules.usuario.controllers.UsuarioController import router as Usuario_router
from app.modules.cliente.controllers.clienteController import router as cliente_router
from app.modules.empleado.controllers.empleadoController import router as empleado_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicializando recursos...")
    await init_db()
    # for route in app.routes:
    #     print(f"method: {route.methods} - endpoint: {route.path} - name: {route.name}")
    yield  # Aquí la aplicación empieza a aceptar solicitudes
    print("Liberando recursos...")

app = FastAPI(
    lifespan=lifespan,
    title='API REMESAS YABI',
    description='API para la administración de los procesos de la empresa de Remesas Yabi. Gestión de clientes, empleados, vehiculos...',
    version='1.0.0', 
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


@app.get("/")
async def read_root():
    return {"message": "Aplicación en ejecución"}


app.include_router(empleado_router, prefix='/empleado', tags=['empleado'])

app.include_router(cliente_router, prefix='/cliente', tags=['cliente'])

app.include_router(Usuario_router, prefix='/usuario', tags=['Usuario'])

app.include_router(vehiculo_router, prefix='/vehiculo', tags=['vehiculo'])


app.include_router(servicio_router, prefix='/servicio', tags=['servicio'])

app.include_router(solicitud_router, prefix='/solicitud', tags=['solicitud'])

app.include_router(auth_router, prefix='/auth', tags=['auth'])

app.include_router(puesto_router, prefix='/puesto', tags=['puesto'])


app.include_router(viaje_router, prefix='/viaje', tags=['viaje'])

app.include_router(factura_router, prefix='/factura', tags=['factura'])
