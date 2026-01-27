from app.extensions import ma
from app.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
             model = Customer # Specify the model to be serialized

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True) # Schema for serializing multiple Customer instances
