import unittest

class UserModel:
    def __init__(self, username, first_name, last_name):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
class TestUserCreation(unittest.TestCase):

    def test_user_creation(self):
        user = UserModel("johndoe", "John", "Doe")

        # Verifique se o nome de usuário do usuário criado é o esperado
        self.assertEqual(user.username, "johndoe")

        # Verifique se o primeiro nome do usuário criado é o esperado
        self.assertEqual(user.first_name, "John")

        # Verifique se o sobrenome do usuário criado é o esperado
        self.assertEqual(user.last_name, "Doe")


if __name__ == '__main__':
    unittest.main()
