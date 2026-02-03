from .schemas import inventory_schema, inventories_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Inventory, db
from .import inventories_bp
from app.extensions import limiter, cache





#Create a new inventory 

@inventories_bp.route("/", methods=['POST'])
def create_inventory():
     try: 
          inventory_data = inventory_schema.load(request.json) # Validate and deserialize input
     except ValidationError as e:
          return jsonify(e.messages),400
     
     new_inventory = Inventory(name=inventory_data['name'], price=inventory_data['price'])
     db.session.add(new_inventory)
     db.session.commit()
     return inventory_schema.jsonify(new_inventory), 201
    

#Get all Inventory items
@inventories_bp.route("/", methods=['GET'])
#@cache.cached(timeout =60)  # Cache the response for 60 seconds
def get_inventories():
     try: 
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))  
        query = select(Inventory)
        inventories = db.paginate(query, page=page, per_page=per_page)
        return inventories_schema.jsonify(inventories), 200
     except:     
          query = select(Inventory)
          inventories = db.session.execute(query).scalars().all()
          return inventories_schema.jsonify(inventories)

#Get specific inventory item
@inventories_bp.route("/<int:inventory_id>", methods=['GET'])
def get_inventory(inventory_id):
     inventory = db.session.get(Inventory, inventory_id)

     if inventory:
          return inventory_schema.jsonify(inventory), 200
     return jsonify({"error": "Inventory item not found"}), 404

#UPDATE SPECIFIC Inventory Item
@inventories_bp.route("/<int:inventory_id>", methods=['PUT'])
def update_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if not inventory:
        return jsonify({"error": "Inventory item not found."}), 404
    
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in inventory_data.items():
        setattr(inventory, key, value)

    db.session.commit()
    return inventory_schema.jsonify(inventory), 200

#DELETE SPECIFIC INVENTORY ITEM
@inventories_bp.route("/<int:inventory_id>", methods=['DELETE'])
def delete_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if not inventory:
        return jsonify({"error": "Inventory item not found."}), 404
    
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": f'Inventory item id: {inventory_id}, successfully deleted.'}), 200
