
from datetime import date
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class OrdenCrear(BaseModel):
    cliente_id: int = Field(gt=0)
    fecha_recepcion: date


class OrdenActualizar(BaseModel):
    estado: Literal["Pendiente", "En proceso", "Finalizada"]


class OrdenRespuesta(BaseModel):
    id: int
    cliente_id: int
    fecha_recepcion: date
    estado: str

    model_config = ConfigDict(from_attributes=True)
