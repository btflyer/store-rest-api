from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('tester', '1234##!').save_to_db()
                auth_resp = client.post(
                    '/auth',
                    data=json.dumps({'username': 'tester', 'password': '1234##!'}),
                    headers={'Content-Type': 'application/json'}
                )
                auth_token = json.loads(auth_resp.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_w_no_auth_not_allowed(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)

    def test_get_nonexisting_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_existing_item_w_auth_returns_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 19.99, 1).save_to_db()
                resp = client.get('/item/testitem', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    def test_delete_existing_item_removes_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 19.99, 1).save_to_db()
                resp = client.delete('/item/testitem')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Item deleted'})


    def test_post_item_creates_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                resp = client.post('/item/testitem', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual(
                    json.loads(resp.data), {'name': 'testitem', 'price': 17.99}
                )

    def test_post_duplicate_item_not_allowed(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 19.99, 1).save_to_db()
                resp = client.post('/item/testitem', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(
                    json.loads(resp.data),
                    {'message': "An item with name 'testitem' already exists."}
                )


    def test_put_adds_new_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                resp = client.put(
                    '/item/testitem',
                    data={'price': 18.99, 'store_id': 1}
                )
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(
                    ItemModel.find_by_name('testitem').price, 18.99
                )
                self.assertDictEqual(
                    json.loads(resp.data),{'name': 'testitem', 'price': 18.99}
                )


    def test_put_updates_existing_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 6.99, 1).save_to_db()
                self.assertEqual(
                    ItemModel.find_by_name('testitem').price, 6.99
                )
                resp = client.put(
                    '/item/testitem',
                    data={'price': 18.99, 'store_id': 1}
                )
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(
                    ItemModel.find_by_name('testitem').price, 18.99
                )
                self.assertDictEqual(
                    json.loads(resp.data),{'name': 'testitem', 'price': 18.99}
                )


    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 6.99, 1).save_to_db()
                resp = client.get('/items')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(
                    json.loads(resp.data),
                    {'items': [{'name': 'testitem', 'price': 6.99}]}
                )
