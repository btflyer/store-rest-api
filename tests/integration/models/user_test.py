from models.user import UserModel

from tests.base_test import BaseTest

class UserTest(BaseTest):
    def test_create(self):
        with self.app_context():
            user = UserModel('testuser','abcd12')

            self.assertIsNone(UserModel.find_by_username('testuser'))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('testuser'))
            self.assertIsNotNone(UserModel.find_by_id(1))

    def test_create_duplicate_usernames_allowed(self):
        with self.app_context():
            user = UserModel('testuser', 'abcd12')
            user.save_to_db()

            user2 = UserModel('testuser', 'defg34')
            user2.save_to_db() #uniqueness not enforced here
            self.assertEqual(len(UserModel.query.filter_by(username=user.username).all()), 2,
                "Expected 2 'testuser' in the database but got a different number.")
