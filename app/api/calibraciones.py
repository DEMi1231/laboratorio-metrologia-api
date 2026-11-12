
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.core.auth import usuario_actual
from app.db.database import get_db
from app.models.calibracion import Calibracion
from app.schemas.calibracion import (
    CalibracionCrear,
    CalibracionRespuesta
)
from app.services.calibracion_service import (
    registrar_calibracion
)


router = APIRouter(
    prefix="/calibraciones",
    tags=["Calibraciones"],
    dependencies=[Depends(usuario_actual)]
)


# Registrar calibración - Usuario autenticado
@router.post(
    "/",
    response_model=CalibracionRespuesta,
    status_code=status.HTTP_201_CREATED
)
def crear_calibracion(
    datos: CalibracionCrear,
    db: Session = Depends(get_db)
):
    return registrar_calibracion(db, datos)


# Listar calibraciones - Usuario autenticado
@router.get(
    "/",
    response_model=list[CalibracionRespuesta]
)
def listar_calibraciones(
    db: Session = Depends(get_db)
):
    consulta = select(Calibracion).options(
        selectinload(Calibracion.puntos)
    )

    return db.scalars(consulta).all()
