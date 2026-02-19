import unittest
from datetime import date
import uuid
from app import create_app, db
from app.models import Service_Ticket, Customer, Mechanic, Inventory


class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # Create tables
        db.create_all()

        # Create test customer with unique email
        self.customer = Customer(
            name="Test Customer",
            email=f"{uuid.uuid4().hex}@email.com",
            phone="251-555-1234",
            password="password123"
        )
        db.session.add(self.customer)
        db.session.commit()

        # Create test service ticket
        self.ticket = Service_Ticket(
            service_date=date.today(),
            service_description="Brake replacement",
            vin="1HGCM82633A004352",
            customer_id=self.customer.id
        )
        db.session.add(self.ticket)
        db.session.commit()

        # Create test mechanic
        self.mechanic = Mechanic(
            name="Test Mechanic",
            email=f"{uuid.uuid4().hex}@mechanic.com",
            phone="251-555-5678"
        )
        db.session.add(self.mechanic)
        db.session.commit()

        # Create test inventory
        self.inventory = Inventory(
            name="Brake Pad",
            price=50.0
        )
        db.session.add(self.inventory)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # --- TESTS ---

    def test_create_service_ticket(self):
        response = self.client.post(
            '/service_tickets/',
            json={
                "service_date": str(date.today()),
                "service_description": "Oil change",
                "vin": "1HGCM82633A004353",
                "customer_id": self.customer.id
            }
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['service_description'], "Oil change")

    def test_get_all_service_tickets(self):
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)

    def test_get_specific_service_ticket(self):
        response = self.client.get(f'/service_tickets/{self.ticket.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['service_description'], "Brake replacement")

    def test_edit_service_ticket_add_mechanic(self):
        response = self.client.put(
            f'/service_tickets/{self.ticket.id}',
            json={"add_mechanic_ids": [self.mechanic.id], "remove_mechanic_ids": []}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['mechanics']), 1)
        self.assertEqual(data['mechanics'][0]['id'], self.mechanic.id)

    def test_add_inventory_to_ticket(self):
        response = self.client.put(
            f'/service_tickets/{self.ticket.id}/add_inventory/{self.inventory.id}'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['inventory_id'], self.inventory.id)
        self.assertEqual(data['ticket_id'], self.ticket.id)