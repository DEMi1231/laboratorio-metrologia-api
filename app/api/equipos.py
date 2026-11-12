
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import usuario_actual, requerir_admin
from app.db.database import get_db
from app.schemas.equipo import (
    EquipoCrear,
    EquipoActualizar,
    EquipoRespuesta
)
from app.repositories import equipo_repository as repo
from app.services import equipo_service as servicio


router = APIRouter(
    prefix="/equipos",
    tags=["Equipos"]
)


# Registrar equipo - Solo administrador
@router.post(
    "/",
    response_model=EquipoRespuesta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requerir_admin)]
)
def crear_equipo(
    datos: EquipoCrear,
    db: Session = Depends(get_db)
):
    return servicio.crear_equipo(db, datos)


# Listar equipos - Usuario autenticado
@router.get(
    "/",
    response_model=list[EquipoRespuesta],
    dependencies=[Depends(usuario_actual)]
)
def listar_equipos(
    db: Session = Depends(get_db)
):
    return repo.listar(db)


# Obtener equipo - Usuario autenticado
@router.get(
    "/{equipo_id}",
    response_model=EquipoRespuesta,
    dependencies=[Depends(usuario_actual)]
)
def obtener_equipo(
    equipo_id: int,
    db: Session = Depends(get_db)
):
    return servicio.obtener_equipo(db, equipo_id)


# Actualizar equipo - Solo administrador
@router.put(
    "/{equipo_id}",
    response_model=EquipoRespuesta,
    dependencies=[Depends(requerir_admin)]
)
def actualizar_equipo(
    equipo_id: int,
    datos: EquipoActualizar,
    db: Session = Depends(get_db)
):
    return servicio.actualizar_equipo(db, equipo_id, datos)


# Eliminar equipo - Solo administrador
@router.delete(
    "/{equipo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(requerir_admin)]
)
def eliminar_equipo(
    equipo_id: int,
    db: Session = Depends(get_db)
):
    servicio.eliminar_equipo(db, equipo_id)
