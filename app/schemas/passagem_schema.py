from marshmallow import fields
from app.extensions import ma
from app.models.passagem import Passagem

class PassagemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Passagem
        load_instance = False

    id = fields.String(dump_only=True)
    passageiro_id = fields.String(required=True)
    voo_id = fields.String(required=True)

    passageiro = fields.Nested(
        "PassageiroSchema", 
        dump_only=True, 
        only=("id", "nome", "cpf")
    )
    voo = fields.Nested(
        "VooSchema", 
        dump_only=True, 
        only=("id",) 
    )
passagem_schema = PassagemSchema()
passagens_schema = PassagemSchema(many=True)