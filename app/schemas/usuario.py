
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: Literal["admin", "metrologo"]
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"
