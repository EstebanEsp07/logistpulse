from datetime import datetime, timezone

from ..extensions import db


class Shipment(db.Model):
    __tablename__ = "shipments"
    id = db.Column(db.Integer, primary_key=True)
    tracking_code = db.Column(db.String(30), unique=True, nullable=False)
    origin = db.Column(db.String(80), nullable=False)
    destination = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="CREATED")
    promised_date = db.Column(db.Date, nullable=False)
    events = db.relationship(
        "TrackingEvent", backref="shipment", order_by="TrackingEvent.occurred_at", cascade="all, delete-orphan"
    )


class TrackingEvent(db.Model):
    __tablename__ = "tracking_events"
    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey("shipments.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    occurred_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
