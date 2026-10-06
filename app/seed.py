from datetime import date, datetime, timezone

from .extensions import db
from .models import Product, ReplenishmentRule, Shipment, StockLevel, TrackingEvent, Warehouse


def seed_if_empty():
    """Datos semilla ficticios para demostrar el esqueleto (sin datos reales)."""
    if Warehouse.query.first():
        return
    ts = lambda d, h: datetime(2026, 10, d, h, 0, tzinfo=timezone.utc)  # noqa: E731
    ship = Shipment(tracking_code="LP-0001", origin="Bodega Quito", destination="Tienda Cuenca",
                    status="IN_TRANSIT", promised_date=date(2026, 10, 12))
    ship.events = [
        TrackingEvent(status="CREATED", location="Bodega Quito", occurred_at=ts(8, 9)),
        TrackingEvent(status="DISPATCHED", location="Bodega Quito", occurred_at=ts(8, 15)),
        TrackingEvent(status="IN_TRANSIT", location="Ambato", occurred_at=ts(9, 11)),
    ]
    # Se insertan primero las entidades "padre" y se confirman con flush(): PostgreSQL
    # valida las claves foráneas y SQLAlchemy no ordena tablas que solo se relacionan
    # por ForeignKey (sin relationship()).
    db.session.add_all(
        [
            Warehouse(id=1, name="Bodega Quito", city="Quito"),
            Warehouse(id=2, name="Bodega Guayaquil", city="Guayaquil"),
            Product(id=1, sku="SKU-001", name="Caja térmica 20L"),
            Product(id=2, sku="SKU-002", name="Sensor de temperatura"),
            Product(id=3, sku="SKU-003", name="Pallet plástico"),
        ]
    )
    db.session.flush()
    db.session.add_all(
        [
            StockLevel(warehouse_id=1, product_id=1, quantity=120, reserved=10),
            StockLevel(warehouse_id=1, product_id=2, quantity=15, reserved=5),
            StockLevel(warehouse_id=2, product_id=3, quantity=60, reserved=0),
            ReplenishmentRule(warehouse_id=1, product_id=1, reorder_point=50, reorder_qty=100),
            ReplenishmentRule(warehouse_id=1, product_id=2, reorder_point=20, reorder_qty=40),
            ship,
        ]
    )
    db.session.commit()
