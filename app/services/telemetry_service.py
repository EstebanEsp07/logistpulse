from ..extensions import db
from ..models import TelemetryReading
from .errors import DomainError

ALLOWED_METRICS = {"temperature", "humidity", "speed", "battery"}


def record_reading(device_id, metric, value, unit):
    """HU-LP-07: registra una lectura. La generación de incidentes (HU-LP-08) queda para el Sprint 2."""
    if not device_id or not isinstance(device_id, str):
        raise DomainError("device_id es obligatorio", 422)
    if metric not in ALLOWED_METRICS:
        raise DomainError(f"metric debe ser una de {sorted(ALLOWED_METRICS)}", 422)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DomainError("value debe ser numérico", 422)
    if not unit:
        raise DomainError("unit es obligatorio", 422)
    reading = TelemetryReading(device_id=device_id, metric=metric, value=float(value), unit=unit)
    db.session.add(reading)
    db.session.commit()
    return reading


def list_readings(device_id=None, metric=None, limit=20):
    """HU-LP-07: últimas lecturas (más recientes primero), con filtros opcionales."""
    if limit < 1 or limit > 100:
        raise DomainError("limit debe estar entre 1 y 100", 400)
    q = TelemetryReading.query
    if device_id:
        q = q.filter_by(device_id=device_id)
    if metric:
        q = q.filter_by(metric=metric)
    return q.order_by(TelemetryReading.id.desc()).limit(limit).all()