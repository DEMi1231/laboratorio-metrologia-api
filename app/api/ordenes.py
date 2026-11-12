
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import usuario_actual, requerir_admin
from app.db.database import get_db
from app.schemas.orden_servicio import (
    OrdenCrear,
    OrdenRespuesta
)
from app.repositories import orden_repository as repo
from app.services import orden_service as servicio


router = APIRouter(
    prefix="/ordenes",
    tags=["Órdenes de Servicio"]
)


# Crear orden - Solo administrador
@router.post(
    "/",
    response_model=OrdenRespuesta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requerir_admin)]
)
def crear_orden(
    datos: OrdenCrear,
    db: Session = Depends(get_db)
):
    return servicio.crear_orden(db, datos)


# Listar órdenes - Usuario autenticado
@router.get(
    "/",
    response_model=list[OrdenRespuesta],
    dependencies=[Depends(usuario_actual)]
)
def listar_ordenes(
    db: Session = Depends(get_db)
):
    return repo.listar(db)


# Consultar orden - Usuario autenticado
@router.get(
    "/{orden_id}",
    response_model=OrdenRespuesta,
    dependencies=[Depends(usuario_actual)]
)
def obtener_orden(
    orden_id: int,
    db: Session = Depends(get_db)
):
    return servicio.obtener_orden(db, orden_id)
