import uuid
from app.errors import RecursoNaoEncontrado, RegraDeNegocio
from app.extensions import db
from app.models.passagem import Passagem
from app.models.passageiro import Passageiro
from app.models.voo import Voo


def listar() -> list[Passagem]:
    stmt = db.select(Passagem)
    return list(db.session.scalars(stmt))


def obter(passagem_id: str) -> Passagem:
    passagem = db.session.get(Passagem, passagem_id)
    if passagem is None:
        raise RecursoNaoEncontrado(f"Passagem {passagem_id} não encontrado.")
    return passagem


def criar(dados: dict) -> Passagem:

    if "passageiro_id" in dados:
        _garantir_passageiro_existe(dados["passageiro_id"])

    if "voo_id" in dados:
        _garantir_voo_existe(dados["voo_id"])

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
        raise RegraDeNegocio(f"A passageiro com ID '{passageiro_id}' não existe no sistema.")

def _garantir_voo_existe(voo_id: str) -> None:
    voo = db.session.get(Voo, voo_id)
    if voo is None:
        raise RegraDeNegocio(f"A voo com ID '{voo_id}' não existe no sistema.")