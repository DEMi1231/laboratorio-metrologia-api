
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    correo: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    telefono: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    direccion: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
