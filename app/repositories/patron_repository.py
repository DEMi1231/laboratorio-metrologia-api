
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patron import Patron


def crear(db: Session, datos):
    patron = Patron(**datos.model_dump())
    db.add(patron)
    db.commit()
    db.refresh(patron)
    return patron


def listar(db: Session):
    return db.scalars(select(Patron)).all()


def obtener(db: Session, patron_id: int):
    return db.get(Patron, patron_id)


def obtener_por_serie(db: Session, numero_serie: str):
    return db.scalar(
        select(Patron).where(
            Patron.numero_serie == numero_serie
        )
    )


def actualizar(db: Session, patron: Patron, datos):
    for campo, valor in datos.model_dump().items():
        setattr(patron, campo, valor)

    db.commit()
    db.refresh(patron)
    return patron
