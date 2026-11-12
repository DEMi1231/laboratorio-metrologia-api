
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_endpoint_publico():
    respuesta = client.get("/health")
    assert respuesta.status_code == 200


def test_clientes_sin_token():
    respuesta = client.get("/clientes/")
    assert respuesta.status_code == 401


def test_calibraciones_sin_token():
    respuesta = client.get("/calibraciones/")
    assert respuesta.status_code == 401


def test_login_incorrecto():
    respuesta = client.post(
        "/auth/login",
        data={
            "username": "usuario_inexistente@ejemplo.com",
            "password": "incorrecta"
        }
    )
    assert respuesta.status_code == 401
