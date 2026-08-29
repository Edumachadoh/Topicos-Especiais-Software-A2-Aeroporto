from flask import Blueprint, jsonify, request

from app.schemas.voo_schema import voo_schema, voos_schema
from app.services import voo_service

voo_bp = Blueprint("voos", __name__)


@voo_bp.get("")
def listar_voos():
    voos = voo_service.listar()
    return jsonify(voos_schema.dump(voos)), 200


@voo_bp.get("/<string:voo_id>")
def obter_voo(voo_id: str):
    voo = voo_service.obter(voo_id)
    return jsonify(voo_schema.dump(voo)), 200


@voo_bp.post("")
def criar_voo():
    dados = voo_schema.load(request.get_json())
    voo = voo_service.criar(dados)
    return jsonify(voo_schema.dump(voo)), 201


@voo_bp.put("/<string:voo_id>")
def substituir_voo(voo_id: str):
    dados = voo_schema.load(request.get_json(), partial=False)
    voo = voo_service.atualizar(voo_id, dados)
    return jsonify(voo_schema.dump(voo)), 200


@voo_bp.patch("/<string:voo_id>")
def atualizar_voo(voo_id: str):
    dados = voo_schema.load(request.get_json(), partial=True)
    voo = voo_service.atualizar(voo_id, dados)
    return jsonify(voo_schema.dump(voo)), 200


@voo_bp.delete("/<string:voo_id>")
def remover_voo(voo_id: str):
    voo_service.remover(voo_id)
    return "", 204