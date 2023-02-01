import os
import unittest
from random import randrange

import lorem

from app import create_app


class TestMachines(unittest.TestCase):
    def test_create_machine(self):
        mock_name = lorem.sentence()
        mock_location = lorem.sentence()
        flask_app = create_app()
        with flask_app.test_client() as test_client:
            response = test_client.post(
                "/machines", json={"name": mock_name, "location": mock_location}
            )
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

            get_current_stock_response = test_client.get(f"/machines/{random_machine_id}")
            get_current_stock_response_json = get_current_stock_response.get_json()
            current_amount_stock = get_current_stock_response_json["stock"].get(item_name, 0)

            update_stock_response = test_client.put(
                f"/machines/{random_machine_id}", json={item_name: random_item_amount}
            )
            update_stock_response_json = update_stock_response.get_json()
            assert update_stock_response.status_code == 200
            assert item_name in update_stock_response_json["stock"]
            assert update_stock_response_json["stock"][item_name] == current_amount_stock + random_item_amount

    def test_delete_stock(self):
        # random_machine_id = randrange(10)
        random_machine_id = 2
        item_name = lorem.sentence()
        random_item_amount = randrange(10)
        flask_app = create_app()
        with flask_app.test_client() as test_client:
            get_current_stock_response = test_client.get(f"/machines/{random_machine_id}")
            get_current_stock_response_json = get_current_stock_response.get_json()
            current_amount_stock = get_current_stock_response_json["stock"].get(item_name, 0)

            if current_amount_stock == 0:
                update_stock_response = test_client.put(
                    f"/machines/{random_machine_id}", json={item_name: random_item_amount + 10}
                )
                current_amount_stock = random_item_amount + 10

            remove_stock_response = test_client.post(
                f"/machines/{random_machine_id}", json={item_name: random_item_amount}
            )
            remove_stock_response_json = remove_stock_response.get_json()
            assert remove_stock_response.status_code == 200
            assert item_name in remove_stock_response_json["stock"]
            assert remove_stock_response_json["stock"][item_name] == current_amount_stock - random_item_amount

if __name__ == "__main__":
    unittest.main()
