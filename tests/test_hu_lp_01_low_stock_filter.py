def test_low_stock_returns_only_items_below_reorder_point(client):
    r = client.get("/api/inventory?warehouse_id=1&low_stock=true")
    skus = [i["sku"] for i in r.get_json()["results"]]
    assert skus == ["SKU-002"]


def test_low_stock_is_empty_when_all_items_are_healthy(client):
    r = client.get("/api/inventory?warehouse_id=2&low_stock=true")
    assert r.get_json()["results"] == []


def test_without_filter_returns_all_items(client):
    r = client.get("/api/inventory?warehouse_id=1")
    assert len(r.get_json()["results"]) == 2


def test_invalid_warehouse_id_returns_400(client):
    assert client.get("/api/inventory?warehouse_id=abc").status_code == 400