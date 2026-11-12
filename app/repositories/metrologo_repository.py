
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.metrologo import Metrologo


def crear(db: Session, datos):
    metrologo = Metrologo(**datos.model_dump())
    db.add(metrologo)
    db.commit()
    db.refresh(metrologo)
    return metrologo


def listar(db: Session):
    return db.scalars(select(Metrologo)).all()


def obtener(db: Session, metrologo_id: int):
    return db.get(Metrologo, metrologo_id)


def obtener_por_correo(db: Session, correo: str):
    return db.scalar(
        select(Metrologo).where(Metrologo.correo == correo)
    )


def actualizar(db: Session, metrologo, datos):
    for campo, valor in datos.model_dump().items():
        setattr(metrologo, campo, valor)

    db.commit()
    db.refresh(metrologo)
    return metrologo
