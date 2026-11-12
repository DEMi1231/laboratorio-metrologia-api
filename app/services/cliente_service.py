
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import cliente_repository as repo


def crear_cliente(db: Session, datos):
    if repo.obtener_por_correo(db, str(datos.correo)):
        raise HTTPException(409, "El correo ya está registrado")

    try:
        return repo.crear(db, datos)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "El correo ya está registrado")


def obtener_cliente(db: Session, cliente_id: int):
    cliente = repo.obtener(db, cliente_id)

    if cliente is None:
        raise HTTPException(404, "Cliente no encontrado")

    return cliente


def actualizar_cliente(db: Session, cliente_id: int, datos):
    cliente = obtener_cliente(db, cliente_id)

    existente = repo.obtener_por_correo(db, str(datos.correo))

    if existente and existente.id != cliente_id:
        raise HTTPException(409, "El correo ya está registrado")

    try:
        return repo.actualizar(db, cliente, datos)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "El correo ya está registrado")


def eliminar_cliente(db: Session, cliente_id: int):
    cliente = obtener_cliente(db, cliente_id)

    try:
        repo.eliminar(db, cliente)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            409,
            "El cliente tiene registros asociados y no puede eliminarse"
        )
