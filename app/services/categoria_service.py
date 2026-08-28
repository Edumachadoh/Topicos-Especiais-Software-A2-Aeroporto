from app.errors import RecursoNaoEncontrado, RegraDeNegocio
from app.extensions import db
from app.models._categoria import Categoria


def listar() -> list[Categoria]:
    stmt = db.select(Categoria).order_by(Categoria.nome)
    return list(db.session.scalars(stmt))


def obter(categoria_id: int) -> Categoria:
    categoria = db.session.get(Categoria, categoria_id)
    if categoria is None:
        raise RecursoNaoEncontrado(f"Categoria {categoria_id} não encontrada.")
    return categoria


def criar(dados: dict) -> Categoria:
    _garantir_nome_disponivel(dados["nome"])
    categoria = Categoria(**dados)
    db.session.add(categoria)
    db.session.commit()
    return categoria


def atualizar(categoria_id: int, dados: dict) -> Categoria:
    categoria = obter(categoria_id)

    if "nome" in dados:
        _garantir_nome_disponivel(dados["nome"], ignorar_id=categoria.id)

    for campo, valor in dados.items():
        setattr(categoria, campo, valor)

    db.session.commit()
    return categoria


def remover(categoria_id: int) -> None:
    categoria = obter(categoria_id)
    db.session.delete(categoria)
    db.session.commit()


def _garantir_nome_disponivel(nome: str, ignorar_id: int | None = None) -> None:
    stmt = db.select(Categoria).where(Categoria.nome == nome)
    if ignorar_id is not None:
        stmt = stmt.where(Categoria.id != ignorar_id)
    if db.session.scalar(stmt) is not None:
        raise RegraDeNegocio(f"Já existe uma categoria com o nome '{nome}'.")
