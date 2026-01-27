from app.extensions import ma
from app.models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
             model = Mechanic # Specify the model to be serialized

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)