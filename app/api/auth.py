
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.usuario import Usuario
from app.core.security import (
    verificar_password,
    crear_token
)
from app.core.auth import usuario_actual
from app.schemas.usuario import (
    TokenRespuesta,
    UsuarioRespuesta
)


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post("/login", response_model=TokenRespuesta)
def login(
    datos: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.scalar(
        select(Usuario).where(
            Usuario.correo == datos.username
        )
    )

    if (
        usuario is None
        or not usuario.activo
        or not verificar_password(
            datos.password,
            usuario.password_hash
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    return {
        "access_token": crear_token(usuario.id),
        "token_type": "bearer"
    }


@router.get("/me", response_model=UsuarioRespuesta)
def perfil(
    usuario: Usuario = Depends(usuario_actual)
):
    return usuario
