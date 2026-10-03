from flask import Blueprint, render_template
from sqlalchemy import text

from ..extensions import db

bp = Blueprint("health", __name__)

ENDPOINTS = [
    {"method": "GET", "path": "/health", "story": "TEC", "desc": "estado del servicio y la BD"},
    {"method": "GET", "path": "/api/inventory?warehouse_id=N&sku=SKU", "story": "HU-LP-01", "desc": "existencias"},
    {"method": "PUT", "path": "/api/replenishment-rules", "story": "HU-LP-02", "desc": "regla de reposición"},
    {"method": "GET", "path": "/api/shipments/<tracking_code>", "story": "HU-LP-04", "desc": "rastreo de envío"},
    {"method": "POST", "path": "/api/telemetry", "story": "HU-LP-07", "desc": "registrar lectura"},
    {"method": "POST", "path": "/api/orders", "story": "HU-LP-10", "desc": "crear pedido validando stock"},
]


def _db_status():
    try:
        db.session.execute(text("SELECT 1"))
        return "up"
    except Exception:  # noqa: BLE001
        return "down"


@bp.get("/health")
def health():
    status = _db_status()
    code = 200 if status == "up" else 503
    return {"status": "ok" if code == 200 else "degraded", "service": "logistpulse", "db": status}, code


@bp.get("/")
def home():
    return render_template("home.html", service="logistpulse", db_status=_db_status(), endpoints=ENDPOINTS)
