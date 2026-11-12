
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClienteBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    correo: EmailStr
    telefono: str | None = Field(default=None, max_length=20)
    direccion: str | None = Field(default=None, max_length=255)


class ClienteCrear(ClienteBase):
    pass


class ClienteActualizar(ClienteBase):
    pass


class ClienteRespuesta(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
