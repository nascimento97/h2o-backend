import pytest


def test_create_weight_requires_auth(client):
    # Sem token
    response = client.post("/weights/", json={"value": 75.5})
    assert response.status_code == 401

@pytest.fixture(scope="module")
def auth_header(client):
    # Cria usuário e obtém token
    client.post("/users/", json={"name": "wuser", "weight_id": 60.0})
    login = client.post("/users/login", json={"name": "wuser"}).json()
    return {"Authorization": f"Bearer {login['access_token']}"}


def test_create_weight(client, auth_header):
    response = client.post("/weights/", json={"value": 80.0}, headers=auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["value"] == 80.0
    assert "id" in data
    assert "created_at" in data
