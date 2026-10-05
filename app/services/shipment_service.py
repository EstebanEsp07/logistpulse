from ..models import Shipment
from .errors import DomainError


def get_shipment(tracking_code):
    """HU-LP-04: recupera un envío por su código de rastreo."""
    shipment = Shipment.query.filter_by(tracking_code=tracking_code).first()
    if not shipment:
        raise DomainError("Código de rastreo no encontrado", 404)
    return shipment


VALID_STATUSES = {"CREATED", "DISPATCHED", "IN_TRANSIT", "DELIVERED"}


def list_shipments(status=None):
    """HU-LP-04: lista envíos, opcionalmente filtrados por estado."""
    if status is not None and status not in VALID_STATUSES:
        raise DomainError(f"status debe ser uno de {sorted(VALID_STATUSES)}", 400)
    q = Shipment.query
    if status:
        q = q.filter_by(status=status)
    return q.order_by(Shipment.promised_date, Shipment.tracking_code).all()