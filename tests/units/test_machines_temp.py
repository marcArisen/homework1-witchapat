# import os
# import unittest
# from random import randrange
#
# import lorem
# import requests
# from flask import Flask
#
#
# class TestMachines(unittest.TestCase):
#     base_url = "http://127.0.0.1:6969"  # TODO: hardcode
#     machine_api = f"{base_url}/machines"
#
#     def test_create_machine(self):
#         mock_name = lorem.sentence()
#         mock_location = lorem.sentence()
#         response = requests.post(
#             url=self.machine_api, json={"name": mock_name, "location": mock_location}
#         )
#         response_json = response.json()
#         assert response.status_code == 200
#         assert response_json["name"] == mock_name
#         assert response_json["location"] == mock_location
#         assert len(response_json["stock"]) == 0
#         return response_json["id"]
#
#     def test_get_machine_by_id(self):
#         random_machine_id = randrange(10)
#         response = requests.get(
#             url=f"{self.machine_api}/{random_machine_id}",
#         )
#         response_json = response.json()
#         assert response_json["id"] == random_machine_id
#         assert response_json["name"] is not None
#         assert response_json["location"] is not None
#         assert response_json["stock"] is not None
#
#     def test_get_all_machines(self):
#         response = requests.get(
#             url=f"{self.machine_api}",
#         )
#         response_json = response.json()
#         for machine in response_json:
#             assert machine["id"] is not None
#             assert machine["name"] is not None
#             assert machine["location"] is not None
#             assert machine["stock"] is not None
#
#     def test_update_stock(self):
#         random_machine_id = randrange(10)
#         item_name = lorem.sentence()
#         random_item_amount = randrange(10)
#         response = requests.put(
#             url=f"{self.machine_api}/{random_machine_id}",
#             json={item_name: random_item_amount},
#         )
#         response_json = response.json()
#         assert item_name in response_json["stock"]
#         assert response_json["stock"][item_name] >= random_item_amount
#
#
# if __name__ == "__main__":
#     unittest.main()
