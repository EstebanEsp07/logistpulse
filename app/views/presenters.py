"""Vista (representación JSON): convierte entidades del Modelo en respuestas."""


def inventory_view(item):
    s = item["stock"]
    return {
        "warehouse_id": s.warehouse_id,
        "sku": s.product.sku,
        "product": s.product.name,
        "quantity": s.quantity,
        "reserved": s.reserved,
        "available": s.available,
        "reorder_point": item["reorder_point"],
        "below_reorder_point": item["below_reorder_point"],
    }


def rule_view(r):
    return {
        "warehouse_id": r.warehouse_id,
        "product_id": r.product_id,
        "reorder_point": r.reorder_point,
        "reorder_qty": r.reorder_qty,
    }


def shipment_view(s):
    return {
        "tracking_code": s.tracking_code,
        "origin": s.origin,
        "destination": s.destination,
        "status": s.status,
        "promised_date": s.promised_date.isoformat(),
        "events": [
            {"status": e.status, "location": e.location, "occurred_at": e.occurred_at.isoformat()}
            for e in s.events
        ],
    }


def telemetry_view(t):
    return {"id": t.id, "device_id": t.device_id, "metric": t.metric, "value": t.value, "unit": t.unit}


def order_view(o):
    return {
        "id": o.id,
        "customer_name": o.customer_name,
        "warehouse_id": o.warehouse_id,
        "status": o.status,
        "lines": [{"product_id": ln.product_id, "quantity": ln.quantity} for ln in o.lines],
    }
