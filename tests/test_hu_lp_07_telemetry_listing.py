def _send(client, device="TRK-01", metric="temperature", value=4.0):
    return client.post("/api/telemetry",
                       json={"device_id": device, "metric": metric, "value": value, "unit": "C"})


def test_latest_readings_come_first_and_respect_limit(client):
    for v in (1.0, 2.0, 3.0):
        _send(client, value=v)
    results = client.get("/api/telemetry?device_id=TRK-01&limit=2").get_json()["results"]
    assert [r["value"] for r in results] == [3.0, 2.0]


def test_filter_by_device_and_metric(client):
    _send(client, device="TRK-01")
    _send(client, device="TRK-02")
    _send(client, device="TRK-02", metric="humidity", value=60)
    results = client.get("/api/telemetry?device_id=TRK-02&metric=humidity").get_json()["results"]
    assert len(results) == 1 and results[0]["metric"] == "humidity"


def test_invalid_limit_returns_400(client):
    assert client.get("/api/telemetry?limit=0").status_code == 400
    assert client.get("/api/telemetry?limit=abc").status_code == 400
