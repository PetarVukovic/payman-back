from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "email": "test@example.com",
        "password_hash": "testpass",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_create_payee():
    # Prvo kreiraj usera ručno ili u setup
    user_id = 1
    response = client.post("/payees/", json={
        "supplier_name": "Test Supplier",
        "iban": "HR1210010051863000160",
        "wallet_address": "0xabc123",
        "kyc_status": "pending",
        "country": "Croatia",
        "user_id": user_id
    })
    assert response.status_code == 200
    assert response.json()["supplier_name"] == "Test Supplier"