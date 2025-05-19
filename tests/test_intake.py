import pytest
from datetime import datetime, timedelta


def test_intake_and_history(client):
    # Cria usuário e token
    client.post("/users/", json={"name": "iuser", "weight_id": 65.0})
    login = client.post("/users/login", json={"name": "iuser"}).json()
    headers = {"Authorization": f"Bearer {login['access_token']}"}

    # Registra ingestões
    for q in [200, 350, 500]:
        resp = client.post("/intake/", json={"quantity": q}, headers=headers)
        assert resp.status_code == 201
        assert resp.json()["quantity"] == q

    # Recupera todo histórico
    resp = client.get("/intake/", headers=headers)
    assert resp.status_code == 200
    history = resp.json()
    assert len(history) == 3

    # Filtrar por quantidade
    resp = client.get("/intake/?quantity=350", headers=headers)
    assert resp.status_code == 200
    filtered = resp.json()
    assert all(item["quantity"] == 350 for item in filtered)

    # Filtrar por intervalo de datas
    now = datetime.utcnow()
    past = (now - timedelta(days=1)).isoformat()
    future = (now + timedelta(days=1)).isoformat()
    url = f"/intake/?date_from={past}&date_to={future}"
    resp = client.get(url, headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 3
