from app.extensions import ma
from app.models import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
        class Meta:
             model = Inventory # Specify the model to be serialized
             include_fk = True  # Include foreign keys in the schema

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True) # Schema for serializing multiple Customer instances
