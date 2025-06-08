from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_payman_sync():
    # Pretpostavljamo da korisnik već postoji (možeš ovdje dodati setup)
    response = client.post("/payments/payman-sync/", params={
        "question": "Give me all payees",
        "user_email": "test@example.com"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Payees processed and stored successfully"