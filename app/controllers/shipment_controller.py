from flask import Blueprint

from ..services import shipment_service as svc
from ..views.presenters import shipment_view

bp = Blueprint("shipments", __name__, url_prefix="/api")


@bp.get("/shipments/<tracking_code>")
def get_shipment(tracking_code):
    """HU-LP-04: estado, ubicación e historial de un envío."""
    return shipment_view(svc.get_shipment(tracking_code))
