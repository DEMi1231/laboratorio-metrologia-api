
from datetime import date

from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class OrdenServicio(Base):
    __tablename__ = "orden_servicio"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("cliente.id"), nullable=False
    )

    fecha_recepcion: Mapped[date] = mapped_column(Date)

    estado: Mapped[str] = mapped_column(
        String(30), default="Pendiente"
    )

    cliente = relationship("Cliente")
