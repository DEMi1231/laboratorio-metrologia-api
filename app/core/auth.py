
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.models.usuario import Usuario


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        usuario_id = int(payload["sub"])

    except (InvalidTokenError, KeyError, ValueError, TypeError):
        raise error

    usuario = db.get(Usuario, usuario_id)

    if usuario is None or not usuario.activo:
        raise error

    return usuario


def requerir_admin(
    usuario: Usuario = Depends(usuario_actual)
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403,
            detail="Se requieren permisos de administrador"
        )

    return usuario
