from marshmallow import fields, validate
from app.extensions import ma
from app.models.voo import Voo

class VooSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Voo
        load_instance = False

    id = fields.String(dump_only=True)
    aeronave_id = fields.String(required=True)
    
    # Nested(dump_only=True) permite que, ao consultar um Voo (GET), 
    # a API retorne automaticamente a lista de passageiros vinculados a ele.
    passageiros = fields.Nested("PassageiroSchema", many=True, dump_only=True)
    aeronave = fields.Nested("AeronaveSchema", dump_only=True)

voo_schema = VooSchema()
voos_schema = VooSchema(many=True)