from flask import Blueprint, jsonify, request

from app.schemas.aeronave_schema import aeronave_schema, aeronaves_schema
from app.services import aeronave_service
from app.utils.pagination import parametros_paginacao, serializar_paginacao


aeronave_bp = Blueprint("aeronaves", __name__)


@aeronave_bp.get("")
def listar_aeronaves():
    pagina, por_pagina = parametros_paginacao()
    paginacao = aeronave_service.listar(
        pagina=pagina, por_pagina=por_pagina,
        tipo=request.args.get("tipo"), modelo=request.args.get("modelo"),
    )
    return jsonify(serializar_paginacao(paginacao, aeronaves_schema)), 200


@aeronave_bp.get("/<string:aeronave_id>")
def obter_aeronave(aeronave_id: str):
    aeronave = aeronave_service.obter(aeronave_id)
    return jsonify(aeronave_schema.dump(aeronave)), 200


@aeronave_bp.post("")
def criar_aeronave():
    dados = aeronave_schema.load(request.get_json())
    aeronave = aeronave_service.criar(dados)
    return jsonify(aeronave_schema.dump(aeronave)), 201


@aeronave_bp.put("/<string:aeronave_id>")
def substituir_aeronave(aeronave_id: str):
    dados = aeronave_schema.load(request.get_json(), partial=False)
    aeronave = aeronave_service.atualizar(aeronave_id, dados)
    return jsonify(aeronave_schema.dump(aeronave)), 200


@aeronave_bp.patch("/<string:aeronave_id>")
def atualizar_aeronave(aeronave_id: str):
    dados = aeronave_schema.load(request.get_json(), partial=True)
    aeronave = aeronave_service.atualizar(aeronave_id, dados)
    return jsonify(aeronave_schema.dump(aeronave)), 200


@aeronave_bp.delete("/<string:aeronave_id>")
def remover_aeronave(aeronave_id: str):
    aeronave_service.remover(aeronave_id)
    return "Aeronave removida com sucesso", 204