import unittest
from app import create_app
from app.models import db, Mechanic

class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        # Sample mechanic for testing
        self.mechanic = Mechanic(
            name="John Mechanic",
            email="john@mechanic.com",
            phone="123-456-7890",
            
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
            db.session.refresh(self.mechanic)

    # ---------------- CREATE ----------------
    def test_create_mechanic(self):
        payload = {
            "name": "Jane Mechanic",
            "email": "jane@mechanic.com",
            "phone": "987-654-3210",
            
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Jane Mechanic")

    # ---------------- GET ALL ----------------
    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) >= 1)

    # ---------------- GET SPECIFIC ----------------
    def test_get_specific_mechanic(self):
        response = self.client.get(f'/mechanics/{self.mechanic.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'john@mechanic.com')

    # ---------------- UPDATE ----------------
    def test_update_mechanic(self):
        payload = {
            "name": "John Updated",
            "email": "",
            "phone": ""
        }
        response = self.client.put(f'/mechanics/{self.mechanic.id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'John Updated')

    # ---------------- DELETE ----------------
    def test_delete_mechanic(self):
        response = self.client.delete(f'/mechanics/{self.mechanic.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully deleted', response.json['message'])

        with self.app.app_context():
            deleted = db.session.get(Mechanic, self.mechanic.id)
            self.assertIsNone(deleted)

    # ---------------- POPULAR ----------------
    def test_popular_mechanics(self):
        response = self.client.get('/mechanics/popular')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    # ---------------- SEARCH ----------------
    def test_search_mechanics(self):
        response = self.client.get('/mechanics/searchs?name=John')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) >= 1)
        self.assertIn('John', response.json[0]['name'])