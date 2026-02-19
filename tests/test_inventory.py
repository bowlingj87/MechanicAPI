import unittest
from app import create_app
from app.models import db, Inventory


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Create sample inventory item
            self.inventory = Inventory(
                name="Brake Pads",
                price=49.99
            )

            db.session.add(self.inventory)
            db.session.commit()
            db.session.refresh(self.inventory)

    # ---------------- CREATE ----------------
    def test_create_inventory(self):
        payload = {
            "name": "Oil Filter",
            "price": 19.99
        }

        response = self.client.post('/inventories/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Oil Filter")
        self.assertEqual(response.json['price'], 19.99)

    # ---------------- GET ALL  ----------------
    def test_get_all_inventories(self):
        response = self.client.get('/inventories/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
        self.assertTrue(len(response.json) >= 1)

    # ---------------- GET SPECIFIC ----------------
    def test_get_specific_inventory(self):
        response = self.client.get(f'/inventories/{self.inventory.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Brake Pads")

    # ---------------- UPDATE ----------------
    def test_update_inventory(self):
        payload = {
            "name": "Premium Brake Pads",
            "price": 59.99
        }

        response = self.client.put(
            f'/inventories/{self.inventory.id}',
            json=payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Premium Brake Pads")
        self.assertEqual(response.json['price'], 59.99)

    # ---------------- DELETE ----------------
    def test_delete_inventory(self):
        response = self.client.delete(
            f'/inventories/{self.inventory.id}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully deleted', response.json['message'])

        with self.app.app_context():
            deleted = db.session.get(Inventory, self.inventory.id)
            self.assertIsNone(deleted)