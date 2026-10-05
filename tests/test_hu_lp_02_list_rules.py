def test_list_rules_by_warehouse(client):
    r = client.get("/api/replenishment-rules?warehouse_id=1")
    assert r.status_code == 200
    assert len(r.get_json()["results"]) == 2


def test_new_rule_appears_in_listing(client):
    body = {"warehouse_id": 2, "product_id": 3, "reorder_point": 30, "reorder_qty": 80}
    client.put("/api/replenishment-rules", json=body)
    results = client.get("/api/replenishment-rules?warehouse_id=2").get_json()["results"]
    assert results == [body]


def test_rule_for_unknown_product_returns_404(client):
    body = {"warehouse_id": 1, "product_id": 999, "reorder_point": 5, "reorder_qty": 10}
    assert client.put("/api/replenishment-rules", json=body).status_code == 404


def test_list_rules_invalid_warehouse_returns_400(client):
    assert client.get("/api/replenishment-rules?warehouse_id=x").status_code == 400