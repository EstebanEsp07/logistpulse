def _order(client, lines, warehouse_id=1):
    return client.post("/api/orders",
                       json={"customer_name": "Tienda Demo", "warehouse_id": warehouse_id, "lines": lines})


def test_order_can_be_retrieved(client):
    created = _order(client, [{"product_id": 1, "quantity": 5}]).get_json()
    r = client.get(f"/api/orders/{created['id']}")
    assert r.status_code == 200 and r.get_json()["lines"] == [{"product_id": 1, "quantity": 5}]


def test_unknown_order_returns_404(client):
    assert client.get("/api/orders/999").status_code == 404


def test_duplicate_lines_are_merged(client):
    r = _order(client, [{"product_id": 1, "quantity": 5}, {"product_id": 1, "quantity": 5}])
    assert r.status_code == 201
    assert r.get_json()["lines"] == [{"product_id": 1, "quantity": 10}]


def test_order_with_invalid_quantity_is_rejected(client):
    assert _order(client, [{"product_id": 1, "quantity": 0}]).status_code == 422


def test_order_for_product_missing_in_warehouse_returns_404(client):
    assert _order(client, [{"product_id": 3, "quantity": 1}], warehouse_id=1).status_code == 404