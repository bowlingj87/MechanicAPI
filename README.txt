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
│   ├── mechanics/
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

Mechanic - id (Primary Key) - name - email - phone - Many-to-many
relationship with Service Tickets

Service Ticket - id (Primary Key) - service_date - service_description -
vin - customer_id (Foreign Key) - Many-to-many relationship with
Mechanics

  --------------------------------------------------
  Relationships
  --------------------------------------------------
  - One Customer can have many Service Tickets - One
  Service Ticket can be assigned to many Mechanics -
  One Mechanic can work on many Service Tickets

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


PUT /<int:service_tickets_id>/assign_mechanic/<int:mechanic_id>
Assign a mechanic to a service ticket

PUT /<int:service_tickets_id>/remove_mechanic/<int:mechanic_id>
Remove a mechanic from a service ticket


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
