
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCrear, ClienteActualizar


def listar(db: Session):
    return db.scalars(select(Cliente)).all()


def obtener(db: Session, cliente_id: int):
    return db.get(Cliente, cliente_id)


def obtener_por_correo(db: Session, correo: str):
    return db.scalar(
        select(Cliente).where(Cliente.correo == correo)
    )


def crear(db: Session, datos: ClienteCrear):
    cliente = Cliente(**datos.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def actualizar(db: Session, cliente: Cliente, datos: ClienteActualizar):
    for campo, valor in datos.model_dump().items():
        setattr(cliente, campo, valor)

    db.commit()
    db.refresh(cliente)
    return cliente


def eliminar(db: Session, cliente: Cliente):
    db.delete(cliente)
    db.commit()
