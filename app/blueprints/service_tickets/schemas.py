from app.extensions import ma
from app.models import Service_Ticket
from marshmallow import fields 

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
        mechanics = fields.Nested("MechanicSchema", many=True)  # Nested field for mechanics
        inventory = fields.Nested("InventorySchema", many=True)  # Nested field for inventory item
        class Meta:
            model = Service_Ticket 
            include_fk = True
            exclude = ("customer",) 

class EditServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ('add_mechanic_ids', 'remove_mechanic_ids')
        
    

service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)
edit_Service_Ticket_Schema = EditServiceTicketSchema()
