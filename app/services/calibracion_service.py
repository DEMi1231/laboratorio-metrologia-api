
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.models.equipo import Equipo
from app.models.metrologo import Metrologo
from app.models.orden_servicio import OrdenServicio
from app.models.patron import Patron
from app.models.calibracion import Calibracion
from app.models.punto_medicion import PuntoMedicion

from app.schemas.calibracion import CalibracionCrear
from app.services.calculos import (
    calcular_error,
    evaluar_conformidad
)


def registrar_calibracion(
    db: Session,
    datos: CalibracionCrear
):
    try:
        # Validar fecha
        if datos.fecha_calibracion > date.today():
            raise HTTPException(
                400, "La fecha no puede ser futura"
            )

        # Validar orden
        orden = db.get(OrdenServicio, datos.orden_id)

        if not orden:
            raise HTTPException(404, "Orden no encontrada")

        # Validar equipo
        equipo = db.get(Equipo, datos.equipo_id)

        if not equipo:
            raise HTTPException(404, "Equipo no encontrado")

        if equipo.cliente_id != orden.cliente_id:
            raise HTTPException(
                400,
                "El equipo no pertenece al cliente de la orden"
            )

        # Validar metrologo
        metrologo = db.get(
            Metrologo, datos.metrologo_id
        )

        if not metrologo:
            raise HTTPException(404, "Metrólogo no encontrado")

        if not metrologo.activo:
            raise HTTPException(
                400, "El metrólogo está inactivo"
            )

        # Evitar patrones duplicados
        if len(datos.patrones_ids) != len(
            set(datos.patrones_ids)
        ):
            raise HTTPException(
                400, "Hay patrones duplicados"
            )

        # Validar todos los patrones
        patrones = []

        for patron_id in datos.patrones_ids:
            patron = db.get(Patron, patron_id)

            if not patron:
                raise HTTPException(
                    404, f"Patrón {patron_id} no encontrado"
                )

            if (
                not patron.vigente
                or patron.fecha_vencimiento < date.today()
                or patron.fecha_vencimiento < datos.fecha_calibracion
            ):
                raise HTTPException(
                    400, f"Patrón {patron_id} no vigente"
                )

            patrones.append(patron)

        # Crear calibracion
        calibracion = Calibracion(
            orden_id=datos.orden_id,
            equipo_id=datos.equipo_id,
            metrologo_id=datos.metrologo_id,
            fecha_calibracion=datos.fecha_calibracion,
            temperatura=datos.temperatura,
            humedad=datos.humedad,
            estado="Registrada"
        )

        db.add(calibracion)
        db.flush()

        # Asociar patrones
        calibracion.patrones.extend(patrones)

        # Registrar puntos
        for punto in datos.puntos:

            error = calcular_error(
                punto.lectura_equipo,
                punto.lectura_patron
            )

            dictamen = evaluar_conformidad(
                error,
                punto.incertidumbre,
                punto.emp
            )

            nuevo_punto = PuntoMedicion(
                calibracion_id=calibracion.id,
                valor_nominal=punto.valor_nominal,
                lectura_patron=punto.lectura_patron,
                lectura_equipo=punto.lectura_equipo,
                error=error,
                incertidumbre=punto.incertidumbre,
                emp=punto.emp,
                dictamen=dictamen
            )

            db.add(nuevo_punto)

        # Confirmar toda la transaccion
        db.commit()
        db.refresh(calibracion)

        return calibracion

    except Exception:
        db.rollback()
        raise
