
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import usuario_actual, requerir_admin
from app.db.database import get_db
from app.schemas.metrologo import (
    MetrologoCrear,
    MetrologoActualizar,
    MetrologoRespuesta
)
from app.repositories import metrologo_repository as repo
from app.services import metrologo_service as servicio


router = APIRouter(
    prefix="/metrologos",
    tags=["Metrólogos"]
)


# Registrar metrólogo - Solo administrador
@router.post(
    "/",
    response_model=MetrologoRespuesta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requerir_admin)]
)
def crear(
    datos: MetrologoCrear,
    db: Session = Depends(get_db)
):
    return servicio.crear_metrologo(db, datos)


# Listar metrólogos - Usuario autenticado
@router.get(
    "/",
    response_model=list[MetrologoRespuesta],
    dependencies=[Depends(usuario_actual)]
)
def listar(
    db: Session = Depends(get_db)
):
    return repo.listar(db)


# Obtener metrólogo - Usuario autenticado
@router.get(
    "/{metrologo_id}",
    response_model=MetrologoRespuesta,
    dependencies=[Depends(usuario_actual)]
)
def obtener(
    metrologo_id: int,
    db: Session = Depends(get_db)
):
    return servicio.obtener_metrologo(db, metrologo_id)


# Actualizar metrólogo - Solo administrador
@router.put(
    "/{metrologo_id}",
    response_model=MetrologoRespuesta,
    dependencies=[Depends(requerir_admin)]
)
def actualizar(
    metrologo_id: int,
    datos: MetrologoActualizar,
    db: Session = Depends(get_db)
):
    return servicio.actualizar_metrologo(
        db, metrologo_id, datos
    )


# Desactivar metrólogo - Solo administrador
@router.patch(
    "/{metrologo_id}/desactivar",
    response_model=MetrologoRespuesta,
    dependencies=[Depends(requerir_admin)]
)
def desactivar(
    metrologo_id: int,
    db: Session = Depends(get_db)
):
    return servicio.desactivar_metrologo(
        db, metrologo_id
    )
