from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_Ticket, db, Mechanic
from .import service_tickets_bp


#Create a new service ticket

@service_tickets_bp.route("/", methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_service_ticket = Service_Ticket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201

#Get all service tickets
@service_tickets_bp.route("/", methods=['GET'])
def get_service_tickets():
     query = select(Service_Ticket)
     service_tickets = db.session.execute(query).scalars().all()

     return service_tickets_schema.jsonify(service_tickets)

#Removes the relationship from the service ticket and the mechanic
@service_tickets_bp.route("/<int:service_ticket_id>/remove_mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic_from_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)

    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    if mechanic not in service_ticket.mechanics:
        return jsonify({"error": "Mechanic is not assigned to this service ticket."}), 400

    service_ticket.mechanics.remove(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(service_ticket), 200

#Adds a relationship between a service ticket and the mechanics. 
@service_tickets_bp.route("/<int:service_ticket_id>/assign_mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic_to_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)

    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    service_ticket.mechanics.append(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(service_ticket), 200
