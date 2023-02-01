import os
import unittest
from random import randrange

import lorem

from app import create_app


class TestMachines(unittest.TestCase):
    base_url = "http://127.0.0.1:6969"  # TODO: hardcode
    machine_api = f"{base_url}/machines"

    def test_create_machine(self):
        mock_name = lorem.sentence()
        mock_location = lorem.sentence()
        flask_app = create_app()
        with flask_app.test_client() as test_client:
            response = test_client.post('/machines', json={"name": mock_name, "location": mock_location})
            response_json = response.get_json()
            assert response.status_code == 200
            assert response_json["name"] == mock_name
            assert response_json["location"] == mock_location
            assert len(response_json["stock"]) == 0
            return response_json["id"]

    def test_get_machine_by_id(self):
        # random_machine_id = randrange(10)
        random_machine_id = 3
        flask_app = create_app()
        with flask_app.test_client() as test_client:
            response = test_client.get(f"/machines/{random_machine_id}")
            response_json = response.get_json()
            assert response_json["id"] == random_machine_id
            assert response_json["name"] is not None
            assert response_json["location"] is not None
            assert response_json["stock"] is not None

    def test_get_all_machines(self):
        flask_app = create_app()
        with flask_app.test_client() as test_client:
            response = test_client.get("/machines")
            response_json = response.get_json()
            for machine in response_json:
                assert machine["id"] is not None
                assert machine["name"] is not None
                assert machine["location"] is not None
                assert machine["stock"] is not None

    def test_update_stock(self):
        # random_machine_id = randrange(10)
        random_machine_id = 2
        item_name = lorem.sentence()
        random_item_amount = randrange(10)
        flask_app = create_app()
        with flask_app.test_client() as test_client:
            response = test_client.put(f"/machines/{random_machine_id}", json={item_name: random_item_amount})
            response_json = response.get_json()
            print(response_json)
            assert response.status_code == 200
            assert item_name in response_json["stock"]
            assert response_json["stock"][item_name] >= random_item_amount


if __name__ == "__main__":
    unittest.main()
