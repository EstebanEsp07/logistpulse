from ..extensions import db


class Warehouse(db.Model):
    __tablename__ = "warehouses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(60), nullable=False)


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(160), nullable=False)
    unit = db.Column(db.String(20), nullable=False, default="unidad")


class StockLevel(db.Model):
    __tablename__ = "stock_levels"
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    reserved = db.Column(db.Integer, nullable=False, default=0)
    product = db.relationship("Product")
    __table_args__ = (db.UniqueConstraint("warehouse_id", "product_id"),)

    @property
    def available(self):
        return self.quantity - self.reserved


class ReplenishmentRule(db.Model):
    __tablename__ = "replenishment_rules"
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    reorder_point = db.Column(db.Integer, nullable=False)
    reorder_qty = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint("warehouse_id", "product_id"),)
