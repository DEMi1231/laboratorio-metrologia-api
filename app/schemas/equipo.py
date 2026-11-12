
from pydantic import BaseModel, ConfigDict, Field


class EquipoBase(BaseModel):
    cliente_id: int = Field(gt=0)
    nombre: str = Field(min_length=2, max_length=150)
    marca: str = Field(min_length=1, max_length=100)
    modelo: str = Field(min_length=1, max_length=100)
    numero_serie: str = Field(min_length=1, max_length=100)
    intervalo: str = Field(min_length=1, max_length=100)


class EquipoCrear(EquipoBase):
    pass


class EquipoActualizar(EquipoBase):
    pass


class EquipoRespuesta(EquipoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
