from app.extensions import ma
from app.models import Service_Ticket

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
             model = Service_Ticket # Specify the model to be serialized
             include_fk = True  # Include foreign keys in the schema
             
service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)