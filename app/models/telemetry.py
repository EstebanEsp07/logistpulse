from datetime import datetime, timezone

from ..extensions import db


class TelemetryReading(db.Model):
    __tablename__ = "telemetry_readings"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(60), nullable=False, index=True)
    metric = db.Column(db.String(40), nullable=False)  # temperature, humidity, ...
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    recorded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
