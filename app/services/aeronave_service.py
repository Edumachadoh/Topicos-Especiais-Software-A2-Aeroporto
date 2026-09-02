import uuid
from app.errors import RecursoNaoEncontrado
from app.extensions import db
from app.models.aeronave import Aeronave


def listar(pagina: int = 1, por_pagina: int = 10, tipo: str | None = None, modelo: str | None = None):
    stmt = db.select(Aeronave).order_by(Aeronave.modelo)
    if tipo:
        stmt = stmt.where(Aeronave.tipo == tipo)
    if modelo:
        stmt = stmt.where(Aeronave.modelo.ilike(f"%{modelo}%"))
    return db.paginate(stmt, page=pagina, per_page=por_pagina, error_out=False)


def obter(aeronave_id: str) -> Aeronave:
    aeronave = db.session.get(Aeronave, aeronave_id)
    if aeronave is None:
        raise RecursoNaoEncontrado(f"Aeronave {aeronave_id} não encontrada.")
    return aeronave


def criar(dados: dict) -> Aeronave:
    if "id" not in dados:
        dados["id"] = str(uuid.uuid4())
        
    aeronave = Aeronave(**dados)
    db.session.add(aeronave)
    db.session.commit()
    return aeronave


def atualizar(aeronave_id: str, dados: dict) -> Aeronave:
    aeronave = obter(aeronave_id)

    for campo, valor in dados.items():
        setattr(aeronave, campo, valor)

    db.session.commit()
    return aeronave


def remover(aeronave_id: str) -> None:
    aeronave = obter(aeronave_id)
    db.session.delete(aeronave)
    db.session.commit()