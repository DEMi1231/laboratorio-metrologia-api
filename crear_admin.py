
from getpass import getpass

from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.usuario import Usuario
from app.core.security import encriptar_password


def main():
    nombre = input("Nombre: ").strip()
    correo = input("Correo: ").strip().lower()
    password = getpass("Contraseña: ")

    if not nombre or not correo or len(password) < 12:
        print("Datos inválidos. Usa una contraseña de al menos 12 caracteres.")
        return

    with SessionLocal() as db:
        existente = db.scalar(
            select(Usuario).where(Usuario.correo == correo)
        )

        if existente:
            print("El usuario ya existe.")
            return

        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            password_hash=encriptar_password(password),
            rol="admin",
            activo=True
        )

        db.add(usuario)
        db.commit()

        print("Administrador creado correctamente.")


if __name__ == "__main__":
    main()
