import uuid
from app.errors import RecursoNaoEncontrado, RegraDeNegocio
from app.extensions import db
from app.models.voo import Voo
from app.models.aeronave import Aeronave


def listar(pagina: int = 1, por_pagina: int = 10, aeronave_id: str | None = None):
    stmt = db.select(Voo)
    if aeronave_id:
        stmt = stmt.where(Voo.aeronave_id == aeronave_id)
    return db.paginate(stmt, page=pagina, per_page=por_pagina, error_out=False)


def obter(voo_id: str) -> Voo:
    voo = db.session.get(Voo, voo_id)
    if voo is None:
        raise RecursoNaoEncontrado(f"Voo {voo_id} não encontrado.")
    return voo


def criar(dados: dict) -> Voo:
    _garantir_aeronave_existe(dados["aeronave_id"])
    
    if "id" not in dados:
        dados["id"] = str(uuid.uuid4())
        
    voo = Voo(**dados)
    db.session.add(voo)
    db.session.commit()
    return voo


def atualizar(voo_id: str, dados: dict) -> Voo:
    voo = obter(voo_id)

    if "aeronave_id" in dados:
        _garantir_aeronave_existe(dados["aeronave_id"])

    for campo, valor in dados.items():
        setattr(voo, campo, valor)

    db.session.commit()
    return voo


def remover(voo_id: str) -> None:
    voo = obter(voo_id)
    db.session.delete(voo)
    db.session.commit()


def _garantir_aeronave_existe(aeronave_id: str) -> None:
    aeronave = db.session.get(Aeronave, aeronave_id)
    if aeronave is None:
        raise RegraDeNegocio(f"A aeronave com ID '{aeronave_id}' não existe no sistema.")