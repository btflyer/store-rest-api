from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest

class StoreTest(BaseTest):
    def test_create_store(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [],
            "The strore items list was not empty even though no items added yet.")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')
            self.assertIsNone(StoreModel.find_by_name('test'), "Bespoke msg test_crud condition")
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name('test'), "Bespoke msg test_crud condition")
            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('test'), "Bespoke msg test_crud condition")
    
    def test_store_relationship_one_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)
            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_relationship_multi(self):
        with self.app_context():
            store = StoreModel('test')
            item1 = ItemModel('first_item', 19.99, 1)
            store.save_to_db()
            item1.save_to_db()

            item2 = ItemModel('second_item', 29.99, 1)
            store.save_to_db()
            item2.save_to_db()

            self.assertEqual(store.items.count(), 2)
            self.assertEqual(store.items.first().name, 'first_item')
    

    def test_store_json(self):
        store = StoreModel('test')
        expected = {
            'id': None,
            'name': 'test',
            'items': []
        }
        self.assertDictEqual(store.json(), expected,
            "Json created by store does not match ctor arguments.")

    def test_store_json_multi(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)
            store.save_to_db()
            item.save_to_db()
            expected = {
                'id': 1,
                'name': 'test',
                'items': [ 
                    { 
                        'name': 'test_item', 
                        'price': 19.99
                    }
                ]
            }
            self.assertDictEqual(store.json(), expected,
                "Json created by store does not match ctor arguments.")