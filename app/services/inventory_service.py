from ..extensions import db
from ..models import Product, ReplenishmentRule, StockLevel, Warehouse
from .errors import DomainError


def list_inventory(warehouse_id=None, sku=None, low_stock=False):
    """HU-LP-01: existencias por almacén/producto con indicador de reposición."""
    q = StockLevel.query.join(Product)
    if warehouse_id is not None:
        q = q.filter(StockLevel.warehouse_id == warehouse_id)
    if sku:
        q = q.filter(Product.sku == sku)
    items = []
    for s in q.order_by(StockLevel.warehouse_id, Product.sku).all():
        rule = ReplenishmentRule.query.filter_by(warehouse_id=s.warehouse_id, product_id=s.product_id).first()
        items.append(
            {
                "stock": s,
                "reorder_point": rule.reorder_point if rule else None,
                "below_reorder_point": bool(rule and s.available <= rule.reorder_point),
            }
        )
    if low_stock:
        items = [i for i in items if i["below_reorder_point"]]
    return items


def upsert_rule(warehouse_id, product_id, reorder_point, reorder_qty):
    """HU-LP-02: crea o actualiza la regla de reposición de un producto en un almacén."""
    for name, value in (("reorder_point", reorder_point), ("reorder_qty", reorder_qty)):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise DomainError(f"{name} debe ser un entero positivo", 422)
    if not db.session.get(Warehouse, warehouse_id):
        raise DomainError("Almacén no encontrado", 404)
    if not db.session.get(Product, product_id):
        raise DomainError("Producto no encontrado", 404)
    rule = ReplenishmentRule.query.filter_by(warehouse_id=warehouse_id, product_id=product_id).first()
    created = rule is None
    if created:
        rule = ReplenishmentRule(warehouse_id=warehouse_id, product_id=product_id,
                                 reorder_point=reorder_point, reorder_qty=reorder_qty)
        db.session.add(rule)
    else:
        rule.reorder_point, rule.reorder_qty = reorder_point, reorder_qty
    db.session.commit()
    return rule, created
