from flask import Blueprint, jsonify, request

from app.schemas.passagem_schema import passagem_schema, passagens_schema
from app.services import passagem_service
from app.utils.pagination import parametros_paginacao, serializar_paginacao

passagem_bp = Blueprint("passagens", __name__)



@passagem_bp.get("")
def listar_passagens():
    pagina, por_pagina = parametros_paginacao()
    paginacao = passagem_service.listar(
        pagina=pagina, por_pagina=por_pagina,
        voo_id=request.args.get("voo_id"), passageiro_id=request.args.get("passageiro_id"),
    )
    return jsonify(serializar_paginacao(paginacao, passagens_schema)), 200


@passagem_bp.get("/<string:passagem_id>")
def obter_passagem(passagem_id: str):
    passagem = passagem_service.obter(passagem_id)
    return jsonify(passagem_schema.dump(passagem)), 200


@passagem_bp.post("")
def criar_passagem():
    dados = passagem_schema.load(request.get_json())
    passagem = passagem_service.criar(dados)
    return jsonify(passagem_schema.dump(passagem)), 201


@passagem_bp.put("/<string:passagem_id>")
def substituir_passagem(passagem_id: str):
    dados = passagem_schema.load(request.get_json(), partial=False)
    passagem = passagem_service.atualizar(passagem_id, dados)
    return jsonify(passagem_schema.dump(passagem)), 200


@passagem_bp.patch("/<string:passagem_id>")
def atualizar_passagem(passagem_id: str):
    dados = passagem_schema.load(request.get_json(), partial=True)
    passagem = passagem_service.atualizar(passagem_id, dados)
    return jsonify(passagem_schema.dump(passagem)), 200


@passagem_bp.delete("/<string:passagem_id>")
def remover_passagem(passagem_id: str):
    passagem_service.remover(passagem_id)
    return "Passagem removida com sucesso", 204
