
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import usuario_actual, requerir_admin
from app.db.database import get_db
from app.repositories import cliente_repository as repo
from app.services import cliente_service as servicio
from app.schemas.cliente import (
    ClienteCrear,
    ClienteActualizar,
    ClienteRespuesta
)


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


# Registrar cliente - Solo administrador
@router.post(
    "/",
    response_model=ClienteRespuesta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requerir_admin)]
)
def crear_cliente(
    datos: ClienteCrear,
    db: Session = Depends(get_db)
):
    return servicio.crear_cliente(db, datos)


# Listar clientes - Usuario autenticado
@router.get(
    "/",
    response_model=list[ClienteRespuesta],
    dependencies=[Depends(usuario_actual)]
)
def listar_clientes(
    db: Session = Depends(get_db)
):
    return repo.listar(db)


# Obtener cliente - Usuario autenticado
@router.get(
    "/{cliente_id}",
    response_model=ClienteRespuesta,
    dependencies=[Depends(usuario_actual)]
)
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    return servicio.obtener_cliente(db, cliente_id)


# Actualizar cliente - Solo administrador
@router.put(
    "/{cliente_id}",
    response_model=ClienteRespuesta,
    dependencies=[Depends(requerir_admin)]
)
def actualizar_cliente(
    cliente_id: int,
    datos: ClienteActualizar,
    db: Session = Depends(get_db)
):
    return servicio.actualizar_cliente(db, cliente_id, datos)


# Eliminar cliente - Solo administrador
@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(requerir_admin)]
)
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    servicio.eliminar_cliente(db, cliente_id)
