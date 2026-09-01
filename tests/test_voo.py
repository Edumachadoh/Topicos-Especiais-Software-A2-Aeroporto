"""Testes de Categoria.

Os primeiros exercitam a API de ponta a ponta; os dois últimos chamam o service
direto, sem HTTP — que é justamente o que a separação em camadas compra.
"""

import pytest

from app.errors import RecursoNaoEncontrado, RegraDeNegocio
from app.services import categoria_service


def test_listar_vazio(client):
    resposta = client.get("/api/categorias")
    assert resposta.status_code == 200
    assert resposta.get_json() == []


def test_criar_categoria(client):
    resposta = client.post("/api/categorias", json={"nome": "Livros"})
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["nome"] == "Livros"
    assert corpo["produtos"] == []
    assert "id" in corpo


def test_criar_categoria_com_nome_curto_devolve_422(client):
    resposta = client.post("/api/categorias", json={"nome": "X"})
    assert resposta.status_code == 422
    assert "nome" in resposta.get_json()["errors"]


def test_criar_categoria_sem_nome_devolve_422(client):
    resposta = client.post("/api/categorias", json={"descricao": "sem nome"})
    assert resposta.status_code == 422


def test_nome_duplicado_devolve_409(client, categoria):
    resposta = client.post("/api/categorias", json={"nome": categoria["nome"]})
    assert resposta.status_code == 409


def test_obter_categoria_inexistente_devolve_404(client):
    resposta = client.get("/api/categorias/999")
    assert resposta.status_code == 404
    assert resposta.get_json()["code"] == 404


def test_detalhe_traz_produtos_aninhados(client, produto):
    resposta = client.get(f"/api/categorias/{produto['categoria_id']}")
    assert resposta.status_code == 200
    produtos = resposta.get_json()["produtos"]
    assert len(produtos) == 1
    assert produtos[0]["nome"] == "Mouse Sem Fio"
    # `exclude=("categoria_id",)` no Nested evita repetir o pai dentro do
    # filho, que já está dentro do pai.
    assert "categoria_id" not in produtos[0]


def test_listagem_nao_traz_produtos(client, produto):
    resposta = client.get("/api/categorias")
    assert "produtos" not in resposta.get_json()[0]


def test_patch_altera_apenas_o_campo_enviado(client, categoria):
    resposta = client.patch(
        f"/api/categorias/{categoria['id']}", json={"descricao": "Nova descrição"}
    )
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["descricao"] == "Nova descrição"
    assert corpo["nome"] == "Eletrônicos"


def test_put_sem_descricao_apaga_a_descricao(client, categoria):
    """PUT é substituição: o que não vem no payload volta ao padrão."""
    resposta = client.put(f"/api/categorias/{categoria['id']}", json={"nome": "Áudio"})
    assert resposta.status_code == 200
    assert resposta.get_json()["descricao"] is None


def test_put_sem_nome_devolve_422(client, categoria):
    resposta = client.put(
        f"/api/categorias/{categoria['id']}", json={"descricao": "só isso"}
    )
    assert resposta.status_code == 422


def test_enviar_campo_dump_only_devolve_422(client):
    """`produtos` é somente-leitura: mandá-lo na entrada é campo desconhecido."""
    resposta = client.post(
        "/api/categorias", json={"nome": "Games", "produtos": [{"nome": "X"}]}
    )
    assert resposta.status_code == 422


def test_corpo_json_malformado_devolve_400(client):
    resposta = client.post(
        "/api/categorias", data="isto não é json", content_type="application/json"
    )
    assert resposta.status_code == 400


def test_content_type_errado_devolve_415(client):
    """Desde o Flask 2.1, `get_json()` distingue os dois casos."""
    resposta = client.post("/api/categorias", data="qualquer coisa")
    assert resposta.status_code == 415


def test_delete_remove_categoria_e_produtos_em_cascata(client, produto):
    categoria_id = produto["categoria_id"]
    assert client.delete(f"/api/categorias/{categoria_id}").status_code == 204
    assert client.get(f"/api/categorias/{categoria_id}").status_code == 404
    # O cascade "all, delete-orphan" levou o produto junto.
    assert client.get("/api/produtos").get_json() == []


# --- Camada de serviço, sem HTTP ---------------------------------------------


def test_service_obter_inexistente_levanta_excecao_de_dominio(app):
    with pytest.raises(RecursoNaoEncontrado):
        categoria_service.obter(999)


def test_service_nome_duplicado_levanta_regra_de_negocio(app):
    categoria_service.criar({"nome": "Livros", "descricao": None})
    with pytest.raises(RegraDeNegocio):
        categoria_service.criar({"nome": "Livros", "descricao": None})
