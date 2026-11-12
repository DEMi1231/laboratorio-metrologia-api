
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import metrologo_repository as repo


def crear_metrologo(db: Session, datos):
    if repo.obtener_por_correo(db, str(datos.correo)):
        raise HTTPException(409, "El correo ya está registrado")

    try:
        return repo.crear(db, datos)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "El correo ya está registrado")


def obtener_metrologo(db: Session, metrologo_id: int):
    metrologo = repo.obtener(db, metrologo_id)

    if metrologo is None:
        raise HTTPException(404, "Metrólogo no encontrado")

    return metrologo


def actualizar_metrologo(db: Session, metrologo_id: int, datos):
    metrologo = obtener_metrologo(db, metrologo_id)
    existente = repo.obtener_por_correo(db, str(datos.correo))

    if existente and existente.id != metrologo_id:
        raise HTTPException(409, "El correo ya está registrado")

    try:
        return repo.actualizar(db, metrologo, datos)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "El correo ya está registrado")


def desactivar_metrologo(db: Session, metrologo_id: int):
    metrologo = obtener_metrologo(db, metrologo_id)

    metrologo.activo = False
    db.commit()
    db.refresh(metrologo)

    return metrologo
