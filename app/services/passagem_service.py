import uuid
from app.errors import RecursoNaoEncontrado, RegraDeNegocio
from app.extensions import db
from app.models.passagem import Passagem
from app.models.passageiro import Passageiro
from app.models.voo import Voo


def listar() -> list[Passagem]:
    stmt = db.select(Passagem).order_by(Passagem.assento)
    return list(db.session.scalars(stmt))


def obter(passagem_id: str) -> Passagem:
    passagem = db.session.get(Passagem, passagem_id)
    if passagem is None:
        raise RecursoNaoEncontrado(f"Passagem {passagem_id} não encontrado.")
    return passagem


def criar(dados: dict) -> Passagem:
    _garantir_passageiro_existe(dados["passageiro_id"])
    _garantir_voo_existe(dados["voo_id"])
    _garantir_assento_livre(dados["voo_id"], dados["assento"])

    if "id" not in dados:
        dados["id"] = str(uuid.uuid4())

    passagem = Passagem(**dados)
    db.session.add(passagem)
    db.session.commit()
    return passagem


def atualizar(passagem_id: str, dados: dict) -> Passagem:
    passagem = obter(passagem_id)

    if "passageiro_id" in dados:
        _garantir_passageiro_existe(dados["passageiro_id"])

    if "voo_id" in dados:
        _garantir_voo_existe(dados["voo_id"])

    novo_voo_id = dados.get("voo_id", passagem.voo_id)
    novo_assento = dados.get("assento", passagem.assento)

    if novo_voo_id != passagem.voo_id or novo_assento != passagem.assento:
        _garantir_assento_livre(novo_voo_id, novo_assento, ignorar_id=passagem.id)

    for campo, valor in dados.items():
        setattr(passagem, campo, valor)

    db.session.commit()
    return passagem


def remover(passagem_id: str) -> None:
    passagem = obter(passagem_id)
    db.session.delete(passagem)
    db.session.commit()


def _garantir_passageiro_existe(passageiro_id: str) -> None:
    passageiro = db.session.get(Passageiro, passageiro_id)
    if passageiro is None:
        raise RegraDeNegocio(
            f"A passageiro com ID '{passageiro_id}' não existe no sistema."
        )


def _garantir_voo_existe(voo_id: str) -> None:
    voo = db.session.get(Voo, voo_id)
    if voo is None:
        raise RegraDeNegocio(f"A voo com ID '{voo_id}' não existe no sistema.")


def _garantir_assento_livre(voo_id: str, assento: str) -> None:
    # onde dentro da table passagens
    # nas passagens desse voo_id
    # verificar se a passagem com aquele assento existe
    assento_selecionado = db.select(Passagem).where(
        Passagem.voo_id == voo_id, Passagem.assento == assento
    )
    # se o acento selecionado for encontrado
    #ele não deixa pegar o acento
    if db.session.scalar(assento_selecionado) is not None:
        raise RegraDeNegocio(f"O assento {assento} já está ocupado para este voo.")
