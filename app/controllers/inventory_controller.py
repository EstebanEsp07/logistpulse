from flask import Blueprint, request

from ..services import inventory_service as svc
from ..services.errors import DomainError
from ..views.presenters import inventory_view

bp = Blueprint("inventory", __name__, url_prefix="/api")


@bp.get("/inventory")
def list_inventory():
    """HU-LP-01: GET /api/inventory?warehouse_id=N&sku=SKU"""
    warehouse_id = request.args.get("warehouse_id")
    if warehouse_id is not None:
        try:
            warehouse_id = int(warehouse_id)
        except ValueError:
            raise DomainError("warehouse_id debe ser entero", 400)
    items = svc.list_inventory(warehouse_id, request.args.get("sku"))
    return {"results": [inventory_view(i) for i in items]}
