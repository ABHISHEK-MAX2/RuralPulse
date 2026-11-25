from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"

def test_get_districts():
    response = client.get("/api/v1/geography/districts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_villages_list():
    response = client.get("/api/v1/geography/villages?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10

def test_get_vulnerability_kpis():
    response = client.get("/api/v1/vulnerability/kpis")
    assert response.status_code == 200
    data = response.json()
    assert "total_villages" in data
    assert data["total_villages"] > 0

def test_login():
    response = client.post("/api/v1/auth/login", json={
        "email": "state_admin@karnataka.gov.in",
        "password": "admin123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "STATE_ADMIN"

def test_closed_loop_intervention():
    # Login to get token
    login_res = client.post("/api/v1/auth/login", json={
        "email": "state_admin@karnataka.gov.in",
        "password": "admin123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch recommendations
    recs = client.get("/api/v1/recommendations?limit=1", headers=headers).json()
    if recs:
        rec_id = recs[0]["id"]
        v_code = recs[0]["village_code"]
        
        # Approve recommendation
        review_res = client.post(f"/api/v1/recommendations/{rec_id}/review", json={
            "status": "APPROVED",
            "notes": "Approved for immediate deployment"
        }, headers=headers)
        assert review_res.status_code == 200
        assert review_res.json()["status"] == "APPROVED"

