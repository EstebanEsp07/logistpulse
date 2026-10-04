from flask import Blueprint, request

from ..services import telemetry_service as svc
from ..services.errors import DomainError
from ..views.presenters import telemetry_view

bp = Blueprint("telemetry", __name__, url_prefix="/api")


@bp.post("/telemetry")
def record_reading():
    """HU-LP-07: POST /api/telemetry {device_id, metric, value, unit}"""
    data = request.get_json(silent=True) or {}
    reading = svc.record_reading(data.get("device_id"), data.get("metric"), data.get("value"), data.get("unit"))
    return telemetry_view(reading), 201


@bp.get("/telemetry")
def list_readings():
    """HU-LP-07: GET /api/telemetry?device_id=&metric=&limit="""
    try:
        limit = int(request.args.get("limit", "20"))
    except ValueError:
        raise DomainError("limit debe ser entero", 400)
    readings = svc.list_readings(request.args.get("device_id"), request.args.get("metric"), limit)
    return {"results": [telemetry_view(r) for r in readings]}
