from flask import Blueprint, request

from ..services import telemetry_service as svc
from ..views.presenters import telemetry_view

bp = Blueprint("telemetry", __name__, url_prefix="/api")


@bp.post("/telemetry")
def record_reading():
    """HU-LP-07: POST /api/telemetry {device_id, metric, value, unit}"""
    data = request.get_json(silent=True) or {}
    reading = svc.record_reading(data.get("device_id"), data.get("metric"), data.get("value"), data.get("unit"))
    return telemetry_view(reading), 201
