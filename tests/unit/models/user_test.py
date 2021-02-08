from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class UserTest(UnitBaseTest):
    def test_creation(self):
        user = UserModel('testuser', '234#%&ab')

        self.assertEqual(user.username, 'testuser',
            "Username after creation does not match ctor argument.")
        self.assertEqual(user.password, '234#%&ab',
            "Password after creation does not match ctor argument.")