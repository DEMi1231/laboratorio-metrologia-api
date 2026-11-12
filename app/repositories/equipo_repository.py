
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.equipo import Equipo


def crear(db: Session, datos):
    equipo = Equipo(**datos.model_dump())

    db.add(equipo)
    db.commit()
    db.refresh(equipo)

    return equipo


def listar(db: Session):
    return db.scalars(select(Equipo)).all()


def obtener(db: Session, equipo_id: int):
    return db.get(Equipo, equipo_id)


def actualizar(db: Session, equipo: Equipo, datos):
    for campo, valor in datos.model_dump().items():
        setattr(equipo, campo, valor)

    db.commit()
    db.refresh(equipo)

    return equipo


def eliminar(db: Session, equipo: Equipo):
    db.delete(equipo)
    db.commit()
