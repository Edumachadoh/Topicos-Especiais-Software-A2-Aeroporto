from marshmallow import fields, validate
from app.extensions import ma
from app.models.aeronave import Aeronave

class AeronaveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Aeronave
        load_instance = False

    id = fields.String(dump_only=True)
    tipo = fields.String(required=True, validate=validate.Length(min=2, max=50))
    capacidade_assentos = fields.Integer(required=True, validate=validate.Range(min=1))
    modelo = fields.String(required=True, validate=validate.Length(min=2, max=50))

aeronave_schema = AeronaveSchema()
aeronaves_schema = AeronaveSchema(many=True)