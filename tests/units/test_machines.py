import json
from unittest import TestCase
from app import create_app
from modules.database.sqlite_service import DatabaseService
from modules.machine.machine import Machine

class TestMachines(TestCase):
    def setUp(self):
        self.app = create_app()
        self.db = DatabaseService()
        self.client = self.app.test_client()
        
    def test_create_machine(self):
        response = self.client.post(
            "/machines",
            data=json.dumps({"name": "Test Machine", "location": "Test Location"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        machine_data = response.get_json()
        self.assertEqual(machine_data["name"], "Test Machine")
        self.assertEqual(machine_data["location"], "Test Location")

    def test_get_all_machines(self):
        machine = Machine(name="Test Machine", location="Test Location")
        inserted_id = self.db.insert_into_machine(machine)
        response = self.client.get("/machines")
        self.assertEqual(response.status_code, 200)
        machines_data = response.get_json()
        self.assertIsInstance(machines_data, list)
        self.assertIn(inserted_id, [m["id"] for m in machines_data])

    def test_get_machine_by_id(self):
        machine = Machine(name="Test Machine", location="Test Location")
        inserted_id = self.db.insert_into_machine(machine)
        response = self.client.get(f"/machines/{inserted_id}")
        self.assertEqual(response.status_code, 200)
        machine_data = response.get_json()
        self.assertEqual(machine_data["name"], "Test Machine")
        self.assertEqual(machine_data["location"], "Test Location")

    def test_add_stock_by_json(self):
        machine = Machine(name="Test Machine", location="Test Location", stocks={"pringles": 10})
        inserted_id = self.db.insert_into_machine(machine)
        response = self.client.put(
            f"/machines/{inserted_id}",
            data=json.dumps({"doritos": 5}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        machine_data = response.get_json()

    def test_delete_stock_by_json(self):
        machine = Machine(name="Test Machine", location="Test Location", stocks={"pringles": 10, "doritos": 5})
        inserted_id = self.db.insert_into_machine(machine)
        response = self.client.post(
            f"/machines/{inserted_id}",
            data=json.dumps({"doritos": 2}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)
        # machine_data = response.get_json()


    def test_delete_machine_by_id(self):
        machine = Machine(name="Test Machine", location="Test Location")
        inserted_id = self.db.insert_into_machine(machine)
        response = self.client.delete(f"/machines/{inserted_id}")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"/machines/{inserted_id}")
        self.assertEqual(response.status_code, 500)

    def test_get_stock_history_by_product_name(self):
        machine = Machine(name="Test Machine", location="Test Location", stocks={"pringles": 10})
        inserted_id = self.db.insert_into_machine(machine)

        response = self.client.put(
            f"/machines/{inserted_id}",
            data=json.dumps({"pringles": 5}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"/stock_history/product/pringles")
        self.assertEqual(response.status_code, 200)
        stock_history_data = response.get_json()
        self.assertIsInstance(stock_history_data, list)
        self.assertTrue(len(stock_history_data) > 0)

    def test_get_stock_history_by_machine_id(self):
        machine = Machine(name="Test Machine", location="Test Location", stocks={"pringles": 10})
        inserted_id = self.db.insert_into_machine(machine)

        response = self.client.put(
            f"/machines/{inserted_id}",
            data=json.dumps({"pringles": 5}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"/stock_history/machine/{inserted_id}")
        self.assertEqual(response.status_code, 200)
        stock_history_data = response.get_json()
        self.assertIsInstance(stock_history_data, dict)
        self.assertTrue(len(stock_history_data) > 0)
