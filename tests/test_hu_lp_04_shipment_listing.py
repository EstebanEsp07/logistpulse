def test_list_shipments_returns_seed_shipment(client):
    results = client.get("/api/shipments").get_json()["results"]
    assert [s["tracking_code"] for s in results] == ["LP-0001"]


def test_filter_by_status(client):
    in_transit = client.get("/api/shipments?status=IN_TRANSIT").get_json()["results"]
    delivered = client.get("/api/shipments?status=DELIVERED").get_json()["results"]
    assert len(in_transit) == 1 and delivered == []


def test_invalid_status_returns_400(client):
    assert client.get("/api/shipments?status=LOST").status_code == 400


def test_detail_endpoint_still_works(client):
    assert client.get("/api/shipments/LP-0001").status_code == 200
    