from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema, edit_Service_Ticket_Schema 
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_Ticket, db, Mechanic, Inventory
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

#Get specific service ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_service_ticket(ticket_id):
    service_ticket = db.session.get(Service_Ticket, ticket_id)

    if service_ticket:
          return service_ticket_schema.jsonify(service_ticket), 200
    return jsonify({"error": "Service ticket not found"}), 404

# Edit service ticket to add or remove mechanics
@service_tickets_bp.route("/<int:service_ticket_id>", methods=['PUT'])
def edit_service_ticket(service_ticket_id):
    try:
        service_tickets_edits = edit_Service_Ticket_Schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Service_Ticket).where(Service_Ticket.id == service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    for mechanic_id in service_tickets_edits['add_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)
            
    for mechanic_id in service_tickets_edits['remove_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket)

#Add inventory items to service ticket
@service_tickets_bp.route("/<int:ticket_id>/add_inventory/<int:inventory_id>", methods=["PUT"])
def add_inventory_to_ticket(ticket_id, inventory_id):
    # Get service ticket
    ticket = db.session.get(Service_Ticket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    # Get inventory 
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory item not found"}), 404

    # Prevent duplicates
    if inventory in ticket.inventory:
        return jsonify({"error": "Inventory item already added to this service ticket"}), 409

    # Add inventory item to ticket
    ticket.inventory.append(inventory)
    db.session.commit()

    return jsonify({
        "message": "Inventory item successfully added to service ticket",
        "ticket_id": ticket.id,
        "inventory_id": inventory.id
    }), 200



