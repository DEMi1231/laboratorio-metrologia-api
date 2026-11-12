
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Equipo(Base):
    __tablename__ = "equipo"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("cliente.id"), nullable=False
    )

    nombre: Mapped[str] = mapped_column(String(150))
    marca: Mapped[str] = mapped_column(String(100))
    modelo: Mapped[str] = mapped_column(String(100))
    numero_serie: Mapped[str] = mapped_column(String(100))
    intervalo: Mapped[str] = mapped_column(String(100))

    cliente = relationship("Cliente")
