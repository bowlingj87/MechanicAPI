Mechanic API

This project is a RESTful API built with Flask, SQLAlchemy, and
Marshmallow. It manages customers, service tickets, and mechanics,
including relationships between them.

  --------------------------------------------------
  Technologies Used
  --------------------------------------------------
  - Python - Flask - Flask-SQLAlchemy -
  Marshmallow - Marshmallow-SQLAlchemy

  --------------------------------------------------

Project Structure

app/
│
├── blueprints/
│   ├── customers/
<<<<<<< HEAD
│   ├── mechanics/
=======
│   ├── inventories/
│ 	 ├── mechanic/
>>>>>>> 3258edba17cb3d93ef8e2689da65fb7cfe696928
│   └── service_tickets/
│
├── __init__.py
├── extensions.py
├── models.py
│
venv/
app.py
config.py
filestructure.txt
requirements.txt
README.txt

  -----------------
  Database Models
  -----------------

Customer - id (Primary Key) - name - email (unique) - phone -
One-to-many relationship with Service Tickets

<<<<<<< HEAD
=======
Inventory - id(Primary) - name - price - Many-to-many relationship
with Service Tickets

>>>>>>> 3258edba17cb3d93ef8e2689da65fb7cfe696928
Mechanic - id (Primary Key) - name - email - phone - Many-to-many
relationship with Service Tickets

Service Ticket - id (Primary Key) - service_date - service_description -
vin - customer_id (Foreign Key) - Many-to-many relationship with
<<<<<<< HEAD
Mechanics
=======
Mechanics and Inventory
>>>>>>> 3258edba17cb3d93ef8e2689da65fb7cfe696928

  --------------------------------------------------
  Relationships
  --------------------------------------------------
  - One Customer can have many Service Tickets - One
  Service Ticket can be assigned to many Mechanics -
<<<<<<< HEAD
  One Mechanic can work on many Service Tickets
=======
  One Mechanic can work on many Service Tickets, One 
  Service Ticket can have many inventory parts attached,
  One inventory part can be assigned to many service tickets
>>>>>>> 3258edba17cb3d93ef8e2689da65fb7cfe696928

  --------------------------------------------------

API Endpoints

Customers Endpoints

Create A New Customer
POST /customers/

Retrieve all Customers
GET /customers/

Retrieve a specific customer
GET /customers/<int:customer_id>/

Update a specific customer
PUT /customers/<int:customer_id>/

Delete Specific Customer
DELETE /customers/<int:customer_id>/

<<<<<<< HEAD
=======
Inventory Endpoints

Create A New Inventory part
POST /inventories/

Retrieve all Inventory
GET /inventories/

Update a specific Inventory
PUT /inventories/<int:inventory_id>/

Delete Specific inventory
DELETE /inventories/<int:inventory_id>/


>>>>>>> 3258edba17cb3d93ef8e2689da65fb7cfe696928

Mechanics Endpoints

Create A New Mechanic
POST /mechanics/

Retrieve all Mechanics
GET /mechanics/

Update a specific mechanic
PUT /mechanic/<int:mechanic_id>/

Delete Specific mechanic
DELETE /mechanic/<int:mechanic_id>/



Service Ticket Endpoints

Create a new service ticket
POST /service_tickets/

Retrieve all service tickets
GET /service_tickets/

<<<<<<< HEAD

PUT /<int:service_tickets_id>/assign_mechanic/<int:mechanic_id>
Assign a mechanic to a service ticket

PUT /<int:service_tickets_id>/remove_mechanic/<int:mechanic_id>
Remove a mechanic from a service ticket
=======
Assign a mechanic to a service ticket
PUT /service_tickets<int:service_tickets_id>/assign_mechanic/<int:mechanic_id>

Remove a mechanic from a service ticket
PUT /service_tickets/<int:service_tickets_id>/remove_mechanic/<int:mechanic_id>

Get Specific service ticket
GET/service_tickets/<int:ticket_id>

Add Inventory item to service ticket
PUT /service_tickets/<int:ticket_id>/add_inventory/<int:inventory_id>
>>>>>>> 3258edba17cb3d93ef8e2689da65fb7cfe696928


How to Run the Application

1.  Create and activate a virtual environment
2.  Install dependencies: pip install flask flask-sqlalchemy marshmallow
    marshmallow-sqlalchemy
3.  Run the application: python app.py

  --------------------------------------------------
  Notes
  --------------------------------------------------
  - Foreign keys are handled using Marshmallow
  schemas - SQLAlchemy ORM is used for relationship
  management - This project follows RESTful API
  design principles

  --------------------------------------------------

Author

Juan Bowling – Backend Specialization
