from flask import Blueprint, request

from ..services import shipment_service as svc
from ..views.presenters import shipment_view

bp = Blueprint("shipments", __name__, url_prefix="/api")


@bp.get("/shipments/<tracking_code>")
def get_shipment(tracking_code):
    """HU-LP-04: estado, ubicación e historial de un envío."""
    return shipment_view(svc.get_shipment(tracking_code))


@bp.get("/shipments")
def list_shipments():
    """HU-LP-04: GET /api/shipments?status=IN_TRANSIT"""
    shipments = svc.list_shipments(request.args.get("status"))
    return {
        "results": [
            {
                "tracking_code": s.tracking_code,
                "status": s.status,
                "destination": s.destination,
                "promised_date": s.promised_date.isoformat(),
            }
            for s in shipments
        ]
    }