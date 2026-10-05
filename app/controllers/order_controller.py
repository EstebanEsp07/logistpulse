from flask import Blueprint, request

from ..services import order_service as svc
from ..services.errors import DomainError
from ..views.presenters import order_view

bp = Blueprint("orders", __name__, url_prefix="/api")


@bp.post("/orders")
def create_order():
    data = request.get_json(silent=True) or {}
    customer_name = data.get("customer_name")
    warehouse_id = data.get("warehouse_id")
    lines = data.get("lines")

    if not customer_name or not warehouse_id or lines is None:
        raise DomainError("customer_name, warehouse_id y lines son obligatorios", 400)

    try:
        warehouse_id = int(warehouse_id)
    except ValueError:
        raise DomainError("warehouse_id debe ser entero", 400)

    if not isinstance(lines, list) or not all(isinstance(x, dict) for x in lines):
        raise DomainError("lines debe ser una lista de objetos", 422)

    return order_view(svc.create_order(customer_name, warehouse_id, lines)), 201


@bp.get("/orders/<int:order_id>")
def get_order(order_id):
    """HU-LP-10: GET /api/orders/<id>"""
    return order_view(svc.get_order(order_id))