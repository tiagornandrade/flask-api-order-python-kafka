import unittest


class UserModel:
    def __init__(self, username, first_name, last_name):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class TestUserCreation(unittest.TestCase):
    def test_user_creation(self):
        user = UserModel("johndoe", "John", "Doe")

        self.assertEqual(user.username, "johndoe")

        self.assertEqual(user.first_name, "John")

        self.assertEqual(user.last_name, "Doe")


if __name__ == "__main__":
    unittest.main()
