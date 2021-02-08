"""System tests for API requests related to stores.

Tests ... .
"""
from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    '/store/teststore'
                )
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('teststore'))
                self.assertDictEqual(
                    json.loads(response.data),
                    {'name': 'teststore', 'items': []}
                )


    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    '/store/teststore'
                )
                self.assertEqual(response.status_code, 201,
                    "Test broken - store creation failed for 'teststore'")
                response = client.post(
                    '/store/teststore'
                )
                self.assertEqual(response.status_code, 400,
                    "Creation of second store was expected to fail but did not. ")
                
                self.assertDictEqual(
                    json.loads(response.data),
                    {'message': "A store with name 'teststore' already exists."}
                )


    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    '/store/teststore'
                )
                self.assertEqual(response.status_code, 201,
                    "Test broken - store creation failed for 'teststore'")
                response = client.delete('/store/teststore')
                self.assertDictEqual(
                    json.loads(response.data),
                    {'message': "Store deleted"}
                )



    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    '/store/teststore'
                )
                self.assertEqual(response.status_code, 201)
                response = client.get('/store/teststore')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    json.loads(response.data),
                    {'name': 'teststore', 'items': []}
                )

    def test_find_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                #bypass posting the store and the item through API
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 19.99, 1).save_to_db()
                response = client.get('/store/teststore')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    json.loads(response.data),
                    {'name': 'teststore', 'items': [
                        {'name': 'testitem', 'price': 19.99}
                    ]}
                )


    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    '/store/teststore'
                )
                self.assertEqual(response.status_code, 201)
                response = client.get('/store/notteststore')
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(
                    json.loads(response.data),
                    {'message': 'Store not found'}
                )


    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    '/store/teststore'
                )
                self.assertEqual(response.status_code, 201,
                    "Test broken - store creation failed for 'teststore'")
                response = client.get('/stores')
                self.assertEqual(response.status_code, 200)
                expected = {
                    'stores': [{ 'name' : 'teststore', 'items': [] }]
                }
                self.assertDictEqual(json.loads(response.data), expected)

    def test_store_list_many_stores(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    '/store/teststore1'
                )
                self.assertEqual(response.status_code, 201,
                    "Test broken - store creation failed for 'teststore1'")
                response = client.post(
                    '/store/teststore2'
                )
                self.assertEqual(response.status_code, 201,
                    "Test broken - store creation failed for 'teststore2'")
                response = client.post(
                    '/store/teststore3'
                )
                self.assertEqual(response.status_code, 201,
                    "Test broken - store creation failed for 'teststore3'")
                response = client.get('/stores')
                self.assertEqual(response.status_code, 200)
                store_list = json.loads(response.data)['stores']
                #print(f"{store_list}")
                self.assertEqual(len(store_list),3)
                for st in ('teststore1', 'teststore2', 'teststore3'):
                    self.assertTrue(
                        st in [ s['name'] for s in store_list]
                    )

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    '/store/teststore'
                )
                self.assertEqual(response.status_code, 201,
                    "Test broken, store creation failed.")
                response = client.post(
                    '/item/testitem', data=dict(price=19.99, store_id=1)
                )
                self.assertEqual(response.status_code, 201,
                    "Test broken, item creation failed.")
                response = client.get('/stores')
                self.assertEqual(response.status_code, 200)
                expected = {
                    'stores': [
                        {
                            'name' : 'teststore', 'items': [
                                { 'name': 'testitem', 'price': 19.99 }
                            ]
                        }
                    ]
                }
                self.assertDictEqual(json.loads(response.data), expected)

