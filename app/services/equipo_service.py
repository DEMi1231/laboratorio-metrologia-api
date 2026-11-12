
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.repositories import equipo_repository as repo


def validar_cliente(db: Session, cliente_id: int):
    cliente = db.get(Cliente, cliente_id)

    if cliente is None:
        raise HTTPException(
            404, "El cliente no existe"
        )


def obtener_equipo(db: Session, equipo_id: int):
    equipo = repo.obtener(db, equipo_id)

    if equipo is None:
        raise HTTPException(
            404, "Equipo no encontrado"
        )

    return equipo


def crear_equipo(db: Session, datos):
    validar_cliente(db, datos.cliente_id)

    try:
        return repo.crear(db, datos)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            409, "No se pudo registrar el equipo"
        )


def actualizar_equipo(db: Session, equipo_id: int, datos):
    equipo = obtener_equipo(db, equipo_id)
    validar_cliente(db, datos.cliente_id)

    try:
        return repo.actualizar(db, equipo, datos)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            409, "No se pudo actualizar el equipo"
        )


def eliminar_equipo(db: Session, equipo_id: int):
    equipo = obtener_equipo(db, equipo_id)

    try:
        repo.eliminar(db, equipo)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            409,
            "El equipo tiene calibraciones asociadas"
        )
