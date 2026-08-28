from marshmallow import fields, validate

from app.extensions import ma
from app.models._categoria import Categoria
from app.schemas._produto_schema import ProdutoSchema


class CategoriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        load_instance = False

    id = fields.Integer(dump_only=True)
    nome = fields.String(required=True, validate=validate.Length(min=2, max=100))
    descricao = fields.String(allow_none=True, load_default=None)
    produtos = fields.Nested(
        ProdutoSchema, many=True, dump_only=True, exclude=("categoria_id",)
    )


categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True, exclude=("produtos",))
