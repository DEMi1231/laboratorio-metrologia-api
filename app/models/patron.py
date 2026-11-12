
from datetime import date

from sqlalchemy import Integer, String, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Patron(Base):
    __tablename__ = "patron"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(String(150))
    numero_serie: Mapped[str] = mapped_column(
        String(100), unique=True
    )

    fecha_vencimiento: Mapped[date] = mapped_column(Date)

    vigente: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
