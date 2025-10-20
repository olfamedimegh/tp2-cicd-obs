from app.main import app

def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json["status"] == "ok"

def test_home():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert "hello" in resp.json