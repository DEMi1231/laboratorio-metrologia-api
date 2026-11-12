
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.orden_servicio import OrdenServicio


def crear(db: Session, datos):
    nueva_orden = OrdenServicio(
        cliente_id=datos.cliente_id,
        fecha_recepcion=datos.fecha_recepcion,
        estado="Pendiente"
    )

    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)

    return nueva_orden


def listar(db: Session):
    return db.scalars(
        select(OrdenServicio)
    ).all()


def obtener(db: Session, orden_id: int):
    return db.get(OrdenServicio, orden_id)
