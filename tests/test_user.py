import pytest

from app.schemas.user import UserCreate, UserLogin


def test_create_and_login_user(client):
    # Cria usuário
    create_data = {"name": "teste", "weight_id": 70.0}
    response = client.post("/users/", json=create_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "teste"
    assert "id" in data

    # Faz login
    login_data = {"name": "teste"}
    response = client.post("/users/login", json=login_data)
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token

    # Logout inválido (sem token)
    response = client.post("/users/logout")
    assert response.status_code == 401

    # Logout válido
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/users/logout", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Logout successful"
