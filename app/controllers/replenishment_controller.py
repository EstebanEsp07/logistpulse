from flask import Blueprint, request

from ..services import inventory_service as svc
from ..services.errors import DomainError
from ..views.presenters import rule_view

bp = Blueprint("replenishment", __name__, url_prefix="/api")


@bp.put("/replenishment-rules")
def upsert_rule():
    """HU-LP-02: PUT /api/replenishment-rules {warehouse_id, product_id, reorder_point, reorder_qty}"""
    data = request.get_json(silent=True) or {}
    try:
        warehouse_id, product_id = int(data["warehouse_id"]), int(data["product_id"])
        reorder_point, reorder_qty = data["reorder_point"], data["reorder_qty"]
    except (KeyError, TypeError, ValueError):
        raise DomainError("Campos obligatorios: warehouse_id, product_id, reorder_point, reorder_qty", 400)
    rule, created = svc.upsert_rule(warehouse_id, product_id, reorder_point, reorder_qty)
    return rule_view(rule), (201 if created else 200)
