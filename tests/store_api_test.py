import unittest
from logic.store_api import StoreApi

class StoreApiTest(unittest.TestCase):

    def test_get_store_order_by_valid_id_success(self):
        ids=2 #int - The ID sometimes runs properly and sometimes not, so it might be better to generate and then test.
        status= 'placed'

        result = StoreApi.get_store_order_id(ids)
        print(f"Status Code: {result.status_code}")
        print(f"Response Body: {result.data}")

        self.assertEqual(result.ok, True)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data['id'], ids)
        self.assertEqual(result.data['status'], status)
        self.assertEqual(result.data['complete'], True)

    def test_get_store_order_by_invalid_id(self):
        ids=0 #int
        result = StoreApi.get_store_order_id(ids)
        self.assertEqual(result.ok, False)
        self.assertEqual(result.status_code, 404)

    def test_get_store_inventory_success(self):
        result = StoreApi().get_store_inventory()

        self.assertEqual(result.ok, True)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(isinstance(result.data, dict))

    def test_create_and_validate_new_order(self):
        ids = 101
        petIds = 10
        order_payload = {
            "id": ids,
            "petId": petIds,
            "quantity": 1,
            "shipDate": "2025-12-10T16:48:55.334Z",
            "status": "placed",
            "complete": True
        }

        create_result = StoreApi().create_store_order(order_payload)
        self.assertEqual(create_result.ok, True)
        self.assertEqual(create_result.status_code, 200)

        self.assertEqual(create_result.data['id'], ids)
        self.assertEqual(create_result.data['status'], "placed")
        self.assertTrue(create_result.data['complete'])

    def test_delete_existing_store_order_success(self):
        # Create a new order first
        order_id = 5001
        order_payload = {
            "id": order_id,
            "petId": 10,
            "quantity": 1,
            "shipDate": "2025-12-10T16:48:55.334Z",
            "status": "placed",
            "complete": True
        }

        create_result = StoreApi().create_store_order(order_payload)
        self.assertTrue(create_result.ok)

        delete_result = StoreApi().delete_store_order(order_id)
        self.assertTrue(delete_result.ok)
        self.assertEqual(delete_result.status_code, 200)

        get_result = StoreApi.get_store_order_id(order_id)
        self.assertEqual(get_result.status_code, 404)

    def test_delete_non_existent_store_order_id(self):
        non_existent_id = 999999999
        delete_result = StoreApi().delete_store_order(non_existent_id)
        self.assertEqual(delete_result.ok, False)
        self.assertEqual(delete_result.status_code, 404)