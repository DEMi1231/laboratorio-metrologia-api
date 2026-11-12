
from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class PatronBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    numero_serie: str = Field(min_length=1, max_length=100)
    fecha_vencimiento: date
    vigente: bool = True


class PatronCrear(PatronBase):
    pass


class PatronActualizar(PatronBase):
    pass


class PatronRespuesta(PatronBase):
    id: int
    disponible: bool

    model_config = ConfigDict(from_attributes=True)
