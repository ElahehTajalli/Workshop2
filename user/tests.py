from django.test import TestCase, Client
from django.contrib.auth.models import User


class SignUpTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.username = "maryam",
        self.first_name = "maryam",
        self.last_name = "ahmadi",
        self.email = 'ahmadi@gmail.com',
        self.password = '12345'


    def test_signup_form(self):
        response = self.c.post('/user/user', data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
        })
        self.assertEqual(response.status_code, 200)

        users = User.objects.all()
        self.assertEqual(users.count(), 1)


    def test_signup_form2(self):
        response = self.c.post('/user/user', data={
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        })
        self.assertEqual(response.status_code, 200)



    def test_signup_form3(self):
        response = self.c.post('/user/user', data={
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
        })
        self.assertEqual(response.status_code, 200)

        exp_data = {
            "errors": {
                "username": [
                    "This field is required."
                ]
            }
        }
        self.assertEqual(exp_data, response.json())





