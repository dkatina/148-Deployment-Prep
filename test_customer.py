import unittest
from faker import Faker
from app import create_app #importing our application factory
from database import db
from unittest.mock import patch

class TestCustomer(unittest.TestCase):

    def setUp(self):
        app = create_app('TestingConfig')
        with app.app_context():
            db.create_all()
        self.app = app.test_client()


    def test_create_customer(self):
        fake = Faker()
        name = fake.name()
        phone = fake.basic_phone_number()
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        admin = 1

        payload = {  #Creating my customer payload from the mocked data
            "name": name,
            "phone": phone,
            "username": username,
            "password": password,
            "email": email,
            "admin": admin
        }

        response = self.app.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], name)

    @patch('services.customerService.save') #patch this particular function when it is called
    def test_create_customer_patch(self, mock_save): #the function we are patchin will be refered to as mock_save
        fake = Faker()
        name = fake.name()
        phone = fake.basic_phone_number()
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        admin = 1
     
        mock_customer = {#using our random data to create an instance of Customer
       'name' : name,
       'phone' : phone,
       'username' : username,
       'email' : email,
       'password' : password,
       'admin' : admin
       }
 
        mock_save.return_value = mock_customer
    
        payload = {  #Creating my customer payload from the mocked data
            "name": name,
            "phone": phone,
            "username": username,
            "password": password,
            "email": email,
            "admin": admin
        }

        response = self.app.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], name)

if __name__ == "__main__":
    unittest.main()