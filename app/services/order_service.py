from ..extensions import db
from ..models import Order, OrderLine, StockLevel, Warehouse
from .errors import DomainError


def create_order(customer_name, warehouse_id, lines):
    """HU-LP-10: crea un pedido validando stock disponible y reservando unidades."""
    if not customer_name:
        raise DomainError("customer_name es obligatorio", 422)
    if not db.session.get(Warehouse, warehouse_id):
        raise DomainError("Almacén no encontrado", 404)
    if not lines:
        raise DomainError("El pedido requiere al menos una línea", 422)
    merged = {}
    for ln in lines:
        pid, qty = ln.get("product_id"), ln.get("quantity")
        if not isinstance(pid, int) or not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
            raise DomainError("Cada línea requiere product_id y quantity enteros positivos", 422)
        merged[pid] = merged.get(pid, 0) + qty
    stocks = {}
    for pid, qty in merged.items():
        stock = StockLevel.query.filter_by(warehouse_id=warehouse_id, product_id=pid).first()
        if not stock:
            raise DomainError(f"El producto {pid} no existe en el almacén", 404)
        if stock.available < qty:
            raise DomainError(f"Stock insuficiente para el producto {pid}", 409)
        stocks[pid] = stock
    order = Order(customer_name=customer_name, warehouse_id=warehouse_id)
    order.lines = [OrderLine(product_id=pid, quantity=qty) for pid, qty in merged.items()]
    for pid, qty in merged.items():
        stocks[pid].reserved += qty
    db.session.add(order)
    db.session.commit()
    return order
