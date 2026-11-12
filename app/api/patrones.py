
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import usuario_actual, requerir_admin
from app.db.database import get_db
from app.schemas.patron import (
    PatronCrear,
    PatronActualizar,
    PatronRespuesta
)
from app.services import patron_service as servicio


router = APIRouter(
    prefix="/patrones",
    tags=["Patrones"]
)


# Crear patrón - Solo administrador
@router.post(
    "/",
    response_model=PatronRespuesta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requerir_admin)]
)
def crear(
    datos: PatronCrear,
    db: Session = Depends(get_db)
):
    return servicio.crear_patron(db, datos)


# Listar patrones - Usuario autenticado
@router.get(
    "/",
    response_model=list[PatronRespuesta],
    dependencies=[Depends(usuario_actual)]
)
def listar(
    db: Session = Depends(get_db)
):
    return servicio.listar_patrones(db)


# Obtener patrón - Usuario autenticado
@router.get(
    "/{patron_id}",
    response_model=PatronRespuesta,
    dependencies=[Depends(usuario_actual)]
)
def obtener(
    patron_id: int,
    db: Session = Depends(get_db)
):
    return servicio.obtener_patron(db, patron_id)


# Actualizar patrón - Solo administrador
@router.put(
    "/{patron_id}",
    response_model=PatronRespuesta,
    dependencies=[Depends(requerir_admin)]
)
def actualizar(
    patron_id: int,
    datos: PatronActualizar,
    db: Session = Depends(get_db)
):
    return servicio.actualizar_patron(
        db, patron_id, datos
    )


# Desactivar patrón - Solo administrador
@router.patch(
    "/{patron_id}/desactivar",
    response_model=PatronRespuesta,
    dependencies=[Depends(requerir_admin)]
)
def desactivar(
    patron_id: int,
    db: Session = Depends(get_db)
):
    return servicio.desactivar_patron(
        db, patron_id
    )
