from flask import Blueprint, jsonify, request

from app.schemas.passageiro_schema import passageiro_schema, passageiros_schema
from app.services import passageiro_service

passageiro_bp = Blueprint("passageiros", __name__)


@passageiro_bp.get("")
def listar_passageiros():
    passageiros = passageiro_service.listar()
    return jsonify(passageiros_schema.dump(passageiros)), 200


@passageiro_bp.get("/<string:passageiro_id>")
def obter_passageiro(passageiro_id: str):
    passageiro = passageiro_service.obter(passageiro_id)
    return jsonify(passageiro_schema.dump(passageiro)), 200


@passageiro_bp.post("")
def criar_passageiro():
    dados = passageiro_schema.load(request.get_json())
    passageiro = passageiro_service.criar(dados)
    return jsonify(passageiro_schema.dump(passageiro)), 201


@passageiro_bp.put("/<string:passageiro_id>")
def substituir_passageiro(passageiro_id: str):
    dados = passageiro_schema.load(request.get_json(), partial=False)
    passageiro = passageiro_service.atualizar(passageiro_id, dados)
    return jsonify(passageiro_schema.dump(passageiro)), 200


@passageiro_bp.patch("/<string:passageiro_id>")
def atualizar_passageiro(passageiro_id: str):
    dados = passageiro_schema.load(request.get_json(), partial=True)
    passageiro = passageiro_service.atualizar(passageiro_id, dados)
    return jsonify(passageiro_schema.dump(passageiro)), 200


@passageiro_bp.delete("/<string:passageiro_id>")
def remover_passageiro(passageiro_id: str):
    passageiro_service.remover(passageiro_id)
    return "", 204