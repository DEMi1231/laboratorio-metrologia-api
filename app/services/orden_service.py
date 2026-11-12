
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.repositories import orden_repository as repo


def crear_orden(db: Session, datos):
    cliente = db.get(Cliente, datos.cliente_id)

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="El cliente no existe"
        )

    if datos.fecha_recepcion > date.today():
        raise HTTPException(
            status_code=400,
            detail="La fecha de recepción no puede ser futura"
        )

    return repo.crear(db, datos)


def obtener_orden(db: Session, orden_id: int):
    orden = repo.obtener(db, orden_id)

    if orden is None:
        raise HTTPException(
            status_code=404,
            detail="Orden no encontrada"
        )

    return orden
