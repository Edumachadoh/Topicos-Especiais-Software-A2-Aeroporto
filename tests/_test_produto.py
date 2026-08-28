"""Testes de Produto."""


def test_criar_produto(client, categoria):
    resposta = client.post(
        "/api/produtos",
        json={
            "nome": "Teclado Mecânico",
            "preco": 349.90,
            "estoque": 10,
            "categoria_id": categoria["id"],
        },
    )
    assert resposta.status_code == 201
    assert resposta.get_json()["nome"] == "Teclado Mecânico"


def test_estoque_ausente_assume_zero(client, categoria):
    resposta = client.post(
        "/api/produtos",
        json={"nome": "Webcam", "preco": 199.0, "categoria_id": categoria["id"]},
    )
    assert resposta.status_code == 201
    assert resposta.get_json()["estoque"] == 0


def test_preco_negativo_devolve_422(client, categoria):
    resposta = client.post(
        "/api/produtos",
        json={"nome": "Teclado", "preco": -10.0, "categoria_id": categoria["id"]},
    )
    assert resposta.status_code == 422
    assert "preco" in resposta.get_json()["errors"]


def test_categoria_inexistente_devolve_422(client):
    resposta = client.post(
        "/api/produtos",
        json={"nome": "Fone", "preco": 99.0, "categoria_id": 999},
    )
    assert resposta.status_code == 422
    assert "999" in resposta.get_json()["description"]


def test_filtro_por_categoria(client, produto, categoria):
    outra = client.post("/api/categorias", json={"nome": "Livros"}).get_json()
    client.post(
        "/api/produtos",
        json={"nome": "Clean Code", "preco": 120.0, "categoria_id": outra["id"]},
    )

    assert len(client.get("/api/produtos").get_json()) == 2

    filtrados = client.get(f"/api/produtos?categoria_id={categoria['id']}").get_json()
    assert len(filtrados) == 1
    assert filtrados[0]["nome"] == "Mouse Sem Fio"


def test_patch_preserva_os_campos_nao_enviados(client, produto):
    resposta = client.patch(f"/api/produtos/{produto['id']}", json={"preco": 119.50})
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["preco"] == 119.50
    assert corpo["estoque"] == 35


def test_put_sem_estoque_zera_o_estoque(client, produto):
    """A diferença entre PUT e PATCH, em um assert.

    Rode este teste ao lado do anterior em aula: mesmo recurso, mesma ausência
    de `estoque` no payload, resultados opostos.
    """
    resposta = client.put(
        f"/api/produtos/{produto['id']}",
        json={
            "nome": "Mouse Sem Fio",
            "preco": 119.50,
            "categoria_id": produto["categoria_id"],
        },
    )
    assert resposta.status_code == 200
    assert resposta.get_json()["estoque"] == 0


def test_mover_para_categoria_inexistente_nao_altera_o_produto(client, produto):
    resposta = client.patch(f"/api/produtos/{produto['id']}", json={"categoria_id": 999})
    assert resposta.status_code == 422
    # A validação acontece antes de qualquer setattr: o produto segue intacto.
    atual = client.get(f"/api/produtos/{produto['id']}").get_json()
    assert atual["categoria_id"] == produto["categoria_id"]


def test_delete_produto(client, produto):
    assert client.delete(f"/api/produtos/{produto['id']}").status_code == 204
    assert client.get(f"/api/produtos/{produto['id']}").status_code == 404


def test_metodo_nao_permitido_devolve_json(client):
    resposta = client.patch("/api/produtos")
    assert resposta.status_code == 405
    assert resposta.get_json()["code"] == 405
