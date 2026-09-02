import uuid
from app.errors import RecursoNaoEncontrado, RegraDeNegocio
from app.extensions import db
from app.models.passageiro import Passageiro


def listar(pagina: int = 1, por_pagina: int = 10, nome: str | None = None):
    stmt = db.select(Passageiro).order_by(Passageiro.nome)
    if nome:
        stmt = stmt.where(Passageiro.nome.ilike(f"%{nome}%"))
    return db.paginate(stmt, page=pagina, per_page=por_pagina, error_out=False)


def obter(passageiro_id: str) -> Passageiro:
    passageiro = db.session.get(Passageiro, passageiro_id)
    if passageiro is None:
        raise RecursoNaoEncontrado(f"Passageiro {passageiro_id} não encontrado.")
    return passageiro


def criar(dados: dict) -> Passageiro:
    _garantir_cpf_disponivel(dados["cpf"])
    
    if "id" not in dados:
        dados["id"] = str(uuid.uuid4())
        
    passageiro = Passageiro(**dados)
    db.session.add(passageiro)
    db.session.commit()
    return passageiro


def atualizar(passageiro_id: str, dados: dict) -> Passageiro:
    passageiro = obter(passageiro_id)

    if "cpf" in dados:
        _garantir_cpf_disponivel(dados["cpf"], ignorar_id=passageiro.id)

    for campo, valor in dados.items():
        setattr(passageiro, campo, valor)

    db.session.commit()
    return passageiro


def remover(passageiro_id: str) -> None:
    passageiro = obter(passageiro_id)
    db.session.delete(passageiro)
    db.session.commit()


def _garantir_cpf_disponivel(cpf: str, ignorar_id: str | None = None) -> None:
    stmt = db.select(Passageiro).where(Passageiro.cpf == cpf)
    if ignorar_id is not None:
        stmt = stmt.where(Passageiro.id != ignorar_id)
    if db.session.scalar(stmt) is not None:
        raise RegraDeNegocio(f"Já existe um passageiro cadastrado com o CPF '{cpf}'.")