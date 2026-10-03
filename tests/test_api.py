def test_health_returns_200(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok", "service": "logistpulse", "db": "up"}


def test_home_view_renders(client):
    assert b"LogistPulse" in client.get("/").data


# HU-LP-01
def test_inventory_lists_stock_and_flags_reorder(client):
    items = client.get("/api/inventory?warehouse_id=1").get_json()["results"]
    by_sku = {i["sku"]: i for i in items}
    assert by_sku["SKU-001"]["available"] == 110 and by_sku["SKU-001"]["below_reorder_point"] is False
    assert by_sku["SKU-002"]["available"] == 10 and by_sku["SKU-002"]["below_reorder_point"] is True


def test_inventory_filter_by_sku(client):
    items = client.get("/api/inventory?sku=SKU-003").get_json()["results"]
    assert len(items) == 1 and items[0]["warehouse_id"] == 2


# HU-LP-02
def test_rule_create_then_update(client):
    body = {"warehouse_id": 2, "product_id": 3, "reorder_point": 30, "reorder_qty": 80}
    assert client.put("/api/replenishment-rules", json=body).status_code == 201
    body["reorder_point"] = 35
    r = client.put("/api/replenishment-rules", json=body)
    assert r.status_code == 200 and r.get_json()["reorder_point"] == 35


def test_rule_rejects_non_positive_values(client):
    body = {"warehouse_id": 1, "product_id": 1, "reorder_point": 0, "reorder_qty": 10}
    assert client.put("/api/replenishment-rules", json=body).status_code == 422


# HU-LP-04
def test_shipment_tracking_found_and_missing(client):
    ok = client.get("/api/shipments/LP-0001").get_json()
    assert ok["status"] == "IN_TRANSIT" and len(ok["events"]) == 3
    assert client.get("/api/shipments/NOPE").status_code == 404


# HU-LP-07
def test_telemetry_accepts_valid_and_rejects_invalid(client):
    good = {"device_id": "TRK-01", "metric": "temperature", "value": 4.5, "unit": "C"}
    assert client.post("/api/telemetry", json=good).status_code == 201
    bad = dict(good, metric="color")
    assert client.post("/api/telemetry", json=bad).status_code == 422
    assert client.post("/api/telemetry", json=dict(good, value="caliente")).status_code == 422


# HU-LP-10
def test_order_reserves_stock_and_blocks_oversell(client):
    body = {"customer_name": "Tienda Demo", "warehouse_id": 1, "lines": [{"product_id": 1, "quantity": 100}]}
    r = client.post("/api/orders", json=body)
    assert r.status_code == 201 and r.get_json()["status"] == "CREATED"
    # disponible = 10 → otra de 100 debe fallar
    assert client.post("/api/orders", json=body).status_code == 409
    inv = client.get("/api/inventory?warehouse_id=1&sku=SKU-001").get_json()["results"][0]
    assert inv["reserved"] == 110 and inv["available"] == 10
