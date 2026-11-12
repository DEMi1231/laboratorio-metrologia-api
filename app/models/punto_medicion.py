
from decimal import Decimal

from sqlalchemy import Integer, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class PuntoMedicion(Base):
    __tablename__ = "punto_medicion"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    calibracion_id: Mapped[int] = mapped_column(
        ForeignKey("calibracion.id"), nullable=False
    )

    valor_nominal: Mapped[Decimal] = mapped_column(
        Numeric(14, 6), nullable=False
    )

    lectura_patron: Mapped[Decimal] = mapped_column(
        Numeric(14, 6), nullable=False
    )

    lectura_equipo: Mapped[Decimal] = mapped_column(
        Numeric(14, 6), nullable=False
    )

    error: Mapped[Decimal] = mapped_column(
        Numeric(14, 6), nullable=False
    )

    incertidumbre: Mapped[Decimal] = mapped_column(
        Numeric(14, 6), nullable=False
    )

    emp: Mapped[Decimal] = mapped_column(
        Numeric(14, 6), nullable=False
    )

    dictamen: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    calibracion = relationship(
        "Calibracion",
        back_populates="puntos"
    )
