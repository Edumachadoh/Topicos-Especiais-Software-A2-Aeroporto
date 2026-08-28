from marshmallow import fields, validate

from app.extensions import ma
from app.models._produto import Produto


class ProdutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Produto
        load_instance = False

    id = fields.Integer(dump_only=True)
    nome = fields.String(required=True, validate=validate.Length(min=2, max=150))
    preco = fields.Float(required=True, validate=validate.Range(min=0.01))
    estoque = fields.Integer(load_default=0, validate=validate.Range(min=0))
    categoria_id = fields.Integer(required=True)


produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True)
