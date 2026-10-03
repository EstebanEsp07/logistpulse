from datetime import datetime, timezone

from ..extensions import db


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="CREATED")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    lines = db.relationship("OrderLine", backref="order", cascade="all, delete-orphan")


class OrderLine(db.Model):
    __tablename__ = "order_lines"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
