# Import UnitTest module
import unittest

# We must tell the interpreter where to find the module we want to test
# Be careful with the path, it must be relative to the root of the project
import sys
sys.path.append('src')

# import the geometries module
from devices import Device

class TestDeviceLifeCycle(unittest.TestCase):
    
    def setUp(self):
        self.new_device_data = {
            "device_name": "Test Device",
            "managed_by_user_id": "new_user@test.at"
        }

        self.new_user_data = {
            "id": "user@test.at",
            "name": "Test User"
        }   
       

    def test_create_new_device(self):
        # Vorbedingung: Gerät ist noch nicht angelegt
        self.assertIsNone(Device.find_by_attribute("device_name", self.new_device_data["device_name"]))

        # Neues Gerät wird in UI angelegt
        new_device = Device(**self.new_device_data)

        # Speichert Gerät in Datenbank
        new_device.store_data()

        # Nachbedingung: Gerät ist angelegt
        self.assertIsNotNone(Device.find_by_attribute("device_name", self.new_device_data["device_name"]))


    def test_update_device_user(self):
        # Administrator wählt Gerät bearbeiten
        self.test_create_new_device()
        self.assertIsNotNone(Device.find_by_attribute("device_name", self.new_device_data["device_name"]))
        device = Device.find_by_attribute("device_name", self.new_device_data["device_name"])
        device.managed_by_user_id = self.new_user_data["id"]
        device.store_data()

        device = Device.find_by_attribute("device_name", self.new_device_data["device_name"])
        self.assertEqual(device.managed_by_user_id, self.new_user_data["id"])
        self.test_delete_device()

    def find_all_devices(self):
        devices = Device.find_all()
        self.assertIsInstance(devices, list)

        # Find the device with the name
        found_device = None
        for device in devices:
            if device.device_name == self.new_device_data["device_name"]:
                found_device = device
                break

        self.assertEqual(found_device.device_name, self.new_device_data["device_name"])
        self.assertEqual(found_device.managed_by_user_id, self.new_device_data["managed_by_user_id"])

    def test_delete_device(self):
        # Vorbedingung: Gerät ist angelegt
        self.assertIsNotNone(Device.find_by_attribute("device_name", self.new_device_data["device_name"]))

        # Administrator wählt Gerät löschen
        device = Device.find_by_attribute("device_name", self.new_device_data["device_name"])
        device.delete()

        # Nachbedingung: Gerät ist gelöscht
        self.assertIsNone(Device.find_by_attribute("device_name", self.new_device_data["device_name"]))

if __name__ == '__main__':
    unittest.main()

