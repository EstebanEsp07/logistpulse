from flask import Blueprint, request

from ..services import order_service as svc
from ..services.errors import DomainError
from ..views.presenters import order_view

bp = Blueprint("orders", __name__, url_prefix="/api")


@bp.post("/orders")
def create_order():
    """HU-LP-10: POST /api/orders {customer_name, warehouse_id, lines:[{product_id, quantity}]}"""
    data = request.get_json(silent=True) or {}
    try:
        warehouse_id = int(data["warehouse_id"])
    except (KeyError, TypeError, ValueError):
        raise DomainError("warehouse_id es obligatorio y debe ser entero", 400)
    lines = data.get("lines")
    if not isinstance(lines, list) or not all(isinstance(x, dict) for x in lines):
        raise DomainError("lines debe ser una lista de objetos", 422)
    return order_view(svc.create_order(data.get("customer_name"), warehouse_id, lines)), 201
