
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings


password_hash = PasswordHash.recommended()


def encriptar_password(password: str) -> str:
    return password_hash.hash(password)


def verificar_password(password: str, hash_guardado: str) -> bool:
    return password_hash.verify(password, hash_guardado)


def crear_token(usuario_id: int) -> str:
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )

    datos = {
        "sub": str(usuario_id),
        "exp": expiracion
    }

    return jwt.encode(
        datos,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
