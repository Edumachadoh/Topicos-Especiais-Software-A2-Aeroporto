import pytest


def test_criar_passageiro_com_sucesso(client):
    payload = {
        "nome": "Carlos Silva",
        "cpf": "123.456.789-01"
    }
    response = client.post("/api/passageiros", json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert "id" in data
    assert data["nome"] == payload["nome"]
    assert data["cpf"] == payload["cpf"]


def test_criar_passageiro_sem_nome_retorna_erro_validacao(client):
    # O campo nome é obrigatório
    payload = {
        "cpf": "123.456.789-01"
    }
    response = client.post("/api/passageiros", json=payload)
    
    assert response.status_code in (400, 422)


def test_listar_passageiros(client):
    p1 = {"nome": "Passageiro A", "cpf": "111.111.111-11"}
    p2 = {"nome": "Passageiro B", "cpf": "222.222.222-22"}
    client.post("/api/passageiros", json=p1)
    client.post("/api/passageiros", json=p2)

    response = client.get("/api/passageiros")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 2


def test_buscar_passageiro_por_id_com_sucesso(client):
    payload = {"nome": "Marina Souza", "cpf": "333.444.555-66"}
    criado = client.post("/api/passageiros", json=payload).get_json()
    passageiro_id = criado["id"]

    response = client.get(f"/api/passageiros/{passageiro_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == passageiro_id
    assert data["nome"] == payload["nome"]
    assert data["cpf"] == payload["cpf"]


def test_buscar_passageiro_inexistente_retorna_404(client):
    id_inexistente = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/passageiros/{id_inexistente}")
    
    assert response.status_code == 404


def test_atualizar_passageiro_put(client):
    criado = client.post(
        "/api/passageiros",
        json={"nome": "Nome Antigo", "cpf": "444.555.666-77"}
    ).get_json()
    passageiro_id = criado["id"]

    payload_put = {
        "nome": "Nome Atualizado Completo",
        "cpf": "444.555.666-77"
    }
    response = client.put(f"/api/passageiros/{passageiro_id}", json=payload_put)
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == passageiro_id
    assert data["nome"] == "Nome Atualizado Completo"


def test_atualizar_passageiro_patch(client):
    criado = client.post(
        "/api/passageiros",
        json={"nome": "Nome Original", "cpf": "555.666.777-88"}
    ).get_json()
    passageiro_id = criado["id"]

    payload_patch = {
        "nome": "Nome Parcialmente Alterado"
    }
    response = client.patch(f"/api/passageiros/{passageiro_id}", json=payload_patch)
    data = response.get_json()

    assert response.status_code == 200
    assert data["nome"] == "Nome Parcialmente Alterado"
    assert data["cpf"] == "555.666.777-88"


def test_deletar_passageiro_delete(client):
    criado = client.post(
        "/api/passageiros",
        json={"nome": "Para Deletar", "cpf": "999.888.777-66"}
    ).get_json()
    passageiro_id = criado["id"]

    delete_response = client.delete(f"/api/passageiros/{passageiro_id}")
    assert delete_response.status_code in (200, 204)

    # Garante que não existe mais após a exclusão
    get_response = client.get(f"/api/passageiros/{passageiro_id}")
    assert get_response.status_code == 404