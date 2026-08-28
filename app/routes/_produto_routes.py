from flask import Blueprint, jsonify, request

from app.schemas._produto_schema import produto_schema, produtos_schema
from app.services import produto_service

produto_bp = Blueprint("produtos", __name__)


@produto_bp.get("")
def listar_produtos():
    categoria_id = request.args.get("categoria_id", type=int)
    produtos = produto_service.listar(categoria_id=categoria_id)
    return jsonify(produtos_schema.dump(produtos)), 200


@produto_bp.get("/<int:produto_id>")
def obter_produto(produto_id: int):
    produto = produto_service.obter(produto_id)
    return jsonify(produto_schema.dump(produto)), 200


@produto_bp.post("")
def criar_produto():
    dados = produto_schema.load(request.get_json())
    produto = produto_service.criar(dados)
    return jsonify(produto_schema.dump(produto)), 201


@produto_bp.put("/<int:produto_id>")
def substituir_produto(produto_id: int):
    dados = produto_schema.load(request.get_json(), partial=False)
    produto = produto_service.atualizar(produto_id, dados)
    return jsonify(produto_schema.dump(produto)), 200


@produto_bp.patch("/<int:produto_id>")
def atualizar_produto(produto_id: int):
    dados = produto_schema.load(request.get_json(), partial=True)
    produto = produto_service.atualizar(produto_id, dados)
    return jsonify(produto_schema.dump(produto)), 200


@produto_bp.delete("/<int:produto_id>")
def remover_produto(produto_id: int):
    produto_service.remover(produto_id)
    return "", 204
