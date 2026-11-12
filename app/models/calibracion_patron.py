
from sqlalchemy import ForeignKey, Table, Column, Integer

from app.db.database import Base


calibracion_patron = Table(
    "calibracion_patron",
    Base.metadata,

    Column(
        "calibracion_id",
        Integer,
        ForeignKey("calibracion.id"),
        primary_key=True
    ),

    Column(
        "patron_id",
        Integer,
        ForeignKey("patron.id"),
        primary_key=True
    )
)
