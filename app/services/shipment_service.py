from ..models import Shipment
from .errors import DomainError


def get_shipment(tracking_code):
    """HU-LP-04: estado y ubicación de un envío por código de rastreo."""
    shipment = Shipment.query.filter_by(tracking_code=tracking_code).first()
    if not shipment:
        raise DomainError("Código de rastreo no encontrado", 404)
    return shipment
