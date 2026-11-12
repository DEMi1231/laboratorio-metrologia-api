
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PuntoCrear(BaseModel):
    valor_nominal: Decimal
    lectura_patron: Decimal
    lectura_equipo: Decimal
    incertidumbre: Decimal = Field(ge=0)
    emp: Decimal = Field(gt=0)


class CalibracionCrear(BaseModel):
    orden_id: int = Field(gt=0)
    equipo_id: int = Field(gt=0)
    metrologo_id: int = Field(gt=0)

    fecha_calibracion: date

    temperatura: Decimal = Field(ge=-50, le=100)
    humedad: Decimal = Field(ge=0, le=100)

    patrones_ids: list[int] = Field(min_length=1)
    puntos: list[PuntoCrear] = Field(min_length=1)


class PuntoRespuesta(PuntoCrear):
    id: int
    error: Decimal
    dictamen: str

    model_config = ConfigDict(from_attributes=True)


class CalibracionRespuesta(BaseModel):
    id: int
    orden_id: int
    equipo_id: int
    metrologo_id: int
    fecha_calibracion: date
    temperatura: Decimal
    humedad: Decimal
    estado: str
    puntos: list[PuntoRespuesta]

    model_config = ConfigDict(from_attributes=True)
