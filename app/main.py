from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import engine
from app.api.clientes import router as clientes_router
from app.api.calibraciones import router as calibraciones_router
from app.api.ordenes import router as ordenes_router
from app.api.equipos import router as equipos_router
from app.api.metrologos import router as metrologos_router
from app.api.patrones import router as patrones_router
from app.api.auth import router as auth_router
from pathlib import Path
from fastapi.responses import FileResponse

app = FastAPI(
    title="Laboratorio de Metrología",
    description="API para administrar calibraciones",
    version="1.0.0"
)

app.include_router(calibraciones_router)
app.include_router(clientes_router)
app.include_router(ordenes_router)
app.include_router(equipos_router)
app.include_router(metrologos_router)
app.include_router(patrones_router)
app.include_router(auth_router)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido al Laboratorio de Metrología",
        "estado": "funcionando"
    }

@app.get("/health")
def verificar_estado():
    return {
        "status": "ok"
    }


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
        raise HTTPException(
            status_code=503,
            detail="Error al conectar con MySQL"
        )

BASE_DIR = Path(__file__).resolve().parent.parent


@app.get("/panel", include_in_schema=False)
def mostrar_frontend():
    return FileResponse(
        BASE_DIR / "frontend" / "index.html"
    )
