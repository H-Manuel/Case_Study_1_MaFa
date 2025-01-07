# Import UnitTest module
import unittest

# We must tell the interpreter where to find the module we want to test
# Be careful with the path, it must be relative to the root of the project
import sys
sys.path.append('src')

# import the geometries module
from users import User

class TestUserLifeCycle(unittest.TestCase):
    
    def setUp(self):
        self.new_user_data = {
            "id": "new_user@test.at",
            "name": "Test User"
        }

    def test_create_new_user(self):
        # Vorbedingung: Nutzer ist noch nicht angelegt
        self.assertIsNone(User.find_by_attribute("ID", self.new_user_data["id"]))

        # Neuer User wird in UI angelegt
        new_user = User(**self.new_user_data)

        # Speichert Nutzer in Datenbank
        new_user.store_data()

        # Nachbedingung: Nutzer ist angeleg

        self.assertIsNotNone(User.find_by_attribute("ID", self.new_user_data["id"]))

    def find_all_users(self):
        users = User.find_all()
        self.assertIsInstance(users, list)

        # Find the user with the id
        found_user = None
        for user in users:
            if user.id == self.new_user_data["id"]:
                found_user = user
                break

        self.assertEqual(found_user.username, self.new_user_data["name"])
        self.assertEqual(found_user.id, self.new_user_data["id"])

    def test_delete_user(self):
        # Vorbedingung: Nutzer ist angelegt
        self.assertIsNotNone(User.find_by_attribute("ID", self.new_user_data["id"]))

        # Administrator wählt Nutzer löschen
        self.user.delete()

        # Nachbedingung: Nutzer ist gelöscht
        self.assertIsNone(User.find_by_attribute("ID", self.new_user_data["id"]))

if __name__ == '__main__':
    unittest.main()


