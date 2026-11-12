
from datetime import date
from decimal import Decimal

from sqlalchemy import Integer, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Calibracion(Base):
    __tablename__ = "calibracion"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    orden_id: Mapped[int] = mapped_column(
        ForeignKey("orden_servicio.id"), nullable=False
    )

    equipo_id: Mapped[int] = mapped_column(
        ForeignKey("equipo.id"), nullable=False
    )

    metrologo_id: Mapped[int] = mapped_column(
        ForeignKey("metrologo.id"), nullable=False
    )

    fecha_calibracion: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    temperatura: Mapped[Decimal] = mapped_column(
        Numeric(6, 2), nullable=False
    )

    humedad: Mapped[Decimal] = mapped_column(
        Numeric(6, 2), nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(30), default="Registrada"
    )

    orden = relationship("OrdenServicio")
    equipo = relationship("Equipo")
    metrologo = relationship("Metrologo")

    patrones = relationship(
        "Patron",
        secondary="calibracion_patron"
    )

    puntos = relationship(
        "PuntoMedicion",
        back_populates="calibracion"
    )
