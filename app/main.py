
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import engine

# Importación de routers
from app.api.clientes import router as clientes_router
from app.api.calibraciones import router as calibraciones_router
from app.api.ordenes import router as ordenes_router
from app.api.equipos import router as equipos_router
from app.api.metrologos import router as metrologos_router
from app.api.patrones import router as patrones_router
from app.api.auth import router as auth_router


# Configuración de logs
logger = logging.getLogger(__name__)


# Inicialización de FastAPI
app = FastAPI(
    title="Laboratorio de Metrología",
    description="API para administrar calibraciones",
    version="1.0.0"
)


# Registro de routers
app.include_router(calibraciones_router)
app.include_router(clientes_router)
app.include_router(ordenes_router)
app.include_router(equipos_router)
app.include_router(metrologos_router)
app.include_router(patrones_router)
app.include_router(auth_router)


# Endpoint principal
@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido al Laboratorio de Metrología",
        "estado": "funcionando"
    }


# Verificar estado de FastAPI
@app.get("/health")
def verificar_estado():
    return {
        "status": "ok"
    }


# Diagnóstico de conexión MySQL
@app.get("/database-test")
def probar_conexion():
    try:
        with engine.connect() as conexion:
            resultado = conexion.execute(
                text("SELECT DATABASE()")
            )

            nombre = resultado.scalar()

        return {
            "estado": "conectado",
            "base_datos": nombre
        }

    except SQLAlchemyError:
        # Registra el error técnico en Railway.
        # No muestra credenciales al usuario.
        logger.exception(
            "Error de conexión MySQL"
        )

        raise HTTPException(
            status_code=503,
            detail="Error al conectar con MySQL"
        )


# Ruta del frontend
BASE_DIR = Path(__file__).resolve().parent.parent


# Mostrar panel web
@app.get("/panel", include_in_schema=False)
def mostrar_frontend():
    archivo = BASE_DIR / "frontend" / "index.html"

    if not archivo.is_file():
        raise HTTPException(
            status_code=404,
            detail="Frontend no encontrado"
        )

    return FileResponse(archivo)
