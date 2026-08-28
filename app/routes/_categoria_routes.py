from flask import Blueprint, jsonify, request

from app.schemas._categoria_schema import categoria_schema, categorias_schema
from app.services import categoria_service

categoria_bp = Blueprint("categorias", __name__)


@categoria_bp.get("")
def listar_categorias():
    categorias = categoria_service.listar()
    return jsonify(categorias_schema.dump(categorias)), 200


@categoria_bp.get("/<int:categoria_id>")
def obter_categoria(categoria_id: int):
    categoria = categoria_service.obter(categoria_id)
    return jsonify(categoria_schema.dump(categoria)), 200


@categoria_bp.post("")
def criar_categoria():
    dados = categoria_schema.load(request.get_json())
    categoria = categoria_service.criar(dados)
    return jsonify(categoria_schema.dump(categoria)), 201


@categoria_bp.put("/<int:categoria_id>")
def substituir_categoria(categoria_id: int):
    dados = categoria_schema.load(request.get_json(), partial=False)
    categoria = categoria_service.atualizar(categoria_id, dados)
    return jsonify(categoria_schema.dump(categoria)), 200


@categoria_bp.patch("/<int:categoria_id>")
def atualizar_categoria(categoria_id: int):
    dados = categoria_schema.load(request.get_json(), partial=True)
    categoria = categoria_service.atualizar(categoria_id, dados)
    return jsonify(categoria_schema.dump(categoria)), 200


@categoria_bp.delete("/<int:categoria_id>")
def remover_categoria(categoria_id: int):
    categoria_service.remover(categoria_id)
    return "", 204
