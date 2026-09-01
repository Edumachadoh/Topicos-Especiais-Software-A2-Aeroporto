from marshmallow import fields, validate
from app.extensions import ma
from app.models.passageiro import Passageiro


class PassageiroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Passageiro
        load_instance = False

    id = fields.String(dump_only=True)
    nome = fields.String(required=True, validate=validate.Length(min=2, max=100))
    # Validando o tamanho exato de 14 caracteres assumindo a máscara padrão XXX.XXX.XXX-XX
    cpf = fields.String(required=True, validate=validate.Length(equal=14))


passageiro_schema = PassageiroSchema()
passageiros_schema = PassageiroSchema(many=True)
