
from decimal import Decimal


def calcular_error(
    lectura_equipo: Decimal,
    lectura_patron: Decimal
) -> Decimal:
    return lectura_equipo - lectura_patron


def evaluar_conformidad(
    error: Decimal,
    incertidumbre: Decimal,
    emp: Decimal
) -> str:

    if abs(error) + incertidumbre <= emp:
        return "Aprobado"

    return "Rechazado"
