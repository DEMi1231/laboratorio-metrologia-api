
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class MetrologoBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    correo: EmailStr
    activo: bool = True


class MetrologoCrear(MetrologoBase):
    pass


class MetrologoActualizar(MetrologoBase):
    pass


class MetrologoRespuesta(MetrologoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
