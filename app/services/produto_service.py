from app.errors import RecursoNaoEncontrado, ReferenciaInvalida
from app.extensions import db
from app.models._categoria import Categoria
from app.models._produto import Produto


def listar(categoria_id: int | None = None) -> list[Produto]:
    stmt = db.select(Produto).order_by(Produto.nome)
    if categoria_id is not None:
        stmt = stmt.where(Produto.categoria_id == categoria_id)
    return list(db.session.scalars(stmt))


def obter(produto_id: int) -> Produto:
    produto = db.session.get(Produto, produto_id)
    if produto is None:
        raise RecursoNaoEncontrado(f"Produto {produto_id} não encontrado.")
    return produto


def criar(dados: dict) -> Produto:
    _garantir_categoria_existe(dados["categoria_id"])
    produto = Produto(**dados)
    db.session.add(produto)
    db.session.commit()
    return produto


def atualizar(produto_id: int, dados: dict) -> Produto:
    produto = obter(produto_id)

    if "categoria_id" in dados:
        _garantir_categoria_existe(dados["categoria_id"])

    for campo, valor in dados.items():
        setattr(produto, campo, valor)

    db.session.commit()
    return produto


def remover(produto_id: int) -> None:
    produto = obter(produto_id)
    db.session.delete(produto)
    db.session.commit()


def _garantir_categoria_existe(categoria_id: int) -> None:
    if db.session.get(Categoria, categoria_id) is None:
        raise ReferenciaInvalida(f"Categoria {categoria_id} não existe.")
