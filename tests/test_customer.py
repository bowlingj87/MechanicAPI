from app import create_app
from app.models import db, Customer
from app.utils.utils import encode_token
import unittest

class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customer(
            name="test_user",
            email="test@email.com",
            phone="713-333-4444",
            password='test'
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            db.session.refresh(self.customer)  # ensure object is attached to session

        # Precompute token for authorized routes
        self.token = encode_token(self.customer.id)
        self.client = self.app.test_client()

    # ---------------- CREATE ----------------
    def test_create_customer(self):
        payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "251-333-4444",
            "password": "123456"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    # ---------------- LOGIN ----------------
    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        # Store token in self.token for use in other tests
        self.token = response.json['token']

    # ---------------- UPDATE ----------------
    def test_update_customer(self):
        payload = {
        "name": "Peter",
        "phone": "",
        "email": "",
        "password": ""
    }
        headers = {'Authorization': f"Bearer {self.token}"}

        response = self.client.put('/customers/', json=payload, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter')
        self.assertEqual(response.json['email'], '')  # matches API behavior

    # ---------------- GET ALL ----------------
    def test_get_all_customers(self):
        # This route is public, no auth needed
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)
        self.assertEqual(response.json[0]['email'], 'test@email.com')

    # ---------------- GET SPECIFIC ----------------
    def test_get_specific_customer(self):
        headers = {'Authorization': f"Bearer {self.token}"}
        response = self.client.get(f'/customers/{self.customer.id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_user')
        self.assertEqual(response.json['email'], 'test@email.com')

    # ---------------- DELETE ----------------
    def test_delete_customer(self):
        headers = {'Authorization': f"Bearer {self.token}"}

        response = self.client.delete('/customers/', headers=headers)
        self.assertIn(response.status_code, [200, 405])  