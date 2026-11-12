
from datetime import date

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import patron_repository as repo


def preparar_respuesta(patron):
    return {
        "id": patron.id,
        "nombre": patron.nombre,
        "numero_serie": patron.numero_serie,
        "fecha_vencimiento": patron.fecha_vencimiento,
        "vigente": patron.vigente,
        "disponible": (
            patron.vigente
            and patron.fecha_vencimiento >= date.today()
        )
    }


def listar_patrones(db: Session):
    return [preparar_respuesta(p) for p in repo.listar(db)]


def obtener_patron(db: Session, patron_id: int):
    patron = repo.obtener(db, patron_id)

    if patron is None:
        raise HTTPException(404, "Patrón no encontrado")

    return preparar_respuesta(patron)


def crear_patron(db: Session, datos):
    if repo.obtener_por_serie(db, datos.numero_serie):
        raise HTTPException(
            409, "El número de serie ya existe"
        )

    try:
        patron = repo.crear(db, datos)
        return preparar_respuesta(patron)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            409, "El número de serie ya existe"
        )


def actualizar_patron(db: Session, patron_id: int, datos):
    patron = repo.obtener(db, patron_id)

    if patron is None:
        raise HTTPException(404, "Patrón no encontrado")

    existente = repo.obtener_por_serie(
        db, datos.numero_serie
    )

    if existente and existente.id != patron_id:
        raise HTTPException(
            409, "El número de serie ya existe"
        )

    try:
        patron = repo.actualizar(db, patron, datos)
        return preparar_respuesta(patron)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            409, "El número de serie ya existe"
        )


def desactivar_patron(db: Session, patron_id: int):
    patron = repo.obtener(db, patron_id)

    if patron is None:
        raise HTTPException(404, "Patrón no encontrado")

    patron.vigente = False
    db.commit()
    db.refresh(patron)

    return preparar_respuesta(patron)
